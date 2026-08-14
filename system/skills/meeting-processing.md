# Skill: meeting-processing

Versie 0.1 - 2026-08-14

## Doel

Een spraakdump of transcript omzetten in geclassificeerde signalen met een
routeringsvoorstel. De spreker heeft nul structuurplicht: die vertelt gewoon wat er
gebeurd is. De classificatie is AI-werk.

## Input

Transcript, spraakdump of losse notities. Plus, indien bekend: wie sprak, wanneer,
met wie, over welk project.

## Signaaltypes

Het vocabulaire (geleend van HQ's signal-types, aangepast naar het atelier):

| Signaal | Herkennen aan | Bestemming |
|---|---|---|
| taak | iemand gaat iets doen | `tasks:` in project.yaml, met owner en due |
| beslissing | een keuze is gemaakt | `decisions/{jaar}/` + canon-queue als canon geraakt wordt |
| projectupdate | status is veranderd | journal-entry + status/next_step in project.yaml |
| learning-kandidaat | een patroon of observatie over hoe wij werken | `working/learnings/`, status hypothesis |
| idee | iets nieuws dat nog geen project is | `ideas/`, status good-ideas tenzij anders gezegd |
| open vraag | iets is onbeslist | `waiting_for` of taak met needs_decision |
| afspraak / follow-up | er is iets toegezegd aan iemand | taak met due |

## Stappen

1. Schrijf het capture-blok volgens `system/templates/capture.md` naar
   `{tenant}/inbox/{datum}-{slug}.md`. Doe dit **eerst**, voordat je routeert. De ruwe
   input mag nooit verloren gaan doordat de routering misgaat.
2. Geef de ruwe tekst weer onder `## Ruw`. Kort niet in, vat niet samen. Wel:
   vervang gevoelige inhoud door een vault-verwijzing en meld dat expliciet.
3. Classificeer onder `## Signalen`. Per signaal: type, inhoud, en de velden die het
   bestemmingsschema vraagt (owner, due, project, scope).
4. Stel de routering voor onder `## Routering`. Per signaal: waar het heen gaat.
   Noem apart wat je niet zeker weet.
5. Vraag om bevestiging bij twijfelgevallen, en voer daarna de routering uit.
6. Zet het capture-bestand op `status: routed` zodra alles geland is. Blijft er iets
   over, dan blijft de status `open` en komt het terug in de weekly review.

## Kwaliteitsregels

- **Twijfel blijft in de inbox.** Wat je niet zeker kunt routeren, laat je staan als
  open item. Fout gerouteerd is erger dan niet gerouteerd: een taak bij de verkeerde
  persoon verdwijnt stil, een open capture-item komt terug.
- **Verzin geen owners of deadlines.** Zei de spreker niet wie of wanneer, laat het
  veld dan leeg en noem het als open punt.
- **Een beslissing is pas een beslissing als iemand hem nam.** "We zouden eigenlijk
  moeten..." is een idee of hypothese, geen beslissing.
- **Een prijsuitspraak is nooit automatisch canon.** "Volgens mij moeten we dit
  voortaan aan 1400 doen" wordt een hypothese plus een canon-queue-voorstel, nooit
  een directe wijziging in `knowledge/pricing/`.

## Policies die gelden

canon-only-via-queue, hypothesis-is-not-canon, sensitive-data-to-vault,
never-invent-pricing, client-isolation.
