# cristiancastellari.it

Codice sorgente del sito personale e blog di Cristian Castellari, pubblicato su GitHub Pages all'indirizzo [cristiancastellari.it](https://cristiancastellari.it).

Il tema — scritto da zero, senza framework CSS/JS di terze parti — è **open source** e riutilizzabile: se ti piace, puoi prenderlo come base per il tuo sito personale. I contenuti (post, CV, progetti) restano ovviamente quelli dell'autore.

## Caratteristiche del tema

- **Jekyll puro**, nessuna pipeline di build front-end: CSS compilato nativamente da Jekyll/Sass, zero JavaScript di terze parti (niente jQuery, niente bundler).
- **Tema chiaro / scuro / automatico**, persistente fra le pagine (`localStorage`), a scelta dell'utente o a seguito di `prefers-color-scheme`.
- **Multi-pagina**: Home, CV/Esperienze, Progetti, Blog (con categorie e paginazione), Contatti — non una singola landing a scroll infinito.
- **Blog** con categorie configurabili, indice categorie con conteggio articoli, paginazione, ricerca client-side (fetch di `search.json`, nessuna libreria esterna), commenti Disqus, bottoni di condivisione con colori di brand.
- **Copertine dei post theme-adaptive**: due immagini per articolo, una per tema chiaro e una per scuro, selezionate puramente via CSS.
- **Statistiche GitHub live** (stelle/fork) sulle card dei progetti, con cache in `localStorage` per restare sotto il rate limit dell'API pubblica.
- Icone via [Fork Awesome](https://forkaweso.me/), con SVG inline per i loghi non presenti nel set (es. X, Bluesky).
- Permalink dei post configurabili e stabili — pensato per non rompere l'indicizzazione quando si cambiano categorie o struttura del blog (vedi `jekyll-redirect-from` in `_config.yml`).

## Stack

- [Jekyll](https://jekyllrb.com/) 3.10 (Ruby, via la gem [`github-pages`](https://github.com/github/pages-gem) che fissa le versioni a quelle usate in produzione), Sass nativo
- Plugin: `jekyll-seo-tag`, `jekyll-redirect-from`, `jekyll-paginate`
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

- `_posts/`: articoli del blog (Markdown)
- `_data/blog.yml`: categorie del blog (nome + URL), usate per il menu di navigazione e l'indice categorie
- `_data/index/`: contenuti strutturati di Home/CV (`careers.yml`, `skills.yml`, `projects.yml`)
- `_layouts/` / `_includes/`: template del tema
- `_sass/`: design system (`_tokens.scss` per palette/tipografia/spaziatura, un file per componente)
- `blog/*.html`: pagine categoria del blog (una per categoria, con `permalink:` esplicito)

### Personalizzare il tema per un sito proprio

- **Identità e social**: sezione `author:`/`social:` in `_config.yml`.
- **Palette colori**: variabili CSS in `_sass/_tokens.scss` (tema chiaro di default, override automatico/esplicito per lo scuro).
- **CV/Esperienze**: `_data/index/careers.yml` (timeline) e `_data/index/skills.yml` (competenze per area).
- **Progetti**: `_data/index/projects.yml`.
- **Categorie del blog**: `_data/blog.yml` — aggiungere una voce qui e creare la pagina categoria corrispondente in `blog/`.

## Changelog

Le modifiche più significative sono tracciate in [CHANGELOG.md](CHANGELOG.md), inclusa la ricostruzione completa del tema (v2.0).

## Licenza

Il repository usa due licenze distinte, dettagliate in [LICENSE](LICENSE):

- **Codice del tema** (`_layouts/`, `_includes/`, `_sass/`, `assets/`): [MIT](LICENSE) — riusabile liberamente, anche per progetti propri.
- **Contenuti** (post del blog, testi di CV/pagine, immagini): [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.it) — riuso consentito con attribuzione e stessa licenza, vedi [disclaimer](https://cristiancastellari.it/about/disclaimer/).
