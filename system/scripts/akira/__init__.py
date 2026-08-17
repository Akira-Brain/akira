"""Gedeelde laag onder de generatoren van Akira.

Waarom dit pakket bestaat: `generate-board.py` en `generate-views.py` moeten dezelfde
getallen produceren. Zouden ze allebei hun eigen versie van "wat is een open taak" of
"wie is next_step_owner" hebben, dan lopen board en site vroeg of laat uit de pas - en
dan is er geen bron van waarheid meer maar twee meningen. Rekenen gebeurt hier, renderen
gebeurt in de scripts.

De constanten staan hier omdat ze door beide worden gebruikt. Ze zijn bewust hardcoded:
dit is een team van vijf, geen configuratie waard. Wie ze wijzigt, legt in de commit uit
waarom de werkelijkheid veranderd is.
"""

import os
from datetime import date

# Vier niveaus omhoog: akira/ -> scripts/ -> system/ -> repo-root.
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

VANDAAG = date.today()
VEROUDERD_NA = 14
DEADLINE_HORIZON = 14

CONCENTRATIE_DREMPEL = 0.5   # aandeel projecten met dezelfde next_step_owner
NU_MAX = 5                   # maximaal aantal projecten op priority: now
DEKKING_DUE_MIN = 0.5        # onder deze dekking is datumanalyse onbetrouwbaar
DEKKING_OWNER_MIN = 0.8      # onder deze dekking is verdelingsanalyse onbetrouwbaar

# Weekbelasting per persoon (hoeveel gedateerd werk valt in welke week) is bewust NIET
# gebouwd. Bij de huidige dekking - 2 van 57 taken heeft een datum - zou die tabel
# alleen ruis tonen en er gezaghebbend uitzien. Bouw hem zodra de dekking van `due`
# boven DEKKING_DUE_MIN komt; maandagplanning is het ritueel dat die datums aanmaakt.
