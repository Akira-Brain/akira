#!/usr/bin/env python3
"""Controleert dat er geen bedragen in de ateliersite staan. Faalt hard als dat wel zo is.

Dit bestaat omdat de afscherming voor 2026-08-17 alleen per ongeluk werkte: prijzen
lekten niet omdat `generate-board.py` het veld `commercial` toevallig nooit las. Er was
geen regel en geen test. Een enkele toevoeging als "toon het offertebedrag per project"
had elke stagiair vanaf dat moment de bedragen laten lezen, zonder dat iemand het merkte.

Drie controles, bewust onafhankelijk van elkaar:

1. STRUCTUREEL - heeft de generator een verboden bron aangeraakt? Vangt een fout in de
   generator zelf, ook als die fout deze keer toevallig niets zichtbaars opleverde.
2. OP DE UITVOER - staat er een bedrag in de gegenereerde HTML? Vangt data die via een
   onverwachte weg binnenkwam, bijvoorbeeld een prijs die iemand in een taaknaam zette.
3. NEGATIEVE CONTROLE - kan deze test uberhaupt nog iets vinden? Een generator die niets
   uitvoert zou anders met vlag en wimpel slagen.

Gebruik:
    python system/scripts/test-geen-lek.py [uitvoermap]
"""

import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from akira import ROOT
from akira.laden import lees_projecten
from akira.toegang import laad_rollen

# Rollen die geen bedragen mogen zien. Wat een rol mag staat in system/access.yaml;
# dit is de lijst waarop deze test scherp staat.
BEPERKTE_ROLLEN = ["atelier"]

# Bedragpatronen. Bewust NIET "elk getal van drie cijfers": dan slaat de test aan op
# jaartallen, dagentellingen ("161 dagen") en projectnummers, wordt hij onbetrouwbaar,
# en zet iemand hem binnen een week uit. Een test die je uitzet is erger dan geen test.
BEDRAG_PATRONEN = [
    (re.compile(r"(?:EUR|eur|€)\s*\d", re.I), "bedrag met valutateken ervoor"),
    (re.compile(r"\d[\d.,]*\s*(?:EUR|euro|€)", re.I), "bedrag met valutateken erachter"),
    # `commercial` staat hier bewust NIET bij: dat is ook de scope-waarde van een
    # beslissingsrecord (D-2026-002 draagt `scope: commercial`), en die categorie is geen
    # bedrag. Een patroon dat structureel op legitieme tekst aanslaat, wordt binnen een
    # week uitgezet - en dan beschermt hij niets meer.
    (re.compile(r"\b(?:quoted|accepted)\b"), "commercieel veld uit project.yaml"),
    (re.compile(r"\b(?:marge|offertebedrag|dagtarief|uurtarief)\b", re.I), "prijsterm"),
]

# Bekende uitzonderingen: (bestandspatroon, regelpatroon, reden).
#
# Bewust nauw: een uitzondering geldt voor een specifieke tekst in een specifiek bestand,
# nooit voor een heel bestand of een heel patroon. Zou je hier `learnings/*` toestaan, dan
# glipt de eerste echte atelierprijs die daar ooit belandt er ongemerkt mee doorheen.
#
# Alle drie hieronder gaan over bedragen die NIET van ons zijn: wat een tweedehands stuk
# opbrengt en wat een ander voor een cursus vraagt. De eis van 17/8 ging over onze eigen
# prijzen, offertes en marges. Vindt Tore dat te ruim, dan is de oplossing deze regels
# weghalen en die bestanden in access.yaml uitsluiten - een regel per stuk.
TOEGESTAAN = [
    (re.compile(r"kennis\.html$"),
     re.compile(r"Google Lens gaf 60 euro"),
     "tweedehands schatting van een jasje tijdens de stockdigitalisering. Die learning "
     "bestaat juist zodat een student zelf tot die prijs kan komen zonder Farah of Luna; "
     "hem verbergen voor stagiairs haalt het punt eruit."),
    (re.compile(r"kennis\.html$"),
     re.compile(r"(750|50) euro"),
     "prijzen van een online cursus van iemand anders, uit de learning over eerst "
     "valideren. Marktobservatie, geen tarief van het atelier."),
]

