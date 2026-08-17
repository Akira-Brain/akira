"""Een kleine markdown-renderer, genoeg voor de bestanden in deze repo.

Waarom zelf en niet een bibliotheek: de enige afhankelijkheid van dit project is PyYAML,
en die staat al in beide workflows. Een tweede pakket toevoegen voor koppen en lijstjes
maakt de bouw fragieler dan de winst rechtvaardigt. De bestanden hier zijn kort en
geschreven door ons, dus de vormen die voorkomen zijn te overzien: koppen, lijsten, vet,
code, citaten, tabellen en alinea's.

Wat er NIET in zit: geneste lijsten, afbeeldingen, voetnoten, HTML-doorvoer. Kom je die
tegen in de uitvoer als platte tekst, dan is dat het signaal om die vorm hier toe te
voegen - niet om er een bibliotheek bij te halen.

Alle invoer wordt ge-escaped voordat er opmaak op wordt losgelaten. De teksten komen uit
de repo en niet van buiten, maar een capture bevat wat iemand heeft ingesproken, en dat
is invoer als alle andere.
"""

import html
import re

_VET = re.compile(r"\*\*(.+?)\*\*")
_CURSIEF = re.compile(r"(?<![\*\w])\*([^\*]+?)\*(?!\*)")
_CODE = re.compile(r"`([^`]+?)`")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _inline(tekst):
    t = html.escape(tekst)
    t = _CODE.sub(r"<code>\1</code>", t)
    t = _VET.sub(r"<strong>\1</strong>", t)
    t = _CURSIEF.sub(r"<em>\1</em>", t)
    t = _LINK.sub(r"\1", t)   # linkdoelen zijn repo-paden; als tekst nuttiger dan als link
    return t


def splits_frontmatter(tekst):
    """Geeft (frontmatter-dict-als-ruwe-regels, rest). Geen yaml-parser nodig."""
    if not tekst.startswith("---"):
        return {}, tekst
    einde = tekst.find("\n---", 3)
    if einde == -1:
        return {}, tekst
    kop, rest = tekst[3:einde], tekst[einde + 4:]
    velden = {}
    for regel in kop.splitlines():
        if ":" in regel and not regel.strip().startswith("#"):
            k, _, v = regel.partition(":")
            velden[k.strip()] = v.strip().strip('"').strip("'")
    return velden, rest.lstrip("\n")


def render(tekst, kop_niveau=3):
    """Markdown naar HTML. `kop_niveau` is het niveau dat `#` krijgt."""
    uit, in_lijst, in_code, in_tabel = [], False, False, False

    def sluit():
        nonlocal in_lijst, in_tabel
        if in_lijst:
            uit.append("</ul>")
            in_lijst = False
        if in_tabel:
            uit.append("</tbody></table></div>")
            in_tabel = False

    for regel in tekst.splitlines():
        kaal = regel.strip()

        if kaal.startswith("```"):
            sluit()
            uit.append("</pre>" if in_code else "<pre>")
            in_code = not in_code
            continue
        if in_code:
            uit.append(html.escape(regel))
            continue

        if not kaal:
            sluit()
            continue

        if kaal.startswith("#"):
            sluit()
            n = len(kaal) - len(kaal.lstrip("#"))
            niveau = min(kop_niveau + n - 1, 6)
            uit.append(f"<h{niveau}>{_inline(kaal.lstrip('# ').strip())}</h{niveau}>")
            continue

        if kaal.startswith(("- ", "* ")):
            if in_tabel:
                sluit()
            if not in_lijst:
                uit.append("<ul>")
                in_lijst = True
            uit.append(f"<li>{_inline(kaal[2:])}</li>")
            continue

        if kaal.startswith(">"):
            sluit()
            uit.append(f"<blockquote>{_inline(kaal.lstrip('> '))}</blockquote>")
            continue

        if kaal.startswith("|") and kaal.endswith("|"):
            cellen = [c.strip() for c in kaal.strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cellen):
                continue   # de scheidingsregel onder de koppen
            if not in_tabel:
                if in_lijst:
                    sluit()
                uit.append('<div class="tabelwrap"><table><tbody>')
                in_tabel = True
                uit.append("<tr>" + "".join(f"<th>{_inline(c)}</th>" for c in cellen) + "</tr>")
            else:
                uit.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in cellen) + "</tr>")
            continue

        if set(kaal) <= set("-") and len(kaal) >= 3:
            sluit()
            uit.append("<hr>")
            continue

        sluit()
        uit.append(f"<p>{_inline(kaal)}</p>")

    sluit()
    if in_code:
        uit.append("</pre>")
    return "\n".join(uit)


def eerste_alinea(tekst):
    """De eerste echte alinea, voor samenvattingen in een lijst."""
    _, rest = splits_frontmatter(tekst)
    for blok in rest.split("\n\n"):
        kaal = blok.strip()
        if kaal and not kaal.startswith(("#", "|", "-", ">", "```")):
            return " ".join(kaal.split())
    return ""
