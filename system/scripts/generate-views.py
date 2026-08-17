#!/usr/bin/env python3
"""Bouwt de kijklaag: een statische site per rol, uit dezelfde bron als het board.

Waarom statisch en per rol, en niet een app met een login die filtert: GitHub kan geen
deel van een repo verbergen (rechten gelden per repo, nooit per map), en GitHub Pages
publiceert een prive-repo gewoon publiek op alles onder Enterprise Cloud. De enige
scheiding die niet stuk kan is er een die al bij het bouwen gebeurt: de ateliersite bevat
geen bedragen omdat ze er nooit in geschreven zijn. Er is geen filter om te omzeilen en
geen payload waar de data alsnog in zit.

Elke lezing loopt via `akira/toegang.py`, ook lezingen die vanzelfsprekend mogen. Alleen
dan is het leeslogboek compleet, en alleen dan kan `test-geen-lek.py` aantonen dat de rol
`atelier` geen enkele verboden bron heeft aangeraakt.

Gebruik:
    python system/scripts/generate-views.py [uitvoermap]      # standaard: dist/
"""

import glob
import html
import json
import os
import shutil
import sys
from datetime import timedelta

from akira import ROOT, VANDAAG, VEROUDERD_NA, DEADLINE_HORIZON, NU_MAX
from akira.laden import lees_projecten, als_datum, naam, open_taken
from akira.analyse import (
    pct, bereken_dekking, bereken_concentratie, bereken_onbeheerd,
    bereken_ongedateerd, bereken_overdue, bereken_ketens, bereken_prioriteitsdruk,
    bereken_verouderd, taken_per_persoon, beslissingen_open, lees_ritmen,
    tel_open_canon,
)
from akira.toegang import laad_rollen, mensen_per_rol
from akira import markdown as md

# De informatie-architectuur, in de volgorde waarin informatie er doorheen beweegt.
# Dit is de kern van de anti-blackbox-eis: niet "welke knoppen zijn er" maar "welke
# vakjes bestaan er en wat komt waar terecht". De teksten zijn voor iemand die de repo
# nooit gezien heeft en dat ook nooit hoeft.
VAKJES = [
    ("company/inbox", "Wat er binnenkomt",
     "Alles wat je tegen Chatty zegt, ruw en onbewerkt. Hier is nog niets uitgezocht. "
     "Binnen enkele minuten wordt het verdeeld over de vakjes hieronder.", "*.md"),
    ("company/projects/active", "Waar we aan werken",
     "Elk project heeft een status, een volgende stap, een eigenaar en taken. Dit is "
     "waar bijna alles uiteindelijk terechtkomt, en waar het bord op gebaseerd is.",
     "*/project.yaml"),
    ("company/decisions", "Wat we besloten hebben",
     "Genomen beslissingen met de reden erbij. Geen mening en geen plan: iets waar we "
     "ons aan houden tot we het expliciet terugdraaien.", "*/*.md"),
    ("company/working/learnings", "Wat we denken te weten",
     "Observaties over hoe wij werken die zich beginnen te herhalen. Nog geen waarheid. "
     "Wie hieruit citeert, zegt erbij dat het een hypothese is.", "*.md"),
    ("company/knowledge", "Wat vaststaat",
     "Bedrijfswaarheid. Prijzen, werkwijzen, positionering. Hier komt alleen iets in "
     "nadat Tore en Farah het hebben goedgekeurd - een AI kan hier nooit rechtstreeks "
     "in schrijven.", "*/*.md"),
    ("company/ideas", "Wat we ooit willen",
     "De parkeerplaats. Ideeen die geen project zijn en misschien nooit worden.", "*.md"),
    ("company/rituals", "Wat we elke week afspreken",
     "De weekplannen van maandag en de wrap-ups van vrijdag, per week bewaard.", "*/*.md"),
    ("company/people", "Wie er is",
     "Collega's, stagiairs en externe contacten. Observaties worden toegevoegd, nooit "
     "overschreven - wat iemand toen deed blijft nuttig.", "*.yaml"),
    ("company/clients", "Wie onze klanten zijn",
     "Per klant een dossier. Gevoelige gegevens staan hier bewust niet in; die liggen "
     "in de Drive-vault en hier staat alleen een verwijzing.", "*/client.yaml"),
]

