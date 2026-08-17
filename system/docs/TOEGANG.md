# TOEGANG - wie ziet wat, en hoe je dat verandert

Versie 0.1 - 2026-08-17

Dit is de enige plek waar staat hoe toegang werkt. Wat een rol *betekent* staat in
`system/access.yaml`; wie welke rol *heeft* staat als `toegang:` op de persoon in
`company/people/{slug}.yaml`. Dit document legt uit hoe die twee samenwerken en wat je
moet doen als er iemand bij komt of weggaat.

## Wat de rollen betekenen

| Rol | Wat die betekent |
|---|---|
| **Administrator** | Alles: bedragen, offertes, prijsvoorstellen, ruwe transcripten, en wie toegang heeft |
| **Atelier** | De volledige projectrealiteit - projecten, taken, mensen, klanten, kennis en weekplannen. Geen bedragen |

Administrator zijn Tore en Farah. Atelier is Luna, en iedereen die tijdelijk meewerkt.

Deze tabel staat ook op de site zelf, bij *Wat kan ik vragen*. Dat is opzet: wie niet kan
opzoeken wat zijn eigen rol inhoudt, zit alsnog in een blackbox.

## De drie deuren

| | GitHub-repo | Ateliersite | Administratorsite |
|---|---|---|---|
| Tore | Admin | ja | ja |
| Farah | Read | ja | ja |
| Luna | geen | ja | nee |
| Stagiairs en studenten | geen | ja | nee |

Luna en stagiairs krijgen geen GitHub-account. Dat is niet uit zuinigheid maar
noodzakelijk: de repo bevat prijzen, en GitHub kan die niet per map verbergen. Wie
leesrecht op de repo heeft, leest alles.

Schrijven doet niemand rechtstreeks. Iedereen praat tegen Chatty, en de automatische
routering schrijft. De sites zijn alleen om te lezen.

## Waarom het zo gebouwd is

Twee harde feiten bepalen de vorm, en het loont om ze te kennen voordat je iets wijzigt.

**GitHub kent geen rechten per map.** Rechten gelden per repo, als geheel. Er is geen
instelling die `company/knowledge/pricing/` verbergt voor iemand die de repo mag lezen.
CODEOWNERS en rulesets sturen alleen wie iets mag *wijzigen*, nooit wie het mag *zien*.

**GitHub Pages publiceert een private repo gewoon publiek.** Uit hun eigen documentatie:

> "GitHub Pages sites are publicly available on the internet, even if the repository for
> the site is private."

Privé publiceren bestaat alleen op Enterprise Cloud - niet op Free, niet op Pro, niet op
Team. Er komt geen waarschuwing en geen bevestigingsvraag. **Zet GitHub Pages niet aan op
deze repo.** Doe je het toch, dan staat alles wat je publiceert op een raadbare URL op het
open internet.

Daarom gebeurt de scheiding bij het bouwen. De ateliersite bevat geen bedragen omdat ze er
nooit in geschreven zijn. Er is geen filter dat je kunt omzeilen en geen verborgen data in
de pagina.

## Iemand toevoegen

**Een stagiair of tijdelijke medewerker.** Twee handelingen, geen bestand nodig.

1. Voeg het e-mailadres toe aan de Access-policy van `akira-atelier` in Cloudflare.
2. Stuur de link naar Chatty en verwijs naar `ONBOARDING.md`.

**Iemand die blijft.** Maak daarnaast `company/people/{slug}.yaml` aan met
`type: internal` en `toegang: atelier`. Dan verschijnt die persoon op de site, met zijn
taken en zijn openstaande werk.

**Iemand die bedragen mag zien.** Zet `toegang: administrator` op zijn persoonsbestand en
voeg het e-mailadres toe aan de Access-policy van `akira-administrator`. Beide zijn nodig:
het bestand bepaalt wat er voor die rol gebouwd wordt, Cloudflare bepaalt wie erbij kan.

## Iemand verwijderen

Haal het e-mailadres uit de Access-policy. Dat is de handeling die telt - vanaf dat moment
komt die persoon er niet meer in. Het persoonsbestand laat je staan: wat iemand deed en wat
er over hem is opgeschreven blijft nuttig, ook als hij weg is. Zet `type: external` als hij
buiten het atelier verder werkt.

Vergeet niet dat iemand die de ateliersite ooit heeft gezien, gezien heeft wat er toen op
stond. Toegang intrekken werkt vooruit, niet terug.

## Een derde rol maken

Kan, kost een blok in `system/access.yaml` plus `toegang:` op de betrokken mensen. Doe het
pas als er een echt verschil is in wat iemand nodig heeft. Een rol die hetzelfde ziet als
een bestaande rol is dezelfde rol met twee namen.

Het referentiesysteem waar dit op geïnspireerd is had zeven rollen, maar die gingen over
*handelingen* - inchecken, items aanmaken, reserveren. Hier kan een rol alleen over *zien*
gaan, omdat schrijven bij iedereen via Chatty loopt. Zeven kijkrollen voor vijf mensen is
zes keer hetzelfde opschrijven.

## Wat Tore eenmalig opzet

1. Cloudflare-account, en twee Pages-projecten: `akira-atelier` en `akira-administrator`.
2. In Zero Trust een Access-applicatie per project. Kies **one-time PIN** als
   inlogmethode: dan hoeft niemand een account te maken, er komt een code per mail.
   **Let op:** sinds 2026 staat one-time PIN niet meer automatisch aan voor nieuwe
   organisaties. Zet hem expliciet aan bij de instellingen van de inlogmethodes.
3. Access-policy per site: `akira-atelier` krijgt alle vijf de adressen,
   `akira-administrator` alleen die van Tore en Farah.
4. Twee repo-secrets in GitHub: `CLOUDFLARE_API_TOKEN` en `CLOUDFLARE_ACCOUNT_ID`.

De gratis tier van Cloudflare Zero Trust dekt 50 gebruikers. Met vijf mensen zit je daar
ruim onder, en er is geen betaalgegeven nodig.

Tokens maak je zelf aan. Plak ze nooit in een AI-gesprek, ook niet in dit project.

## Wat de bescherming afdwingt

`system/scripts/test-geen-lek.py` draait bij elke publicatie en doet vier controles:

1. Heeft de generator een bron aangeraakt die voor die rol verboden is?
2. Staat er een bedragpatroon in de HTML?
3. Staat een van de bedragen die op dit moment écht in `commercial` staan, letterlijk in
   de ateliersite? Dit vangt kale getallen zonder euroteken, die de patronen missen.
4. Kan de test überhaupt nog iets vinden, of test hij lucht?

Faalt een van de vier, dan wordt er niets gepubliceerd - ook de administratorsite niet.

**Zet deze test nooit uit om een publicatie door te laten.** Tot 17 augustus 2026 lekten
prijzen niet, maar alleen bij toeval: het boardscript las het veld `commercial` nergens.
Er was geen regel en geen test. Eén normale toevoeging had elke stagiair de bedragen laten
lezen zonder dat iemand het merkte. Deze test is wat dat toeval vervangt.

## Waar het niet over gaat

Toegang tot de Drive-vault staat hier los van. Gevoelige klantgegevens - maten,
privéadressen, contracten - horen niet in de repo en staan er ook niet in; er staat alleen
een verwijzing. Wie bij die documenten mag, regel je in Drive.
