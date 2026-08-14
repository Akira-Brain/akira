# Skill: project-update

Versie 0.1 - 2026-08-14

## Doel

"Ik heb net X gedaan" of "ik heb net Y gehoord" verwerken naar de juiste projectmap,
zodat de status altijd klopt zonder dat iemand een formulier invult.

## Input

Een vrije uitspraak over een project. Vaak zonder dat de projectnaam expliciet valt.

## Stappen

1. **Identificeer het project.** Match op slug, titel, klantnaam of mensen. Is het
   ambigu, vraag dan. Bestaat het project nog niet, stel dan voor het aan te maken
   (of het als idee te parkeren als het nog geen opdracht is).
2. **Schrijf een journal-entry** in `projects/active/{slug}/journal/{datum}.md`. Append,
   nooit overschrijven. Twee tot vijf zinnen: wat is er gebeurd, wat betekent het.
3. **Werk `project.yaml` bij**: `status`, `next_step`, `next_step_owner`, `waiting_for`,
   `updated`. Kwam er een taak bij, voeg die toe aan `tasks:`. Is een taak af, zet
   `status: done` in plaats van de regel te verwijderen.
4. **Oogst signalen** die niet in het project thuishoren: learning-kandidaten naar
   `working/learnings/`, ideeen naar `ideas/`, beslissingen naar `decisions/`.
5. **Regenereer BOARD.md** van de tenant.
6. **Meld in een zin** wat je gewijzigd hebt. Niet meer.

## De belangrijkste velden

`next_step` en `waiting_for` zijn de twee velden waar dit hele systeem op draait.

- `next_step` moet een concrete eerste handeling zijn, niet een doel. "Offerte
  afwerken" is slecht. "Fittingdatum voorstellen aan Toos" is goed.
- `waiting_for` moet de werkelijke blokkade benoemen, inclusief bij wie hij ligt.
  Dit veld is het antwoord op "welke clients wachten op ons of wij op hen".

Laat je deze twee velden vaag, dan is de daily brief waardeloos en valt het project
alsnog tussen de mazen. Dat is precies het probleem dat dit systeem moest oplossen.

## Policies die gelden

boards-are-generated, handoff-at-session-end, sensitive-data-to-vault,
canon-only-via-queue (raakt de update een prijs of werkwijze, dan queue-voorstel,
geen directe canon-wijziging).
