#!/usr/bin/env python3
"""Bouwt de kijklaag: een statische site per rol, uit dezelfde bron als het board.

Waarom statisch en per rol, en niet een app met een login die filtert: GitHub kan geen
deel van een repo verbergen (rechten gelden per repo, nooit per map), en GitHub Pages
publiceert een prive-repo gewoon publiek op alles onder Enterprise Cloud. De enige
scheiding die niet stuk kan is er een die al bij het bouwen gebeurt: de ateliersite bevat
geen bedragen omdat ze er nooit in geschreven zijn. Er is geen filter dat je kunt omzeilen
en geen payload waar de data alsnog in zit.

Elke lezing loopt via `akira/toegang.py`, ook lezingen die vanzelfsprekend mogen. Alleen
dan is het leeslogboek compleet, en alleen dan kan `test-geen-lek.py` aantonen dat de rol
`atelier` geen enkele verboden bron heeft aangeraakt.

Gebruik:
    python system/scripts/generate-views.py [uitvoermap]      # standaard: dist/
"""

import html
import json
import os
import shutil
import sys
from datetime import timedelta

from akira import ROOT, VANDAAG, VEROUDERD_NA, DEADLINE_HORIZON, NU_MAX
from akira.laden import lees_projecten, als_datum, naam, open_taken, lees_tekst
from akira.analyse import (
    pct, bereken_dekking, bereken_concentratie, bereken_onbeheerd,
    bereken_ongedateerd, bereken_overdue, bereken_ketens, bereken_prioriteitsdruk,
    bereken_verouderd, taken_per_persoon, beslissingen_open, lees_ritmen,
    tel_open_canon,
)
from akira.toegang import laad_rollen, mensen_per_rol

# De informatie-architectuur, in de volgorde waarin informatie er doorheen beweegt.
# Dit is de kern van de anti-blackbox-eis: niet "welke knoppen zijn er" maar "welke
# vakjes bestaan er en wat komt waar terecht". De teksten zijn voor iemand die de repo
# nooit gezien heeft en dat ook nooit hoeft.
VAKJES = [
    ("company/inbox", "Wat er binnenkomt",
     "Alles wat je tegen Chatty zegt, ruw en onbewerkt. Hier is nog niets uitgezocht. "
     "Binnen enkele minuten wordt het verdeeld over de vakjes hieronder.", "*.md"),
    ("company/projects/active", "Waar we aan werken",
     "Elk project heeft een status, een volgende stap, een eigenaar en taken. Dit is "
     "waar bijna alles uiteindelijk terechtkomt, en waar het board op gebaseerd is.", "*/project.yaml"),
    ("company/decisions", "Wat we besloten hebben",
     "Genomen beslissingen met de reden erbij. Geen mening en geen plan: iets waar we "
     "ons aan houden tot we het expliciet terugdraaien.", "*/*.md"),
    ("company/working/learnings", "Wat we denken te weten",
     "Observaties over hoe wij werken die zich beginnen te herhalen. Nog geen waarheid. "
     "Wie hieruit citeert, zegt erbij dat het een hypothese is.", "*.md"),
    ("company/knowledge", "Wat vaststaat",
     "Bedrijfswaarheid. Prijzen, werkwijzen, positionering. Hier komt alleen iets in "
     "nadat Tore en Farah het hebben goedgekeurd - een AI kan hier nooit rechtstreeks "
     "in schrijven.", "*/*.md"),
    ("company/ideas", "Wat we ooit willen",
     "De parkeerplaats. Ideeen die geen project zijn en misschien nooit worden.", "*.md"),
    ("company/rituals", "Wat we elke week afspreken",
     "De weekplannen van maandag en de wrap-ups van vrijdag, per week bewaard.", "*/*.md"),
    ("company/people", "Wie er is",
     "Collega's, stagiairs en externe contacten. Observaties worden toegevoegd, nooit "
     "overschreven - wat iemand toen deed blijft nuttig.", "*.yaml"),
    ("company/clients", "Wie onze klanten zijn",
     "Per klant een dossier. Gevoelige gegevens staan hier bewust niet in; die liggen "
     "in de Drive-vault en hier staat alleen een verwijzing.", "*/client.yaml"),
]

