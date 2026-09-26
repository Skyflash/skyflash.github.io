"""Genera il CV in PDF a partire dai dati del sito.

Due versioni dallo stesso template:
  - pubblica  -> static/assets/cv/CV_Cristian_Castellari.pdf (solo città, niente dati personali)
  - recruiter -> static/assets/cv/CV_Cristian_Castellari_completo.pdf (indirizzo, telefono,
                 data di nascita e consenso privacy da private.yml; PDF e yml ignorati da git)

Esperienze e competenze arrivano da _data/index/; il resto da tools/cv/cv.yml.
Il PDF viene stampato con Microsoft Edge in modalità headless.

Uso:  python tools/cv/build.py
Richiede: PyYAML (pip install pyyaml) e Microsoft Edge.
"""

import datetime
import html
import re
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "out"
PUBLIC_PDF = ROOT / "static" / "assets" / "cv" / "CV_Cristian_Castellari.pdf"
# Nella stessa cartella per comodità, ma ignorato da git: il repo è pubblico
RECRUITER_PDF = PUBLIC_PDF.with_name("CV_Cristian_Castellari_completo.pdf")

MONTHS_LONG = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
               "agosto", "settembre", "ottobre", "novembre", "dicembre"]

# Icone Material Design (Apache 2.0), solo il path SVG
ICONS = {
    "place": "M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z",
    "home": "M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z",
    "phone": "M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z",
    "mail": "M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z",
    "event": "M17 12h-5v5h5v-5zM16 1v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-1V1h-2zm3 18H5V8h14v11z",
    "link": "M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z",
    "person": "M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z",
}


def e(text):
    return html.escape(str(text), quote=True)


def icon(name):
    return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="{ICONS[name]}"/></svg>'


def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def short_date(text):
    """'Gennaio 2022 - Presente' -> 'gen 2022 - Presente' (stile del vecchio CV)."""
    return " ".join(w.lower()[:3] if w.lower() in MONTHS_LONG else w for w in str(text).split())


def contact(ico, label, lines, href=None):
    # <wbr> dopo gli slash: gli URL lunghi vanno a capo lì e non a metà parola
    body = "<br>".join(e(line).replace("/", "/<wbr>") for line in lines)
    if href:
        body = f'<a href="{e(href)}">{body}</a>'
    return (f'<div class="contact">{icon(ico)}<div><div class="contact__label">{e(label)}</div>'
            f'<div class="contact__value">{body}</div></div></div>')


def timeline(items, cls=""):
    rows = []
    for it in items:
        desc = f'<p class="tl__desc">{e(it["desc"])}</p>' if it.get("desc") else ""
        org = f'<div class="tl__org">{e(it["org"])}</div>' if it.get("org") else ""
        rows.append(
            f'<div class="tl__item"><div class="tl__date">{e(it["date"])}</div>'
            f'<div class="tl__body"><div class="tl__title">{e(it["title"])}</div>{org}{desc}</div></div>'
        )
    return f'<div class="tl {cls}">{"".join(rows)}</div>'


def section(title, content, cls=""):
    return f'<section class="sec {cls}"><h2 class="sec__title">{e(title)}</h2>{content}</section>'


