# Haus von FEB AI OS

Versie 0.1 - 2026-08-14

Het gedeelde bedrijfsgeheugen van Haus von FEB. Plain files in een private repo:
projecten, kennis, beslissingen, mensen, learnings. ChatGPT en Claude zijn interfaces
erbovenop en zijn inwisselbaar. De intelligentie van het atelier hoort bij het atelier.

## Voor wie dit leest zonder technische achtergrond

Je hoeft deze repo nooit te openen. Je praat met de AI, de AI onderhoudt deze bestanden.
Dit is de archiefkast, niet het kantoor.

Wat je kunt vragen:

- "Wat moet ik vandaag weten?" -> de daily brief
- "Ik heb net met Luna gesproken, ik spreek even alles in" -> capture en routering
- "Nieuwe aanvraag, analyseer dit" -> inquiry-analysis
- "Dit project is klaar, wat hebben we geleerd?" -> learning-oogst

## Hoe het in elkaar zit

```
AGENTS.md      het charter: wat elke AI-sessie eerst leest
system/        het OS zelf: schemas, templates, skills, policies. Geen bedrijfsdata.
company/       het atelier: projecten, kennis, klanten, mensen, beslissingen
personal/      tore/ en farah/: eigen projecten en ideeen, zelfde structuur
integrations/  verwijzingen naar Google Drive. Nooit de inhoud zelf.
```

De belangrijkste plekken in `company/`:

| Bestand | Wat |
|---|---|
| `BOARD.md` | gegenereerd overzicht: nu / next / later / waiting |
| `canon-queue.md` | voorgestelde wijzigingen aan bedrijfswaarheid, wachtend op akkoord |
| `projects/active/{slug}/project.yaml` | de bron van alle status en prioriteit |
| `knowledge/` | alleen goedgekeurde bedrijfswaarheid (canon) |
| `working/` | hypotheses en learnings die nog geen canon zijn |
| `inbox/` | ruwe captures, nog niet gerouteerd |

## De drie wetten

1. **Capture -> working -> canon.** Niets wordt bedrijfswaarheid zonder dat een mens
   akkoord geeft.
2. **Risico-gebaseerde schrijfrechten.** AI schrijft vrij in operationele zones,
   gelabeld in working, en alleen als voorstel in canon.
3. **Tenant-isolatie.** Company, personal en later klanten delen structuur, nooit inhoud.

## Wat hier nooit in mag

Persoonsgevoelige klantdata (maten, priveadressen, privenummers), contracten,
ondertekende documenten, gedetailleerde financiele administratie, credentials.
Die leven in de Drive-vault; hier staat hooguit een pointer. Git vergeet niet:
eenmaal gecommit is verwijderen pijnlijk. Voorkomen is de enige strategie.

## Status

V0.1 scaffold. Nog te doen voor dit systeem echt leeft:

- braindump-sessie: alle lopende projecten en ideeen invullen
- 6-8 canon-startbestanden via de canon-queue goedkeuren
- ChatGPT-interfacetest (bepaalt Farah's capture-pad)
- privacy-baseline vastleggen voordat klantdata de repo raakt

Ontwerpgrondslag: Fase 1 (HQ reverse engineering) en Fase 2 (systeemarchitectuur),
beide 2026-08-14.
