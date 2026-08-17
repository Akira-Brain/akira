---
capture: "2026-08-17-tore-richting-projectmanagement-en-ux"
tenant: company
source: Tore
date: 2026-08-17
status: routed
bron: "WhatsApp spraaknotitie 2026-08-17 08:30, getranscribeerd (131 regels)"
---

## Ruw

Strategische richtingaanwijzing van Tore over waar Akira nu naartoe moet, na een eerste
blik op de gebouwde infrastructuur.

**De kritiek.** "We hebben nu gewoon een eerste infrastructuur, maar de meerwaarde is er
nog niet." Twee redenen: het is nog niet gebruiksvriendelijk, en het is nog niet
inzichtelijk. De user-experience-dimensie ontbreekt volledig. De basisinfrastructuur ligt
er, maar het moet nu conceptueel en qua ontwerp naar de ervaring: hoe leeft dit samen met
de realiteit van een team van mensen.

**Wat centraal moet staan: projectmanagement.** Niet kennisbeheer. "Wat staat er altijd
centraal hier is projecten." De kernvragen die Akira moet aandrijven: wat moet er
gebeuren, wanneer, en met welke prioriteit. Vanuit een teamdimensie waarin verschillende
mensen als worker bees samenwerken, dingen uitvoeren, en op dingen botsen.

**Drie vaste vergadertypes die ondersteund moeten worden:**

1. *Maandag week-planning.* Team zit samen, Tore begeleidt het proces. Hij opent een
   Google Doc en vraagt: what's on your mind, wat staat er op de calendar, wat zit er in
   de pijplijn, wat waren de vorige weken, wat komen de volgende weken. Iedereen
   braindumpt. Dan pakt hij dat een voor een vast: wat moet er hiervoor gebeuren, wat zijn
   de deadlines, wie doet wat tegen wanneer. Het resultaat is een grote geneste lijst of
   outline. "Dat bereikt het allerbeste voor ons."
2. *Vrijdag wrap-up.* Wat is er deze week gebeurd, wat hebben we geleerd, wat willen we
   beter doen, wat zijn onze prioriteiten. **Gebeurt momenteel niet meer.** Reden die
   Tore zelf geeft: "omdat er eigenlijk niets meer gebeurt, we bouwen niet verder daarop,
   en daarom valt dat ook wel in het water."
3. *Client project kick-off.* Twee momenten: voor de opdracht binnen is (workload
   inschatten, negotiation points met Farah en Luna), en na binnenhalen (team-alignment op
   het project, deliverables bepalen, reverse-engineeren naar taken en deadlines).

**Het denkwerk blijft manueel, en dat moet ook.** Expliciet: "ik denk in de eerste plaats
dat het grotendeels een manueel denkproces blijft, en moet blijven ook." Het
vergaderproces eindigt in een Google Doc. De vraag is wat daarna gebeurt: die doc in
ChatGPT gooien, onder een klantmap, en er automatisch dingen uit laten filteren.

**Commands en views.** Daarna moet je kunnen zeggen: geef mij een overzicht van al onze
lopende projecten, de taken per persoon, de deadlines per persoon. Ook: zijn er projecten
die nu botsen met elkaar. Vaste commands die standaard templates opleveren, gepopuleerd
met overzichten en tabellen, vanuit een project- en taskmanagement-standpunt. Ook gedacht
per departement (bijvoorbeeld iemand van social media met eigen standaard commands).

**Tweede groot punt: het mag geen blackbox zijn.** Het team moet inzicht hebben in de
database die erachter zit, niet alleen via het chatinterface. "Een database mag niet enkel
door de robot worden beheerd, maar ook door de mens zelf." Reden: als je de architectuur
niet kent, weet je ook niet welke informatie er voorhanden is om te gebruiken - het
triggert de mens niet. Iedereen moet begrijpen hoe informatie in het bedrijf wordt
onderverdeeld, zodat ze in hun eigen cognitieve brein snappen hoe informatie stroomt en
wat er beschikbaar is. Na een meeting moet iemand begrijpen: deze meeting wordt nu
opgedeeld in deze soorten vakjes.

