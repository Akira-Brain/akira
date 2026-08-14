# Skill: daily-brief

Versie 0.1 - 2026-08-14

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

- **boards-are-generated**: lees uit `project.yaml`, niet uit BOARD.md. BOARD.md kan
  verouderd zijn; de yaml is de bron.
- **hypothesis-is-not-canon**: noem signalen als hypothese, nooit als feit.
- **never-invent-pricing**: staat er geen bedrag, zeg dan dat het er niet staat.
- Verzin nooit een item om de brief voller te maken. Een lege categorie sla je over.
  Een brief die niets te melden heeft, is een geldig antwoord.
