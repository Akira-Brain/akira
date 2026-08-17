# Aansluiten op Akira

Versie 0.2 - 2026-08-16

Akira is het gedeelde geheugen van het atelier. Je praat ertegen, en wat je vertelt
belandt automatisch op de juiste plek: taken bij het juiste project, beslissingen in het
beslissingsregister, ideeën op de parkeerplaats.

**Iedereen gebruikt hetzelfde: Chatty in ChatGPT.** Farah, Tore, Luna, stagiairs. Er is
geen aparte technische route en er zijn geen uitzonderingen.

---

## Opzetten: twee minuten, één keer

Je hebt nodig: een ChatGPT-account en een link van Tore. Verder niets. Geen GitHub, geen
installatie, geen wachtwoorden.

1. Vraag Tore de link naar **Chatty**.
2. Open die link in ChatGPT. Zet hem bij je favorieten of op je startscherm.
3. Zeg wie je bent bij je eerste bericht: *"Hoi, ik ben Luna."*

Klaar. Er is geen stap vier.

---

## Gebruiken

Praat gewoon. Na een gesprek, na een fitting, na een telefoon met een klant. Inspreken
werkt vaak makkelijker dan typen.

> "Ik heb net met de klant gebeld. De fitting gaat door op donderdag, en zij vroeg of we
> ook accessoires kunnen sourcen. Ik moet daar nog een prijs voor doorgeven."

Je hoeft niets te structureren. Niet nadenken over of iets een taak is of een
beslissing, niet bedenken waar het hoort. Dat is precies het werk dat Chatty doet.

Wat je zegt wordt binnen enkele minuten verwerkt. Je hoeft daar niets voor te doen en
niets van op te volgen.

---

## Zelf kijken

Praten is de manier om iets *in* Akira te krijgen. Om te zien wat erin zit is er een
website. Je hoeft daar niets voor te installeren en geen account te maken: je vult je
e-mailadres in, krijgt een code toegestuurd, en bent binnen.

Wat je er vindt:

| Pagina | Waarvoor |
|---|---|
| Het bord | Wat er loopt, wat er vastzit, welke deadlines eraan komen |
| Projecten | Per project de taken, de geschiedenis en waar het op wacht |
| Mensen | Wat er op wiens lijst staat |
| Wat we weten | Wat vaststaat, en wat we alleen nog vermoeden |
| Wat er binnenkwam | Welke gesprekken zijn verwerkt |
| De kaart | Hoe informatie hier verdeeld wordt - lees deze een keer rustig door |
| Wat kan ik vragen | De vragen die je kunt stellen, in gewone taal |

**Begin bij De kaart.** Die legt uit welke vakjes er zijn en wat waar terechtkomt. Wie dat
een keer gezien heeft, weet daarna ook wat hij kan vragen - en dat is precies waarom die
pagina er staat.

De site is om te lezen. Wijzigen doe je door het te zeggen.

Twee dingen die je zult merken. **Bedragen staan er niet op**, tenzij je zaakvoerder bent;
op de kaart zie je wél welke vakjes er zijn die je niet kunt openen, zodat je weet wat je
aan wie kunt vragen. En **de pagina's zijn zo actueel als de laatste keer dat ze gebouwd
zijn** - bovenaan staat wanneer dat was.

---

## Wat je moet weten

**Zeg het gewoon zoals het is.** Half afgemaakte zinnen, twijfels, "ik weet niet meer
precies wanneer" - allemaal prima. Chatty vult niets in wat je niet gezegd hebt. Weet
hij niet wie iets moet doen of wanneer, dan laat hij dat leeg in plaats van te gokken.

**Vertel geen gevoelige klantinformatie.** Maten, privéadressen, privénummers,
gezondheid, contractdetails: die horen niet in Akira. Komen ze toch voorbij, dan laat
Chatty ze eruit en zet er een verwijzing in de plaats. Noem ze liever gewoon niet.

**Je kunt niets stukmaken.** Chatty mag alleen vastleggen. Hij kan geen prijzen
wijzigen, geen bedrijfsafspraken aanpassen en geen bestanden overschrijven. Dat is
technisch afgeschermd, niet alleen afgesproken.

**Chatty beslist niets.** Zeg je iets over een prijs of een werkwijze, dan noteert hij
dat als voorstel. Het wordt pas bedrijfswaarheid als Tore en Farah akkoord geven.

**Zeg het als iets niet klopt.** Vertel het aan Tore. Alles wat Chatty vastlegt is
zichtbaar en terug te draaien.

---

# Voor Tore: wat je één keer opzet

Daarna is elke nieuwe persoon een kwestie van een link doorsturen.

| Stap | Wat | Waar |
|---|---|---|
| 1 | Fine-grained token aanmaken: Issues read/write, Contents read-only, alleen repo `akira` | GitHub settings |
| 2 | Custom GPT "Chatty" maken met dat token en de instructies | `integrations/chatgpt-capture/README.md` |
| 3 | GPT delen via link | ChatGPT |
| 4 | `claude setup-token` en bewaren als repo-secret `CLAUDE_CODE_OAUTH_TOKEN` | GitHub repo settings |

Stap 4 laat de automatische routering draaien. Zonder dat secret komen captures wel
binnen als issue, maar worden ze niet verwerkt.

## Iemand nieuw laten aansluiten

Stuur de link naar Chatty en verwijs naar het eerste deel van dit document. Meer is het
niet. Zij hebben geen GitHub-account nodig, staan niet in de organisatie en krijgen geen
enkel recht op de repo.

Dat is bewust: hoe minder mensen rechtstreeks toegang hebben tot het geheugen, hoe minder
er per ongeluk kan gebeuren. Iedereen praat, één token schrijft, de automatisering
routeert.

## Wat niet via Chatty kan

Drie dingen blijven bewust buiten het dagelijkse praten:

- **Canon goedkeuren.** Voorstellen voor prijzen, werkwijzen en positionering verzamelen
  zich in `company/canon-queue.md`. Er is geen geautomatiseerde beoordeling meer, ook niet
  via de API: goedkeuren doe je met "akkoord" tegen een AI-sessie die dan de wijziging
  doorvoert, samen met Farah.
- **Volledige vergadertranscripten** (bijvoorbeeld van Plaud). Te lang voor een GitHub
  issue (die zijn beperkt tot 65.536 tekens - meerdere van jullie eigen transcripten
  zaten daar al overheen) en te veel oordeel voor de goedkope automatische route. Die
  verwerk je in een live sessie op je eigen Claude-abonnement (Claude Code, of een andere
  sessie met bevestigde schrijftoegang tot de repo), volgens
  `system/skills/meeting-processing.md`. Geen Action, geen API-kosten voor dat werk;
  Chatty en de automatische routering blijven puur voor korte dagelijkse captures.
- **De wekelijkse review.** Verouderde statussen nalopen, openstaande captures afhandelen,
  learnings met genoeg bewijs promoveren. Skill: `system/skills/weekly-review.md`.

Dat is samen misschien een uur per week, geen dagelijkse handeling. Het dagelijkse werk
loopt volledig via Chatty, en de API-kosten blijven daardoor beperkt tot precies dat:
korte captures routeren, een paar cent per stuk.

## Wat je in de gaten houdt

- **Openstaande capture-issues** die niet vanzelf sluiten. Dat betekent dat de routering
  iets niet kon plaatsen; het staat in de comment.
- **De canon-queue.** Wacht op akkoord van jou en Farah. Blijft met opzet mensenwerk.
- **De wekelijkse review.** Het ritueel dat de rest overeind houdt. Twee keer overslaan
  is het signaal om te versimpelen, niet om uit te breiden.
