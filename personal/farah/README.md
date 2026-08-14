# personal/farah - placeholder

Versie 0.1 - 2026-08-14

Deze tenant is nog niet in gebruik. Hij wordt geactiveerd zodra de
ChatGPT-interfacetest is uitgevoerd en duidelijk is via welk pad Farah captures
aanlevert.

## De drie paden

| Pad | Hoe | Status |
|---|---|---|
| A (gebouwd) | Custom GPT met Action schrijft captures weg als GitHub Issue met label `capture`; Tore routeert via skill `capture-intake`. Token heeft alleen Issues-rechten, geen bestandsrechten. | opzetklaar, zie `integrations/chatgpt-capture/` |
| B (terugval) | De capture-GPT mailt het blok naar een vast adres; een verwerkingsronde in Claude leest de mailbox en routeert. | achter de hand |
| C (werkt vandaag) | Farah deelt het blok met Tore; Tore's Claude routeert het in seconden. | beschikbaar |

Pad A wijkt op een punt af van het oorspronkelijke ontwerp: captures landen als GitHub
Issue in plaats van als bestand in `company/inbox/`. Reden: een token kan wel
Issues-rechten krijgen zonder bestandsrechten, maar niet schrijfrechten op alleen de
map `inbox/`. De issue-route geeft dus een echte, door GitHub afgedwongen grens in
plaats van een afspraak in een prompt. De inbox-map blijft bestaan voor captures die
via Tore of via pad B binnenkomen.

## Wat al vaststaat, ongeacht het pad

Het **capture-contract** verandert niet. Elke interactie van Farah eindigt in een
capture-blok volgens `system/templates/capture.md`, met frontmatter (source, datum,
tenant), de ruwe weergave, en door AI geclassificeerde signalen. Alleen de bezorging
verschilt per pad.

Dat is met opzet zo ontworpen: de interfacelaag is het minst stabiele deel van het hele
plan, dus mag het ontwerp er niet van afhangen.

## Wat hier komt te staan

Zelfde ministructuur als `personal/tore/`: `BOARD.md`, `projects/`, `ideas/`, `inbox/`,
`knowledge/`, `decisions/`.

## Wat Farah nooit hoeft te doen

Git begrijpen, bestandsnamen kiezen, mappen kennen, of beslissen waar een opmerking
thuishoort. Zij spreekt, het systeem classificeert. Lukt dat niet, dan is dat een fout
van het ontwerp, niet van de gebruiker.
