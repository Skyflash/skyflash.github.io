# cristiancastellari.it

Codice sorgente del sito personale e blog di Cristian Castellari, pubblicato su GitHub Pages all'indirizzo [cristiancastellari.it](https://cristiancastellari.it).

Il tema — scritto da zero, senza framework CSS/JS di terze parti — è **open source** e riutilizzabile: se ti piace, puoi prenderlo come base per il tuo sito personale. I contenuti (post, CV, progetti) restano ovviamente quelli dell'autore.

## Caratteristiche del tema

- **Jekyll puro**, nessuna pipeline di build front-end: CSS compilato nativamente da Jekyll/Sass, zero JavaScript di terze parti (niente jQuery, niente bundler).
- **Multilingua (italiano/inglese)**: permalink sotto prefisso `/it/`/`/en/`, switcher lingua con tag `hreflang`, tutto gestito via front matter e `_data/i18n.yml` — nessun plugin i18n (non compatibile con la whitelist plugin di GitHub Pages).
- **Tema chiaro / scuro / automatico**, persistente fra le pagine (`localStorage`), a scelta dell'utente o a seguito di `prefers-color-scheme`.
- **Multi-pagina**: Home, CV/Esperienze, Progetti, Blog (con categorie e paginazione), Contatti — non una singola landing a scroll infinito.
- **Blog** con categorie configurabili (proprie per lingua), indice categorie con conteggio articoli, paginazione filtrata per lingua, ricerca client-side (fetch di `search.json`, nessuna libreria esterna, risultati filtrati sulla lingua corrente), commenti Disqus, bottoni di condivisione con colori di brand.
- **Copertine dei post theme-adaptive**: due immagini per articolo, una per tema chiaro e una per scuro, selezionate puramente via CSS.
- **Statistiche GitHub live** (stelle/fork) sulle card dei progetti, con cache in `localStorage` per restare sotto il rate limit dell'API pubblica.
- Icone via [Fork Awesome](https://forkaweso.me/), con SVG inline in `_includes/icons/` per i loghi non presenti nel set (X, Bluesky) e per le bandiere dello switcher lingua.
- Permalink dei post configurabili e stabili — pensato per non rompere l'indicizzazione quando si cambiano categorie o struttura del blog (vedi `jekyll-redirect-from` in `_config.yml`).
- **Favicon configurabile**: una chiave `favicon:` in `_config.yml`, nessun path hardcoded nei template.
- **Cookie consent GDPR** con [CookieConsent v3](https://cookieconsent.orestbida.com/) (MIT, gratuito): banner IT/EN nativo, categorie tecnici/terze parti, tema agganciato ai token CSS del sito, blocco dichiarativo degli script di terze parti (es. Disqus) fino al consenso.

## Stack

- [Jekyll](https://jekyllrb.com/) 3.10 (Ruby, via la gem [`github-pages`](https://github.com/github/pages-gem) che fissa le versioni a quelle usate in produzione), Sass nativo
- Plugin: `jekyll-seo-tag`, `jekyll-redirect-from` (la paginazione del blog è gestita a mano, non da un plugin, perché deve filtrare per lingua)
- [Fork Awesome](https://forkaweso.me/) per le icone

Nessuna dipendenza Node/npm: non serve alcuna build front-end.

## Sviluppo locale

Richiede Ruby (con Bundler).

```bash
# dipendenze Ruby (Jekyll e plugin)
bundle install

# avvia il server di sviluppo su http://127.0.0.1:4000
bundle exec jekyll serve

# per vedere anche i post con data futura (es. articoli programmati)
bundle exec jekyll serve --future
```

## Struttura del repository

- `_posts/it/`, `_posts/en/`: articoli del blog (Markdown), organizzati per lingua. I post esistenti prima del multilingua restano solo in `it/`; i nuovi si scrivono in entrambe le lingue collegandole con lo stesso `translation_key` in front matter.
- `it/`, `en/`: pagine statiche per lingua (Home, CV, Progetti, Contatti, pagine categoria del blog), ciascuna con `permalink:` esplicito e — dove esiste una versione nell'altra lingua — lo stesso `translation_key`.
- `_data/blog.yml`: categorie del blog, una riga per lingua per categoria (nome visualizzato + URL); il campo `name` è anche la chiave con cui i post si associano alla categoria.
- `_data/i18n.yml`: dizionario delle stringhe UI condivise (nav, bottoni, paginazione, ecc.), `{it, en}` per chiave.
- `_data/index/`: contenuti strutturati di Home/CV (`careers.yml`, `skills.yml`, `projects.yml`), campi testo come mappa `{it, en}`.
- `_layouts/` / `_includes/`: template del tema; `_includes/icons/` per le SVG inline (loghi social, bandiere).
- `_sass/`: design system (`_tokens.scss` per palette/tipografia/spaziatura, un file per componente).

### Segnalare l'aggiornamento di un post

Ogni post può avere un campo `last_modified_at:` nel front matter (formato `AAAA-MM-GG`, o `AAAA-MM-GG HH:MM:SS`):

```yaml
---
title: Il mio post
date: '2019-12-16 11:30:00'
last_modified_at: '2026-08-17'
---
```

Se presente e diverso dal giorno di `date`, `_layouts/post.html` mostra "Aggiornato il" accanto a data/tempo di lettura. È **volutamente manuale**, non calcolato in automatico dal log Git: un calcolo automatico risentirebbe di qualunque commit tecnico che tocca il file (refactor, migrazioni, correzioni di battitura) anche senza una vera revisione del contenuto. Impostalo a mano solo quando aggiorni davvero un post nel merito.

### Personalizzare il tema per un sito proprio

- **Identità e social**: sezione `author:` in `_config.yml`.
- **Favicon**: chiave `favicon:` in `_config.yml` (svg, ico, jpg, png vanno tutti bene).
- **Lingua di default**: `default_lang` in `_config.yml` — unico punto da cambiare per spostare il fallback su un'altra lingua.
- **Palette colori**: variabili CSS in `_sass/_tokens.scss` (tema chiaro di default, override automatico/esplicito per lo scuro) — `_sass/_cookieconsent.scss` la riusa automaticamente, nessuna palette separata da mantenere.
- **Cookie consent**: categorie, testi IT/EN e shortname Disqus in `_includes/cookieconsent.html` / `_includes/comments.html`.
- **CV/Esperienze**: `_data/index/careers.yml` (timeline) e `_data/index/skills.yml` (competenze per area).
- **Progetti**: `_data/index/projects.yml`.
- **Categorie del blog**: `_data/blog.yml` — aggiungere una riga per lingua e creare la pagina categoria corrispondente in `it/`/`en/`.
- **Stringhe UI**: `_data/i18n.yml` — una chiave per etichetta, valore per lingua.

## Changelog

Le modifiche più significative sono tracciate in [CHANGELOG.md](CHANGELOG.md), inclusi la ricostruzione completa del tema (v2.0) e il sito multilingua IT/EN (v2.1).

## Licenza

Il repository usa due licenze distinte, dettagliate in [LICENSE](LICENSE):

- **Codice del tema** (`_layouts/`, `_includes/`, `_sass/`, `assets/`): [MIT](LICENSE) — riusabile liberamente, anche per progetti propri.
- **Contenuti** (post del blog, testi di CV/pagine, immagini): [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.it) — riuso consentito con attribuzione e stessa licenza, vedi [disclaimer](https://cristiancastellari.it/it/about/disclaimer/).
