"""Bestanden inlezen en de kleine hulpfuncties die overal terugkomen.

Alles hier is leesbewerking zonder oordeel: geen filtering op rol, geen redactie. Dat
gebeurt een laag hoger in `toegang.py`, zodat er precies een plek is waar bepaald wordt
wat iemand mag zien.
"""

import glob
import os
import sys

from . import ROOT

try:
    import yaml
except ImportError:
    sys.exit("PyYAML ontbreekt: pip install pyyaml")

from datetime import date, datetime


def lees_projecten(tenant="company"):
    """Alle actieve projecten van een tenant, met `_slug` erbij geplakt.

    Defensief: een leeg of stuk yaml-bestand levert een leeg dict op in plaats van een
    crash. Een board dat een project mist is erger zichtbaar dan een board dat niet
    draait, dus dit degradeert liever dan dat het valt.
    """
    projecten = []
    patroon = os.path.join(ROOT, tenant, "projects", "active", "*", "project.yaml")
    for pad in sorted(glob.glob(patroon)):
        with open(pad, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        data["_slug"] = os.path.basename(os.path.dirname(pad))
        data["_pad"] = os.path.relpath(pad, ROOT).replace("\\", "/")
        projecten.append(data)
    return projecten


def als_datum(waarde):
    """Maakt er een `date` van, of None. Slikt zowel date-objecten als YYYY-MM-DD."""
    if isinstance(waarde, date):
        return waarde
    if isinstance(waarde, str):
        try:
            return datetime.strptime(waarde.strip(), "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


def naam(p):
    """Toonbare naam van een project."""
    return p.get("title") or p["_slug"]


def open_taken(p):
    """Taken die nog werk zijn: niet done, niet dropped."""
    return [
        t for t in (p.get("tasks") or [])
        if t.get("status") not in ("done", "dropped")
    ]


def lees_yaml(relpad):
    """Een enkel yaml-bestand relatief aan de repo-root. None als het er niet is."""
    pad = os.path.join(ROOT, relpad)
    if not os.path.exists(pad):
        return None
    with open(pad, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def lees_tekst(relpad):
    """Een tekstbestand relatief aan de repo-root. None als het er niet is."""
    pad = os.path.join(ROOT, relpad)
    if not os.path.exists(pad):
        return None
    with open(pad, encoding="utf-8") as f:
        return f.read()
