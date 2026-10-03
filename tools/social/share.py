"""Prepara la condivisione di un post su LinkedIn, Facebook e Threads.

Niente API e niente token: per ogni social copia il testo negli appunti e apre
la finestra di condivisione nel browser, già compilata dove il social lo
permette. Si controlla, si incolla dove serve e si pubblica a mano.

  - LinkedIn: testo e link già compilati
  - Threads:  testo e link già compilati (massimo 500 caratteri)
  - Facebook: solo il link; il testo si incolla dagli appunti

Il testo viene dal front matter del post:

  social: "Un testo per tutti i social"

oppure, per scriverne uno diverso per social (quelli mancanti usano `default`):

  social:
    default: "Testo per LinkedIn e Facebook"
    threads: "Versione corta per Threads"

Senza `social:` si usa `intro`. Il link al post viene aggiunto in fondo.

Uso:  python tools/social/share.py [post.md] [--lang it|en] [--only linkedin,threads] [--force]
Senza percorso prende il post più recente nella lingua scelta (predefinita: it).
Richiede: PyYAML (pip install pyyaml).
"""

import argparse
import datetime
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
NETWORKS = ["linkedin", "facebook", "threads"]
THREADS_MAX = 500


def site_url():
    config = yaml.safe_load((ROOT / "_config.yml").read_text(encoding="utf-8"))
    return (config["url"] + (config.get("baseurl") or "")).rstrip("/")


def read_front_matter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"---\s*\n(.*?)\n---", text, re.S)
    if not match:
        sys.exit(f"{path}: front matter non trovato")
    return yaml.safe_load(match.group(1))


def latest_post(lang):
    today = datetime.date.today().isoformat()
    # Il nome del file inizia con la data: l'ordine alfabetico è quello cronologico.
    # I post datati nel futuro non sono ancora online, quindi si saltano.
    posts = [p for p in sorted((ROOT / "_posts" / lang).glob("*.md")) if p.name[:10] <= today]
    if not posts:
        sys.exit(f"Nessun post in _posts/{lang}/")
    return posts[-1]


def post_url(path, fm):
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
    return site_url() + fm["permalink"].replace(":title", slug)


def texts(fm):
    social = fm.get("social") or fm.get("intro") or fm["title"]
    if isinstance(social, str):
        social = {"default": social}
    default = social.get("default") or fm.get("intro") or fm["title"]
    return {n: social.get(n, default).strip() for n in NETWORKS}


def is_live(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=15) as r:
            return r.status == 200
    except (urllib.error.URLError, TimeoutError):
        return False


def copy_to_clipboard(text):
    # clip.exe legge UTF-16 senza rovinare accenti e trattini lunghi (niente BOM, finirebbe incollato)
    subprocess.run(["clip"], input=text.encode("utf-16-le"), check=True)


def share_url(network, text, url):
    q = urllib.parse.quote
    if network == "linkedin":
        return f"https://www.linkedin.com/feed/?shareActive=true&text={q(text + chr(10) + chr(10) + url)}"
    if network == "facebook":
        return f"https://www.facebook.com/sharer/sharer.php?u={q(url)}"
    return f"https://www.threads.net/intent/post?text={q(text)}&url={q(url)}"


def main():
    parser = argparse.ArgumentParser(description="Condivide un post su LinkedIn, Facebook e Threads.")
    parser.add_argument("post", nargs="?", type=Path, help="file del post (predefinito: il più recente)")
    parser.add_argument("--lang", default="it", choices=["it", "en"])
    parser.add_argument("--only", help="elenco separato da virgole, es. linkedin,threads")
    parser.add_argument("--force", action="store_true", help="non controllare che il post sia online")
    args = parser.parse_args()

    path = (args.post or latest_post(args.lang)).resolve()
    fm = read_front_matter(path)
    url = post_url(path, fm)
    networks = args.only.split(",") if args.only else NETWORKS
    for n in networks:
        if n not in NETWORKS:
            sys.exit(f"Social sconosciuto: {n} (validi: {', '.join(NETWORKS)})")

    print(f"Post: {fm['title']}\n      {url}\n")

    # Un link condiviso prima che il post sia online resta in cache con l'anteprima
    # sbagliata (o con un 404) per giorni, soprattutto su Facebook e LinkedIn.
    if not args.force and not is_live(url):
        sys.exit("Il post non risponde ancora: aspetta il deploy, oppure usa --force.")

    all_texts = texts(fm)
    for n in networks:
        text = all_texts[n]
        # Su Threads il link è un campo a parte, ma conta nei 500 caratteri
        if n == "threads" and len(text) + len(url) + 1 > THREADS_MAX:
            print(f"! Threads: testo + link fanno {len(text) + len(url) + 1} caratteri, il massimo è {THREADS_MAX}.")
            print("  Aggiungi una versione corta in social: threads: nel front matter.\n")
        copy_to_clipboard(text if n != "linkedin" else text + "\n\n" + url)
        print(f"[{n}] testo copiato negli appunti, apro la finestra di condivisione...")
        webbrowser.open(share_url(n, text, url))
        if n != networks[-1]:
            input("      Invio per passare al social successivo... ")
    print("\nFatto.")


if __name__ == "__main__":
    main()
