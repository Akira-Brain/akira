# AGENTS.md - charter Akira

Versie 0.1 - 2026-08-14. Dit bestand wordt door elke AI-sessie als eerste gelezen.
Houd het onder ~100 regels. Alles wat hier niet staat, wordt on demand geladen.

## Wat dit is

Dit is het bedrijfsgeheugen van Haus von FEB: plain files (Markdown + YAML) in een
private repo. AI-modellen zijn inwisselbare interfaces erbovenop. De intelligentie
hoort bij het bedrijf, niet bij een model, een account of een persoon.

## Drie wetten

1. **Capture -> working -> canon.** Niets wordt bedrijfswaarheid zonder menselijke
   goedkeuring. Ruwe input landt in `inbox/`, hypotheses in `working/`, alleen
   goedgekeurde waarheid in `knowledge/`.
2. **Risico-gebaseerde schrijfrechten.** Zie zones hieronder. Bij twijfel: niet schrijven,
   maar voorstellen.
3. **Tenant-isolatie.** `company/`, `personal/tore/`, `personal/farah/` en later klanten
   delen schemas en skills, nooit inhoud. Vermenging is een categorie-1-fout.

## Layout

```
system/       het OS: schemas, templates, skills, policies. Bevat GEEN bedrijfsdata.
company/      tenant Haus von FEB (atelier)
personal/     tore/ en farah/ - eigen ministructuur, eigen BOARD
integrations/ pointers naar Drive en externe systemen, nooit inhoud
```

Per tenant: `knowledge/` (alleen canon), `working/` (hypotheses/learnings), `projects/`,
`ideas/`, `people/`, `clients/`, `decisions/`, `inbox/`, `BOARD.md`, `canon-queue.md`.

## Schrijfzones

| Zone | AI mag | Waar |
|---|---|---|
| Laag | vrij schrijven | `inbox/`, `projects/*/journal/`, `handoff.md`, status/next_step/tasks in `project.yaml`, `ideas/` |
| Midden | schrijven, altijd met status-frontmatter | `working/`, notes in `people/` en `clients/` |
| Hoog | alleen voorstellen via `canon-queue.md` | `knowledge/`, `policies/`, `company.yaml`, pricing, canon-rakende `decisions/` |
| Verboden | nooit | persoonsgevoelige klantdata, contracten, financiele documenten, credentials |

Verboden materiaal gaat naar de Drive-vault; de repo houdt alleen een pointer. Kom je
gevoelige inhoud tegen in een capture, vervang die dan door een vault-verwijzing en meld
dat expliciet in de capture.

## Sessierituelen

**Start.** Lees `BOARD.md` van de tenant en de `handoff.md` van het gekozen project.
Verder niets eager laden. Vraag waar de gebruiker heen wil voordat je meer opent. Is de
vraag eigenlijk een kleine actie, sla dan het hele contextcircus over en doe die actie.

**Einde.** Veranderde je iets, dan: werk `project.yaml` bij (status, next_step, tasks),
overschrijf `handoff.md`, schrijf een journal-entry, oogst learning-kandidaten,
regenereer `BOARD.md`, commit. Las je alleen, maak dan geen handoff.

## Harde regels

- Canon citeer je als waarheid; `working/` citeer je altijd als "hypothese, nog niet
  goedgekeurd".
- Spreken twee bronnen elkaar tegen: canon > working > capture. Binnen canon wint de
  jongste `updated`. Meld het conflict als canon-queue-item, negeer het nooit.
- Verzin nooit een prijs. Staat het niet in de pricing-canon, zeg dat dan.
- Werk in een sessie in een tenant, tenzij expliciet anders gevraagd. De daily brief mag
  over Tore's eigen tenants heen kijken.
- BOARD.md en elk overzicht zijn gegenereerde views. Bewerk ze nooit met de hand; de
  bron is altijd `project.yaml`.
- Twijfel je waar iets hoort, laat het in `inbox/` staan. Fout gerouteerd is erger dan
  niet gerouteerd.

## Load on demand

| Wanneer | Lees |
|---|---|
| Werkwijze van een taak | `system/skills/{skill}.md` |
| Structuur van een bestand | `system/schemas/{ding}.schema.yaml` |
| Nieuw bestand aanmaken | `system/templates/` |
| Regels bij een handeling | `system/policies/` en `{tenant}/policies/` |
| Navigatie | `system/docs/INDEX.md` |
| Waar een document staat | `integrations/drive-map.yaml` |

## Skills

`daily-brief` (wat moet ik weten), `meeting-processing` (spraak/transcript -> signalen),
`project-update` (ik heb net X gedaan), `inquiry-analysis` (nieuwe aanvraag),
`weekly-review` (gardening). Roep ze aan door het bestand te lezen en de stappen te volgen.
