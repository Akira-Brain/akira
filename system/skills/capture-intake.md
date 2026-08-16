# Skill: capture-intake

Versie 0.1 - 2026-08-14

## Doel

De captures die via Farah's GPT als GitHub Issue binnenkomen routeren naar hun plek in
de repo, en het issue sluiten. Dit is de tweede helft van pad A: Farah's kant stopt bij
het issue, deze skill maakt er bedrijfsgeheugen van.

Draai dit dagelijks als er captures zijn, en in elk geval bij de weekly review.

## Dit draait automatisch

De workflow `.github/workflows/capture-intake.yml` voert deze skill uit zodra er een
issue met label `capture` binnenkomt. Niemand hoeft iets te starten. Deze skill blijft
staan als de bron van waarheid over hoe er gerouteerd wordt, en om hem met de hand te
kunnen draaien wanneer dat nodig is.

**Waarom automatisch routeren de canon-poort niet aantast.** Routeren schrijft in de
lage- en midden-risicozones uit `AGENTS.md`: taken, projectstatus, journals, ideeen,
hypotheses. Daar mag AI volgens het ontwerp vrij schrijven, gelabeld waar dat hoort. De
menselijke poort zit een niveau hoger, bij canon, en die verandert niet: raakt een
capture een prijs of een werkwijze, dan komt er een voorstel in `canon-queue.md` en
verandert er niets in `knowledge/`.

**Waar de grens mechanisch zit.** De workflow staged uitsluitend een vaste allowlist van
paden en gebruikt nooit `git add -A`. `company/knowledge/`, `company/policies/`,
`company/company.yaml` en `system/` worden nooit gestaged, plus er draait een aparte
controlestap die wijzigingen daar terugdraait. Ook als het model zich vergist, of als
iemand instructies in een issue-tekst zet, kan de canon niet geraakt worden.

**Wat menselijk blijft.** De canon-queue goedkeuren, en de weekly review, waar de open
punten terugkomen die de routering niet zeker kon plaatsen.

## Input

Openstaande issues met label `capture` in `akira`. Ophalen via de GitHub-
connector of `gh issue list --label capture --state open`.

## Stappen

1. **Haal de openstaande captures op**, oudste eerst. Werk ze een voor een af; batchen
   leidt tot slordige routering.
2. **Lees de Ruw-sectie, niet alleen de Signalen.** De GPT van Farah classificeert
   redelijk, maar mist nuance en context die jij wel hebt. Behandel de Signalen-sectie
   als een voorstel, niet als waarheid.
3. **Route elk signaal** volgens de tabel hieronder.
4. **Los de ONBEKEND-velden op** waar je het antwoord weet. Weet je het niet, laat het
   signaal dan staan als open punt in de weekly review in plaats van te gokken.
5. **Regenereer BOARD.md** van de geraakte tenant.
6. **Sluit het issue** met een comment die opsomt waar alles geland is, met paden.
   Blijft er iets onopgelost, laat het issue dan open en zet erbij wat er nog mist.

## Routeringstabel

| Signaal | Bestemming |
|---|---|
| taak | `tasks:` in de betreffende `project.yaml` |
| beslissing | `decisions/{jaar}/D-{jaar}-{nr}.md`; raakt het canon, dan OOK een canon-queue-item |
| projectupdate | journal-entry + `status` / `next_step` / `waiting_for` in project.yaml |
| learning-kandidaat | `working/learnings/{slug}.md`, status `hypothesis` |
| idee | `ideas/{slug}.md`, status `good-ideas` tenzij anders gezegd |
| open vraag | `waiting_for` in project.yaml, of taak met `needs_decision: true` |
| follow-up | taak met `due` en de juiste owner |

## Regels

- **Een capture die naar een onbekend project verwijst, maak je niet stilzwijgend aan.**
  Vraag het na, of noteer als open punt. Een verzonnen projectmap is erger dan een
  ongerouteerd signaal.
- **Prijsuitspraken uit een capture worden nooit canon.** Ze worden een hypothese in
  `working/`, plus eventueel een canon-queue-voorstel. Zie policy
  `canon-only-via-queue`.
- **Kwam er toch gevoelige informatie door**, ondanks de instructie aan Farah's GPT:
  verwijder die uit het issue (bewerk de issue-tekst), vervang door een
  vault-verwijzing, en schrijf ze niet over naar de repo. Meld het aan Tore, want dan
  klopt er iets niet aan de GPT-instructie. Let op: de issue-historie op GitHub bewaart
  bewerkingen, dus bij echt gevoelig materiaal is het issue verwijderen de veiligere
  route.
- **Sluit nooit een issue waarvan je de inhoud niet volledig gerouteerd hebt.** Het open
  issue is het enige spoor dat er nog werk ligt.

## Outputvorm van de afsluitende comment

```
Gerouteerd:
- taak Luna sourcen accessoires -> projects/active/awards-2026/project.yaml
- beslissing tweede fitting -> decisions/2026/D-2026-015.md
- idee bridal gids -> ideas/bridal-styling-gids.md

Niet gerouteerd:
- opmerking over prijsniveau red carpet: als hypothese gezet in
  working/learnings/red-carpet-prijsniveau.md, canon ongewijzigd
```

## Policies die gelden

canon-only-via-queue, hypothesis-is-not-canon, sensitive-data-to-vault,
never-invent-pricing, client-isolation, boards-are-generated.
