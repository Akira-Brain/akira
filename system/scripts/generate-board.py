#!/usr/bin/env python3
"""Genereert company/BOARD.md uit de project.yaml-bestanden.

Waarom dit een script is en geen taak voor het model: het board is per ontwerp een
gegenereerde view (beslissing D5). Liet je een model het bijwerken, dan bewerkt het
stukjes prozа en loopt de inhoud stil uit de pas met de yaml. Dat gebeurde ook: de
eerste versie miste deadlines volledig en telde captures verkeerd, waardoor de daily
brief meldde dat er geen deadlines waren terwijl er een over zes dagen stond.

Deterministisch, gratis, en altijd in overeenstemming met de bron.

Gebruik:
    python system/scripts/generate-board.py [aantal_open_captures]
"""

import sys
import glob
import os
from datetime import date, datetime, timedelta

try:
    import yaml
except ImportError:
    sys.exit("PyYAML ontbreekt: pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VANDAAG = date.today()
VEROUDERD_NA = 14
DEADLINE_HORIZON = 14


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