CSS = """
:root {
  --bg:#faf9f7; --vlak:#fff; --rand:#e3ded6; --tekst:#22201d; --zacht:#6b655c;
  --accent:#8a5a2b; --alarm:#9c2f2f; --alarm-vlak:#fbf0ef; --ok:#3f6b45;
  --schaduw:0 1px 2px rgba(0,0,0,.05);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg:#171614; --vlak:#211f1c; --rand:#3a3630; --tekst:#ece8e1; --zacht:#a09889;
    --accent:#d09a5e; --alarm:#e08b84; --alarm-vlak:#2e1f1d; --ok:#8fbf97;
    --schaduw:0 1px 2px rgba(0,0,0,.3);
  }
}
:root[data-theme="dark"] {
  --bg:#171614; --vlak:#211f1c; --rand:#3a3630; --tekst:#ece8e1; --zacht:#a09889;
  --accent:#d09a5e; --alarm:#e08b84; --alarm-vlak:#2e1f1d; --ok:#8fbf97;
  --schaduw:0 1px 2px rgba(0,0,0,.3);
}
* { box-sizing:border-box; }
body {
  margin:0; background:var(--bg); color:var(--tekst);
  font:16px/1.6 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
}
.wrap { max-width:60rem; margin:0 auto; padding:1.5rem 1.25rem 5rem; }
header { border-bottom:1px solid var(--rand); margin-bottom:1.75rem; padding-bottom:1rem; }
h1 { font-size:1.6rem; margin:0 0 .3rem; letter-spacing:-.01em; }
h2 { font-size:1.15rem; margin:2.25rem 0 .75rem; letter-spacing:-.01em; }
h3 { font-size:.95rem; margin:1.5rem 0 .5rem; color:var(--zacht);
     text-transform:uppercase; letter-spacing:.06em; }
h4 { font-size:1rem; margin:1.2rem 0 .4rem; }
nav { display:flex; flex-wrap:wrap; gap:.4rem; margin:.85rem 0 0; }
nav a {
  padding:.3rem .7rem; border:1px solid var(--rand); border-radius:99px;
  text-decoration:none; color:var(--zacht); font-size:.85rem; background:var(--vlak);
}
nav a:hover { color:var(--tekst); border-color:var(--accent); }
nav a[aria-current="page"] { color:var(--bg); background:var(--accent); border-color:var(--accent); }
a { color:var(--accent); }
.meta { color:var(--zacht); font-size:.85rem; }
.oud { color:var(--alarm); font-weight:600; }
.kaart {
  background:var(--vlak); border:1px solid var(--rand); border-radius:.6rem;
  padding:1rem 1.1rem; margin:.6rem 0; box-shadow:var(--schaduw);
}
.kaart h4 { margin:0 0 .2rem; font-size:1rem; }
.kaart p { margin:.35rem 0 0; color:var(--zacht); font-size:.92rem; }
.pad { font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.8rem; color:var(--zacht); }
.telling { float:right; font-size:.85rem; color:var(--zacht); }
.afgeschermd { border-style:dashed; opacity:.75; }
.tabelwrap { overflow-x:auto; margin:.5rem 0 1rem; }
table { border-collapse:collapse; width:100%; font-size:.93rem; }
th,td { text-align:left; padding:.5rem .6rem; border-bottom:1px solid var(--rand); vertical-align:top; }
th { color:var(--zacht); font-weight:600; font-size:.8rem;
     text-transform:uppercase; letter-spacing:.05em; }
tr:last-child td { border-bottom:none; }
.waarschuwing {
  background:var(--alarm-vlak); border-left:3px solid var(--alarm);
  padding:.75rem 1rem; margin:1rem 0; border-radius:0 .4rem .4rem 0;
}
.leeg { color:var(--zacht); font-style:italic; }
ul { padding-left:1.15rem; } li { margin:.2rem 0; }
blockquote { margin:.6rem 0; padding-left:.9rem; border-left:3px solid var(--rand);
             color:var(--zacht); }
pre { background:var(--vlak); border:1px solid var(--rand); border-radius:.4rem;
      padding:.7rem .9rem; overflow-x:auto; font-size:.85rem; }
code { font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.88em; }
.label { display:inline-block; padding:.1rem .5rem; border-radius:99px; font-size:.75rem;
         border:1px solid var(--rand); color:var(--zacht); }
.label.canon { color:var(--ok); border-color:var(--ok); }
.label.hypothese { color:var(--accent); border-color:var(--accent); }
footer { margin-top:3rem; padding-top:1rem; border-top:1px solid var(--rand);
         color:var(--zacht); font-size:.82rem; }
"""

# Navigatie per rol. `commercieel.html` bestaat alleen voor administrator - niet
# verborgen met CSS maar simpelweg niet gebouwd, want een pagina die er niet is kan
# niemand opvragen.
NAV_BASIS = [
    ("index.html", "Het bord"),
    ("projecten/index.html", "Projecten"),
    ("mensen/index.html", "Mensen"),
    ("kennis.html", "Wat we weten"),
    ("ontvangst.html", "Wat er binnenkwam"),
    ("kaart.html", "De kaart"),
    ("vragen.html", "Wat kan ik vragen"),
]
NAV_ADMIN_EXTRA = [("commercieel.html", "Commercieel")]


def e(x):
    """HTML-escape. Alles wat uit de yaml komt gaat hierlangs."""
    return html.escape(str(x if x is not None else ""))


def nav_voor(rol):
    return NAV_BASIS + (NAV_ADMIN_EXTRA if rol == "administrator" else [])


def shell(titel, rol, inhoud, actief, diepte=0):
    op = "../" * diepte
    nav = "".join(
        f'<a href="{op}{b}"{" aria-current=\"page\"" if b == actief else ""}>{e(t)}</a>'
        for b, t in nav_voor(rol)
    )
    return f"""<!doctype html>
<html lang="nl"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{e(titel)} - Akira</title>
<style>{CSS}</style>
</head><body><div class="wrap">
<header>
  <h1>{e(titel)}</h1>
  <div class="meta">Haus von FEB &middot; weergave voor <strong>{e(rol)}</strong>
    &middot; bijgewerkt {VANDAAG.isoformat()}</div>
  <nav>{nav}</nav>
</header>
{inhoud}
<footer>
  Gegenereerd uit de Akira-repo op {VANDAAG.isoformat()}. Deze pagina is een weergave,
  geen bron - wijzigen doe je door het tegen Chatty te zeggen.
</footer>
</div></body></html>
"""


def tabel(koppen, rijen, leeg="geen"):
    if not rijen:
        return f'<p class="leeg">{e(leeg)}</p>'
    th = "".join(f"<th>{e(k)}</th>" for k in koppen)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rijen)
    return (f'<div class="tabelwrap"><table><thead><tr>{th}</tr></thead>'
            f"<tbody>{trs}</tbody></table></div>")


def projectlink(p, diepte=0):
    op = "../" * diepte
    return f'<a href="{op}projecten/{e(p["_slug"])}.html">{e(naam(p))}</a>'


# --- pagina: het bord ------------------------------------------------------------