Met een uitdrukkelijke beperking: toegang moet gesegmenteerd zijn. "Eigenlijk niemand moet
toegang hebben tot pricing, behalve ik en Farah. En misschien Luna in bepaalde mate."

**Derde groot punt: van kennis naar standard operations.** De kern: "een keer de kennis
vastklikken, en dan kunnen we van daar verder ontwikkelen." Dat vastgeklikte wordt de
nieuwe bedrijfsbrede waarheid en de standard operating procedure. Daarna kan Akira
meedenken over welke modules, skills en agents daarop gebouwd kunnen worden.

Zijn eigen werkende voorbeeld: hij heeft een Claude-project voor offers, met een
zelfgebouwde skill. Komt er een aanvraag per mail binnen, dan gooit hij die erin en zegt
"nieuw offer". De skill herkent zelf de stages: welke informatie ontbreekt nog om
uberhaupt een zinvol gesprek met de klant te voeren, welke kwalificatievragen moeten
gesteld worden, en drafts de mail. Zodra alle info er is, kijkt hij er kritisch naar en
benoemt typische patronen - bijvoorbeeld: klanten maken het in hun woorden veel kleiner
dan het in realiteit is, of ze benoemen het alsof het maar een halve dag werk is terwijl
de hele waarde van brand endorsement wordt stilgezwegen. Die kennis moet bruikbaar worden
door andere mensen: "meer en meer mijn best practices uitdelegeren aan iemand die dat
management gaat overpakken."

**Onboarding als scenario.** Iemand die een nieuwe functie komt vervullen (bijvoorbeeld
social media management), of studenten die binnenkomen, moeten kunnen inloggen op de
company brain en daar de volledige uitleg krijgen. Scenario's bedenken van hoe een team
echt leeft: mensen komen erbij, gaan weg, voeren taken uit, lopen vast op dingen.

**Expliciete prioritering.** Over de Plaud-automatisering: "ik denk dat het beter is om
eerst na te denken, voordat we dat gaan volrammen met automatische informatiestromen -
beter om eerst na te denken over hoe Akira ons team gaat ondersteunen, projectmanagement-
gewijs." Dus: automatisering pauzeren, eerst het ontwerp.

**Verwijzingen.** Nog eens kijken naar HQ for Work, specifiek naar hun denkwerk over de
user-experience-dimensie van teams, hun commands en de policies die daaraan vasthangen.
En nog eens teruggrijpen naar de oorspronkelijke projectbriefing.

## Signalen

- **beslissing**: projectmanagement wordt de kern van Akira, niet kennisbeheer | scope: system | raakt canon: nee (interne richting, geen bedrijfswaarheid)
- **beslissing**: de Plaud-automatisering wordt gepauzeerd tot het ontwerp van de projectmanagement-laag er ligt
- **open vraag**: hoe wordt toegang gesegmenteerd zodat het team inzicht heeft in de database, maar pricing beperkt blijft tot Tore, Farah en deels Luna - dit kan niet met de huidige een-repo-opzet
- **taak**: ontwerp de projectmanagement-laag: welke commands, welke views, welke templates | owner: tore | due: ONBEKEND
- **taak**: ontwerp hoe de drie vergadertypes (maandag planning, vrijdag wrap-up, client kick-off) door Akira ondersteund worden | owner: tore | due: ONBEKEND
- **taak**: Tore's bestaande offer-skill uit zijn persoonlijke Claude-project overbrengen naar system/skills/ | owner: tore | due: ONBEKEND
- **taak**: informatie-architectuur expliciet en leesbaar maken voor het hele team (welke vakjes bestaan er, wat komt waar terecht) | owner: tore | due: ONBEKEND
- **learning-kandidaat**: de vrijdag wrap-up stierf omdat er niet op voortgebouwd werd - een ritueel zonder zichtbaar gevolg houdt geen stand
- **idee**: standaard commands per departement (bijvoorbeeld social media)
- **idee**: onboarding-scenario waarbij een nieuwe medewerker of student inlogt op de company brain voor volledige uitleg
- **idee**: conflictdetectie tussen projecten ("botsen er projecten met elkaar")

## Routering

Handmatig verwerkt op 2026-08-17. Zie `projects/active/akira-ai-os/` - dit is de eerste
capture die het Akira-project zelf als onderwerp heeft.
