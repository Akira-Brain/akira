#!/usr/bin/env python3
"""Genereert company/BOARD.md uit de project.yaml-bestanden.

Waarom dit een script is en geen taak voor het model: het board is per ontwerp een
gegenereerde view (beslissing D5). Liet je een model het bijwerken, dan bewerkt het
stukjes prozа en loopt de inhoud stil uit de pas met de yaml. Dat gebeurde ook: de
eerste versie miste deadlines volledig en telde captures verkeerd, waardoor de daily
brief meldde dat er geen deadlines waren terwijl er een over zes dagen stond.

Deterministisch, gratis, en altijd in overeenstemming met de bron.

Het script leest op een plek buiten project.yaml: company/rituals/, om te tellen hoe
lang geleden de laatste maandagplanning en vrijdag wrap-up waren. Dat is bewust. Het
ritueel dat hier eerder is doodgebloed, deed dat onzichtbaar - niemand miste het,
want niets telde het. Een directorylisting is deterministisch, dus de garantie van dit
script blijft overeind.

Bekende zwakte: dit script leest alleen company/. Zolang personal/tore/ eigen werk
draagt, zijn de belastingcijfers voor Tore structureel te laag - het board ziet zijn
persoonlijke tenant niet.

Gebruik:
    python system/scripts/generate-board.py [aantal_open_captures]
"""

import sys
import glob
import os
import re
from datetime import date, datetime, timedelta

try:
    import yaml
