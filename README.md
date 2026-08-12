# cristiancastellari.it

Codice sorgente del sito personale e blog di Cristian Castellari, pubblicato su GitHub Pages all'indirizzo [cristiancastellari.it](https://cristiancastellari.it).

Il tema di partenza era [Jalpc](https://github.com/jarrekk/Jalpc), ma negli anni personalizzazioni, contenuti e correzioni hanno preso una strada propria: questo repository va considerato indipendente, non un fork da tenere allineato all'originale.

## Stack

- [Jekyll](https://jekyllrb.com/) 4.x (Ruby)
- [Bootstrap 3](https://getbootstrap.com/docs/3.4/), jQuery, [Chart.js](https://www.chartjs.org/), [Font Awesome 5](https://fontawesome.com/)
- Asset CSS/JS compressi con [UglifyJS](https://github.com/mishoo/UglifyJS) e [clean-css](https://github.com/clean-css/clean-css)

## Sviluppo locale

Richiede Ruby (con Bundler) e Node.js.

```bash
# dipendenze Ruby (Jekyll e plugin)
bundle install

# dipendenze npm (librerie front-end e tool di build)
npm install

# compila gli asset CSS/JS in static/assets
npm run build

# avvia il server di sviluppo Jekyll su http://127.0.0.1:4000
bundle exec jekyll serve
```

Dopo aver modificato una libreria front-end (`package.json`) o gli script in `_includes/sections/*.html`, va rilanciato `npm run build` prima di ricompilare con Jekyll, altrimenti i vecchi asset compressi restano quelli in uso.

## Contenuti

- `_posts/`: articoli del blog (Markdown)
- `_data/`: contenuti strutturati della landing page (esperienze, competenze, progetti, link) e delle sezioni del blog
- `_layouts/` / `_includes/`: template del tema
- `build/`: script Node per compilare e comprimere gli asset front-end

## Changelog

Le modifiche più significative, in particolare quelle di manutenzione/aggiornamento dipendenze, sono tracciate in [CHANGELOG.md](CHANGELOG.md).

## Licenza

Codice distribuito con licenza [MIT](LICENSE). Tema di partenza [Jalpc](https://github.com/jarrekk/Jalpc) di jarrekk, anch'esso MIT.
