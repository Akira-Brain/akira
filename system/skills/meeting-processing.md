# Skill: meeting-processing

Versie 0.2 - 2026-08-16. Herschreven na de eerste echte toepassing op zes historische
vergadertranscripten; wat hieronder staat is geteste praktijk, niet alleen ontwerp.

## Twee heel verschillende soorten input - en waarom dat uitmaakt

**Korte capture** ("ik heb net met Luna gesproken..."): een paar zinnen, een handvol
signalen. Dit gaat via Chatty, wordt een GitHub issue met label `capture`, en wordt
volledig automatisch en goedkoop verwerkt door de workflow
`.github/workflows/capture-intake.yml` (Haiku, dertig turns, een paar cent per stuk).
Niemand hoeft hiervoor iets te doen.

**Vol vergadertranscript** (bijvoorbeeld een Plaud-opname van een strategiesessie, vaak
duizend-plus regels): dit gaat NIET via die automatische route. Twee harde redenen:

1. **Oordeel.** Een lang transcript vraagt beslissingen die een goedkoop model met een
   turnlimiet niet betrouwbaar kan nemen: is dit een nieuw project of hoort het bij een
   bestaand project, is deze passage gevoelig genoeg om weg te laten, is dit een
   uitgesproken beslissing of hardop denken, is dit canon-waardig of een losse gedachte.
2. **Grootte.** GitHub-issues hebben een harde limiet van 65.536 tekens. Van de vier
   transcripten die als eerste test gebruikt zijn, waren er drie groter dan dat (de
   grootste: 75.090 tekens) - het zou de belangrijkste vergadering van de hele batch
   (de Groen-sessie, die tot de beeldcreatie/stijlcreatie-herpositionering leidde)
   gewoon stil hebben laten falen als hij als issue was binnengekomen.

Om die reden verwerkt een **mens samen met Claude in een live sessie** een vol
transcript, niet een onbewaakte Action. Concreet: open een Claude Code-sessie (zoals
deze) met toegang tot de repo, of een andere sessie waarvan bevestigd is dat hij
bestanden kan lezen en schrijven en kan committen. Plak het transcript, en vraag om het
volgens deze skill te verwerken. Dit gebruikt het Claude-abonnement, geen API-kosten.

**Praktisch, met Plaud:** neem de vergadering op zoals gewoonlijk, exporteer het
transcript als tekst (.txt of .docx, ook op de gratis Plaud-laag beschikbaar), en plak
dat in de sessie. Een volledig automatische keten (Plaud stuurt rechtstreeks door naar
GitHub) is bewust niet gebouwd: dat vraagt Plaud's betaalde AutoFlow/Zapier-laag, en
zou zonder eerst het tekenlimiet-probleem op te lossen alsnog stuklopen op lange
vergaderingen. Dit is voorlopig een bewuste, kleine handeling per vergadering.

## Signaaltypes

| Signaal | Herkennen aan | Bestemming |
|---|---|---|
| taak | iemand gaat iets doen | `tasks:` in project.yaml, met owner en due |
| beslissing | een keuze is gemaakt | `decisions/{jaar}/` + canon-queue als canon geraakt wordt |
| projectupdate | status is veranderd | journal-entry + status/next_step in project.yaml |
| learning-kandidaat | een patroon of observatie over hoe wij werken | `working/learnings/`, status hypothesis |
| idee | iets nieuws dat nog geen project is | `ideas/`, status good-ideas tenzij anders gezegd |
| open vraag | iets is onbeslist | `waiting_for` of taak met needs_decision |
| afspraak / follow-up | er is iets toegezegd aan iemand | taak met due |

## Stappen voor een kort capture

1. Schrijf het capture-blok volgens `system/templates/capture.md` naar
   `{tenant}/inbox/{datum}-{slug}.md`. Doe dit **eerst**, voordat je routeert.
2. Geef de ruwe tekst weer onder `## Ruw`. Kort niet in bij korte captures.
3. Classificeer onder `## Signalen`, route onder `## Routering`.
4. Zet het capture-bestand op `status: routed` zodra alles geland is.

## Stappen voor een vol vergadertranscript