def pagina_bord(projecten, toegang):
    wachtend = [p for p in projecten if p.get("status") in ("waiting", "blocked")]
    lopend = [p for p in projecten if p not in wachtend]
    uit = []

    for prio, kop in (("now", "Nu"), ("next", "Next"), ("later", "Later")):
        groep = [p for p in lopend if p.get("priority") == prio]
        uit.append(f"<h2>{kop}</h2>")
        uit.append(tabel(
            ["Project", "Volgende stap", "Bij wie"],
            [[projectlink(p), e(p.get("next_step") or "-"),
              e(p.get("next_step_owner") or "-")] for p in groep],
            "niets op deze lijst"))

    uit.append("<h2>Wacht op iemand anders</h2>")
    uit.append(tabel(["Project", "Wacht op"],
                     [[projectlink(p), e(p.get("waiting_for") or "onbekend")]
                      for p in wachtend], "niets"))

    deadlines = []
    for p in projecten:
        d = als_datum(p.get("deadline"))
        if d and VANDAAG <= d <= VANDAAG + timedelta(days=DEADLINE_HORIZON):
            deadlines.append((d, p))
    deadlines.sort(key=lambda x: x[0])
    uit.append(f"<h2>Deadlines binnen {DEADLINE_HORIZON} dagen</h2>")
    uit.append(tabel(["Datum", "Over", "Project"],
                     [[d.isoformat(),
                       "vandaag" if (d - VANDAAG).days == 0
                       else f"{(d - VANDAAG).days} dagen", projectlink(p)]
                      for d, p in deadlines], "geen deadline in zicht"))

    uit.append("<h2>Beslissingen die op iemand wachten</h2>")
    uit.append(tabel(["Project", "Waarover"],
                     [[e(pr), e(v)] for pr, v in beslissingen_open(projecten)], "geen"))

    uit.append("<h2>Botsingen en belasting</h2>")
    dekking = bereken_dekking(projecten)
    uit.append("<h3>Dekking</h3>")
    uit.append(tabel(["Veld", "Ingevuld", "Dekking"], [
        ["Taken met een eigenaar", f"{dekking['met_owner']} van {dekking['taken']}",
         pct(dekking['met_owner'], dekking['taken'])],
        ["Taken met een datum", f"{dekking['met_due']} van {dekking['taken']}",
         pct(dekking['met_due'], dekking['taken'])],
        ["Projecten met een deadline",
         f"{dekking['met_deadline']} van {dekking['projecten']}",
         pct(dekking['met_deadline'], dekking['projecten'])],
    ]))
    uit.append('<p class="meta">Staat er hieronder "geen", lees dat dan samen met deze '
               "tabel. Bij een lage dekking betekent een lege lijst eerder "
               '"niet meetbaar" dan "geen probleem".</p>')

    verdeling, over, totaal = bereken_concentratie(projecten)
    uit.append("<h3>Wie is de volgende stap</h3>")
    uit.append("<ul>" + "".join(
        f"<li>{e(w)}: {n} van {totaal} projecten ({pct(n, totaal)})</li>"
        for w, n in verdeling) + "</ul>")
    for w, n in over:
        uit.append(f'<div class="waarschuwing"><strong>{e(w)}</strong> is de volgende stap '
                   f"op {n} van {totaal} projecten ({pct(n, totaal)}). Elk project dat "
                   "vooruit moet, wacht op dezelfde persoon.</div>")

    onbeheerd = bereken_onbeheerd(projecten)
    uit.append("<h3>Taken zonder eigenaar</h3>")
    if onbeheerd:
        uit.append(f"<p>{sum(n for _, n in onbeheerd)} open taken hebben geen naam "
                   "erbij. Dit is de werklijst voor de maandagplanning.</p>")
    uit.append(tabel(["Project", "Taken zonder eigenaar"],
                     [[e(pr), n] for pr, n in onbeheerd], "geen"))

    ongedateerd = bereken_ongedateerd(projecten)
    uit.append("<h3>Taken zonder datum</h3>")
    if ongedateerd:
        uit.append(f"<p>{sum(n for _, n in ongedateerd)} open taken hebben geen datum. "
                   "Zolang dat zo is, valt er niet op te plannen.</p>")
    uit.append(tabel(["Project", "Taken zonder datum"],
                     [[e(pr), n] for pr, n in ongedateerd[:8]], "geen"))

    otaken, odeadlines = bereken_overdue(projecten)
    uit.append("<h3>Over datum heen</h3>")
    uit.append(tabel(["Hoe lang", "Project", "Wat", "Wie"],
                     [[f'<span class="oud">{d} dagen</span>', e(pr), e(t), e(o)]
                      for d, pr, t, o in otaken] +
                     [[f'<span class="oud">{d} dagen</span>', e(pr),
                       "projectdeadline verstreken", "-"] for d, pr in odeadlines],
                     "niets over datum"))

    ketens, fouten, _ = bereken_ketens(projecten)
    uit.append("<h3>Wat waarop wacht</h3>")
    if ketens:
        regels = []
        for doel, afh in ketens:
            wachters = ", ".join(f"{e(s)} (wacht op: {e(u)})" for s, u in afh)
            regels.append(f"<li><strong>{e(doel)}</strong> blokkeert {len(afh)} "
                          f"project{'en' if len(afh) != 1 else ''}: {wachters}</li>")
        uit.append("<ul>" + "".join(regels) + "</ul>")
    else:
        uit.append('<p class="leeg">geen vastgelegde afhankelijkheden</p>')
    if fouten:
        uit.append('<div class="waarschuwing"><strong>Datafouten in de afhankelijkheden:'
                   "</strong><ul>" + "".join(f"<li>{e(f)}</li>" for f in fouten) +
                   "</ul></div>")

    nu, nu_oud = bereken_prioriteitsdruk(projecten)
    uit.append("<h3>Prioriteitsdruk</h3>")
    if len(nu) > NU_MAX:
        uit.append(f'<div class="waarschuwing">{len(nu)} projecten staan op Nu, de '
                   f"drempel is {NU_MAX}. Daarvan zijn er {len(nu_oud)} langer dan "
                   f'{VEROUDERD_NA} dagen niet bijgewerkt: "nu" betekent hier dan weinig '
                   "meer. De vrijdag wrap-up is het moment om die lijst opnieuw te kiezen."
                   "</div>")
    else:
        uit.append(f"<p>{len(nu)} projecten op Nu, drempel {NU_MAX}. "
                   f"Daarvan {len(nu_oud)} verouderd.</p>")

    ritmen = lees_ritmen()
    # Twee lezingen die buiten de gewone toegangsweg omgaan, allebei expliciet gemeld
    # zodat test-geen-lek.py ze ziet. De ritmebestanden mag `atelier` gewoon zien; de
    # canon-queue niet, maar het AANTAL open voorstellen is geen bedrag en geen inhoud.
    for soort, d in ritmen.items():
        if d:
            toegang.noteer_gelezen(f"company/rituals/{d.year}/W-{soort}.md")
    if not toegang.mag("company/canon-queue.md"):
        toegang.noteer_uitzondering(
            "company/canon-queue.md",
            "alleen het aantal open voorstellen wordt getoond, nooit de inhoud - "
            "de voorstellen zelf dragen bedragen")

    uit.append("<h2>Gezondheid</h2>")

    def ritme(d):
        if not d:
            return '<span class="oud">nog nooit gedraaid</span>'
        return f"{d.isoformat()} ({(VANDAAG - d).days} dagen geleden)"

    uit.append(tabel(["Meting", "Stand"], [
        ["Actieve projecten", len(projecten)],
        [f"Projecten niet bijgewerkt in {VEROUDERD_NA} dagen",
         len(bereken_verouderd(projecten))],
        ["Voorstellen die op goedkeuring wachten", tel_open_canon()],
        ["Laatste maandagplanning", ritme(ritmen["maandag"])],
        ["Laatste vrijdag wrap-up", ritme(ritmen["vrijdag"])],
    ]))
    return "\n".join(uit)