CSS = """
:root {
  --bg:#faf9f7; --vlak:#fff; --rand:#e3ded6; --tekst:#22201d; --zacht:#6b655c;
  --accent:#8a5a2b; --alarm:#9c2f2f; --alarm-vlak:#fbf0ef; --ok:#3f6b45;
  --schaduw:0 1px 2px rgba(0,0,0,.05);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg:#171614; --vlak:#211f1c; --rand:#3a3630; --tekst:#ece8e1; --zacht:#a09889;
    --accent:#d09a5e; --alarm:#e08b84; --alarm-vlak:#2e1f1d; --ok:#8fbf97;
    --schaduw:0 1px 2px rgba(0,0,0,.3);
  }
}
:root[data-theme="dark"] {
  --bg:#171614; --vlak:#211f1c; --rand:#3a3630; --tekst:#ece8e1; --zacht:#a09889;
  --accent:#d09a5e; --alarm:#e08b84; --alarm-vlak:#2e1f1d; --ok:#8fbf97;
  --schaduw:0 1px 2px rgba(0,0,0,.3);
}
* { box-sizing:border-box; }
body {
  margin:0; background:var(--bg); color:var(--tekst);
  font:16px/1.6 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
}
.wrap { max-width:60rem; margin:0 auto; padding:1.5rem 1.25rem 5rem; }
header { border-bottom:1px solid var(--rand); margin-bottom:1.75rem; padding-bottom:1rem; }
h1 { font-size:1.6rem; margin:0 0 .3rem; letter-spacing:-.01em; }
h2 { font-size:1.15rem; margin:2.25rem 0 .75rem; letter-spacing:-.01em; }
h3 { font-size:.95rem; margin:1.5rem 0 .5rem; color:var(--zacht);
     text-transform:uppercase; letter-spacing:.06em; }
nav { display:flex; flex-wrap:wrap; gap:.4rem; margin:.85rem 0 0; }
nav a {
  padding:.3rem .7rem; border:1px solid var(--rand); border-radius:99px;
  text-decoration:none; color:var(--zacht); font-size:.85rem; background:var(--vlak);
}
nav a:hover { color:var(--tekst); border-color:var(--accent); }
nav a[aria-current="page"] { color:var(--bg); background:var(--accent); border-color:var(--accent); }
a { color:var(--accent); }
.meta { color:var(--zacht); font-size:.85rem; }
.oud { color:var(--alarm); font-weight:600; }
.kaart {
  background:var(--vlak); border:1px solid var(--rand); border-radius:.6rem;
  padding:1rem 1.1rem; margin:.6rem 0; box-shadow:var(--schaduw);
}
.kaart h4 { margin:0 0 .2rem; font-size:1rem; }
.kaart p { margin:.35rem 0 0; color:var(--zacht); font-size:.92rem; }
.pad { font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.8rem; color:var(--zacht); }
.telling { float:right; font-size:.85rem; color:var(--zacht); }
.afgeschermd { border-style:dashed; opacity:.75; }
.tabelwrap { overflow-x:auto; margin:.5rem 0 1rem; }
table { border-collapse:collapse; width:100%; font-size:.93rem; }
th,td { text-align:left; padding:.5rem .6rem; border-bottom:1px solid var(--rand); vertical-align:top; }
th { color:var(--zacht); font-weight:600; font-size:.8rem;
     text-transform:uppercase; letter-spacing:.05em; }
tr:last-child td { border-bottom:none; }
.waarschuwing {
  background:var(--alarm-vlak); border-left:3px solid var(--alarm);
  padding:.75rem 1rem; margin:1rem 0; border-radius:0 .4rem .4rem 0;
}
.leeg { color:var(--zacht); font-style:italic; }
ul { padding-left:1.15rem; } li { margin:.2rem 0; }
footer { margin-top:3rem; padding-top:1rem; border-top:1px solid var(--rand);
         color:var(--zacht); font-size:.82rem; }
"""

