# Skill: weekly-review

Versie 0.1 - 2026-08-14

## Doel

Het gardening-ritueel. Dit is het hart van het systeem: zonder deze wekelijkse ronde
vervuilt het geheugen en verouderen de statussen, en dan sterft het systeem aan
wantrouwen. Duur: 30 tot 45 minuten.

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
   belangrijkste vraag van de hele review.
3. **Wezen in de inbox.** Captures met status ongelijk aan `routed`. Route ze alsnog,
   of gooi ze bewust weg. Een inbox die vol blijft staan, is een inbox die niemand
   meer leest.
4. **Learnings met genoeg evidence.** Hypotheses met voldoende evidence-verwijzingen
   of met `review_after` bereikt. Voorstellen om te promoveren naar `proposed` en dus
   naar de canon-queue van volgende week.
5. **Afgeronde projecten.** Projecten met `status: done`: is de learning-oogst gedaan?
   Zo ja, verplaats naar `archive/{jaar}/`. De oogstvraag is verplicht, het antwoord
   "geen learnings" is toegestaan.
6. **Taken zonder eigenaar of met verlopen deadline.** Kort langslopen.

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

## Policies die gelden

canon-only-via-queue, hypothesis-is-not-canon, boards-are-generated.