# --- pagina's: projecten ---------------------------------------------------------

def pagina_projecten(projecten):
    uit = ["<p>Alle lopende projecten. Klik door voor de taken, de geschiedenis en waar "
           "een project op wacht.</p>"]
    for prio, kop in (("now", "Nu"), ("next", "Next"), ("later", "Later"),
                      (None, "Zonder prioriteit")):
        groep = [p for p in projecten
                 if (p.get("priority") == prio if prio
                     else p.get("priority") not in ("now", "next", "later"))]
        if not groep:
            continue
        uit.append(f"<h2>{kop}</h2>")
        rijen = []
        for p in groep:
            d = als_datum(p.get("updated"))
            oud = d and (VANDAAG - d).days > VEROUDERD_NA
            sinds = (f'<span class="oud">{(VANDAAG - d).days} dagen</span>' if oud
                     else (f"{(VANDAAG - d).days} dagen" if d else "onbekend"))
            rijen.append([projectlink(p, 1), e(p.get("status") or "-"),
                          e(p.get("next_step_owner") or "-"),
                          str(len(open_taken(p))), sinds])
        uit.append(tabel(["Project", "Status", "Volgende stap bij", "Open taken",
                          "Niet bijgewerkt"], rijen))
    return "\n".join(uit)


def pagina_project(p, projecten, toegang):
    uit = []
    d = als_datum(p.get("updated"))
    oud = d and (VANDAAG - d).days > VEROUDERD_NA
    rijen = [
        ["Status", e(p.get("status") or "-")],
        ["Prioriteit", e(p.get("priority") or "-")],
        ["Volgende stap", e(p.get("next_step") or "-")],
        ["Bij wie", e(p.get("next_step_owner") or "-")],
        ["Deadline", e(p.get("deadline") or "geen")],
        ["Bijgewerkt", (f'<span class="oud">{p.get("updated")} - {(VANDAAG - d).days} '
                        f"dagen geleden</span>" if oud else e(p.get("updated") or "-"))],
    ]
    if p.get("client"):
        rijen.append(["Klant", e(p["client"])])
    if p.get("waiting_for"):
        rijen.append(["Wacht op", e(p["waiting_for"])])
    uit.append(tabel(["Veld", "Waarde"], rijen))

    if p.get("commercial"):
        c = p["commercial"]
        uit.append("<h2>Commercieel</h2>")
        uit.append(tabel(["Veld", "Waarde"], [
            ["Status", e(c.get("status") or "-")],
            ["Geoffreerd", e(c.get("quoted") if c.get("quoted") is not None else "-")],
            ["Aanvaard", e(c.get("accepted") if c.get("accepted") is not None else "-")],
        ]))

    taken = p.get("tasks") or []
    uit.append("<h2>Taken</h2>")
    rijen = []
    for t in taken:
        due = als_datum(t.get("due"))
        laat = due and due < VANDAAG and t.get("status") not in ("done", "dropped")
        rijen.append([
            e(t.get("task")),
            e(t.get("owner") or "niemand"),
            (f'<span class="oud">{due.isoformat()} - {(VANDAAG - due).days} dagen over'
             "</span>" if laat else (due.isoformat() if due else "geen datum")),
            e(t.get("status") or "open"),
            "ja" if t.get("needs_decision") else "",
        ])
    uit.append(tabel(["Wat", "Wie", "Wanneer", "Status", "Beslissing nodig"], rijen,
                     "geen taken vastgelegd"))

    if p.get("blocked_by"):
        uit.append("<h2>Wacht op andere projecten</h2>")
        rijen = []
        for b in p["blocked_by"]:
            if isinstance(b, dict):
                rijen.append([e(b.get("project")), e(b.get("until") or "?")])
        uit.append(tabel(["Project", "Tot wanneer"], rijen))

    blokkeert = [q for q in projecten
                 for b in (q.get("blocked_by") or [])
                 if isinstance(b, dict) and b.get("project") == p["_slug"]]
    if blokkeert:
        uit.append("<h2>Dit project blokkeert</h2>")
        uit.append("<ul>" + "".join(f"<li>{projectlink(q, 1)}</li>"
                                    for q in blokkeert) + "</ul>")

    basis = f"company/projects/active/{p['_slug']}"
    for bestand, kop in (("handoff.md", "Waar het nu staat"), ("brief.md", "De opdracht")):
        tekst = _lees_md(toegang, f"{basis}/{bestand}")
        if tekst:
            uit.append(f"<h2>{kop}</h2>")
            uit.append(md.render(tekst))

    journaal = sorted(glob.glob(os.path.join(ROOT, basis, "journal", "*.md")), reverse=True)
    if journaal:
        uit.append("<h2>Geschiedenis</h2>")
        for pad in journaal:
            rel = os.path.relpath(pad, ROOT).replace("\\", "/")
            tekst = _lees_md(toegang, rel)
            if tekst:
                uit.append(f'<div class="kaart">'
                           f'<p class="pad">{e(os.path.basename(pad)[:-3])}</p>'
                           f"{md.render(tekst, kop_niveau=4)}</div>")
    return "\n".join(uit)


