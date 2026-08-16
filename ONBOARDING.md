# Aansluiten op Akira

Versie 0.1 - 2026-08-16

Akira is het gedeelde geheugen van het atelier. Je praat ertegen, en wat je vertelt
belandt automatisch op de juiste plek: taken bij het juiste project, beslissingen in het
beslissingsregister, ideeën op de parkeerplaats.

Er zijn twee manieren om aan te sluiten. Welke voor jou geldt hangt af van wat je doet,
niet van hoe technisch je bent.

---

# Voor iedereen in het atelier

**Farah, Luna, stagiairs, studenten, nieuwe medewerkers.**

Je hebt nodig: een ChatGPT-account en een link van Tore. Verder niets. Geen GitHub, geen
installatie, geen wachtwoorden om te onthouden.

## Opzetten (twee minuten, één keer)

1. Vraag Tore de link naar **Chatty**.
2. Open die link in ChatGPT. Zet hem bij je favorieten of op je startscherm, zodat je
   hem terugvindt.
3. Zeg wie je bent bij je eerste bericht: *"Hoi, ik ben Luna."* Chatty onthoudt dat
   binnen het gesprek en zet je naam bij alles wat hij vastlegt.

Klaar. Er is geen stap vier.

## Gebruiken

Praat gewoon. Na een gesprek, na een fitting, na een telefoon met een klant. Inspreken
mag ook, dat werkt vaak makkelijker dan typen.

> "Ik heb net met de klant gebeld. De fitting gaat door op donderdag, en zij vroeg of we
> ook accessoires kunnen sourcen. Ik moet daar nog een prijs voor doorgeven."

Je hoeft niets te structureren. Niet nadenken over of iets een taak is of een
beslissing, niet bedenken waar het hoort. Dat is precies het werk dat Chatty doet.

Wat je zegt wordt binnen enkele minuten verwerkt. Je hoeft daar niets voor te doen en
niets van op te volgen.

## Wat je vooral moet weten

**Zeg het gewoon zoals het is.** Half afgemaakte zinnen, twijfels, "ik weet niet meer
precies wanneer" - allemaal prima. Chatty vult niets in wat je niet gezegd hebt. Weet
hij niet wie iets moet doen of wanneer, dan laat hij dat leeg in plaats van te gokken.

**Vertel geen gevoelige klantinformatie.** Maten, privéadressen, privénummers,
gezondheid, contractdetails: die horen niet in Akira. Komen ze toch voorbij, dan laat
Chatty ze eruit en zet er een verwijzing in de plaats. Noem ze liever gewoon niet.

**Je kunt niets stukmaken.** Chatty mag alleen vastleggen. Hij kan geen prijzen
wijzigen, geen bedrijfsafspraken aanpassen en geen bestanden overschrijven. Dat is
technisch afgeschermd, niet alleen afgesproken.

**Zeg het als iets niet klopt.** Vertel het aan Tore. Alles wat Chatty vastlegt is
zichtbaar en terug te draaien.

---

# Voor wie met Claude Code werkt

**Tore, of een latere technische collega.**

Claude Code kan rechtstreeks met de repo praten via GitHub's MCP-server.

1. Maak een fine-grained token aan op
   https://github.com/settings/personal-access-tokens
   - Repository access: alleen `akira`
   - Permissions: **Issues** read and write, **Contents** read-only
   - Geef nooit Contents write
2. Voeg de server toe:

```bash
claude mcp add --transport http akira-captures https://api.githubcopilot.com/mcp/x/issues --header "Authorization: Bearer JOUW_TOKEN"
```

De connectors van claude.ai werken hiervoor **niet**: GitHub's MCP-server ondersteunt
geen automatische client-registratie en claude.ai biedt geen veld voor een header. Zie
`integrations/claude-capture/README.md`.

---

# Voor Tore: wat je één keer opzet

Dit hoeft maar één keer, en daarna is elke nieuwe persoon een kwestie van een link
doorsturen.

| Stap | Wat | Waar |
|---|---|---|
| 1 | Fine-grained token aanmaken (Issues read/write, Contents read-only) | GitHub settings |
| 2 | Custom GPT "Chatty" maken met dat token en de instructies | `integrations/chatgpt-capture/README.md` |
| 3 | GPT delen via link | ChatGPT |
| 4 | `claude setup-token` en bewaren als repo-secret `CLAUDE_CODE_OAUTH_TOKEN` | GitHub repo settings |

Stap 4 is wat de automatische routering laat draaien. Zonder dat secret komen captures
wel binnen als issue, maar worden ze niet verwerkt.

## Iemand nieuw laten aansluiten

Stuur de link naar Chatty en verwijs naar het eerste deel van dit document. Meer is het
niet. Zij hebben geen GitHub-account nodig, staan niet in de organisatie en krijgen geen
enkel recht op de repo.

Dat is bewust: hoe minder mensen rechtstreeks toegang hebben tot het geheugen, hoe
minder er per ongeluk kan gebeuren. Iedereen praat, één token schrijft, de automatisering
routeert.

## Wat je in de gaten houdt

- **Openstaande capture-issues** die niet vanzelf sluiten. Dat betekent dat de routering
  iets niet kon plaatsen; het staat in de comment.
- **De canon-queue.** Voorstellen voor prijzen en werkwijzen wachten daar op akkoord van
  jou en Farah. Dat blijft mensenwerk, met opzet.
- **De wekelijkse review.** Het ritueel dat de rest overeind houdt.
