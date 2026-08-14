---
id: canon-only-via-queue
title: Canon wijzigt alleen via de canon-queue
scope: global
trigger: schrijfactie in knowledge/, policies/, company.yaml of een decision met canon_impact
enforcement: hard
version: 1
updated: 2026-08-14
---

## Rule

AI schrijft NOOIT rechtstreeks in `knowledge/`, `policies/` of `company.yaml`. Elke
voorgestelde wijziging aan bedrijfswaarheid gaat als item naar `{tenant}/canon-queue.md`
en wacht op expliciet menselijk akkoord. Pas na dat akkoord voert de AI de wijziging uit
en zet `approved_by` en `updated`.

## Rationale

Dit is de bewuste verbetering ten opzichte van HQ, waar `/learn` rechtstreeks in het
gedeelde geheugen schrijft zonder goedkeuringspoort. Zonder poort wordt een gedeeld
AI-geheugen na zes maanden een verzameling half-juiste observaties die niemand meer
durft te vertrouwen, en dan valt het hele systeem terug op de hoofden van mensen.

Een prijs, een positionering of een werkwijze is een bedrijfsbeslissing. Die hoort een
mens te nemen. De AI mag hem uitstekend voorbereiden.

## Correct

> Farah: "Volgens mij moeten we red carpet voortaan aan 1400 doen."
>
> AI: Genoteerd als hypothese in `working/learnings/red-carpet-prijsniveau.md` en als
> voorstel in de canon-queue, met de drie projecten die het ondersteunen als evidence.
> De canon staat nog op 1100 tot jullie akkoord geven.

## Incorrect

> Farah: "Volgens mij moeten we red carpet voortaan aan 1400 doen."
>
> AI: *werkt `knowledge/pricing/red-carpet.md` bij naar 1400*

De tweede vorm maakt een losse gedachte tot bedrijfswaarheid. Een week later offreert
het systeem 1400 zonder dat iemand dat besloten heeft.
