# Skill: inquiry-analysis

Versie 0.1 - 2026-08-14

## Doel

Een nieuwe aanvraag analyseren voordat er een prijs op geplakt wordt: wat vraagt de
klant werkelijk, wat weten we nog niet, wat deden we bij vergelijkbare opdrachten, en
wat zegt de canon over de prijs.

## Input

Een mail, bericht of mondelinge beschrijving van een aanvraag.

## Stappen

1. **Identificeer klant en scope.** Bestaat de klant al in `clients/`? Zo ja, lees
   `client.yaml` en de projecthistorie. Zo nee, stel een nieuw klantrecord voor.
2. **Extraheer de vraag**: type opdracht, aantal looks, fittings, sourcing, reizen,
   deliverables, timing, usage rights, betrokken partijen.
3. **Benoem wat ontbreekt.** Dit is de belangrijkste stap. Lijst expliciet op welke
   informatie je nodig hebt voor een verantwoorde offerte en nog niet hebt. Een
   analyse die doet alsof alles bekend is, is gevaarlijker dan geen analyse.
4. **Zoek vergelijkbare projecten** in `projects/archive/` en `projects/active/`.
   Match op type, omvang, klanttype. Noem per vergelijkbaar project: wat was de scope,
   wat was de prijs, wat liep er anders dan verwacht.
5. **Toets aan de canon.** Lees het relevante bestand in `knowledge/pricing/`. Noem de
   canonwaarde. Wijkt de situatie af, benoem dan waarom en hoeveel, met verwijzing
   naar de canon-rationale.
6. **Raadpleeg relevante learnings** in `working/learnings/`. Presenteer die
   uitdrukkelijk als hypothese, niet als feit. ("We hebben het vermoeden dat sourcing
   structureel onderschat wordt - nog niet bevestigd.")
7. **Lever de analyse** en stel voor een projectmap aan te maken met status `scoping`.

## Outputvorm

```
Aanvraag: {klant} - {type opdracht}

Wat gevraagd wordt
- ...

Wat we nog niet weten (nodig voor een offerte)
- ...

Vergelijkbare opdrachten
- {project}: scope, prijs, wat afweek

Wat de canon zegt
- {waarde} volgens knowledge/pricing/{bestand}. Rationale: ...

Signalen en risico's
- ... (learnings als hypothese gemarkeerd)

Voorstel
- projectmap aanmaken / eerst deze vragen stellen
```

## Policies die gelden

- **never-invent-pricing**: noem alleen bedragen die uit de canon, een eerdere offerte
  of de klant zelf komen. Ontbreekt een canonwaarde, zeg dat er nog geen canon is en
  stel voor er een te maken. Nooit interpoleren of "inschatten".
- **client-isolation**: gebruik informatie uit andere klantdossiers alleen als
  geanonimiseerd patroon ("bij vergelijkbare tourprojecten"), nooit met namen of
  bedragen van klant A in een analyse voor klant B.
- **hypothesis-is-not-canon**, **sensitive-data-to-vault**.
