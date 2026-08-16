# personal/farah - placeholder

Versie 0.1 - 2026-08-14

Deze tenant is nog niet in gebruik. Hij wordt geactiveerd zodra de
ChatGPT-interfacetest is uitgevoerd en duidelijk is via welk pad Farah captures
aanlevert.

## De drie paden

| Pad | Hoe | Status |
|---|---|---|
| A1 (gebouwd) | Custom GPT met Action schrijft captures weg als GitHub Issue met label `capture`. Token heeft alleen Issues-rechten, geen bestandsrechten. Farah heeft geen GitHub-account nodig. | opzetklaar, zie `integrations/chatgpt-capture/` |
| A2 (gebouwd) | Claude met twee afgeschermde GitHub-connectors doet hetzelfde in vijf minuten opzet, zonder token en zonder vervaldatum. Vereist wel een GitHub-account met toegang tot de repo. | opzetklaar, zie `integrations/claude-capture/` |
| B (terugval) | De capture-GPT mailt het blok naar een vast adres; een verwerkingsronde in Claude leest de mailbox en routeert. | achter de hand |
| C (werkt vandaag) | Farah deelt het blok met Tore; Tore's Claude routeert het in seconden. | beschikbaar |

Beide varianten van pad A wijken op een punt af van het oorspronkelijke ontwerp:
captures landen als GitHub Issue in plaats van als bestand in `company/inbox/`. Reden:
schrijfrechten op alleen de map `inbox/` bestaan niet in GitHub, maar rechten op alleen
issues wel. De issue-route geeft dus een echte, afgedwongen grens in plaats van een
afspraak in een prompt. De inbox-map blijft bestaan voor captures die via Tore of via
pad B binnenkomen.

De keuze tussen A1 en A2 hangt aan een vraag: wil Farah een GitHub-account? Zo ja, dan
is A2 korter en is er niets te onderhouden. Zo nee, dan is A1 de route, want daar maakt
Tore het token aan en raakt Farah GitHub nooit aan.

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
