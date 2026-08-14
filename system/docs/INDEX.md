# INDEX - navigatiekaart

Versie 0.1 - 2026-08-14

Voor AI-sessies: dit is de kaart. Lees hieruit gericht wat je nodig hebt, in plaats van
de repo te doorzoeken. Alles wat niet in `AGENTS.md` staat, vind je hier.

## Ik wil weten...

| Vraag | Ga naar |
|---|---|
| Waar werken we aan? | `{tenant}/BOARD.md`, bron is `projects/active/*/project.yaml` |
| Wat is de stand van project X? | `projects/active/{slug}/handoff.md` |
| Wat gebeurde er eerder bij X? | `projects/active/{slug}/journal/` |
| Wat kost een red carpet? | `company/knowledge/pricing/` |
| Waarom werken we zo? | `company/knowledge/` (canon) |
| Wat vermoeden we nog maar? | `company/working/` (hypotheses, learnings) |
| Wat wacht op goedkeuring? | `{tenant}/canon-queue.md` |
| Wie is deze persoon? | `company/people/{slug}.yaml` |
| Wat weten we van deze klant? | `company/clients/{slug}/client.yaml` |
| Waarom hebben we dit besloten? | `company/decisions/{jaar}/` |
| Waar staat dat document? | `integrations/drive-map.yaml` |
| Wat is er net binnengekomen? | `{tenant}/inbox/` |

## Hoe doe ik...

| Taak | Skill |
|---|---|
| Ochtendoverzicht geven | `system/skills/daily-brief.md` |
| Spraakdump verwerken | `system/skills/meeting-processing.md` |
| Captures van Farah routeren | `system/skills/capture-intake.md` |
| Projectstatus bijwerken | `system/skills/project-update.md` |
| Nieuwe aanvraag analyseren | `system/skills/inquiry-analysis.md` |
| Wekelijkse opruimronde | `system/skills/weekly-review.md` |

## Structuur van een bestand

Alle schemas staan in `system/schemas/` met commentaar per veld. Nieuw bestand
aanmaken: kopieer uit `system/templates/`.

## Regels

`system/policies/` bevat zeven policies. De harde vier die je altijd moet kennen:
`canon-only-via-queue`, `never-invent-pricing`, `client-isolation`,
`sensitive-data-to-vault`.