# Uitzonderingen die de generator zelf mag melden: afgeleide getallen uit een bron
# waarvan de inhoud niet mag. Alleen deze paden, en alleen als er een reden bij staat.
TOEGESTANE_UITZONDERINGEN = {"company/canon-queue.md", "company/inbox/"}


def controle_structureel(uitvoer):
    """Heeft de generator voor een beperkte rol een verboden bron aangeraakt?"""
    fouten = []
    rollen = laad_rollen()
    for rol in BEPERKTE_ROLLEN:
        logpad = os.path.join(uitvoer, "_logs", f"{rol}.json")
        if not os.path.exists(logpad):
            fouten.append(f"{rol}: geen leeslogboek gevonden op {logpad} - "
                          f"de generator heeft niet gedraaid, dus deze test bewijst niets")
            continue
        with open(logpad, encoding="utf-8") as f:
            log = json.load(f)
        toegang = rollen[rol]
        for pad in log.get("gelezen", []):
            if not toegang.mag(pad):
                fouten.append(f"{rol}: heeft `{pad}` gelezen, maar dat mag niet")
        for uitz in log.get("uitzonderingen", []):
            pad, reden = uitz.get("pad"), (uitz.get("reden") or "").strip()
            if pad not in TOEGESTANE_UITZONDERINGEN:
                fouten.append(f"{rol}: onbekende uitzondering op `{pad}` - "
                              f"zet hem in TOEGESTANE_UITZONDERINGEN of haal hem weg")
            if not reden:
                fouten.append(f"{rol}: uitzondering op `{pad}` zonder reden")
    return fouten


def controle_uitvoer(uitvoer):
    """Staat er een bedrag in de gegenereerde HTML van een beperkte rol?"""
    fouten = []
    for rol in BEPERKTE_ROLLEN:
        map_ = os.path.join(uitvoer, rol)
        bestanden = glob.glob(os.path.join(map_, "**", "*.html"), recursive=True)
        if not bestanden:
            fouten.append(f"{rol}: geen HTML gevonden in {map_}")
            continue
        for pad in bestanden:
            with open(pad, encoding="utf-8") as f:
                tekst = f.read()
            for nr, regel in enumerate(tekst.splitlines(), 1):
                if any(bp.search(pad) and rp.search(regel)
                       for bp, rp, _ in TOEGESTAAN):
                    continue
                for patroon, wat in BEDRAG_PATRONEN:
                    m = patroon.search(regel)
                    if m:
                        # Context ROND de match tonen, niet het begin van de regel: de
                        # HTML staat grotendeels op een regel, dus het begin daarvan
                        # zegt niets over waar het bedrag vandaan komt.
                        a, b = max(0, m.start() - 70), min(len(regel), m.end() + 70)
                        kort = ("..." if a else "") + regel[a:b].strip() + \
                               ("..." if b < len(regel) else "")
                        fouten.append(
                            f"{rol}: {os.path.basename(pad)}:{nr} bevat {wat}\n"
                            f"          {kort}")
                        break
    return fouten


def controle_echte_bedragen(uitvoer):
    """Staan de bedragen die ECHT in de bron staan, ergens in een beperkte uitvoer?

    Dit is de sterkste van de vier controles, en hij bestaat omdat de patroonzoektocht
    een blinde vlek heeft: `6000` in een tabelcel draagt geen valutateken en lijkt dus op
    elk ander getal. Zou een toekomstige pagina het kale bedrag renderen, dan glipt het
    langs BEDRAG_PATRONEN heen.

    Hier zoeken we niet naar iets dat op een bedrag lijkt, maar naar de exacte getallen
    die op dit moment in `commercial` staan. Geen patroon, geen gok - de waarde zelf.
    """
    fouten = []
    bedragen = {}
    for p in lees_projecten():
        c = p.get("commercial") or {}
        for veld in ("quoted", "accepted"):
            if isinstance(c.get(veld), (int, float)):
                bedragen[str(c[veld])] = f"{p['_slug']}.{veld}"

    for rol in BEPERKTE_ROLLEN:
        for pad in glob.glob(os.path.join(uitvoer, rol, "**", "*.html"), recursive=True):
            with open(pad, encoding="utf-8") as f:
                tekst = f.read()
            for bedrag, herkomst in bedragen.items():
                if re.search(rf"(?<![\d.,]){re.escape(bedrag)}(?![\d.,])", tekst):
                    fouten.append(
                        f"{rol}: {os.path.basename(pad)} bevat het exacte bedrag "
                        f"{bedrag} uit {herkomst}")
    return fouten, len(bedragen)