1. **Lees het hele transcript voordat je iets schrijft.** Een half gelezen transcript
   leidt tot gemiste context - een terloopse opmerking op regel 200 verklaart soms een
   beslissing op regel 900.
2. **Een capture-bestand per vergadering**, niet per signaal. De `## Ruw`-sectie is bij
   een lang transcript een **grondige, thematisch geordende prozasamenvatting met
   citaten waar relevant** - geen woordelijke kopie van het hele transcript. Doel: iemand
   die niet aanwezig was, moet de vergadering kunnen begrijpen uit deze samenvatting
   alleen. Verwijs naar het bronbestand (bestandsnaam, aantal regels) zodat het volledige
   transcript terug te vinden is als er ooit twijfel is.
3. **Een vergadering mag meerdere, echt losstaande projecten opleveren.** Maak gerust
   meerdere nieuwe projecten aan als de inhoud dat rechtvaardigt. Vermijd wel het
   omgekeerde: gooi geen ongerelateerde onderwerpen in één project omdat ze in dezelfde
   vergadering ter sprake kwamen.
4. **Canon gaat altijd naar de queue, nooit direct naar `knowledge/`.** Schrijf een
   voorstel in `company/canon-queue.md`, in het bestaande format (V-nummer, bestand,
   huidig/voorstel, rationale, evidence, "nodig: akkoord van Tore en Farah"). Dit geldt
   ongeacht hoe overtuigend of vaak herhaald de uitspraak in het transcript was. Hoe
   zwaarder de mogelijke impact (bijvoorbeeld: hoe het bedrijf zichzelf noemt, een
   volledige herpositionering), hoe explicieter je dat gewicht benoemt in het voorstel -
   zodat Tore en Farah niet per ongeluk iets grote in een paar seconden wegklikken.
5. **Wees eerlijk over verlopen tijd.** Transcripten zijn vaak weken tot maanden oud.
   Een actiepunt met een deadline die al voorbij is, wordt geen taak die "nog moet
   gebeuren" maar een `next_step` die vraagt om een statuscheck: "bevestigen wat hiermee
   gebeurd is." Verzin nooit een uitkomst; vraag ernaar.
6. **Laat gevoelige informatie over derden weg of houd het strikt zakelijk.**
   Gezondheids-, familie- of privésituaties van klanten, prospects of anderen horen hier
   niet integraal in, ook niet als ze letterlijk zo in het transcript staan. Vermeld aan
   het eind van de `## Ruw`-sectie kort en zonder details wat is weggelaten.
7. **Bij een naderende turn- of tijdslimiet: eerst redden, dan verfijnen.** Volgorde van
   prioriteit als het krap wordt: (1) het capture-bestand met de volledige samenvatting
   opslaan, (2) canon-relevante punten in de queue zetten, (3) pas daarna projecten,
   taken en mensen verder uitwerken. Een bewaarde samenvatting die nog niet volledig
   gerouteerd is, is behouden werk; een verloren transcript is dat niet.
8. **Regenereer BOARD.md met het script** (`python system/scripts/generate-board.py`),
   niet met de hand - zie de reden in `system/scripts/generate-board.py` zelf.
9. Commit met een duidelijke boodschap en push. Er is geen automatische stap die dit
   voor je doet bij een vol transcript.

## Kwaliteitsregels (gelden voor beide vormen)

- **Twijfel blijft in de inbox.** Wat je niet zeker kunt routeren, laat je staan als
  open item. Fout gerouteerd is erger dan niet gerouteerd.
- **Verzin geen owners, deadlines of prijzen.** Staat het er niet, laat het leeg en
  noem het als open punt.
- **Een beslissing is pas een beslissing als iemand hem nam.** "We zouden eigenlijk
  moeten..." is een idee of hypothese, geen beslissing.
- **Een prijs- of positioneringsuitspraak is nooit automatisch canon**, hoe vaak of hoe
  stellig ook herhaald in het transcript.

## Policies die gelden

canon-only-via-queue, hypothesis-is-not-canon, sensitive-data-to-vault,
never-invent-pricing, client-isolation.
