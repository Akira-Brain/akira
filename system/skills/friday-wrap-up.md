# Skill: friday-wrap-up

Versie 0.1 - 2026-08-17. Ontworpen, nog niet in een echte vergadering toegepast; verwacht
een herschrijving na de eerste vrijdag, zoals `meeting-processing.md` er een kreeg na de
eerste zes transcripten.

## Doel

De week afsluiten met het team en de prioriteiten van volgende week vastleggen. Wat is er
gebeurd, wat sluiten we af, wat hebben we geleerd, waar gaan we volgende week op zitten.

**Dit ritueel is hier eerder al eens doodgebloed.** De reden was niet gebrek aan
intentie maar gebrek aan gevolg: er werd niets op voortgebouwd, dus viel het in het water.
Twee dingen in deze skill zijn daar direct op ontworpen, en ze zijn geen versiering:

1. **Vrijdag is het enige moment waarop `priority` verandert.** De prioriteiten die hier
   gekozen worden, worden weggeschreven als `priority: now`; al het andere zakt naar
   `next`. Daarmee *is* de sectie `## Nu` op het board maandagochtend letterlijk de
   beslissing van vrijdag. Sla vrijdag over en de Nu-lijst blijft staan zoals hij stond -
   zichtbaar, elke ochtend, in de daily brief. De afwezigheid van het ritueel wordt
   daarmee het meest zichtbare ding in het systeem in plaats van het minst zichtbare.
2. **Vrijdag is waar taken sluiten.** Op het moment van schrijven staan alle 57 taken in
   de repo op `open` - er is geen enkele afsluitbeweging. Maandag opent taken en niets
   sluit ze, dus groeit de lijst alleen maar en wordt hij onbetrouwbaar. Dat is precies
   hoe de eerdere Notion- en Asana-pogingen hier zijn gestorven.

## Input

Het gesprek zelf (transcript, spraakdump of live). Plus verplicht: het bestand van vorige
week, `company/rituals/{jaar}/W{nn-1}-vrijdag.md`.

**Ruwe signalen eruit halen doe je niet hier.** Volg `system/skills/meeting-processing.md`,
sectie "Stappen voor een vol vergadertranscript", stap 1 tot en met 3 en 6. Dat levert een
capture-bestand in `company/inbox/` en de geclassificeerde signalen. Deze skill begint bij
wat daar uitkomt en geeft het een andere vorm.

## Stappen

1. **Score vorige week.** Open `W{nn-1}-vrijdag.md` en loop de sectie
   `## Prioriteiten voor volgende week` langs. Elke prioriteit krijgt `gehaald`,
   `niet gehaald` of `vervallen`, met één redenregel. "Geen tijd" is geen reden zonder te
   benoemen wát de tijd nam. Bestaat het bestand niet, noteer dat als eerste regel - dat
   is de meting die het doodbloeden vangt.
2. **Sluit taken af.** Per persoon: alle taken met een `due` in de afgelopen week krijgen
   `done`, `dropped`, of een nieuwe datum met reden. Geen taak blijft stil staan met een
   verlopen deadline. Dit gebeurt hier of het gebeurt nergens.
3. **Wat is er gebeurd.** Projecten waarvan `updated` in deze week viel. Twee tot vijf
   zinnen per project, als journal-entry naar `projects/active/{slug}/journal/{datum}.md`.
   Append, nooit overschrijven - zelfde regel als in `project-update.md`.
4. **Wat hebben we geleerd.** Learning-kandidaten naar `working/learnings/{slug}.md` met
   `status: hypothesis`. Hier niet promoveren; promoveren is werk voor `weekly-review`.
5. **Wat willen we beter doen.** Elke verbetering wordt exact één van drie dingen: een
   taak op `akira-ai-os`, een voorstel in `canon-queue.md`, of een expliciete "hier doen
   we niets mee, want...". Die derde optie is verplicht aanwezig als optie - zonder een
   plek om dingen bewust te laten vallen wordt de lijst een kerkhof.
6. **Prioriteiten voor volgende week.** Drie tot vijf, in de vaste vorm
   `{project-slug} - {concrete uitkomst} - {eigenaar}`. Een prioriteit zonder projectslug
   is geen prioriteit maar een wens. Schrijf daarna `priority: now` op precies die
   projecten en `priority: next` op alle andere actieve projecten, en meld hardop welke
   projecten van Nu af vallen. Het board kent een drempel van vijf op Nu; zit je erboven,
   dan is dit het moment om te kiezen.