PAGINAS = [
    ("index.html", "Het bord"),
    ("kaart.html", "De kaart"),
]


def e(x):
    """HTML-escape. Alles wat uit de yaml komt gaat hierlangs."""
    return html.escape(str(x if x is not None else ""))


def shell(titel, rol, inhoud, actief):
    nav = "".join(
        f'<a href="{b}"{" aria-current=\"page\"" if b == actief else ""}>{e(t)}</a>'
        for b, t in PAGINAS
    )
    return f"""<!doctype html>
<html lang="nl"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{e(titel)} - Akira</title>
<style>{CSS}</style>
</head><body><div class="wrap">
<header>
  <h1>{e(titel)}</h1>
  <div class="meta">Haus von FEB &middot; weergave voor <strong>{e(rol)}</strong>
    &middot; bijgewerkt {VANDAAG.isoformat()}</div>
  <nav>{nav}</nav>
</header>
{inhoud}
<footer>
  Gegenereerd uit de Akira-repo op {VANDAAG.isoformat()}. Deze pagina is een weergave,
  geen bron - wijzigen doe je door het tegen Chatty te zeggen.
</footer>
</div></body></html>
"""


def tabel(koppen, rijen, leeg="geen"):
    if not rijen:
        return f'<p class="leeg">{e(leeg)}</p>'
    th = "".join(f"<th>{e(k)}</th>" for k in koppen)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rijen)
    return f'<div class="tabelwrap"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


# --- pagina: het bord ------------------------------------------------------------

