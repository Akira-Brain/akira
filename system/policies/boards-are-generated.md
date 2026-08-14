---
id: boards-are-generated
title: Boards en overzichten zijn gegenereerde views
scope: global
trigger: lezen of schrijven van BOARD.md of enig overzichtsbestand
enforcement: hard
version: 1
updated: 2026-08-14
---

## Rule

`BOARD.md` en elk ander overzicht worden altijd gegenereerd uit de `project.yaml`'s.
Bewerk ze nooit met de hand. Beantwoord een statusvraag altijd uit de yaml-bestanden,
niet uit BOARD.md: die kan verouderd zijn. Wijzig je een project, regenereer dan het
board voordat je de sessie afsluit.

## Rationale

Dubbele administratie is de dood van elk systeem. Twee plekken die hetzelfde beweren
betekent dat er altijd een verouderd is, en zodra iemand een keer een verkeerd
antwoord krijgt, vertrouwt niemand het overzicht nog. Dat is precies hoe de eerdere
Notion- en Asana-pogingen zijn doodgebloed.

Een gegenereerde view kan nooit uit de pas lopen met de bron, want hij heeft geen eigen
inhoud.

## Correct

> Vraag: "Wat staat er op waiting?"
> AI leest alle project.yaml's, filtert op `status: waiting`, antwoordt, en regenereert
> BOARD.md als er iets veranderd is.

## Incorrect

> AI leest BOARD.md, antwoordt daaruit, en werkt vervolgens BOARD.md handmatig bij met
> een nieuw item zonder de project.yaml aan te raken.

Nu bestaat er een taak die alleen op het board staat. Bij de volgende regeneratie is hij
weg.