def render(cv, careers, skills, private):
    photo = (ROOT / cv["photo"]).as_uri()
    fonts = (HERE / "fonts").as_uri()

    # Colonna laterale
    side = [f'<img class="photo" src="{photo}" alt="">', '<h3 class="side__title">Contatti</h3>']
    if private:
        side.append(contact("home", "Indirizzo", private["address"]))
        side.append(contact("phone", "Telefono", [private["phone"]]))
    else:
        side.append(contact("place", "Città", [cv["city"]]))
    side.append(contact("mail", "E-mail", [cv["email"]], f'mailto:{cv["email"]}'))
    if private:
        side.append(contact("event", "Data di nascita", [private["birth_date"]]))
    side.append(contact("link", "Sito web", [cv["website"].replace("https://", "")], cv["website"]))
    side.append(contact("person", "LinkedIn", [cv["linkedin"].replace("www.", "")], f'https://{cv["linkedin"]}'))

    side.append('<h3 class="side__title">Lingue</h3>')
    for lang in cv["languages"]:
        level = f'<span class="lang__level">{e(lang["level"])}</span>' if lang.get("level") else ""
        side.append(f'<div class="lang"><span>{e(lang["name"])}</span>{level}</div>')

    # Certificazioni nella colonna laterale: sotto le lingue la prima pagina ha spazio libero
    side.append('<h3 class="side__title">Certificazioni</h3>')
    for c in cv["certifications"]:
        side.append(f'<div class="cert"><div class="cert__name">{e(c["name"])}</div>'
                    f'<div class="cert__meta">{e(c["org"])} · {e(c["date"])}</div></div>')

    # Colonna principale
    jobs = [{
        "date": short_date(c["date"]["it"]),
        "title": c["job"]["it"],
        "org": c["name"]["it"],
        "desc": cv.get("career_desc", {}).get(c["job"]["it"], c["desc"]["it"]),
    } for c in careers]

    # Etichette invece delle barre del sito: le percentuali restano solo online
    skill_groups = []
    for cat in skills["categories"]:
        tags = "".join(f'<span class="tag">{e(s["name"]["it"])}</span>' for s in cat["skills"])
        skill_groups.append(f'<div class="skills__group"><h3>{e(cat["name"]["it"])}</h3><div class="tags">{tags}</div></div>')

    profile = "".join(
        f'<p class="pf"><span class="pf__title">{e(x["title"])}.</span> {e(x["text"])}</p>'
        for x in cv.get("profile_sections", []))
    if cv.get("profile_closing"):
        profile += f'<p class="pf">{e(cv["profile_closing"])}</p>'

    def cards(items, cls=""):
        rows = []
        for p in items:
            if "inline" in cls:
                # Progetti personali: nome cliccabile e descrizione, tutto su una riga
                name = f'<a href="{e(p["url"])}">{e(p["name"])}</a>' if p.get("url") else e(p["name"])
                rows.append(f'<div class="proj"><span class="proj__name">{name}</span>'
                            f'<p class="proj__desc">{e(p["desc"])}</p></div>')
                continue
            # Una riga a tutta larghezza: nome, poi ente/data/link sulla stessa riga, sotto la descrizione
            url = p.get("url", "")
            meta = [e(x) for x in (p.get("org"), p.get("date")) if x]
            if url:
                meta.append(f'<a href="{e(url)}">{e(url.replace("https://", ""))}</a>')
            rows.append(
                f'<div class="proj"><div><span class="proj__name">{e(p["name"])}</span>'
                + (f'<span class="proj__meta"> · {" · ".join(meta)}</span>' if meta else "") + '</div>'
                f'<p class="proj__desc">{e(p["desc"])}</p></div>'
            )
        return f'<div class="projs {cls}">{"".join(rows)}</div>'

    main = [
        f'<header class="head"><h1>{e(cv["name"])}</h1><div class="head__role">{e(cv["title"])}</div>'
        f'<div class="head__sub">{e(cv.get("subtitle", ""))}</div>'
        f'<p class="head__profile">{e(cv["profile"])}</p>{profile}</header>',
        section("Esperienza professionale", timeline(jobs)),
        section("Competenze", f'<div class="skills">{"".join(skill_groups)}</div>'),
        section("Progetti principali", cards(cv["projects"])),
        section("Progetti personali e open source", cards(cv["personal_projects"], "projs--inline")),
        section("Corsi", '<div class="courses">' + "".join(
            f'<div class="course"><span class="course__date">{e(c["date"])}</span>'
            f'<span><span class="course__name">{e(c["name"])}</span> · <span class="course__org">{e(c["org"])}</span></span></div>'
            for c in cv["courses"]) + '</div>'
            + (f'<p class="courses__older"><strong>Corsi precedenti:</strong> {e(cv["courses_older"])}</p>'
               if cv.get("courses_older") else "")),
    ]
    today = datetime.date.today()
    updated = f"CV aggiornato a {MONTHS_LONG[today.month - 1]} {today.year}."
    footer = f'<p class="updated">{updated}</p>'
    # Nota in fondo alla colonna blu di pagina 2, che è vuota: consenso privacy per i recruiter,
    # invito a chiedere i recapiti completi nella versione pubblica. Presuppone 2 pagine (vedi README).
    if private:
        footer += f'<p class="side-note">{e(private["privacy"])}</p>'
    elif cv.get("public_note"):
        # Trattino non separabile (U+2011): "e-mail" non va a capo a metà
        note = e(cv["public_note"]).replace("-", chr(0x2011))
        footer += f'<p class="side-note side-note--short">{note}</p>'
    main.append(footer)

    css = (HERE / "cv.css").read_text(encoding="utf-8").replace("{{FONTS}}", fonts)
    return f"""<!doctype html>
<html lang="it"><head><meta charset="utf-8">
<title>CV {e(cv["name"])}</title>
<style>{css}</style></head>
<body><div class="strip"></div>
<aside class="side">{"".join(side)}</aside>
<main class="main">{"".join(main)}</main>
</body></html>"""


def find_edge():
    candidates = [
        shutil.which("msedge"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    sys.exit("Microsoft Edge non trovato")


def to_pdf(edge, html_path, pdf_path):
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    pdf_path.unlink(missing_ok=True)
    # Profilo dedicato: senza, Edge può agganciarsi a un'istanza già aperta e uscire subito
    subprocess.run([
        edge, "--headless", "--disable-gpu", "--no-pdf-header-footer", "--no-first-run",
        f"--user-data-dir={OUT / '.edge-profile'}",
        f"--print-to-pdf={pdf_path}", html_path.as_uri(),
    ], check=True, capture_output=True)
    # msedge.exe può restituire subito il controllo e scrivere il PDF in background:
    # aspetta che il file compaia e che la dimensione smetta di cambiare
    size, deadline = -1, time.monotonic() + 60
    while time.monotonic() < deadline:
        if pdf_path.exists() and pdf_path.stat().st_size == size and size > 0:
            break
        size = pdf_path.stat().st_size if pdf_path.exists() else -1
        time.sleep(0.5)
    else:
        sys.exit(f"Edge non ha generato {pdf_path}")
    print(f"  {pdf_path.relative_to(ROOT)}")


def main():
    cv = load(HERE / "cv.yml")
    careers = load(ROOT / "_data" / "index" / "careers.yml")
    skills = load(ROOT / "_data" / "index" / "skills.yml")
    private_path = HERE / "private.yml"
    private = load(private_path) if private_path.exists() else None

    OUT.mkdir(exist_ok=True)
    edge = find_edge()
    print("PDF generati:")

    public_html = OUT / "cv-pubblico.html"
    public_html.write_text(render(cv, careers, skills, None), encoding="utf-8")
    to_pdf(edge, public_html, PUBLIC_PDF)

    if private:
        recruiter_html = OUT / "cv-recruiter.html"
        recruiter_html.write_text(render(cv, careers, skills, private), encoding="utf-8")
        to_pdf(edge, recruiter_html, RECRUITER_PDF)
    else:
        print("  (versione recruiter saltata: manca tools/cv/private.yml)")


if __name__ == "__main__":
    main()