def pagina_bord(projecten, toegang):
    wachtend = [p for p in projecten if p.get("status") in ("waiting", "blocked")]
    lopend = [p for p in projecten if p not in wachtend]
    uit = []

    for prio, kop in (("now", "Nu"), ("next", "Next"), ("later", "Later")):
        groep = [p for p in lopend if p.get("priority") == prio]
        uit.append(f"<h2>{kop}</h2>")
        uit.append(tabel(
            ["Project", "Volgende stap", "Bij wie"],
            [[f"<strong>{e(naam(p))}</strong>", e(p.get("next_step") or "-"),
              e(p.get("next_step_owner") or "-")] for p in groep],
            "niets op deze lijst"))

    uit.append("<h2>Wacht op iemand anders</h2>")
    uit.append(tabel(["Project", "Wacht op"],
                     [[f"<strong>{e(naam(p))}</strong>", e(p.get("waiting_for") or "onbekend")]
                      for p in wachtend], "niets"))

    deadlines = []
    for p in projecten:
        d = als_datum(p.get("deadline"))
        if d and VANDAAG <= d <= VANDAAG + timedelta(days=DEADLINE_HORIZON):
            deadlines.append((d, p))
    deadlines.sort(key=lambda x: x[0])
    uit.append(f"<h2>Deadlines binnen {DEADLINE_HORIZON} dagen</h2>")
    uit.append(tabel(["Datum", "Over", "Project"],
                     [[d.isoformat(),
                       "vandaag" if (d - VANDAAG).days == 0
                       else f"{(d - VANDAAG).days} dagen", e(naam(p))]
                      for d, p in deadlines], "geen deadline in zicht"))

    beslissingen = beslissingen_open(projecten)
    uit.append("<h2>Beslissingen die op iemand wachten</h2>")
    uit.append(tabel(["Project", "Waarover"],
                     [[e(pr), e(v)] for pr, v in beslissingen], "geen"))

    uit.append("<h2>Botsingen en belasting</h2>")
    dekking = bereken_dekking(projecten)
    uit.append("<h3>Dekking</h3>")
    uit.append(tabel(["Veld", "Ingevuld", "Dekking"], [
        ["Taken met een eigenaar", f"{dekking['met_owner']} van {dekking['taken']}",
         pct(dekking['met_owner'], dekking['taken'])],
        ["Taken met een datum", f"{dekking['met_due']} van {dekking['taken']}",
         pct(dekking['met_due'], dekking['taken'])],
        ["Projecten met een deadline",
         f"{dekking['met_deadline']} van {dekking['projecten']}",
         pct(dekking['met_deadline'], dekking['projecten'])],
    ]))
    uit.append('<p class="meta">Staat er hieronder "geen", lees dat dan samen met deze '
               "tabel. Bij een lage dekking betekent een lege lijst eerder "
               '"niet meetbaar" dan "geen probleem".</p>')

    verdeling, over, totaal = bereken_concentratie(projecten)
    uit.append("<h3>Wie is de volgende stap</h3>")
    uit.append("<ul>" + "".join(
        f"<li>{e(w)}: {n} van {totaal} projecten ({pct(n, totaal)})</li>"
        for w, n in verdeling) + "</ul>")
    for w, n in over:
        uit.append(f'<div class="waarschuwing"><strong>{e(w)}</strong> is de volgende stap '
                   f"op {n} van {totaal} projecten ({pct(n, totaal)}). Elk project dat "
                   "vooruit moet, wacht op dezelfde persoon.</div>")

    onbeheerd = bereken_onbeheerd(projecten)
    uit.append("<h3>Taken zonder eigenaar</h3>")
    if onbeheerd:
        uit.append(f"<p>{sum(n for _, n in onbeheerd)} open taken hebben geen naam "
                   "erbij. Dit is de werklijst voor de maandagplanning.</p>")
    uit.append(tabel(["Project", "Taken zonder eigenaar"],
                     [[e(pr), n] for pr, n in onbeheerd], "geen"))

    ongedateerd = bereken_ongedateerd(projecten)
    uit.append("<h3>Taken zonder datum</h3>")
    if ongedateerd:
        uit.append(f"<p>{sum(n for _, n in ongedateerd)} open taken hebben geen datum. "
                   "Zolang dat zo is, valt er niet op te plannen.</p>")
    uit.append(tabel(["Project", "Taken zonder datum"],
                     [[e(pr), n] for pr, n in ongedateerd[:8]], "geen"))

    otaken, odeadlines = bereken_overdue(projecten)
    uit.append("<h3>Over datum heen</h3>")
    uit.append(tabel(["Hoe lang", "Project", "Wat", "Wie"],
                     [[f'<span class="oud">{d} dagen</span>', e(pr), e(t), e(o)]
                      for d, pr, t, o in otaken] +
                     [[f'<span class="oud">{d} dagen</span>', e(pr),
                       "projectdeadline verstreken", "-"] for d, pr in odeadlines],
                     "niets over datum"))

    ketens, fouten, per_slug = bereken_ketens(projecten)
    uit.append("<h3>Wat waarop wacht</h3>")
    if ketens:
        regels = []
        for doel, afh in ketens:
            wachters = ", ".join(f"{e(s)} (wacht op: {e(u)})" for s, u in afh)
            regels.append(f"<li><strong>{e(doel)}</strong> blokkeert {len(afh)} "
                          f"project{'en' if len(afh) != 1 else ''}: {wachters}</li>")
        uit.append("<ul>" + "".join(regels) + "</ul>")
    else:
        uit.append('<p class="leeg">geen vastgelegde afhankelijkheden</p>')
    if fouten:
        uit.append('<div class="waarschuwing"><strong>Datafouten in de afhankelijkheden:'
                   "</strong><ul>" + "".join(f"<li>{e(f)}</li>" for f in fouten) +
                   "</ul></div>")

    nu, nu_oud = bereken_prioriteitsdruk(projecten)
    uit.append("<h3>Prioriteitsdruk</h3>")
    if len(nu) > NU_MAX:
        uit.append(f'<div class="waarschuwing">{len(nu)} projecten staan op Nu, de '
                   f"drempel is {NU_MAX}. Daarvan zijn er {len(nu_oud)} langer dan "
                   f'{VEROUDERD_NA} dagen niet bijgewerkt: "nu" betekent hier dan weinig '
                   "meer. De vrijdag wrap-up is het moment om die lijst opnieuw te kiezen."
                   "</div>")
    else:
        uit.append(f"<p>{len(nu)} projecten op Nu, drempel {NU_MAX}. "
                   f"Daarvan {len(nu_oud)} verouderd.</p>")

    ritmen = lees_ritmen()
    # Twee lezingen die buiten de gewone toegangsweg omgaan, allebei expliciet gemeld
    # zodat test-geen-lek.py ze ziet. De ritmebestanden mag `atelier` gewoon zien; de
    # canon-queue niet, maar het AANTAL open voorstellen is geen bedrag en geen inhoud.
    for soort, d in ritmen.items():
        if d:
            toegang.noteer_gelezen(f"company/rituals/{d.year}/W-{soort}.md")
    if not toegang.mag("company/canon-queue.md"):
        toegang.noteer_uitzondering(
            "company/canon-queue.md",
            "alleen het aantal open voorstellen wordt getoond, nooit de inhoud - "
            "de voorstellen zelf dragen bedragen")

    uit.append("<h2>Gezondheid</h2>")
    def ritme(d):
        if not d:
            return '<span class="oud">nog nooit gedraaid</span>'
        return f"{d.isoformat()} ({(VANDAAG - d).days} dagen geleden)"
    uit.append(tabel(["Meting", "Stand"], [
        ["Actieve projecten", len(projecten)],
        [f"Projecten niet bijgewerkt in {VEROUDERD_NA} dagen", len(bereken_verouderd(projecten))],
        ["Taken open per persoon", ", ".join(
            f"{e(w)}: {n}" for w, n in sorted(taken_per_persoon(projecten).items(),
                                              key=lambda x: -x[1]))],
        ["Voorstellen die op goedkeuring wachten", tel_open_canon()],
        ["Laatste maandagplanning", ritme(ritmen["maandag"])],
        ["Laatste vrijdag wrap-up", ritme(ritmen["vrijdag"])],
    ]))
    return "\n".join(uit)


