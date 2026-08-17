"""De berekeningen over alle projecten heen.

Deze functies zijn de reden dat er een gedeelde laag is. Ze rekenen dingen uit die een
model met de hand vroeg of laat stil verkeerd rekent - eigenaarsconcentratie over
zeventien bestanden, een afhankelijkheidsgraaf, dekkingspercentages. Zowel het board als
de site leest ze hier, zodat er geen tweede antwoord kan ontstaan.

Ontwerpregel die in al deze functies terugkomt: dekking gaat voor bevinding. Een lege
lijst betekent "geen probleem" of "geen data", en die twee zien er identiek uit tenzij je
er de dekkingstabel naast legt.
"""

import glob
import os
import re
from datetime import timedelta

from . import ROOT, VANDAAG, VEROUDERD_NA, CONCENTRATIE_DREMPEL
from .laden import als_datum, naam, open_taken


def pct(deel, totaal):
    return f"{round(100 * deel / totaal)}%" if totaal else "n.v.t."


def bereken_dekking(projecten):
    """Hoeveel van de velden waar de rest op rekent, is uberhaupt ingevuld.

    Dit staat bovenaan de sectie omdat een lege lijst eronder anders niet te lezen is:
    "geen botsingen" en "geen data om botsingen uit af te leiden" zien er identiek uit.
    """
    taken = [t for p in projecten for t in open_taken(p)]
    return {
        "taken": len(taken),
        "met_due": sum(1 for t in taken if als_datum(t.get("due"))),
        "met_owner": sum(1 for t in taken if t.get("owner")),
        "projecten": len(projecten),
        "met_deadline": sum(1 for p in projecten if als_datum(p.get("deadline"))),
    }


def bereken_concentratie(projecten):
    """Verdeling van next_step_owner. Vuurt boven CONCENTRATIE_DREMPEL.

    Dit is het antwoord op "botsen er projecten met elkaar". Meestal niet - ze botsen
    allemaal met dezelfde persoon.
    """
    verdeling = {}
    for p in projecten:
        eigenaar = p.get("next_step_owner") or "niemand"
        verdeling[eigenaar] = verdeling.get(eigenaar, 0) + 1
    totaal = len(projecten) or 1
    gesorteerd = sorted(verdeling.items(), key=lambda x: -x[1])
    overschrijders = [
        (naam_, n) for naam_, n in gesorteerd if n / totaal > CONCENTRATIE_DREMPEL
    ]
    return gesorteerd, overschrijders, totaal


def bereken_onbeheerd(projecten):
    """Open taken zonder eigenaar, per project. De werklijst voor maandag."""
    rijen = []
    for p in projecten:
        zonder = [t for t in open_taken(p) if not t.get("owner")]
        if zonder:
            rijen.append((naam(p), len(zonder)))
    return sorted(rijen, key=lambda x: -x[1])


def bereken_ongedateerd(projecten):
    """Open taken zonder due-datum, per project."""
    rijen = []
    for p in projecten:
        zonder = [t for t in open_taken(p) if not als_datum(t.get("due"))]
        if zonder:
            rijen.append((naam(p), len(zonder)))
    return sorted(rijen, key=lambda x: -x[1])


def bereken_overdue(projecten):
    """Taken en projecten waarvan de datum voorbij is.

    Toont dagen, niet de datum: "161 dagen" leest als alarm, "2026-03-09" niet.
    """
    taken, deadlines = [], []
    for p in projecten:
        for t in open_taken(p):
            d = als_datum(t.get("due"))
            if d and d < VANDAAG:
                taken.append(((VANDAAG - d).days, naam(p), t.get("task"),
                              t.get("owner") or "niemand"))
        d = als_datum(p.get("deadline"))
        if d and d < VANDAAG:
            deadlines.append(((VANDAAG - d).days, naam(p)))
    return sorted(taken, key=lambda x: -x[0]), sorted(deadlines, key=lambda x: -x[0])


