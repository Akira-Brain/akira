# Skill: daily-brief

Versie 0.2 - 2026-08-17. De groep Botsingen toegevoegd en de bronregel gesplitst, nu het
board berekende cijfers bevat die je niet met de hand moet naschatten.

## Doel

De vraag "wat moet ik vandaag weten?" beantwoorden in een overzicht dat in dertig
seconden te lezen is. Dit is de noordster-interactie uit het mandaat: Farah opent
ChatGPT, stelt die ene vraag, en weet waar ze staat.

## Input

Wie vraagt het (tore | farah) en optioneel een tenant-scope. Standaard: de eigen
tenant plus `company/`. Tore mag over zijn eigen tenants heen kijken; Farah ziet
`company/` en later `personal/farah/`, nooit `personal/tore/`.

## Bronnen - en alleen deze

- alle `project.yaml` in `{tenant}/projects/active/`
- `{tenant}/canon-queue.md`
- `{tenant}/ideas/` met status `priority`
- `{tenant}/inbox/` met status ongelijk aan `routed`
- `company/BOARD.md`, uitsluitend de sectie `## Botsingen en belasting`

Lees geen kennisbestanden, geen archief, geen journals. Dit is een statusvraag, geen
onderzoeksvraag.

## Stappen

1. Verzamel de project.yaml's van de gevraagde tenant(s).
2. Groepeer:
   - **Beslissingen nodig**: taken met `needs_decision: true`, plus openstaande
     canon-queue-items. Noem per stuk het project en de vraag.
   - **Clients waiting**: projecten met `status: waiting`. Toon het `waiting_for`-veld
     letterlijk; dat is de eigenlijke informatie.
   - **Taken per persoon**: open taken gegroepeerd op `owner`, overdue eerst.
   - **Deadlines**: alles met `deadline` binnen 14 dagen.
   - **Vastgelopen**: `status: active` maar `updated` ouder dan 14 dagen. Dit vangt
     de scatteredness die dit systeem moet oplossen.
   - **Botsingen**: citeer de regels uit `## Botsingen en belasting` op het board
     letterlijk, parafraseer ze niet en reken ze niet na. Noem hooguit de twee
     zwaarste punten - eigenaarsconcentratie en de langste keten - tenzij er iets over
     datum heen staat, want dat gaat voor. Meldt het board niets, sla de groep over.
   - **Signalen**: learnings in `working/` die genoeg evidence hebben om `proposed`
     te worden. Alleen noemen, niet promoveren.
3. Presenteer in die volgorde, met aantallen. Kort. Geen inleiding, geen samenvatting
   achteraf.
4. Sluit af met een vraag: waar wil je mee beginnen.

## Outputvorm

```
Beslissingen nodig (2)
- Selah Sue tour: prijs tweede fitting - wacht sinds 6/8
- canon-queue: red carpet basisprijs 1100 -> 1400

Clients waiting (3)
- Selah Sue: bevestiging management over tourdata
...

Luna - 4 open taken, 1 overdue
Stagiaires - 6 taken

Vastgelopen (1)
- AS Adventure: niets gewijzigd sinds 24/7
```

## Policies die gelden

- **boards-are-generated, aangescherpt op 2026-08-17.** Projectfeiten - status,
  next_step, taken, deadlines - lees je uit `project.yaml`, nooit uit BOARD.md. Dat
  blijft ongewijzigd.
  De berekende sectie `## Botsingen en belasting` lees je juist wél uit BOARD.md, en
  nergens anders. Reden: dat is een berekening over alle projecten heen
  (eigenaarsconcentratie, ketens, dekking). Een model dat dat met de hand herrekent,
  rekent het vroeg of laat stil verkeerd - zo rapporteerde de eerste boardversie een
  deadline over zes dagen als "geen deadlines".
  De oorspronkelijke reden voor het verbod, dat het board verouderd kan zijn, los je niet
  op met wantrouwen maar met verversen: draai eerst
  `python system/scripts/generate-board.py`, lees daarna. Kun je het script niet draaien,
  meld dan expliciet dat die sectie mogelijk verouderd is en sla hem over. Reken hem
  nooit zelf uit.
- **hypothesis-is-not-canon**: noem signalen als hypothese, nooit als feit.
- **never-invent-pricing**: staat er geen bedrag, zeg dan dat het er niet staat.
- Verzin nooit een item om de brief voller te maken. Een lege categorie sla je over.
  Een brief die niets te melden heeft, is een geldig antwoord.