# --- pagina: de kaart ------------------------------------------------------------

def pagina_kaart(toegang):
    """De informatie-architectuur, leesbaar voor wie de repo nooit zag.

    Afgeschermde vakjes worden WEL getoond, met de melding dat de inhoud niet voor deze
    rol is. Ze weglaten zou een tweede blackbox maken: je kunt niet begrijpen hoe
    informatie stroomt als een deel van de stroom onzichtbaar is. Segmentatie waarvan je
    het bestaan kent, is geen geheim systeem maar een afspraak.
    """
    import glob
    uit = ["<p>Alles wat je tegen Akira zegt wordt verdeeld over een vast aantal vakjes. "
           "Dit is dat rijtje. Wie weet welke vakjes er zijn, weet ook wat hij kan "
           "vragen.</p>",
           '<div class="kaart"><h4>Wat er gebeurt als je iets vertelt</h4>'
           "<p>Je praat tegen Chatty &rarr; het komt ruw binnen bij "
           "<em>Wat er binnenkomt</em> &rarr; binnen enkele minuten wordt het verdeeld "
           "over de juiste vakjes hieronder &rarr; raakt het prijzen of werkwijzen, dan "
           "wordt het een <em>voorstel</em> en beslissen Tore en Farah of het "
           "bedrijfswaarheid wordt.</p></div>",
           "<h2>De vakjes</h2>"]

    for pad, kop, wat, patroon in VAKJES:
        zichtbaar = toegang.mag(f"{pad}/{patroon.replace('*/', 'x/').replace('*', 'x')}")
        bestanden = glob.glob(os.path.join(ROOT, pad, patroon))
        aantal = len(bestanden)
        if zichtbaar:
            telling = f"{aantal} {'item' if aantal == 1 else 'items'}"
            klasse = "kaart"
            extra = ""
        else:
            telling = "niet voor jouw rol"
            klasse = "kaart afgeschermd"
            extra = ("<p><em>Dit vakje bestaat wel, maar de inhoud is voor de "
                     "zaakvoerders. Je weet dus dat het er is, en aan wie je het kunt "
                     "vragen.</em></p>")
        uit.append(f'<div class="{klasse}"><span class="telling">{e(telling)}</span>'
                   f'<h4>{e(kop)}</h4><p>{e(wat)}</p>{extra}'
                   f'<p class="pad">{e(pad)}/</p></div>')

    uit.append("<h2>De drie regels waar dit op rust</h2>")
    uit.append(tabel(["Regel", "Wat het betekent"], [
        ["Ruw &rarr; vermoeden &rarr; waarheid",
         "Niets wordt bedrijfswaarheid zonder dat een mens ja zegt. Een AI mag "
         "vastleggen en voorstellen, nooit vaststellen."],
        ["Wie het mag zien, staat vast",
         "Wat jouw rol betekent lees je hieronder. Het is geen instelling van het "
         "moment maar een afspraak die in de repo staat."],
        ["Overzichten zijn altijd gemaakt, nooit getypt",
         "Deze pagina's worden gegenereerd uit de projectbestanden. Klopt er iets niet, "
         "dan klopt de bron niet - en die repareer je door het te zeggen."],
    ]))

    uit.append("<h2>Wat de rollen betekenen</h2>")
    rollen = laad_rollen()
    wie = mensen_per_rol()
    uit.append(tabel(["Rol", "Wat die betekent", "Wie"], [
        [f"<strong>{e(r)}</strong>", e(t.betekent),
         e(", ".join(wie.get(r, [])) or "-")]
        for r, t in rollen.items()]))
    uit.append('<p class="meta">Stagiairs en tijdelijke medewerkers krijgen de rol '
               "atelier via hun e-mailadres, zonder eigen bestand.</p>")
    return "\n".join(uit)