except ImportError:
    sys.exit("PyYAML ontbreekt: pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VANDAAG = date.today()
VEROUDERD_NA = 14
DEADLINE_HORIZON = 14

# Drempels voor de sectie "Botsingen en belasting". Bewust hardcoded en bewust laag:
# dit is een team van vijf, geen configuratie waard. Wie ze wil wijzigen, wijzigt ze
# hier en legt in de commit uit waarom de werkelijkheid veranderd is.
CONCENTRATIE_DREMPEL = 0.5   # aandeel projecten met dezelfde next_step_owner
NU_MAX = 5                   # maximaal aantal projecten op priority: now
DEKKING_DUE_MIN = 0.5        # onder deze dekking is datumanalyse onbetrouwbaar
DEKKING_OWNER_MIN = 0.8      # onder deze dekking is verdelingsanalyse onbetrouwbaar

# Weekbelasting per persoon (hoeveel gedateerd werk valt in welke week) is bewust NIET
# gebouwd. Bij de huidige dekking - 2 van 57 taken heeft een datum - zou die tabel
# alleen ruis tonen en er gezaghebbend uitzien. Bouw hem zodra de dekking van `due`
# boven DEKKING_DUE_MIN komt; maandagplanning is het ritueel dat die datums aanmaakt.


def lees_projecten():
    projecten = []
    patroon = os.path.join(ROOT, "company", "projects", "active", "*", "project.yaml")
    for pad in sorted(glob.glob(patroon)):
        with open(pad, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        data["_slug"] = os.path.basename(os.path.dirname(pad))
        projecten.append(data)
    return projecten


def als_datum(waarde):
    if isinstance(waarde, date):
        return waarde
    if isinstance(waarde, str):
        try:
            return datetime.strptime(waarde.strip(), "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


def tabel(projecten):
    if not projecten:
        return "*leeg*\n"
    regels = ["| Project | Volgende stap | Bij wie |", "|---|---|---|"]
    for p in projecten:
        regels.append(
            f"| **{p.get('title') or p['_slug']}** "
            f"| {p.get('next_step') or '-'} "
            f"| {p.get('next_step_owner') or '-'} |"
        )
    return "\n".join(regels) + "\n"


def naam(p):
    """Toonbare naam van een project."""
    return p.get("title") or p["_slug"]


def open_taken(p):
    """Taken die nog werk zijn: niet done, niet dropped."""
    return [
        t for t in (p.get("tasks") or [])
        if t.get("status") not in ("done", "dropped")
    ]


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


def lees_ritmen():
    """Wanneer draaide de laatste maandagplanning en vrijdag wrap-up.

    De enige plek waar dit script buiten project.yaml leest. Zie de moduledocstring.
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


def main():
    open_captures = sys.argv[1] if len(sys.argv) > 1 else "onbekend"
    projecten = lees_projecten()

    wachtend = [p for p in projecten if p.get("status") in ("waiting", "blocked")]
    lopend = [p for p in projecten if p not in wachtend]
    per_prio = {
        prio: [p for p in lopend if p.get("priority") == prio]
        for prio in ("now", "next", "later")
    }

    # Deadlines binnen de horizon
    deadlines = []
    for p in projecten:
        d = als_datum(p.get("deadline"))
        if d and VANDAAG <= d <= VANDAAG + timedelta(days=DEADLINE_HORIZON):
            deadlines.append((d, p))
    deadlines.sort(key=lambda x: x[0])

    # Beslissingen en taken
    beslissingen, taken_per_persoon = [], {}
    for p in projecten:
        for t in p.get("tasks") or []:
            if t.get("status") in ("done", "dropped"):
                continue
            eigenaar = t.get("owner") or "niemand toegewezen"
            taken_per_persoon.setdefault(eigenaar, 0)
            taken_per_persoon[eigenaar] += 1
            if t.get("needs_decision"):
                beslissingen.append((p.get("title") or p["_slug"], t.get("task")))

    verouderd = [
        p for p in projecten
        if p.get("status") == "active"
        and (als_datum(p.get("updated")) or VANDAAG) < VANDAAG - timedelta(days=VEROUDERD_NA)
    ]

    queue = os.path.join(ROOT, "company", "canon-queue.md")
    open_canon = 0
    if os.path.exists(queue):
        with open(queue, encoding="utf-8") as f:
            inhoud = f.read().split("## Afgehandeld")[0]
        open_canon = inhoud.count("### V-")

    uit = [
        "# BOARD - Haus von FEB",
        "",
        "**GEGENEREERD BESTAND. Bewerk dit niet met de hand.**",
        "Bron: alle `project.yaml` in `projects/active/`, via",
        "`system/scripts/generate-board.py`.",
        "",
        f"Laatst gegenereerd: {VANDAAG.isoformat()}",
        "",
        "---",
        "",
        "## Nu",
        "",
        tabel(per_prio["now"]),
        "## Next",
        "",
        tabel(per_prio["next"]),
        "## Later",
        "",
        tabel(per_prio["later"]),
        "## Waiting",
        "",
    ]

    if wachtend:
        uit.append("| Project | Wacht op |")
        uit.append("|---|---|")
        for p in wachtend:
            uit.append(
                f"| **{p.get('title') or p['_slug']}** | {p.get('waiting_for') or 'onbekend'} |"
            )
        uit.append("")
    else:
        uit.append("*leeg*\n")

    uit += ["---", "", f"## Deadlines binnen {DEADLINE_HORIZON} dagen", ""]
    if deadlines:
        uit.append("| Datum | Over | Project |")
        uit.append("|---|---|---|")
        for d, p in deadlines:
            dagen = (d - VANDAAG).days
            wanneer = "vandaag" if dagen == 0 else f"{dagen} dag{'en' if dagen != 1 else ''}"
            uit.append(f"| {d.isoformat()} | {wanneer} | {p.get('title') or p['_slug']} |")
        uit.append("")
    else:
        uit.append("*geen*\n")

    uit += ["## Beslissingen die op iemand wachten", ""]
    if beslissingen:
        for project, vraag in beslissingen:
            uit.append(f"- **{project}**: {vraag}")
        uit.append("")
    else:
        uit.append("*geen*\n")

    uit += ["## Open taken per persoon", ""]
    if taken_per_persoon:
        for persoon, aantal in sorted(taken_per_persoon.items(), key=lambda x: -x[1]):
            uit.append(f"- {persoon}: {aantal}")
        uit.append("")
    else:
        uit.append("*geen*\n")

    # --- Botsingen en belasting ---------------------------------------------------
    dekking = bereken_dekking(projecten)
    conc_verdeling, conc_over, conc_totaal = bereken_concentratie(projecten)
    onbeheerd = bereken_onbeheerd(projecten)
    ongedateerd = bereken_ongedateerd(projecten)
    overdue_taken, overdue_deadlines = bereken_overdue(projecten)
    ketens, keten_fouten, per_slug = bereken_ketens(projecten)
    nu_projecten, nu_verouderd = bereken_prioriteitsdruk(projecten)

    uit += ["---", "", "## Botsingen en belasting", "", "### Dekking", ""]

    def pct(deel, totaal):
        return f"{round(100 * deel / totaal)}%" if totaal else "n.v.t."

    uit += [
        "| Veld | Ingevuld | Dekking |",
        "|---|---|---|",
        f"| Taken met een eigenaar | {dekking['met_owner']} van {dekking['taken']} "
        f"| {pct(dekking['met_owner'], dekking['taken'])} |",
        f"| Taken met een datum | {dekking['met_due']} van {dekking['taken']} "
        f"| {pct(dekking['met_due'], dekking['taken'])} |",
        f"| Projecten met een deadline | {dekking['met_deadline']} van {dekking['projecten']} "
        f"| {pct(dekking['met_deadline'], dekking['projecten'])} |",
        "",
        "Staat er hieronder \"geen\", lees dat dan samen met deze tabel. Bij een lage "
        "dekking betekent een lege lijst eerder \"niet meetbaar\" dan \"geen probleem\". "
        f"Datumanalyse is pas betrouwbaar boven {round(DEKKING_DUE_MIN * 100)}% gedateerde "
        f"taken, verdelingsanalyse boven {round(DEKKING_OWNER_MIN * 100)}% toegewezen taken.",
        "",
        "### Eigenaarsconcentratie",
        "",
    ]

    for eigenaar, aantal in conc_verdeling:
        uit.append(f"- {eigenaar}: {aantal} van {conc_totaal} projecten "
                   f"({pct(aantal, conc_totaal)})")
    uit.append("")
    if conc_over:
        for eigenaar, aantal in conc_over:
            uit.append(
                f"**{eigenaar} is next_step_owner op {aantal} van {conc_totaal} projecten "
                f"({pct(aantal, conc_totaal)}) - de drempel is "
                f"{round(CONCENTRATIE_DREMPEL * 100)}%. Elk project dat vooruit moet, "
                f"wacht op dezelfde persoon.**"
            )
        uit.append("")
    else:
        uit.append("Geen enkele persoon zit boven de drempel.\n")

    uit += ["### Taken zonder eigenaar", ""]
    if onbeheerd:
        totaal_onbeheerd = sum(n for _, n in onbeheerd)
        uit.append(f"{totaal_onbeheerd} open taken hebben geen eigenaar. Dit is de "
                   f"werklijst voor de maandagplanning.")
        uit.append("")
        uit.append("| Project | Taken zonder eigenaar |")
        uit.append("|---|---|")
        for project, aantal in onbeheerd:
            uit.append(f"| {project} | {aantal} |")
        uit.append("")
    else:
        uit.append("*geen*\n")

    uit += ["### Taken zonder datum", ""]
    if ongedateerd:
        totaal_ongedateerd = sum(n for _, n in ongedateerd)
        uit.append(f"{totaal_ongedateerd} open taken hebben geen `due`. Zolang dat zo is, "
                   f"valt er niet op te plannen.")
        uit.append("")
        for project, aantal in ongedateerd[:5]:
            uit.append(f"- {project}: {aantal}")
        if len(ongedateerd) > 5:
            uit.append(f"- (en {len(ongedateerd) - 5} andere projecten)")
        uit.append("")
    else:
        uit.append("*geen*\n")

    uit += ["### Over datum heen", ""]
    if overdue_taken or overdue_deadlines:
        for dagen, project, taak, eigenaar in overdue_taken:
            uit.append(f"- **{dagen} dagen** - {project}: {taak} ({eigenaar})")
        for dagen, project in overdue_deadlines:
            uit.append(f"- **{dagen} dagen** - {project}: projectdeadline verstreken")
        uit.append("")
    else:
        uit.append("*geen*\n")

    uit += ["### Ketens", ""]
    if ketens:
        for doel, afhankelijken in ketens:
            doelproject = per_slug.get(doel, {})
            bijgewerkt = als_datum(doelproject.get("updated"))
            ouderdom = (
                f" Dit project is {(VANDAAG - bijgewerkt).days} dagen niet bijgewerkt."
                if bijgewerkt else ""
            )
            wachters = ", ".join(
                f"{slug} (wacht op: {until})" for slug, until in afhankelijken
            )
            uit.append(
                f"- **{doel} blokkeert {len(afhankelijken)} "
                f"project{'en' if len(afhankelijken) != 1 else ''}:** {wachters}.{ouderdom}"
            )
        uit.append("")
    else:
        uit.append("*geen vastgelegde afhankelijkheden* - zie de dekkingstabel: "
                   "`blocked_by` is optioneel en wordt alleen ingevuld tijdens de "
                   "rituelen.\n")

    if keten_fouten:
        uit += ["### Datafouten", ""]
        for fout in keten_fouten:
            uit.append(f"- {fout}")
        uit.append("")

    uit += ["### Prioriteitsdruk", ""]
    if len(nu_projecten) > NU_MAX:
        uit.append(
            f"**{len(nu_projecten)} projecten staan op Nu, de drempel is {NU_MAX}.** "
            f"Daarvan zijn er {len(nu_verouderd)} langer dan {VEROUDERD_NA} dagen niet "
            f"bijgewerkt: \"nu\" betekent op dit board dan weinig meer."
        )
    else:
        uit.append(f"{len(nu_projecten)} projecten op Nu, drempel {NU_MAX}. "
                   f"Daarvan {len(nu_verouderd)} verouderd.")
    uit.append("")
    uit.append("De vrijdag wrap-up is het moment waarop deze lijst opnieuw gekozen wordt.")
    uit.append("")

    # --- Gezondheid ---------------------------------------------------------------
    ritmen = lees_ritmen()

    def ritme_regel(label, d):
        if not d:
            return f"| {label} | geen gevonden |"
        dagen = (VANDAAG - d).days
        return f"| {label} | {d.isoformat()} ({dagen} dagen geleden) |"

    uit += [
        "---",
        "",
        "## Gezondheid",
        "",
        "| Meting | Aantal |",
        "|---|---|",
        f"| Actieve projecten | {len(projecten)} |",
        f"| Projecten met verouderde status (>{VEROUDERD_NA} dagen) | {len(verouderd)} |",
        f"| Ongerouteerde captures | {open_captures} |",
        f"| Openstaande canon-voorstellen | {open_canon} |",
        ritme_regel("Laatste maandagplanning", ritmen["maandag"]),
        ritme_regel("Laatste vrijdag wrap-up", ritmen["vrijdag"]),
        "",
        "Lopen deze getallen structureel op, dan is dat het signaal om te versimpelen,",
        "niet om uit te breiden.",
        "",
    ]

    doel = os.path.join(ROOT, "company", "BOARD.md")
    with open(doel, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(uit))

    print(
        f"BOARD.md gegenereerd: {len(projecten)} projecten, "
        f"{len(deadlines)} deadlines, {len(beslissingen)} beslissingen, "
        f"{len(verouderd)} verouderd"
    )


if __name__ == "__main__":
    main()
