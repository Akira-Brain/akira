---
id: sensitive-data-to-vault
title: Gevoelige data gaat naar de vault, nooit in de repo
scope: global
trigger: schrijfactie waarbij persoonsgegevens, contracten of financiele details voorkomen
enforcement: hard
version: 1
updated: 2026-08-14
---

## Rule

Deze categorieen komen nooit in de repo:

- persoonsgegevens van klanten voorbij de naam van een zakelijke contactpersoon: maten,
  priveadressen, privenummers, gezondheids- of familiecontext
- contracten en ondertekende documenten
- gedetailleerde financiele administratie
- credentials, API-keys, tokens
- alles onder NDA waarvan de NDA opslag elders verbiedt

Kom je zulke inhoud tegen in een capture, vervang die dan door een vault-verwijzing en
meld de vervanging expliciet in het capture-bestand. Bij klanten met `sensitivity: high`
staat in de repo alleen de slug en de initialen.

## Rationale

Git vergeet niet. Eenmaal gecommitte gevoelige data verwijderen vereist het herschrijven
van de historie op elke kloon, en dan nog blijft het risico dat er ergens een kopie
staat. Voorkomen is de enige werkende strategie.

Daarbij: spraakcaptures bevatten van nature namen en details. Dit is het meest
waarschijnlijke pad waarlangs gevoelige informatie hier ongemerkt binnenkomt.

## Correct

> `## Ruw`
> "...en haar maten heb ik doorgekregen, die staan in de vault-map van de klant."
>
> *(AI-notitie: maten uit deze capture verwijderd en vervangen door een verwijzing naar
> `clients/selah-sue/` vault.)*

## Incorrect

> `## Ruw`
> "...en haar maten zijn 86-64-90, ze woont in de Lange Leemstraat."

Deze regel staat vanaf nu permanent in de git-historie.