def controle_negatief(uitvoer):
    """Kan deze test nog iets vinden, of test hij lucht?

    Zonder deze controle zou een generator die per ongeluk lege pagina's schrijft
    slagen. Rapporteert expliciet of er uberhaupt bedragen in de bron staan om te
    beschermen - "niets gevonden" en "niets te vinden" zien er anders identiek uit.
    """
    meldingen = []
    projecten = lees_projecten()
    met_bedrag = [
        p for p in projecten
        if (p.get("commercial") or {}).get("quoted") is not None
        or (p.get("commercial") or {}).get("accepted") is not None
    ]

    zelftest = "<p>Offerte 3500 EUR bevestigen</p>"
    if not any(patroon.search(zelftest) for patroon, _ in BEDRAG_PATRONEN):
        return ["ZELFTEST FAALT: de patronen herkennen zelfs `3500 EUR` niet. "
                "Deze test beschermt op dit moment niets."], []

    if not met_bedrag:
        meldingen.append(
            f"Let op: geen van de {len(projecten)} projecten heeft nu een bedrag in "
            f"`commercial`. De uitvoercontrole is dus groen zonder iets te bewijzen. "
            f"De patroonzelftest slaagde wel, dus de test werkt - er is alleen niets "
            f"te beschermen. Zodra er een offerte in staat, wordt dit een echte test.")
    else:
        namen = ", ".join(p["_slug"] for p in met_bedrag[:5])
        meldingen.append(f"{len(met_bedrag)} project(en) dragen een bedrag ({namen}). "
                         f"De uitvoercontrole test daarmee iets echts.")

    # Tegencontrole: de zaakvoerders horen de bedragen JUIST te zien. Zoekt op de exacte
    # waarden en niet op patronen, want een kaal `6000` in een tabelcel draagt geen
    # valutateken. Ontbreken ze daar ook, dan is de generator stuk in plaats van streng.
    admin = os.path.join(uitvoer, "administrator")
    if met_bedrag and os.path.isdir(admin):
        waarden = {str(v) for p in met_bedrag for v in
                   ((p.get("commercial") or {}).get("quoted"),
                    (p.get("commercial") or {}).get("accepted"))
                   if isinstance(v, (int, float))}
        tekst = ""
        for pad in glob.glob(os.path.join(admin, "**", "*.html"), recursive=True):
            with open(pad, encoding="utf-8") as f:
                tekst += f.read()
        ontbreekt = [w for w in waarden
                     if not re.search(rf"(?<![\d.,]){re.escape(w)}(?![\d.,])", tekst)]
        if ontbreekt:
            meldingen.append(
                f"Let op: {len(ontbreekt)} bedrag(en) uit de bron staan ook niet in de "
                f"administrator-uitvoer ({', '.join(sorted(ontbreekt))}). Dat is geen "
                f"lek, maar waarschijnlijk wel een bug - de zaakvoerders horen ze juist "
                f"wel te zien.")
    return [], meldingen


def main():
    uitvoer = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "dist")
    if not os.path.isdir(uitvoer):
        sys.exit(f"Uitvoermap {uitvoer} bestaat niet - draai eerst generate-views.py")

    harde_fouten, meldingen = controle_negatief(uitvoer)
    exacte, aantal_bedragen = controle_echte_bedragen(uitvoer)
    fouten = (harde_fouten + controle_structureel(uitvoer) +
              controle_uitvoer(uitvoer) + exacte)

    for m in meldingen:
        print(f"  {m}")
    print(f"  {aantal_bedragen} exact bedrag/bedragen uit de bron gecontroleerd tegen "
          f"de uitvoer van: {', '.join(BEPERKTE_ROLLEN)}.")

    if fouten:
        print(f"\nGEEN-LEK TEST GEFAALD - {len(fouten)} probleem/problemen:\n")
        for f in fouten:
            print(f"  - {f}")
        print("\nEr wordt niets gepubliceerd. Repareer de bron of de toegangsregels;\n"
              "zet deze test niet uit.")
        sys.exit(1)

    print(f"\nGeen-lek test geslaagd voor: {', '.join(BEPERKTE_ROLLEN)}")


if __name__ == "__main__":
    main()
