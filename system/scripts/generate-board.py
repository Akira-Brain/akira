#!/usr/bin/env python3
"""Genereert company/BOARD.md uit de project.yaml-bestanden.

Waarom dit een script is en geen taak voor het model: het board is per ontwerp een
gegenereerde view (beslissing D5). Liet je een model het bijwerken, dan bewerkt het
stukjes proza en loopt de inhoud stil uit de pas met de yaml. Dat gebeurde ook: de
eerste versie miste deadlines volledig en telde captures verkeerd, waardoor de daily
brief meldde dat er geen deadlines waren terwijl er een over zes dagen stond.

Deterministisch, gratis, en altijd in overeenstemming met de bron.

Rekenen gebeurt niet hier maar in `akira/analyse.py`, gedeeld met `generate-views.py`.
Dit bestand doet alleen nog opmaak. Reden: zouden board en site elk hun eigen telling
hebben, dan lopen ze uit de pas en is er geen bron van waarheid meer maar twee meningen.

LET OP bij wijzigen: Chatty leest dit bestand via een hardgecodeerd pad
(`company/BOARD.md`) en `system/skills/daily-brief.md` citeert de sectie "Botsingen en
belasting" letterlijk. De kopstructuur veranderen breekt de daily brief van Farah.

Bekende zwakte: dit script leest alleen company/. Zolang personal/tore/ eigen werk
draagt, zijn de belastingcijfers voor Tore structureel te laag - het board ziet zijn
persoonlijke tenant niet.

Gebruik:
    python system/scripts/generate-board.py [aantal_open_captures]
"""

import os
import sys
from datetime import timedelta

from akira import (
    ROOT, VANDAAG, VEROUDERD_NA, DEADLINE_HORIZON,
    CONCENTRATIE_DREMPEL, NU_MAX, DEKKING_DUE_MIN, DEKKING_OWNER_MIN,
)
from akira.laden import lees_projecten, als_datum, open_taken
from akira.analyse import (
    pct, bereken_dekking, bereken_concentratie, bereken_onbeheerd,
    bereken_ongedateerd, bereken_overdue, bereken_ketens, bereken_prioriteitsdruk,
    bereken_verouderd, taken_per_persoon, beslissingen_open, lees_ritmen,
    tel_open_canon,
)


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

    beslissingen = beslissingen_open(projecten)
    per_persoon = taken_per_persoon(projecten)
    verouderd = bereken_verouderd(projecten)
    open_canon = tel_open_canon()

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
    if per_persoon:
        for persoon, aantal in sorted(per_persoon.items(), key=lambda x: -x[1]):
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