def _lees_md(toegang, relpad):
    """Markdown lezen met de toegangsregels toegepast."""
    if not toegang.mag(relpad):
        toegang.geweigerd.append(relpad)
        return None
    pad = os.path.join(ROOT, relpad)
    if not os.path.exists(pad):
        return None
    toegang.gelezen.append(relpad)
    with open(pad, encoding="utf-8") as f:
        return f.read()


# --- pagina's: mensen ------------------------------------------------------------

def _mensen(toegang):
    uit = []
    for pad in sorted(glob.glob(os.path.join(ROOT, "company", "people", "*.yaml"))):
        rel = os.path.relpath(pad, ROOT).replace("\\", "/")
        data = toegang.lees_yaml(rel)
        if data:
            data["_slug"] = data.get("slug") or os.path.basename(pad)[:-5]
            uit.append(data)
    return uit


def pagina_mensen(mensen, projecten):
    intern = [m for m in mensen if m.get("type") == "internal"]
    extern = [m for m in mensen if m.get("type") != "internal"]
    tellingen = taken_per_persoon(projecten)
    uit = ["<h2>Het team</h2>"]
    uit.append(tabel(["Wie", "Rol", "Open taken"], [
        [f'<a href="{e(m["_slug"])}.html">{e(m.get("name"))}</a>',
         e(m.get("role") or "-"), str(tellingen.get(m["_slug"], 0))]
        for m in intern], "niemand vastgelegd"))
    uit.append("<h2>Externe contacten</h2>")
    uit.append(tabel(["Wie", "Rol", "Organisatie"], [
        [f'<a href="{e(m["_slug"])}.html">{e(m.get("name"))}</a>',
         e(m.get("role") or "-"), e(m.get("organization") or "-")]
        for m in extern], "geen"))
    if tellingen.get("niemand toegewezen"):
        uit.append(f'<div class="waarschuwing">'
                   f'{tellingen["niemand toegewezen"]} open taken hebben helemaal geen '
                   "naam erbij. Die staan dus op niemands lijst.</div>")
    return "\n".join(uit)


def pagina_persoon(m, projecten):
    slug = m["_slug"]
    uit = [tabel(["Veld", "Waarde"], [
        ["Rol", e(m.get("role") or "-")],
        ["Organisatie", e(m.get("organization") or "-")],
        ["Intern of extern", e(m.get("type") or "-")],
    ] + ([["Toegang", e(m.get("toegang") or "atelier")]]
         if m.get("type") == "internal" else []))]

    eigenaar_van = [p for p in projecten if p.get("next_step_owner") == slug]
    if eigenaar_van:
        uit.append("<h2>Is de volgende stap op</h2>")
        uit.append(tabel(["Project", "Volgende stap"],
                         [[projectlink(p, 1), e(p.get("next_step") or "-")]
                          for p in eigenaar_van]))

    taken = []
    for p in projecten:
        for t in open_taken(p):
            if t.get("owner") == slug:
                due = als_datum(t.get("due"))
                taken.append((due, p, t))
    taken.sort(key=lambda x: (x[0] is None, x[0] or VANDAAG))
    uit.append("<h2>Open taken</h2>")
    rijen = []
    for due, p, t in taken:
        laat = due and due < VANDAAG
        rijen.append([e(t.get("task")), projectlink(p, 1),
                      (f'<span class="oud">{due.isoformat()} - '
                       f'{(VANDAAG - due).days} dagen over</span>' if laat
                       else (due.isoformat() if due else "geen datum"))])
    uit.append(tabel(["Wat", "Project", "Wanneer"], rijen, "geen open taken"))

    if m.get("notes"):
        uit.append("<h2>Wat we van deze persoon weten</h2>")
        for n in m["notes"]:
            if isinstance(n, dict):
                uit.append(f'<div class="kaart"><p class="pad">{e(n.get("date"))}</p>'
                           f'<p>{e(n.get("text"))}</p></div>')
        uit.append('<p class="meta">Notities worden toegevoegd, nooit overschreven. '
                   "Een observatie van toen blijft nuttig, ook als hij nu niet meer "
                   "klopt - corrigeren doe je door er een nieuwe bij te zetten.</p>")
    return "\n".join(uit)


# --- pagina: wat we weten --------------------------------------------------------

