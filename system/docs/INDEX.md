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
| Wie mag wat zien? | `system/docs/TOEGANG.md`, regels in `system/access.yaml` |
| Wat ziet het team zelf? | de gegenereerde kijklaag, `system/scripts/generate-views.py` |

## Hoe doe ik...

| Taak | Skill |
|---|---|
| Ochtendoverzicht geven | `system/skills/daily-brief.md` |
| Maandagplanning begeleiden | `system/skills/monday-planning.md` |
| Vrijdag wrap-up doen | `system/skills/friday-wrap-up.md` |
| Klantopdracht opstarten | `system/skills/client-kickoff.md` |
| Spraakdump verwerken | `system/skills/meeting-processing.md` |
| Captures van Farah routeren | `system/skills/capture-intake.md` |
| Projectstatus bijwerken | `system/skills/project-update.md` |
| Nieuwe aanvraag analyseren | `system/skills/inquiry-analysis.md` |
| Wekelijkse opruimronde | `system/skills/weekly-review.md` |

## Structuur van een bestand

Alle schemas staan in `system/schemas/` met commentaar per veld. Nieuw bestand
aanmaken: kopieer uit `system/templates/`.

## Regels

`system/policies/` bevat acht policies. De harde vijf die je altijd moet kennen:
`canon-only-via-queue`, `never-invent-pricing`, `pricing-is-need-to-know`,
`client-isolation`, `sensitive-data-to-vault`.

De laatste twee prijsregels lijken op elkaar en zijn het niet: `never-invent-pricing` gaat
over prijzen die niet bestaan (verzin er geen), `pricing-is-need-to-know` over prijzen die
wel bestaan (deel ze niet met iedereen).
