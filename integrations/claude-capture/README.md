# Capture-pad via Claude (variant A2) - GEKOZEN PAD

Versie 0.2 - 2026-08-16. Dit is het gekozen capture-pad voor Akira.
De Custom GPT in `../chatgpt-capture/` blijft bestaan als terugval.

## Rollen: wie krijgt wat

Akira staat sinds 2026-08-16 in de organisatie `Akira-Brain` en blijft privé. Dat was
een voorwaarde voor dit pad: op een private repo van een persoonlijk account laat GitHub
geen read-only collaborators toe, waardoor iedereen die je toevoegt schrijfrechten op
alle bestanden krijgt. In een organisatie kan het wel per persoon:

| Wie | Rol | Mag |
|---|---|---|
| Farah, studenten, stagiairs | **Read** | issues aanmaken (captures), bestanden lezen, niets pushen |
| Luna, als zij captures beheert | **Triage** | daarnaast labelen en sluiten |
| Tore | **Admin** | alles, inclusief de routering |

Met rol Read maakt het niet meer uit welke MCP-URL iemand in zijn Claude plakt: ook de
volledige server kan dan geen bestanden schrijven, omdat het account het niet mag. De
grens verschuift van "goed geconfigureerd" naar "GitHub staat het niet toe", en dat is
de enige plek waar hij thuishoort.

## Wat dit is

Claude praat rechtstreeks met GitHub via de gehoste MCP-server van GitHub. Geen token
aanmaken, geen OpenAPI-schema, geen vervaldatum. Captures landen als GitHub Issue met
label `capture`.

Vanaf dat moment gebeurt de rest **automatisch**: de workflow
`.github/workflows/capture-intake.yml` routeert de capture naar de juiste plek in de repo,
regenereert het BOARD, meldt op het issue waar alles geland is en sluit het. Niemand hoeft
iets te starten. Je praat, en het staat erin.

Blijft er iets onduidelijk, dan blijft het issue open staan met een comment die zegt wat
er niet geplaatst kon worden. Dat komt terug in de weekly review.

**Eenmalige voorwaarde:** de workflow draait op GitHub's servers, waar niemand ingelogd
is, en heeft dus een eigen credential nodig. Dat kan gewoon op het bestaande
Claude-abonnement:

```bash
claude setup-token
```

Bewaar de uitvoer als repo-secret `CLAUDE_CODE_OAUTH_TOKEN`
(Settings -> Secrets and variables -> Actions -> New repository secret).

Geen aparte API-facturatie nodig. Wie liever losse facturatie heeft die niet meetelt met
het persoonlijke abonnement, kan in plaats daarvan een `ANTHROPIC_API_KEY` gebruiken; de
regel om te wisselen staat in de workflow.

## Twee connectors, elk apart afgeschermd

Dit is de kern van de opzet. GitHub's MCP-server laat je per URL bepalen welke tools
Claude te zien krijgt, en dat gebruiken we om dezelfde grens te trekken als bij het
token in de GPT-variant.

| Connector | URL | Wat het mag |
|---|---|---|
| Akira - captures | `https://api.githubcopilot.com/mcp/x/issues` | issues lezen en aanmaken |
| Akira - lezen | `https://api.githubcopilot.com/mcp/x/repos/readonly` | bestanden lezen, niets schrijven |

Voeg **nooit** `https://api.githubcopilot.com/mcp/` zonder pad toe. Dat is de volledige
server, inclusief schrijfrechten op bestanden, en dan kan de sessie in `knowledge/` en
`policies/` schrijven. Precies wat het ontwerp verbiedt.

De tweede connector is alleen nodig voor de daily brief. Laat je hem weg, dan kan Claude
wel captures wegschrijven maar het BOARD niet lezen.

## Opzetten (ongeveer vijf minuten per persoon)

0. Alleen als er iemand anders dan de eigenaar aansluit: staat de repo in een
   organisatie en heeft die persoon rol Read of Triage? Zie de voorwaarde bovenaan.
1. Claude.ai -> **Settings -> Connectors -> Add custom connector**.
2. Plak de eerste URL uit de tabel. Naam: `Akira - captures`. Opslaan.
3. Klik **Connect** en log in bij GitHub in het venster dat opent. Keur de toegang goed.
4. Herhaal stap 1 tot 3 voor de tweede URL, naam `Akira - lezen`.
5. Maak een **Project** aan met de naam `Chatty`. Plak `project-instructions.md` in de
   projectinstructies.
6. Test met de zin uit "Testen" hieronder.

Op Claude Free kan maar een connector tegelijk. Neem dan alleen de eerste; de daily
brief komt dan voorlopig van Tore.

## Testen

Zeg in het project:

> Ik heb net met Luna gesproken. Zij gaat accessoires sourcen voor de shoot van volgende
> week, dat moet tegen donderdag klaar zijn. En we twijfelen nog of we een tweede fitting
> inplannen, dat moet Farah beslissen.

Geslaagd als er op https://github.com/Akira-Brain/akira/issues een issue verschijnt met
label `capture`, met Luna's taak inclusief deadline, en met de fittingvraag als open
beslissing voor Farah in plaats van als taak. En met niets erin dat niet gezegd is.

## Verschillen met de GPT-variant

| | Custom GPT | Claude-connector |
|---|---|---|
| Opzet | ~20 min, token + OpenAPI-schema | ~5 min, twee URL's plakken |
| Inloggen | fine-grained token, verloopt na 90 dagen | OAuth, geen vervaldatum om te bewaken |
| Wie is de schrijver | het token van Tore | de ingelogde persoon zelf |
| GitHub-account nodig | nee | **ja**, met toegang tot de private repo |
| Hardheid van de grens | het token kan technisch geen bestanden schrijven | de connector toont alleen issue-tools |

Dat laatste verschil is echt maar klein: bij de GPT zit de grens in de credential zelf,
bij Claude in welke tools de connector aanbiedt. Beide voorkomen schrijven in
`knowledge/`. De credential-variant is strikter, de connector-variant is eenvoudiger.

De praktische vraag is de voorlaatste regel: **wil Farah een GitHub-account?** Zo ja,
dan is deze route korter en is er niets te onderhouden. Zo nee, dan blijft de GPT-variant
staan, want daar maakt Tore het token en raakt Farah GitHub nooit aan.

Voor Tore zelf is er geen afweging: hij heeft al een GitHub-account, dus dit is de
snelste manier om het hele capture-pad vandaag nog te testen.