def pagina_kennis(toegang):
    uit = ["<p>Twee soorten kennis, en het verschil is belangrijk. Wat <strong>vaststaat"
           "</strong> is goedgekeurd door Tore en Farah en mag je als waarheid gebruiken. "
           "Wat we <strong>vermoeden</strong> is een observatie die zich begint te "
           "herhalen - noem dat altijd als vermoeden, ook als het waarschijnlijk klopt.</p>"]

    uit.append('<h2><span class="label canon">vastgelegd</span> Wat vaststaat</h2>')
    canon = []
    for pad in sorted(glob.glob(os.path.join(ROOT, "company", "knowledge", "*", "*.md"))):
        rel = os.path.relpath(pad, ROOT).replace("\\", "/")
        tekst = _lees_md(toegang, rel)
        if tekst is None:
            continue
        fm, _ = md.splits_frontmatter(tekst)
        canon.append((os.path.basename(os.path.dirname(pad)),
                      fm.get("title") or os.path.basename(pad)[:-3],
                      md.eerste_alinea(tekst)))
    if canon:
        uit.append(tabel(["Gebied", "Onderwerp", "Waar het over gaat"],
                         [[e(g), f"<strong>{e(t)}</strong>", e(s[:200])]
                          for g, t, s in canon]))
    else:
        uit.append('<p class="leeg">Nog niets vastgelegd.</p>')

    aantal = tel_open_canon()
    if aantal:
        uit.append(f'<div class="waarschuwing">{aantal} voorstellen wachten op '
                   "goedkeuring van Tore en Farah. Tot dat gebeurt zijn het voorstellen, "
                   "geen afspraken - ook als ze redelijk klinken.</div>")

    uit.append('<h2><span class="label hypothese">vermoeden</span> Wat we denken te '
               "weten</h2>")
    learnings = []
    for pad in sorted(glob.glob(os.path.join(ROOT, "company", "working",
                                             "learnings", "*.md"))):
        rel = os.path.relpath(pad, ROOT).replace("\\", "/")
        tekst = _lees_md(toegang, rel)
        if tekst is None:
            continue
        fm, _ = md.splits_frontmatter(tekst)
        learnings.append((fm.get("statement") or os.path.basename(pad)[:-3],
                          fm.get("status") or "hypothese",
                          md.eerste_alinea(tekst)))
    uit.append(tabel(["Observatie", "Stand", "Toelichting"],
                     [[f"<strong>{e(s)}</strong>", e(st), e(t[:200])]
                      for s, st, t in learnings], "nog niets"))

    uit.append("<h2>Wat we besloten hebben</h2>")
    besluiten = []
    for pad in sorted(glob.glob(os.path.join(ROOT, "company", "decisions", "*", "*.md")),
                      reverse=True):
        rel = os.path.relpath(pad, ROOT).replace("\\", "/")
        tekst = _lees_md(toegang, rel)
        if tekst is None:
            continue
        fm, _ = md.splits_frontmatter(tekst)
        besluiten.append((fm.get("date") or "?", fm.get("decision") or
                          os.path.basename(pad)[:-3], fm.get("scope") or "-"))
    uit.append(tabel(["Wanneer", "Wat", "Waarover"],
                     [[e(d), f"<strong>{e(w)}</strong>", e(s)] for d, w, s in besluiten],
                     "nog geen beslissingen vastgelegd"))
    return "\n".join(uit)


# --- pagina: wat er binnenkwam ---------------------------------------------------

def pagina_ontvangst(toegang):
    """Wat er is binnengekomen en wat ermee gebeurd is.

    Voor `atelier` staat hier bewust GEEN ruwe tekst. Transcripten en captures zitten vol
    bedragen, half afgemaakte uitspraken en dingen die iemand nog niet af had. Wat er wel
    staat is dat er iets binnenkwam, wanneer, van wie en waarover - metadata, geen inhoud.
    Dat is precies wat de eis vroeg: begrijpen dat een gesprek wordt opgedeeld, zonder
    het gesprek opnieuw te lezen.
    """
    mag_inhoud = toegang.mag("company/inbox/x.md")
    uit = ["<p>Alles wat iemand vertelt komt hier eerst binnen en wordt daarna verdeeld "
           "over de projecten, beslissingen en ideeen. Dit is dat logboek.</p>"]

    if not mag_inhoud:
        toegang.noteer_uitzondering(
            "company/inbox/",
            "alleen datum, onderwerp en bron uit de bestandsnaam en frontmatter - "
            "nooit de tekst van de capture zelf")
        uit.append('<div class="kaart"><p>Je ziet hier <strong>dat</strong> er iets '
                   "binnenkwam, niet <strong>wat</strong> er precies gezegd is. Ruwe "
                   "gesprekken bevatten bedragen en onaffe gedachten; die blijven bij "
                   "Tore en Farah. Wat eruit voortkwam zie je wel - bij de projecten en "
                   "bij wat we weten.</p></div>")

    rijen = []
    for pad in sorted(glob.glob(os.path.join(ROOT, "company", "inbox", "*.md")),
                      reverse=True):
        naam_ = os.path.basename(pad)[:-3]
        with open(pad, encoding="utf-8") as f:
            fm, rest = md.splits_frontmatter(f.read())
        datum = fm.get("date") or naam_[:10]
        bron = fm.get("source") or "-"
        onderwerp = naam_[11:].replace("-", " ") if len(naam_) > 11 else naam_
        status = fm.get("status") or "-"
        if mag_inhoud:
            rijen.append([e(datum), e(bron), e(onderwerp), e(status),
                          f"{len(rest.split())} woorden"])
        else:
            rijen.append([e(datum), e(bron), e(onderwerp), e(status)])

    koppen = (["Wanneer", "Van wie", "Waarover", "Verwerkt", "Omvang"] if mag_inhoud
              else ["Wanneer", "Van wie", "Waarover", "Verwerkt"])
    uit.append(tabel(koppen, rijen, "nog niets binnengekomen"))
    uit.append('<p class="meta">Staat er bij Verwerkt iets anders dan "routed", dan is '
               "die capture nog niet verdeeld. Dat is het enige wat je in de gaten hoeft "
               "te houden.</p>")
    return "\n".join(uit)


# --- pagina: wat kan ik vragen ---------------------------------------------------