def bereken_ketens(projecten):
    """Bouwt de afhankelijkheidsgraaf uit blocked_by.

    Rapporteert datafouten (onbekende slug, zelfverwijzing, cyclus) apart en breekt een
    cyclus nooit stil: een graaf die zichzelf stilletjes repareert, verbergt precies de
    fout die je wilt zien.
    """
    per_slug = {p["_slug"]: p for p in projecten}
    blokkeert = {}   # slug -> [(afhankelijke slug, until)]
    fouten = []

    for p in projecten:
        for entry in (p.get("blocked_by") or []):
            if not isinstance(entry, dict):
                fouten.append(f"{p['_slug']}: blocked_by-item is geen mapping "
                              f"(verwacht `project:` en `until:`)")
                continue
            doel = entry.get("project")
            until = entry.get("until")
            if not doel:
                fouten.append(f"{p['_slug']}: blocked_by-item zonder `project:`")
                continue
            if not until:
                fouten.append(f"{p['_slug']}: blocked_by naar {doel} zonder `until:` - "
                              f"zonder die stap blijft dit eeuwig geblokkeerd op papier")
            if doel == p["_slug"]:
                fouten.append(f"{p['_slug']}: blocked_by verwijst naar zichzelf")
                continue
            if doel not in per_slug:
                # Kan een afgerond en gearchiveerd project zijn: dan is de blokkade weg.
                fouten.append(f"{p['_slug']}: blocked_by verwijst naar onbekend project "
                              f"`{doel}` (afgerond, hernoemd of typefout?)")
                continue
            if (per_slug[doel].get("status") or "") in ("done", "archived"):
                continue  # opgelost, telt niet als blokkade
            blokkeert.setdefault(doel, []).append((p["_slug"], until or "?"))

    # Cyclusdetectie over de opgebouwde graaf.
    naar = {}
    for doel, afhankelijken in blokkeert.items():
        for slug, _ in afhankelijken:
            naar.setdefault(slug, []).append(doel)
    kleur = {}

    def bezoek(slug, pad):
        kleur[slug] = "grijs"
        for volgende in naar.get(slug, []):
            if kleur.get(volgende) == "grijs":
                fouten.append("cyclus in blocked_by: " + " -> ".join(pad + [volgende]))
            elif kleur.get(volgende) != "zwart":
                bezoek(volgende, pad + [volgende])
        kleur[slug] = "zwart"

    for slug in list(naar):
        if kleur.get(slug) != "zwart":
            bezoek(slug, [slug])

    gesorteerd = sorted(blokkeert.items(), key=lambda x: -len(x[1]))
    return gesorteerd, fouten, per_slug


def bereken_prioriteitsdruk(projecten):
    """Hoeveel projecten staan op Nu, en hoeveel daarvan zijn verouderd."""
    nu = [p for p in projecten if p.get("priority") == "now"]
    verouderd = [
        p for p in nu
        if (als_datum(p.get("updated")) or VANDAAG) < VANDAAG - timedelta(days=VEROUDERD_NA)
    ]
    return nu, verouderd


def bereken_verouderd(projecten):
    """Actieve projecten waarvan de status te lang niet is aangeraakt."""
    return [
        p for p in projecten
        if p.get("status") == "active"
        and (als_datum(p.get("updated")) or VANDAAG) < VANDAAG - timedelta(days=VEROUDERD_NA)
    ]


def taken_per_persoon(projecten):
    """Open taken geteld per eigenaar, met een expliciete bak voor niemand.

    Die bak is het punt: 32 taken zonder naam verdwijnen anders uit het beeld, terwijl
    dat juist de werklijst is.
    """
    telling = {}
    for p in projecten:
        for t in open_taken(p):
            eigenaar = t.get("owner") or "niemand toegewezen"
            telling[eigenaar] = telling.get(eigenaar, 0) + 1
    return telling


def beslissingen_open(projecten):
    """(project, vraag) voor elke open taak met needs_decision."""
    uit = []
    for p in projecten:
        for t in open_taken(p):
            if t.get("needs_decision"):
                uit.append((naam(p), t.get("task")))
    return uit


def lees_ritmen():
    """Wanneer draaide de laatste maandagplanning en vrijdag wrap-up.

    De enige plek waar deze laag buiten project.yaml leest. Dat is bewust: het ritueel
    dat hier eerder is doodgebloed, deed dat onzichtbaar - niemand miste het, want niets
    telde het. Een directorylisting is deterministisch, dus de garantie blijft overeind.
    """
    resultaat = {}
    for soort in ("maandag", "vrijdag"):
        patroon = os.path.join(ROOT, "company", "rituals", "*", f"W*-{soort}.md")
        datums = []
        for pad in glob.glob(patroon):
            with open(pad, encoding="utf-8") as f:
                kop = f.read(400)
            gevonden = re.search(r"^datum:\s*(\d{4}-\d{2}-\d{2})", kop, re.MULTILINE)
            if gevonden:
                d = als_datum(gevonden.group(1))
                if d:
                    datums.append(d)
        resultaat[soort] = max(datums) if datums else None
    return resultaat


def tel_open_canon():
    """Openstaande canon-voorstellen, geteld voor de gezondheidstabel.

    Telt alleen het aantal. De inhoud van de queue is administrator-materiaal (er staan
    levende prijsvoorstellen in), maar het getal zelf is dat niet.
    """
    pad = os.path.join(ROOT, "company", "canon-queue.md")
    if not os.path.exists(pad):
        return 0
    with open(pad, encoding="utf-8") as f:
        inhoud = f.read().split("## Afgehandeld")[0]
    return inhoud.count("### V-")
