# Skill: client-kickoff

Versie 0.1 - 2026-08-17. Ontworpen, nog niet op een echte opdracht toegepast.

## Doel

Een klantopdracht van "we praten erover" naar "iedereen weet wat hij deze week doet"
brengen. Twee momenten, bewust niet samengevouwen omdat ze verschillende vragen
beantwoorden:

- **Modus A, voor de deal:** kunnen en willen we dit, wat kost het ons werkelijk, en waar
  ligt onze ondergrens in de onderhandeling.
- **Modus B, na de deal:** wat zijn de deliverables, en wat betekent dat voor vandaag en
  morgen.

## Input

Modus A: de aanvraag, plus de analyse die er al ligt. Modus B: de afgesproken scope en
prijs.

**Grens met `inquiry-analysis`.** Die skill is de solo-bureaupas op een binnenkomende
aanvraag: wat wordt er gevraagd, wat weten we nog niet, wat deden vergelijkbare opdrachten,
wat zegt de pricing-canon. Deze skill is de **vergadering die daarop volgt**, met Farah en
Luna erbij. Modus A stap 1 is daarom: is `inquiry-analysis` al gedraaid? Zo nee, draai die
eerst. Herhaal de uitkomst hier niet - verwijs ernaar en begin bij de lijst "wat we nog
niet weten".

**Ruwe signalen eruit halen doe je niet hier.** Volg `system/skills/meeting-processing.md`,
sectie "Stappen voor een vol vergadertranscript", stap 1 tot en met 3 en 6.

## Stappen - modus A, voor de deal

1. Check dat `inquiry-analysis` gedraaid is. Zo niet, eerst dat.
2. **Deliverables uitschrijven** zoals wij ze zouden leveren, met een ruwe omvang in
   dagdelen per stuk. Ruw is genoeg; dit is geen schatting die ergens wordt vastgelegd.
3. **Expliciet uitschrijven wat we niet leveren.** Dit is de sectie die later ruzie
   voorkomt, en de sectie die het makkelijkst wordt overgeslagen.
4. **Workload per persoon**, met de kolom "botst met" gevuld uit `## Botsingen en
   belasting` op het board. Dit is de enige plek in het systeem waar conflictdetectie wordt
   gebruikt *voordat* er werk is toegezegd - daarna is het alleen nog constateren.
5. **Onderhandelpunten**, met per punt: onze inzet, waar we stoppen, en wie het voert.
   Bedragen komen uit de pricing-canon of uit een eerdere offerte. Is er geen canonwaarde,
   dan staat er "geen canon" en gaat er een voorstel naar `canon-queue.md` - je verzint hier
   geen prijs.
6. **Risico's**, met de learnings uit `working/` er expliciet bij als hypothese, niet als
   feit.
7. **Beslissing:** doorgaan, afwijzen, of eerst deze vragen stellen.

## Stappen - modus B, na de deal

1. **Deliverables met een einddatum per stuk.**
2. **Terugrekenen.** Per deliverable een ladder terug in de tijd: wat moet er af zijn
   voordat dit af kan zijn, en wanneer. Dit is de kern van deze modus - je werkt van de
   einddatum naar vandaag, niet andersom.
3. **`project.yaml` volledig invullen:** `commercial.status` naar `won`, `deadline`,
   `client`, `people`, en de volledige `tasks`-lijst met owner en due uit de ladder.
4. **Wat we nog niet weten** wordt `waiting_for` of een taak met `needs_decision: true`.
   Hangt het project op een ander project, dan `blocked_by` met de stap erbij.
5. **Vandaag en morgen** als aparte sectie. Wie doet wat, deze week nog.
6. Board regenereren, committen.

## Outputvorm

Modus A:

```markdown
# Kick-off A - {klant} - scoping, 2026-08-17

Aanwezig: tore, farah, luna
Basis: analyse van 2026-08-14 (inbox/2026-08-14-aanvraag-{klant}.md)

## Wat we leveren als dit doorgaat
- Beeld-audit collectie - farah - 2 dagdelen
- Shoot met 4 silhouetten - farah + luna - 3 dagdelen

## Wat we niet leveren
- Postproductie en social publishing - dat blijft bij de klant
- Copywriting - buiten scope, wel afstemming

## Workload
| Wie | Dagdelen | Botst met |
|---|---|---|
| farah | 4 | W36: staat al op merkenpitch-focus |
| luna | 3 | niets in die week |

## Onderhandelpunten
| Punt | Onze inzet | Waar we stoppen | Wie voert dit |
|---|---|---|---|
| Beeld-audit vooraf | verplicht in het traject | niet weglaten | tore |
| Aantal silhouetten | 4 | 3, niet minder | farah |

## Risico's
- Sourcing wordt bij eerste opdrachten structureel onderschat (hypothese,
  working/learnings/, nog niet bevestigd)

## Beslissing
Doorgaan, mits de beeld-audit in scope blijft.
```

Modus B:

```markdown
# Kick-off B - {klant} - alignment, 2026-08-24

## Deliverables en einddatum
- Campagnebeelden opgeleverd - 2026-09-20

## Terugrekenen
Campagnebeelden klaar 2026-09-20
  <- shoot 2026-09-15 (farah, luna)
    <- sourcing af 2026-09-10 (luna)
      <- moodboard goedgekeurd door klant 2026-09-03 (farah)
        <- moodboard af 2026-08-28 (tore)

## Vandaag en morgen
- tore: moodboard-richting kiezen - vandaag
- luna: leveranciers aanschrijven - morgen

## Wat naar project.yaml gaat
deadline: 2026-09-20, commercial.status: won, client: {slug}
tasks: vier taken uit de ladder hierboven, met owner en due

## Afhankelijkheden
Geen.
```

## Bekende zwakte

De dagdelen in modus A worden nergens vastgelegd en dus ook nooit teruggemeten. Dat is
bewust - een effortveld dat niemand bijhoudt maakt berekeningen die er gezaghebbend
uitzien en het niet zijn. Het gevolg is wel dat "4 dagdelen" een gevoel blijft en geen
cijfer dat over een jaar te toetsen is. Wil je dat ooit toetsen, dan is de weg: de
werkelijke duur bij oplevering noteren in het journal, niet een schattingsveld toevoegen.

## Policies die gelden

never-invent-pricing, canon-only-via-queue, hypothesis-is-not-canon, client-isolation,
sensitive-data-to-vault, boards-are-generated.
