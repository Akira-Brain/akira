"""Wie mag welk bestand zien, en welke velden worden eruit gestript.

Dit is de enige plek waar die vraag beantwoord wordt. Elke lezing in `generate-views.py`
loopt hierlangs, ook lezingen waarvan op voorhand duidelijk is dat ze mogen - want alleen
dan is het leeslogboek compleet, en alleen dan kan `test-geen-lek.py` structureel
controleren dat de rol `atelier` nooit een verboden bron heeft aangeraakt.

Twee regels die de rest verklaren:

1. **Exclude wint van include.** `company/knowledge/**` staat toe, `company/knowledge/pricing/**`
   verbiedt, en de prijzen blijven dus buiten beeld. Andersom zou de volgorde in het
   bestand bepalen wat er lekt, en dat is geen eigenschap die je wilt.
2. **Standaard dicht.** Wat door geen enkel include-patroon geraakt wordt, gaat niet mee.
   Een nieuw veld of een nieuwe map verschijnt daarmee nooit vanzelf op de ateliersite.
"""

import copy
import os
import re

from . import ROOT
from .laden import lees_yaml

STANDAARDROL = "atelier"   # smalste rol; geldt als `toegang:` ontbreekt


def _naar_regex(patroon):
    """Zet een glob-patroon om in een regex.

    `**` loopt over mapgrenzen heen, `*` niet. Dat onderscheid is de reden dat we niet
    gewoon fnmatch gebruiken: daar matcht `*` ook slashes, waardoor
    `company/knowledge/*` per ongeluk ook `company/knowledge/pricing/tarieven.md` raakt.
    """
    uit, i = [], 0
    while i < len(patroon):
        c = patroon[i]
        if patroon.startswith("**", i):
            uit.append(".*")
            i += 2
        elif c == "*":
            uit.append("[^/]*")
            i += 1
        elif c == "?":
            uit.append("[^/]")
            i += 1
        else:
            uit.append(re.escape(c))
            i += 1
    return re.compile("^" + "".join(uit) + "$")


class Toegang:
    """De toegangsregels van een rol, plus het logboek van wat er is gelezen."""

    def __init__(self, rol, config):
        self.rol = rol
        self.betekent = (config.get("betekent") or "").strip()
        self._include = [_naar_regex(p) for p in (config.get("include") or [])]
        self._exclude = [_naar_regex(p) for p in (config.get("exclude") or [])]
        self._velden_uit = config.get("velden_uit") or {}
        self.gelezen = []       # relpaden die zijn vrijgegeven
        self.geweigerd = []     # relpaden die zijn tegengehouden
        self.uitzonderingen = []  # bewuste afwijkingen, met reden - zie noteer_uitzondering

    def mag(self, relpad):
        """Mag deze rol dit pad zien? Exclude wint, daarna include, anders nee."""
        relpad = relpad.replace("\\", "/").lstrip("./")
        if any(r.match(relpad) for r in self._exclude):
            return False
        return any(r.match(relpad) for r in self._include)

    def lees_yaml(self, relpad):
        """Yaml lezen met de regels toegepast. None als het niet mag of niet bestaat."""
        if not self.mag(relpad):
            self.geweigerd.append(relpad)
            return None
        data = lees_yaml(relpad)
        if data is None:
            return None
        self.gelezen.append(relpad)
        return self.strip_velden(os.path.basename(relpad), data)

    def strip_velden(self, bestandsnaam, data):
        """Haalt de velden weg die deze rol niet hoort te zien.

        Kopieert eerst. Zonder die kopie zou het strippen voor `atelier` ook het dict
        aanpassen dat `administrator` nog moet renderen - dezelfde objecten, een
        moeilijk te vinden bug, en de verkeerde kant op: te weinig in plaats van te veel.
        """
        velden = self._velden_uit.get(bestandsnaam)
        if not velden or not isinstance(data, dict):
            return data
        schoon = copy.deepcopy(data)
        for veld in velden:
            schoon.pop(veld, None)
        return schoon

    def noteer_uitzondering(self, relpad, reden):
        """Een bewuste lezing van een verboden bron vastleggen, met de reden.

        Er is precies een geldig soort uitzondering: een AFGELEID getal uit een bron
        waarvan de inhoud niet mag. Het aantal openstaande canon-voorstellen bijvoorbeeld
        is geen geheim, de voorstellen zelf wel.

        Waarom dit een aparte methode is en geen stilzwijgende omweg: zonder deze
        registratie zou zo'n lezing onzichtbaar zijn voor `test-geen-lek.py`, en dan is
        de bescherming weer precies zo toevallig als voor 2026-08-17. Een uitzondering
        die je moet opschrijven, is een uitzondering die iemand kan terugvinden.

        Voeg hier nooit een uitzondering toe die hele tekst doorlaat. Kan het niet als
        getal, dan hoort het niet in deze uitvoer.
        """
        self.uitzonderingen.append({"pad": relpad, "reden": reden})

    def noteer_gelezen(self, relpad):
        """Een lezing melden die elders gebeurde (bijvoorbeeld via lees_projecten).

        Nodig omdat de laadlaag geen weet heeft van rollen. Zonder deze melding zou het
        leeslogboek incompleet zijn en de structurele test dus niets waard.
        """
        if self.mag(relpad):
            self.gelezen.append(relpad)
            return True
        self.geweigerd.append(relpad)
        return False


def laad_rollen():
    """Alle rollen uit system/access.yaml."""
    config = lees_yaml("system/access.yaml")
    if not config or not config.get("rollen"):
        raise SystemExit("system/access.yaml ontbreekt of bevat geen `rollen`")
    return {naam: Toegang(naam, cfg) for naam, cfg in config["rollen"].items()}


def rol_van_persoon(persoon):
    """De rol van een persoonsrecord. Ontbreekt het veld, dan de smalste rol."""
    if (persoon.get("type") or "") != "internal":
        return None
    return persoon.get("toegang") or STANDAARDROL


def mensen_per_rol():
    """{rol: [slug, ...]} uit company/people/. Alleen interne mensen hebben een rol."""
    import glob
    uit = {}
    for pad in sorted(glob.glob(os.path.join(ROOT, "company", "people", "*.yaml"))):
        data = lees_yaml(os.path.relpath(pad, ROOT).replace("\\", "/")) or {}
        rol = rol_van_persoon(data)
        if rol:
            uit.setdefault(rol, []).append(data.get("slug") or
                                           os.path.basename(pad)[:-5])
    return uit
