# Skill: monday-planning

Versie 0.1 - 2026-08-17. Ontworpen, nog niet in een echte vergadering toegepast; verwacht
een herschrijving na de eerste maandag.

## Doel

Een braindump van het team omzetten in een geneste outline waarin elke tak eindigt bij een
naam, een concrete handeling en een datum - en die outline daarna wegschrijven naar de
projecten zonder de outline zelf te verliezen.

Dit is het ritueel zoals het al bestaat: het team zit samen, Tore begeleidt, iedereen
braindumpt ("wat staat er op de agenda, wat zit er in de pijplijn, waar denken jullie
aan"), en daarna gaat hij er één voor één doorheen met "wat moet hiervoor gebeuren, wat
zijn de deadlines, wie doet wat tegen wanneer". Deze skill verandert dat proces niet - het
denkwerk blijft menselijk. Wat de skill toevoegt is dat het resultaat ergens landt.

**Dit is de enige plek in het systeem waar datums ontstaan.** Op het moment van schrijven
hebben 55 van de 57 taken geen `due`. Zolang dat zo blijft, valt er niet te plannen en kan
het board geen belasting berekenen.

## Input

Het gesprek zelf (transcript, spraakdump of live). Plus verplicht: het bestand van vorige
vrijdag, `company/rituals/{jaar}/W{nn-1}-vrijdag.md`.

**Ruwe signalen eruit halen doe je niet hier.** Volg `system/skills/meeting-processing.md`,
sectie "Stappen voor een vol vergadertranscript", stap 1 tot en met 3 en 6. Dat levert een
capture-bestand in `company/inbox/` en de geclassificeerde signalen. Deze skill begint bij
wat daar uitkomt en geeft het een andere vorm.

## Stappen

1. **Open eerst het vrijdagbestand, vóór de braindump.** Lees de sectie
   `## Prioriteiten voor volgende week`. Elke prioriteit daar krijgt in deze vergadering
   één van drie verdicts: *opgenomen* (hij komt terug in de outline), *uitgesteld met
   reden*, of *vervallen met reden*. Een prioriteit die stilzwijgend ontbreekt is een
   defect in dit ritueel, niet in dat van vrijdag. Bestaat het vrijdagbestand niet, zeg dat
   hardop en noteer het in de header - dat is de meting die het doodbloeden vangt.
2. **Neem de braindump ongefilterd op** via de capture uit `meeting-processing`. Nog niet
   structureren, nog niet toewijzen. Eerst alles op tafel.
3. **Loop de topics één voor één langs**, in de volgorde waarin ze aan tafel behandeld
   worden. Per topic altijd dezelfde vier vragen, in deze volgorde:
   - wat moet er gebeuren
   - wat is de deadline, en waar komt die vandaan (klant, eigen keuze, extern moment)
   - wie doet wat tegen wanneer
   - welke beslissing hangt eraan vast
4. **Bind elk topic aan een projectslug.** Bestaat het project, koppel het. Bestaat het
   niet, markeer `NIEUW` (dan maak je het project aan volgens het schema) of
   `GEEN PROJECT` (dan gaat het naar `ideas/` of blijft het in de sectie
   `## Niet geplaatst` staan). Een topic dat nergens aan bindt, wordt geen taak.
5. **Elke taak krijgt een `due`, of een expliciete "geen datum, en waarom".** Accepteer
   geen "deze week" - zet dat tijdens de vergadering hardop om naar een datum. Verzin geen
   datum die niemand gezegd heeft; is er geen, dan staat er waarom niet.
6. **Toon de routeringstabel vóór je schrijft.** De mensen aan tafel lezen wat er in welke
   `project.yaml` gaat landen en bevestigen dat. Niet eerst schrijven en dan rapporteren.
7. **Schrijf weg naar `project.yaml`:** taken toevoegen aan `tasks:`, plus `next_step`,
   `next_step_owner` en `updated`. **Raak `priority` niet aan** - dat is het instrument van
   de vrijdag wrap-up, en twee rituelen die aan hetzelfde veld draaien maken allebei
   betekenisloos.
8. **Regenereer het board en lees `## Botsingen en belasting` terug aan de kamer.** Eindigt
   iemand deze planning met opvallend veel gedateerd werk, of blijkt de
   eigenaarsconcentratie verder opgelopen, dan zeg je dat vóórdat mensen weglopen.
9. Sla op als `company/rituals/{jaar}/W{nn}-maandag.md` en commit.

## Outputvorm

```markdown
---
ritueel: maandag-planning
week: 2026-W34
datum: 2026-08-17
aanwezig: [tore, farah, luna]
status: verwerkt
---

# Weekplan W34 - 17 t/m 23 augustus 2026

Vorige vrijdag gaf drie prioriteiten mee (W33-vrijdag.md):
- Scenariokeuze starmaker afronden -> opgenomen, punt 1
- Checkroom-instructie af -> uitgesteld, Luna was ziek
- Stock sale najaar datum prikken -> vervallen, wacht op zaalbevestiging

## 1. Scenariokeuze starmaker -> positionering-starmaker

Wat moet er gebeuren
- Scenario hybride uitschrijven, pros en cons, max 2 A4
- Voorleggen aan Farah, daarna aan Jasmijn

Deadline: 2026-08-21 (eigen keuze; website en bel-en-bo staan hierop stil)

Wie doet wat tegen wanneer
- tore: scenario uitschrijven, tegen 2026-08-20
- farah: doorlezen en reageren, tegen 2026-08-21

Open beslissing: welke termen horen bij Starmaker (staat open sinds 16/7)

## 2. Checkroom-instructie -> stock-digitalisering

Wat moet er gebeuren
- Waardebepalingscriteria uitschrijven zodat een stagiair zelfstandig kan werken

Deadline: 2026-08-22 (eigen keuze)

Wie doet wat tegen wanneer
- luna: instructiedocument afwerken, tegen 2026-08-22

## Niet geplaatst

- "iets met TikTok voor de stock sale" - te vaag; Luna werkt het uit tegen vrijdag

## Wat naar project.yaml gaat

| Project | Wat | Veld |
|---|---|---|
| positionering-starmaker | taak "Scenario hybride uitschrijven" - tore - 2026-08-20 | tasks |
| positionering-starmaker | next_step + updated | kern |
| stock-digitalisering | taak "Instructiedocument afwerken" - luna - 2026-08-22 | tasks |

## Belasting na deze planning (uit BOARD.md)

tore 4 gedateerde taken deze week, luna 2, farah 1.
Eigenaarsconcentratie staat nog op 82% - er is deze planning niets gedelegeerd.
```

## Bekende zwakte

Dit ritueel maakt datums aan, maar niets valideert of ze realistisch zijn. Er is bewust
geen effort- of capaciteitsveld: een schatting die niemand invult is erger dan geen
schatting, want een berekening op lege velden ziet er gezaghebbend uit en is ruis. De enige
correctielus is dat de vrijdag wrap-up scoort wat niet gehaald werd.

Dat is dun, en het is de meest waarschijnlijke reden dat dit ontwerp tegenvalt. Blijkt na
enkele weken dat structureel de helft van de datums niet gehaald wordt, dan is de conclusie
niet "we hebben een effort-veld nodig" maar "we plannen te veel per week" - en dat is een
gesprek, geen schema.

## Policies die gelden

canon-only-via-queue, hypothesis-is-not-canon, boards-are-generated,
sensitive-data-to-vault, never-invent-pricing.
