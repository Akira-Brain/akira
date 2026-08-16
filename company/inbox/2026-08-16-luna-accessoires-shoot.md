---
capture: "2026-08-16-luna-accessoires-shoot"
tenant: company
source: farah-voice
date: 2026-08-16
status: open
---

## Ruw

Bron: GitHub issue #1 en #2 (dezelfde capture, twee bronnen):
- Issue #1: "2026-08-16 - Luna - accessoires sourcen voor shoot volgende week" (source: Luna)
- Issue #2: "2026-08-16 - Tore - test Haiku, gesprek met Luna" (source: Tore)

> Ik heb net met Luna gesproken. Zij gaat accessoires sourcen voor de shoot van volgende
> week, dat moet tegen donderdag klaar zijn. En we twijfelen nog of we een tweede fitting
> inplannen, dat moet Farah beslissen.

## Signalen

- **taak**: accessoires sourcen voor de shoot van volgende week - owner: Luna - due:
  donderdag (welke donderdag is niet gespecificeerd)
- **open vraag** (in de capture zelf "beslissing" genoemd, maar nog niet genomen): wel of
  geen tweede fitting inplannen voor diezelfde shoot - te beslissen door Farah - raakt
  geen prijzen of werkwijze

## Routering

Niet gerouteerd. Geen van beide signalen verwijst naar een project dat bestaat in
`company/projects/active/`. Er is geen project dat een shoot, accessoires-sourcing of een
(tweede) fitting voor Luna in deze periode vermeldt.

Onduidelijk gebleven:
- **Welk project dit is.** Volgens de regel wordt een onbekend project niet stilzwijgend
  aangemaakt. Zonder project kan de taak niet in `tasks:` en kan de open vraag niet als
  `waiting_for` of `needs_decision: true` gezet worden. Navragen bij Farah/Luna welk
  project dit betreft, of alsnog een project aanmaken zodra dat duidelijk is.
- **Welke donderdag bedoeld wordt.** Niet gespecificeerd in de capture; niet gegokt.
- **Wie de tweede-fitting-beslissing vastlegt zodra Farah beslist heeft.** Zonder project
  is er geen plek om dat aan te haken.