# --- bouwen ----------------------------------------------------------------------

def bouw(rol, toegang, uitvoer):
    map_ = os.path.join(uitvoer, rol)
    os.makedirs(map_, exist_ok=True)

    projecten = []
    for p in lees_projecten():
        if not toegang.noteer_gelezen(p["_pad"]):
            continue
        projecten.append(toegang.strip_velden("project.yaml", p))
    toegang.noteer_gelezen("company/BOARD.md")

    paginas = {
        "index.html": ("Het bord", pagina_bord(projecten, toegang)),
        "kaart.html": ("De kaart", pagina_kaart(toegang)),
    }
    for bestand, (titel, inhoud) in paginas.items():
        with open(os.path.join(map_, bestand), "w", encoding="utf-8", newline="\n") as f:
            f.write(shell(titel, rol, inhoud, bestand))

    return {"rol": rol, "projecten": len(projecten),
            "gelezen": sorted(set(toegang.gelezen)),
            "geweigerd": sorted(set(toegang.geweigerd)),
            "uitzonderingen": toegang.uitzonderingen}


def main():
    uitvoer = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "dist")
    if os.path.isdir(uitvoer):
        shutil.rmtree(uitvoer)
    os.makedirs(os.path.join(uitvoer, "_logs"), exist_ok=True)

    for rol, toegang in laad_rollen().items():
        log = bouw(rol, toegang, uitvoer)
        with open(os.path.join(uitvoer, "_logs", f"{rol}.json"), "w",
                  encoding="utf-8", newline="\n") as f:
            json.dump(log, f, indent=2, ensure_ascii=False)
        print(f"{rol}: {log['projecten']} projecten, "
              f"{len(log['gelezen'])} bronnen gelezen, "
              f"{len(log['geweigerd'])} geweigerd")


if __name__ == "__main__":
    main()
