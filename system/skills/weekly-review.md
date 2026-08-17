# Skill: weekly-review

Versie 0.2 - 2026-08-17. Aangepast omdat er nu een tweede vrijdagritueel bestaat
(`friday-wrap-up`); de taakverdeling tussen die twee staat hieronder en moet in beide
bestanden identiek blijven.

## Doel

Het gardening-ritueel. Dit is het hart van het systeem: zonder deze wekelijkse ronde
vervuilt het geheugen en verouderen de statussen, en dan sterft het systeem aan
wantrouwen. Duur: 30 tot 45 minuten.

Dit is de **solo-onderhoudsronde**, niet de teamvergadering. Wat er met het team gebeurt -
taken afsluiten, prioriteiten kiezen - hoort in `friday-wrap-up`.

## Input

Geen. Dit draait over de hele tenant.

## Stappen

1. **Canon-queue langslopen.** Presenteer elk openstaand voorstel: wat verandert, wat
   is de rationale, welke evidence. Vraag per stuk om akkoord, afwijzing of uitstel.
   Bij akkoord: voer de wijziging uit, zet `approved_by` en `updated`, archiveer het
   queue-item. Bij afwijzing: noteer waarom in het bronbestand, zodat hetzelfde
   voorstel niet over een maand terugkomt.
2. **Verouderde statussen.** Alle projecten met `status: active` en `updated` ouder dan
   14 dagen. Per stuk: nog steeds actief, of parked, waiting, of done? Dit is de
   belangrijkste vraag van de hele review. Het aantal lees je van het board; de vraag per
   project stel je hier.
3. **Wezen in de inbox.** Captures met status ongelijk aan `routed`. Route ze alsnog,
   of gooi ze bewust weg. Een inbox die vol blijft staan, is een inbox die niemand
   meer leest.
4. **Learnings met genoeg evidence.** Hypotheses met voldoende evidence-verwijzingen
   of met `review_after` bereikt. Voorstellen om te promoveren naar `proposed` en dus
   naar de canon-queue van volgende week.
5. **Afgeronde projecten.** Projecten met `status: done`: is de learning-oogst gedaan?
   Zo ja, verplaats naar `archive/{jaar}/`. De oogstvraag is verplicht, het antwoord
   "geen learnings" is toegestaan.
Taken zonder eigenaar en taken over datum stonden hier als stap 6. Die zijn verhuisd: het
board toont ze nu onder `## Botsingen en belasting`, en de maandagplanning wijst ze toe.
Dat is de plek waar mensen aan tafel zitten die de taak kunnen aannemen.

## Outputvorm

Een lijst, gegroepeerd per stap, met per item een concrete vraag die met ja/nee of een
korte keuze te beantwoorden is. Geen proza. De review moet af te werken zijn terwijl
iemand koffie drinkt.

## De gezondheidsmeting

Meld aan het eind drie getallen:

- aantal projecten met verouderde status
- aantal ongerouteerde captures
- aantal openstaande canon-queue-items

Lopen deze structureel op, dan is dat het signaal om te **versimpelen, niet uit te
breiden**. Twee overgeslagen reviews op rij is hetzelfde signaal. Het systeem sterft
aan gebrek aan ritueel, niet aan gebrek aan functies: de eerdere Notion- en
Asana-pogingen bewijzen dat.

## Grens met friday-wrap-up

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

## Policies die gelden

canon-only-via-queue, hypothesis-is-not-canon, boards-are-generated.