def pagina_vragen(toegang, rol):
    uit = ["<p>Je hoeft niets te onthouden van hoe Akira werkt. Dit is wat je kunt "
           "vragen, in gewone taal. Praten kan tegen Chatty in ChatGPT.</p>",
           "<h2>De vragen die het vaakst nodig zijn</h2>"]
    uit.append(tabel(["Als je dit wilt weten", "Zeg dit"], [
        ["Wat moet ik vandaag doen", '"Wat moet ik vandaag weten?"'],
        ["Waar staat een project", '"Hoe staat het met [project]?"'],
        ["Wat ligt er bij mij", '"Wat staat er op mijn lijst?"'],
        ["Iets vertellen wat er gebeurd is", "Vertel het gewoon. Structureren hoeft niet."],
        ["Wat is er afgesproken over iets", '"Wat weten we over [onderwerp]?"'],
    ]))

    uit.append("<h2>De vaste momenten</h2>")
    skills = []
    for pad in sorted(glob.glob(os.path.join(ROOT, "system", "skills", "*.md"))):
        rel = os.path.relpath(pad, ROOT).replace("\\", "/")
        tekst = _lees_md(toegang, rel)
        if tekst is None:
            continue
        naam_ = os.path.basename(pad)[:-3]
        doel = ""
        if "## Doel" in tekst:
            blok = tekst.split("## Doel", 1)[1].split("##", 1)[0].strip()
            doel = " ".join(blok.split("\n\n")[0].split())
        skills.append((naam_, doel))
    uit.append(tabel(["Moment", "Waar het voor is"],
                     [[f"<strong>{e(n)}</strong>", e(d[:230])] for n, d in skills],
                     "geen werkwijzen gevonden"))

    uit.append("<h2>Wat de rollen betekenen</h2>")
    rollen = laad_rollen()
    wie = mensen_per_rol()
    uit.append(tabel(["Rol", "Wat die betekent", "Wie"], [
        [f"<strong>{e(r)}</strong>" + (" &larr; jij" if r == rol else ""),
         e(t.betekent), e(", ".join(wie.get(r, [])) or "-")]
        for r, t in rollen.items()]))
    uit.append('<p class="meta">Stagiairs en tijdelijke medewerkers krijgen de rol '
               "atelier via hun e-mailadres, zonder eigen bestand.</p>")

    uit.append("<h2>Wat Akira nooit doet</h2>")
    uit.append("<ul>"
               "<li>Een prijs verzinnen. Staat een bedrag nergens vast, dan zegt hij dat.</li>"
               "<li>Zelf beslissen dat iets bedrijfsafspraak is. Dat doen Tore en Farah.</li>"
               "<li>Gevoelige klantgegevens opslaan - maten, priveadressen, contracten. "
               "Die horen hier niet en worden eruit gehaald.</li>"
               "<li>Invullen wat jij niet gezegd hebt. Weet hij niet wie of wanneer, dan "
               "blijft het leeg in plaats van een gok.</li>"
               "</ul>")
    return "\n".join(uit)


# --- pagina: commercieel (alleen administrator) ----------------------------------

def pagina_commercieel(projecten, toegang):
    uit = ['<div class="kaart"><p>Deze pagina bestaat alleen in de '
           "administrator-weergave. Ze wordt niet gebouwd voor de ateliersite, dus er is "
           "geen versie van die site waarin deze bedragen verborgen zitten - ze staan er "
           "domweg niet in.</p></div>"]

    rijen = []
    for p in projecten:
        c = p.get("commercial") or {}
        if not c:
            continue
        rijen.append([projectlink(p), e(c.get("status") or "-"),
                      e(c.get("quoted") if c.get("quoted") is not None else "-"),
                      e(c.get("accepted") if c.get("accepted") is not None else "-"),
                      e(p.get("client") or "-")])
    uit.append("<h2>Per project</h2>")
    uit.append(tabel(["Project", "Stand", "Geoffreerd", "Aanvaard", "Klant"], rijen,
                     "geen enkel project draagt commerciele gegevens"))

    met = [r for r in rijen if r[2] != "-" or r[3] != "-"]
    uit.append(f'<p class="meta">{len(met)} van {len(projecten)} projecten dragen een '
               "bedrag. Bij een lage dekking zegt een overzicht als dit weinig over hoe "
               "het bedrijf ervoor staat.</p>")

    uit.append("<h2>Voorstellen die op jullie wachten</h2>")
    tekst = _lees_md(toegang, "company/canon-queue.md")
    if tekst:
        open_deel = tekst.split("## Afgehandeld")[0]
        uit.append(md.render(open_deel.split("## Openstaand", 1)[-1]))
    else:
        uit.append('<p class="leeg">canon-queue niet leesbaar</p>')

    uit.append("<h2>Prijzen die vastliggen</h2>")
    prijzen = sorted(glob.glob(os.path.join(ROOT, "company", "knowledge",
                                            "pricing", "*.md")))
    if prijzen:
        for pad in prijzen:
            rel = os.path.relpath(pad, ROOT).replace("\\", "/")
            t = _lees_md(toegang, rel)
            if t:
                uit.append(f'<div class="kaart">{md.render(t, kop_niveau=4)}</div>')
    else:
        uit.append('<p class="leeg">Er staat nog geen enkele prijs in de canon. Elke '
                   "vraag over wat iets kost wordt daarom beantwoord met \"dat ligt niet "
                   "vast\".</p>")
    return "\n".join(uit)


# --- bouwen ----------------------------------------------------------------------

def schrijf(map_, bestand, titel, rol, inhoud, diepte=0):
    pad = os.path.join(map_, bestand)
    os.makedirs(os.path.dirname(pad), exist_ok=True)
    with open(pad, "w", encoding="utf-8", newline="\n") as f:
        f.write(shell(titel, rol, inhoud, bestand, diepte))


