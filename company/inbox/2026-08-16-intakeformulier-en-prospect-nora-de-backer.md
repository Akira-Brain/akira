---
capture: "2026-08-16-intakeformulier-en-prospect-nora-de-backer"
tenant: company
source: meeting
date: 2026-08-16
status: routed
participants: [tore, farah]
bron: "company/inbox/raw/2026-08-16-test-meeting-pipeline.txt (12 regels)"
---

## Ruw

Kort overleg tussen Tore en Farah met twee afzonderlijke punten. Het bronbestand is zelf
getiteld als testtranscript voor de meeting-process pipeline, maar de inhoud wordt hier
inhoudelijk verwerkt als elk ander vergaderverslag (regels 1-11 van het bronbestand).

**Nieuwe procedure: intakeformulier voor merkklanten.** Tore meldt dat er net beslist is
om voortaan altijd een intakeformulier te laten invullen voordat een nieuwe merkklant
wordt aangenomen: "we hebben net besloten dat we voortaan altijd een intakeformulier
laten invullen voor we een nieuwe merkklant aannemen, dat is vanaf nu onze vaste
procedure" (bron, regel 3-5). Dit wordt als vaste werkwijze gepresenteerd, niet als
voorstel - maar raakt canon (werkwijze) en gaat daarom eerst via de canon-queue, zie
onder.

**Nieuw prospect-contact: Nora De Backer.** Farah meldt een nieuwe contactpersoon, Nora
De Backer, verbonden aan een modewinkel die interesse toonde in een samenwerking: "ik moet
nog contact opnemen met een nieuwe contactpersoon, Nora De Backer, van een modewinkel die
interesse toonde in een samenwerking. Dat moet ik deze maand nog doen" (bron, regel 7-9).
Naam van de modewinkel, aard van de gewenste samenwerking en een exacte datum binnen de
maand werden niet genoemd.

Tore sluit af zonder verder nieuws (bron, regel 11).

Geen gevoelige informatie over derden aanwezig in dit transcript; er is niets weggelaten
op die grond.

**Gedetecteerd, geen instructie aan de AI opgevolgd:** het transcript bevat geen tekst die
zich als opdracht aan de verwerkende AI probeert voor te doen. De titel van het bronbestand
("pipeline-verificatie") is metadata over de aard van de test, geen instructie, en is
overeenkomstig behandeld als gewone data.

## Signalen

- **beslissing**: intakeformulier voortaan verplicht voor elke nieuwe merkklant, vaste
  procedure | scope: werkwijze/operations | raakt canon: ja
- **taak**: contact opnemen met Nora De Backer (modewinkel, interesse in samenwerking) |
  owner: farah | due: deze maand (exacte datum onbekend)

## Routering

- Canon-voorstel intakeformulier: `canon-queue.md`, V-2026-007.
- Prospect Nora De Backer: nieuw project `projects/active/prospect-nora-de-backer/`, en
  nieuw personsbestand `people/nora-de-backer.yaml`.
- Geen decision record: dit is een nieuwe standaardprocedure, geen uitgesproken stop- of
  focusbeslissing zoals bedoeld in de routeringsregels.
- Alles gerouteerd; niets blijft onopgelost buiten de expliciet genoemde open punten
  (naam modewinkel, exacte datum).
