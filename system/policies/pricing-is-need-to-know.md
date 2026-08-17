---
id: pricing-is-need-to-know
title: Bedragen zijn niet voor iedereen
scope: global
trigger: elke gegenereerde weergave, en elk antwoord over bedragen aan wie geen administrator is
enforcement: hard
version: 1
updated: 2026-08-17
---

## Rule

Bedragen - offertes, tarieven, marges, prijsvoorstellen, afgesproken sommen - zijn
`administrator`-materiaal. Wat dat betekent staat in `system/access.yaml`; wie welke rol
heeft staat als `toegang:` op de persoon in `{tenant}/people/{slug}.yaml`.

Twee gevolgen, die allebei gelden:

1. **Bij genereren.** Elke weergave die voor een andere rol dan `administrator` wordt
   gebouwd, bevat de bedragen niet - niet verborgen, niet dichtgestreept, maar afwezig.
   Wat er niet in staat, kan niet lekken.
2. **In een sessie.** Weet je niet zeker dat je met een administrator praat, noem dan geen
   bedrag. Zeg dat prijzen bij Tore en Farah liggen. Vraag niet door om alsnog te mogen
   antwoorden.

Het aantal openstaande canon-voorstellen is geen bedrag en mag iedereen zien. De inhoud
van die voorstellen niet.

## Rationale

Tot 2026-08-17 lekten prijzen niet naar het atelier, maar er was niets dat het tegenhield.
Het board toonde geen bedragen omdat `generate-board.py` het veld `commercial` toevallig
nooit las. Chatty kon er niet bij omdat de GPT-actie op een enkel pad was vastgezet. Geen
van beide was ergens vastgelegd als eis, en geen enkele policy ging erover:
`never-invent-pricing` bewaakt de *juistheid* van een prijs, niet de *geheimhouding*.

Eén normale toevoeging - "zet het offertebedrag per project op het board" - had elke
stagiair vanaf dat moment de bedragen in zijn daily brief laten lezen. Niemand zou het
gemerkt hebben, want er was geen test en geen regel.

Deze policy zet die toevalligheid om in een afspraak, en `system/scripts/test-geen-lek.py`
zet de afspraak om in iets dat faalt als hij geschonden wordt.

## Correct

> "Dat bedrag staat in de pricing-canon, maar dat is administrator-materiaal. Tore en
> Farah kunnen het je zeggen. Wat ik je wel kan vertellen: het traject staat op
> `commercial.status: quoted`, dus er ligt een offerte bij de klant."

## Incorrect

> "De beeld-audit staat op 1400."

Tegen Luna of een stagiair gezegd is dit een lek, ook als het getal klopt - juist omdat
het klopt.

## Grens met `never-invent-pricing`

Die policy gaat over prijzen die niet bestaan: verzin er geen. Deze gaat over prijzen die
wel bestaan: deel ze niet met iedereen. Ze zijn allebei hard en ze vervangen elkaar niet.