7. **Lees de gezondheidsgetallen van het board**, tel ze niet zelf. Loopt er iets op, zeg
   dat, en maak er een taak van in plaats van het te noteren.
8. Sla op als `company/rituals/{jaar}/W{nn}-vrijdag.md`, regenereer het board met
   `python system/scripts/generate-board.py`, en commit.

## Outputvorm

```markdown
---
ritueel: vrijdag-wrap-up
week: 2026-W34
datum: 2026-08-21
aanwezig: [tore, farah, luna]
status: verwerkt
---

# Wrap-up W34

## Score van W33

- positionering-starmaker scenariokeuze: NIET GEHAALD - Jasmijn kon pas donderdag
- stock-digitalisering instructiedocument: GEHAALD
- stock sale datum prikken: VERVALLEN - zaal geeft pas in september uitsluitsel

Twee van drie niet gehaald, beide door externe wachttijd. Tweede week op rij.

## Afgesloten deze week

- luna: 2 taken done, 1 dropped
- tore: 1 done, 3 blijven open met nieuwe datum

## Wat er gebeurd is

- positionering-starmaker: scenario half uitgeschreven, pros en cons staan
- groen-aanvraag: nog geen antwoord op de conceptmail

## Geleerd (hypothese, naar working/learnings/)

- Externe adviseurs plannen wij in alsof ze intern beschikbaar zijn. Twee weken op rij
  is dat de reden dat een prioriteit niet gehaald werd.

## Beter doen

- Taak die van een externe afhangt: `due` wordt de datum dat wíj opvolgen, niet de datum
  dat het af moet zijn -> taak op akira-ai-os
- Vergaderdoc eerder rondsturen -> hier doen we niets mee, kost meer dan het oplevert

## Prioriteiten voor W35

1. positionering-starmaker - scenario af en voorgelegd aan Farah - tore
2. stock-digitalisering - instructiedocument af - luna
3. groen-aanvraag - offerte de deur uit - farah

Nu-lijst wordt daarmee die drie. Van Nu af: as-adventure-second-life, boek,
cannes-red-carpet-2027, festival-showroom-2026, private-styling-verhuur.

## Gezondheid (uit BOARD.md, niet zelf geteld)

verouderde status 13 - ongerouteerde captures 0 - canon-queue 6
Canon-queue staat al drie weken op zes. Taak aangemaakt op akira-ai-os.
```

## Grens met weekly-review

De vrijdag wrap-up is de **teamvergadering**: wat is er gebeurd, wat sluiten we af, wat
leren we, wat zijn de prioriteiten van volgende week. De weekly review is de
**solo-onderhoudsronde**: canon-queue, wezen in de inbox, learnings promoveren,
archiveren.

| Onderwerp | vrijdag wrap-up | weekly review |
|---|---|---|
| taken afsluiten | ja, met het team | nee |
| verouderde projectstatus | alleen het aantal noemen | ja, per project uitvragen |
| learnings | ruw oogsten naar `working/` | promoveren naar `proposed` |
| canon-queue | nee | ja |
| wezen in de inbox | nee | ja |
| afgeronde projecten archiveren | nee | ja |
| prioriteiten volgende week | ja, dit is de kern | nee |

**Het risico van deze verdeling, expliciet:** beide rituelen vallen op vrijdag, en de
eigenaar is op 14 van de 17 projecten de volgende stap. Twee vaste verplichtingen op
dezelfde dag voor dezelfde persoon betekent doorgaans dat er één sterft, en dat wordt dan
de teamvergadering - precies degene die hier al eens gestorven is. Sterft de wrap-up twee
keer op rij, dan is dat het signaal om de cadans te heroverwegen, niet om er functies bij
te bouwen.

## Bekende zwakte

Dit ritueel meet of prioriteiten gehaald zijn, maar niet of ze realistisch waren. Er is
bewust geen effort- of capaciteitsveld (zie de dekkingsredenering in
`generate-board.py`): een schatting die niemand invult, is erger dan geen schatting. De
enige correctielus is dat vrijdag scoort wat niet gehaald werd. Blijkt na een aantal weken
dat structureel de helft niet gehaald wordt, dan is dat een signaal over de planning zelf,
niet over de week.

## Policies die gelden

canon-only-via-queue, hypothesis-is-not-canon, boards-are-generated,
sensitive-data-to-vault, never-invent-pricing.