def bouw(rol, toegang, uitvoer):
    map_ = os.path.join(uitvoer, rol)
    os.makedirs(map_, exist_ok=True)

    projecten = []
    for p in lees_projecten():
        if not toegang.noteer_gelezen(p["_pad"]):
            continue
        projecten.append(toegang.strip_velden("project.yaml", p))
    toegang.noteer_gelezen("company/BOARD.md")
    mensen = _mensen(toegang)

    schrijf(map_, "index.html", "Het bord", rol, pagina_bord(projecten, toegang))
    schrijf(map_, "kaart.html", "De kaart", rol, pagina_kaart(toegang))
    schrijf(map_, "kennis.html", "Wat we weten", rol, pagina_kennis(toegang))
    schrijf(map_, "ontvangst.html", "Wat er binnenkwam", rol, pagina_ontvangst(toegang))
    schrijf(map_, "vragen.html", "Wat kan ik vragen", rol, pagina_vragen(toegang, rol))

    schrijf(map_, "projecten/index.html", "Projecten", rol,
            pagina_projecten(projecten), diepte=1)
    for p in projecten:
        schrijf(map_, f"projecten/{p['_slug']}.html", naam(p), rol,
                pagina_project(p, projecten, toegang), diepte=1)

    schrijf(map_, "mensen/index.html", "Mensen", rol,
            pagina_mensen(mensen, projecten), diepte=1)
    for m in mensen:
        schrijf(map_, f"mensen/{m['_slug']}.html", m.get("name") or m["_slug"], rol,
                pagina_persoon(m, projecten), diepte=1)

    if rol == "administrator":
        schrijf(map_, "commercieel.html", "Commercieel", rol,
                pagina_commercieel(projecten, toegang))

    return {"rol": rol, "projecten": len(projecten), "mensen": len(mensen),
            "gelezen": sorted(set(toegang.gelezen)),
            "geweigerd": sorted(set(toegang.geweigerd)),
            "uitzonderingen": toegang.uitzonderingen}


def pagina_kaart(toegang):
    """De informatie-architectuur, leesbaar voor wie de repo nooit zag.

    Afgeschermde vakjes worden WEL getoond, met de melding dat de inhoud niet voor deze
    rol is. Ze weglaten zou een tweede blackbox maken: je kunt niet begrijpen hoe
    informatie stroomt als een deel van de stroom onzichtbaar is. Segmentatie waarvan je
    het bestaan kent, is geen geheim systeem maar een afspraak.
    """
    uit = ["<p>Alles wat je tegen Akira zegt wordt verdeeld over een vast aantal vakjes. "
           "Dit is dat rijtje. Wie weet welke vakjes er zijn, weet ook wat hij kan "
           "vragen.</p>",
           '<div class="kaart"><h4>Wat er gebeurt als je iets vertelt</h4>'
           "<p>Je praat tegen Chatty &rarr; het komt ruw binnen bij "
           "<em>Wat er binnenkomt</em> &rarr; binnen enkele minuten wordt het verdeeld "
           "over de juiste vakjes hieronder &rarr; raakt het prijzen of werkwijzen, dan "
           "wordt het een <em>voorstel</em> en beslissen Tore en Farah of het "
           "bedrijfswaarheid wordt.</p></div>",
           "<h2>De vakjes</h2>"]

    for pad, kop, wat, patroon in VAKJES:
        proef = f"{pad}/{patroon.replace('*/', 'x/').replace('*', 'x')}"
        zichtbaar = toegang.mag(proef)
        aantal = len(glob.glob(os.path.join(ROOT, pad, patroon)))
        if zichtbaar:
            telling = f"{aantal} {'item' if aantal == 1 else 'items'}"
            klasse, extra = "kaart", ""
        else:
            telling = "niet voor jouw rol"
            klasse = "kaart afgeschermd"
            extra = ("<p><em>Dit vakje bestaat wel, maar de inhoud is voor de "
                     "zaakvoerders. Je weet dus dat het er is, en aan wie je het kunt "
                     "vragen.</em></p>")
        uit.append(f'<div class="{klasse}"><span class="telling">{e(telling)}</span>'
                   f'<h4>{e(kop)}</h4><p>{e(wat)}</p>{extra}'
                   f'<p class="pad">{e(pad)}/</p></div>')

    uit.append("<h2>De drie regels waar dit op rust</h2>")
    uit.append(tabel(["Regel", "Wat het betekent"], [
        ["Ruw &rarr; vermoeden &rarr; waarheid",
         "Niets wordt bedrijfswaarheid zonder dat een mens ja zegt. Een AI mag "
         "vastleggen en voorstellen, nooit vaststellen."],
        ["Wie het mag zien, staat vast",
         "Wat jouw rol betekent staat bij <em>Wat kan ik vragen</em>. Het is geen "
         "instelling van het moment maar een afspraak die in de repo staat."],
        ["Overzichten zijn altijd gemaakt, nooit getypt",
         "Deze pagina's worden gegenereerd uit de projectbestanden. Klopt er iets niet, "
         "dan klopt de bron niet - en die repareer je door het te zeggen."],
    ]))
    return "\n".join(uit)


def main():
    uitvoer = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "dist")
    if os.path.isdir(uitvoer):
        shutil.rmtree(uitvoer)
    os.makedirs(os.path.join(uitvoer, "_logs"), exist_ok=True)

    for rol, toegang in laad_rollen().items():
        log = bouw(rol, toegang, uitvoer)
        with open(os.path.join(uitvoer, "_logs", f"{rol}.json"), "w",
                  encoding="utf-8", newline="\n") as f:
            json.dump(log, f, indent=2, ensure_ascii=False)
        print(f"{rol}: {log['projecten']} projecten, {log['mensen']} mensen, "
              f"{len(log['gelezen'])} bronnen gelezen, "
              f"{len(log['geweigerd'])} geweigerd")


if __name__ == "__main__":
    main()
