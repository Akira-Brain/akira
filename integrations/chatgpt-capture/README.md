# Farah's capture-pad: Custom GPT naar GitHub

Versie 0.1 - 2026-08-14. Dit is pad A uit het ontwerp, in de vorm die vandaag werkt.

## Wat dit is

**Terugvalpad.** Het gekozen pad is `../claude-capture/`; deze variant blijft staan voor
wie geen GitHub-account wil of kan hebben.

Farah praat met een Custom GPT in ChatGPT. Die GPT schrijft elke capture weg als
GitHub Issue in `akira`, met het label `capture`. Daarna neemt de workflow
`.github/workflows/capture-intake.yml` het automatisch over.

```
Farah spreekt
   -> Custom GPT classificeert
   -> GitHub Issue met label "capture"   (Farah's kant stopt hier)
   -> workflow capture-intake routeert automatisch
   -> project.yaml / ideas/ / working/ / decisions/
   -> issue gesloten met vermelding waar alles landde
```

## Waarom Issues en geen bestanden

Twee redenen, en de tweede is de belangrijkste.

**Betrouwbaarheid.** De GitHub Contents API wil base64-gecodeerde inhoud. Een
taalmodel dat lange gesproken tekst naar base64 omzet, maakt fouten, en die fouten zijn
stil: je merkt pas weken later dat een capture onleesbaar is weggeschreven. De Issues
API neemt gewoon platte tekst aan.

**Structurele afscherming.** Een fine-grained token kan rechten krijgen op *Issues*
zonder enig recht op bestanden. Farah's GPT kan daardoor letterlijk niets in
`knowledge/`, `policies/` of welk bestand dan ook wijzigen, ook niet als het model
zich vergist of iemand het probeert over te halen. Dat is een echte grens, afgedwongen
door GitHub, niet een afspraak in een prompt.

Dat is precies het capture-zone-principe uit het ontwerp, alleen dan met tanden.

## Opzetten

Ongeveer twintig minuten. Stap 1 en 2 doet Tore, stap 3 en 4 doen jullie samen.

### 1. Repo klaarzetten

De repo `akira` moet op GitHub staan (privé) en er moet een label `capture`
bestaan. Labels maak je aan bij Issues -> Labels -> New label. Maak hem aan voordat je
test: een issue met een onbekend label kan mislukken.

### 2. Token aanmaken

**Dit doet Tore zelf. Deel het token met niemand, ook niet met een AI-sessie.**

GitHub -> Settings -> Developer settings -> Personal access tokens -> Fine-grained
tokens -> Generate new token.

| Instelling | Waarde |
|---|---|
| Token name | `farah-capture-gpt` |
| Expiration | 90 dagen (zet een herinnering in de agenda) |
| Resource owner | het account dat eigenaar is van de repo |
| Repository access | Only select repositories -> **alleen** `akira` |
| Permissions -> Issues | **Read and write** |
| Permissions -> Contents | **Read-only** (alleen nodig voor de daily brief) |
| Permissions -> Metadata | Read-only (zet GitHub zelf aan) |

Geef **nooit** Contents write. Dat is het hele punt van deze opzet.

Wil je de daily brief voorlopig overslaan, laat Contents dan helemaal weg. Dan kan het
token uitsluitend captures aanmaken en lezen.

### 3. De Custom GPT maken

In ChatGPT: linksboven -> GPTs -> Create -> Configure.

- **Name**: Chatty
- **Instructions**: plak de volledige inhoud van `gpt-instructions.md` (alles onder de
  streep).
- **Capabilities**: zet Web Browsing, DALL-E en Code Interpreter uit. Niet nodig, en
  minder oppervlak.
- **Actions** -> Create new action:
  - **Schema**: plak `openapi.yaml` ongewijzigd. De paden wijzen al naar
    `github.com/Akira-Brain/akira`.
  - **Authentication**: API Key, Auth Type **Bearer**, en plak het token uit stap 2.
- Bewaren, en delen met Farah (Only people with a link, of via je workspace).

### 4. Testen

Zeg tegen de GPT: *"Ik heb net met Luna gesproken. Zij gaat accessoires sourcen voor de
shoot van volgende week, dat moet tegen donderdag klaar zijn. En we twijfelen nog of we
een tweede fitting inplannen, dat moet Farah beslissen."*

Geslaagd als:

- er een issue verschijnt met label `capture`
- de taak voor Luna staat er met een due-datum
- de fittingvraag staat als open beslissing voor Farah, niet als taak
- er niets verzonnen is dat niet gezegd werd

Test daarna ook de daily brief: *"Wat moet ik vandaag weten?"* Werkt `getBoard` niet
(dat is het meest fragiele onderdeel, zie hieronder), dan is dat geen blokkade: haal de
Action weg en laat Farah de brief voorlopig van Tore krijgen.

## Wat hieraan fragiel is

**De daily brief.** `getBoard` leunt op de header `Accept: application/vnd.github.raw`
om platte tekst te krijgen in plaats van base64. Of een Custom GPT die header
betrouwbaar meestuurt, moet blijken. Faalt dit, dan verlies je alleen de leeskant.
De captures blijven werken.

**Tokenverloop.** Na 90 dagen stopt het stilzwijgend. Zet de herinnering echt in de
agenda; het faalsymptoom is "Chatty doet niks meer" en dat is verwarrend voor Farah.

**Abonnementsvereisten.** Welke ChatGPT-abonnementen Custom GPT Actions toestaan,
verandert regelmatig. Loopt stap 3 vast op het abonnement, dan is dat het moment om
pad B (mailen) te proberen in plaats van hierin te blijven duwen.

**De routering gebeurt automatisch** via de workflow. Faalt die, dan blijven captures
dat dagelijks of wekelijks, maar doe het: een issue-lijst die volloopt is dezelfde
faalwijze als een inbox die niemand leest.

## Wat dit bewust niet doet

Farah kan hiermee niets goedkeuren, geen prijs wijzigen en geen canon aanraken. Ze kan
ook niets stukmaken. Dat is geen wantrouwen richting Farah: het is dat een taalmodel dat
de hele dag vrij mag schrijven in een gedeeld bedrijfsgeheugen, dat geheugen vroeg of
laat vervuilt. De grens zit op de plek waar hij hoort.
