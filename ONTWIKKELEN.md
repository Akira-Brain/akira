# Ontwikkelen aan Akira

Versie 0.1 - 2026-08-20

Voor wie aan het systeem zelf werkt (Tore, of een AI-sessie namens hem) - niet voor het
dagelijkse gebruik. Dagelijks gebruik staat in `ONBOARDING.md`, de AI-charter in
`AGENTS.md`, de navigatie in `system/docs/INDEX.md`.

## Op een nieuwe machine beginnen

Alles wat je nodig hebt om lokaal te werken zit in deze repo. Er zijn geen geheimen nodig
om te bewerken of te genereren - die leven server-side (zie onderaan).

```bash
git clone https://github.com/Akira-Brain/akira.git
cd akira
python -m pip install pyyaml     # de enige afhankelijkheid
```

Python 3.10 of nieuwer. Verder niets: geen node, geen venv verplicht, geen build.

## De lokale lus

Drie scripts, in deze volgorde. Ze lezen `company/` en schrijven gegenereerde views.

```bash
python system/scripts/generate-board.py 0     # bouwt company/BOARD.md
python system/scripts/generate-views.py        # bouwt dist/atelier + dist/administrator
python system/scripts/test-geen-lek.py         # faalt als er een bedrag in de ateliersite staat
```

- `generate-board.py` neemt het aantal open captures als argument; lokaal geeft `0` een
  schone run. In CI komt dat getal uit `gh issue list`.
- `dist/` is gitignored - het is een bouwproduct, nooit een commit. De publicatie naar
  Cloudflare gebeurt in `.github/workflows/publish-views.yml`, niet lokaal.
- `BOARD.md` is datumgevoelig: draai je het script op een andere dag, dan veranderen de
  "X dagen"-tellers en de datumstempel. Dat is geen echte wijziging in de data. Commit een
  geregenereerde BOARD.md alleen als er ook een databron veranderde; anders `git checkout --
  company/BOARD.md`.

## Wijzigingen controleren voor je commit

```bash
# alle YAML valideert
python -c "import glob,yaml; [list(yaml.safe_load_all(open(p,encoding='utf-8'))) for p in glob.glob('**/*.yaml',recursive=True) if '/dist/' not in p]"

# de leaktest slaagt (dit is de poort die ook in CI staat)
python system/scripts/generate-views.py && python system/scripts/test-geen-lek.py
```

Raak je `generate-board.py` of de gedeelde laag in `system/scripts/akira/` aan, controleer
dan dat `BOARD.md` byte-identiek blijft tenzij je de vorm bewust wijzigt - vijf plekken en
Chatty lezen dat bestand (zie de docstring bovenin het script).

## Waar de geheimen leven (en waarom je ze lokaal niet nodig hebt)

Niets gevoeligs staat in de repo. Om te bewerken of te genereren heb je geen enkel token
nodig. De tokens bestaan alleen waar de automatisering draait:

| Geheim | Waar | Waarvoor |
|---|---|---|
| `ANTHROPIC_API_KEY` | GitHub repo secrets | de capture- en meeting-workflows |
| `MEETINGS_INBOX_TOKEN` | GitHub repo secrets | ophalen uit de losse meetings-inbox-repo |
| `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` | GitHub repo secrets | publiceren naar Cloudflare Pages |
| Fine-grained PAT | in de Custom GPT "Chatty" | captures als issue aanmaken |

GitHub Actions-secrets zijn server-side en overleven een nieuwe kloon vanzelf - je hoeft ze
op de laptop niet opnieuw te zetten. Maak je ooit een token opnieuw aan, doe dat in de
GitHub- of Cloudflare-instellingen en plak het nergens in een AI-gesprek. Zie
`system/docs/TOEGANG.md` voor het volledige verhaal.

## Waar de stand van zaken staat

- **Wat er net gebouwd is**: de kijklaag en de toegangslaag (rollen, twee gescheiden sites,
  de leaktest). De laatste commits vertellen het waarom - de berichten zijn uitvoerig.
- **Wat er nog moet**: `reports/2026-08-20-foundation-audit.md`. Dat is een audit tegen de
  Foundation Kit met tien bevindingen (F1-F10), gerangschikt. De goedkoopste eerst: een
  spend-cap op de Anthropic-API (F1), de 2FA-keuze opschrijven als risico (F2), en een
  minimale eval-set voor de onbewaakte AI (F4).
- **Bewust gepauzeerd**: de Plaud-automatisering (twee setup-stappen), en het leeggooien van
  de 17 modelgegenereerde projecten - dat wacht tot het atelier live gaat.

## Wat NIET in de repo staat en je elders vindt

- De ontwerpdossiers (Fase 1 HQ-reverse-engineering, Fase 2 architectuur) en de
  oorspronkelijke projectbriefing leven buiten de repo, op Tore's schijf. Audit-bevinding F5
  stelt voor de dragende beslissingen alsnog als ADR in `docs/decisions/` vast te leggen.
- Claude Code's eigen geheugen en plan-bestanden zijn per-machine en reizen niet mee met de
  kloon. De inhoud ervan zit grotendeels al in de commitgeschiedenis.
