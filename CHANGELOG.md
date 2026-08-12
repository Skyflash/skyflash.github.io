# Changelog

Tutte le modifiche rilevanti al sito sono documentate in questo file.

## [2.0.0] - 2026-08-14 — Ricostruzione completa del sito

### Contesto

Il tema precedente (derivato da [Jalpc](https://github.com/jarrekk/Jalpc): Bootstrap 3, jQuery, layout one-page a scroll) è stato sostituito da zero con un tema scritto interamente per questo sito: nessuna dipendenza da framework CSS/JS di terze parti, nessuna pipeline di build front-end, palette e componenti propri. Il lavoro è stato svolto sul branch `redesign-2026`, con [Claude Code](https://claude.com/claude-code) come collaboratore — la serie di articoli "Il nuovo sito" (parti [1](https://cristiancastellari.it/blog/progetti-personali/il-nuovo-sito-parte-1-perche-ripartire-da-zero/), [2](https://cristiancastellari.it/blog/progetti-personali/il-nuovo-sito-parte-2-i-bug-nascosti-in-un-sito-nuovo/), [3](https://cristiancastellari.it/blog/progetti-personali/il-nuovo-sito-parte-3-le-copertine-che-si-adattano-al-tema/), [4](https://cristiancastellari.it/blog/progetti-personali/il-nuovo-sito-parte-4-le-ultime-finiture/)) racconta il processo per esteso.

**Vincolo rispettato al 100%: permalink invariati.** Ogni post del blog e ogni pagina categoria mantiene esattamente lo stesso URL del sito precedente (verificato per diff completo dell'elenco URL generato, ripetuto più volte durante il lavoro) — nessun impatto sull'indicizzazione Google.

### Stack e architettura

- Via Bootstrap 3, jQuery e tutti i plugin jQuery (metismenu, jquery-slimscroll, peity, wowjs, particles.js, pace-progress, gritter), Chart.js, l'intera pipeline npm di build (`build/`, `package.json`, bundle compilati) — CSS compilato nativamente da Jekyll/Sass, zero JavaScript di terze parti.
- Icone tramite [Fork Awesome](https://forkaweso.me/) (già vendorizzato nel repo, mai collegato prima), più alcune icone SVG inline scritte a mano per i loghi non presenti nel set (X/Twitter, Bluesky — entrambi rebrand successivi al 2016).
- Design system proprio in `_sass/_tokens.scss`: palette a custom property CSS, tema chiaro/scuro/automatico a 3 stati (`prefers-color-scheme` + override esplicito via `[data-theme]`, persistente fra le pagine tramite `localStorage`).
- Struttura multi-pagina: Home, CV (`/cv/`), Progetti (`/progetti/`), Blog (`/blog/` + pagine categoria), Contatti (`/contatti/`) — al posto della singola pagina a scroll infinito.

### Contenuti

- Competenze e timeline di carriera aggiornate (in `_data/index/skills.yml` e `_data/index/careers.yml`), competenze raggruppate per area invece del radar Chart.js.
- Categorie del blog riorganizzate e rinominate per un taglio più tecnico: **Kace**, **Filosofia di Lavoro**, **Strumenti**, **Infrastruttura & Sistemi**, **Fuori dall'Ufficio**, **Progetti Personali** (rimossa la categoria WordPress e un post di test senza contenuto reale).
- `/blog/`: aggiunto un indice di categorie navigabile con conteggio articoli, e paginazione ogni 15 post (`jekyll-paginate`).
- Bottoni di condivisione (`social.html`) riscritti: link aggiornati (X al posto di Twitter, endpoint LinkedIn corrente, Reddit su https, tutti i parametri con `url_encode`), aggiunti Bluesky/WhatsApp/Telegram, colori di brand per icona con hover a colore pieno.
- Copertine dei post con tecnica theme-adaptive: due immagini per articolo (una per tema chiaro, una per scuro), scelta puramente via CSS senza JavaScript.

### Bug corretti durante la ricostruzione

- Tema chiaro/scuro che non persisteva navigando fra le pagine su Brave (il fix via `<head>` inline veniva bloccato dagli shield privacy del browser); risolto rendendo `theme.js` autosufficiente.
- Sottolineatura CSS dei link che "sanguinava" nei bottoni/card annidati in blocchi di prosa (bottone CV, card Contatti) — regola `.prose a` troppo generica, corretta con esclusioni esplicite.
- Pillole categoria sulle card dei post che puntavano a URL inesistenti dopo la rinomina delle categorie (logica che indovinava l'URL dal nome invece di leggerlo da `_data/blog.yml`).
- `jekyll-paginate`: quattro pagine che scrivevano tutte sullo stesso file di destinazione, causato da un `permalink:` esplicito in front matter che aveva priorità assoluta sulla riassegnazione di `Page#dir` fatta dal plugin.
- Voce di menu "Blog" che non portava a `/blog/` cliccandoci sopra direttamente (link e toggle del sottomenu condividevano lo stesso elemento).
- Box commenti Disqus che restava vuoto al primo caricamento (senza il cookie `cookiebar` già presente, il parsing del cookie lanciava un'eccezione non gestita che interrompeva l'intero script).
- Card statistiche GitHub (stelle/fork) che andavano a capo per pochi pixel nella pagina Progetti; risolto allargando leggermente il container generale (1280→1360px) e riducendo il padding delle pillole statistiche.
- Hero della home page: spazio vuoto crescente fra testo e foto a schermi larghi (causato da `justify-content: space-between` su un contenitore a piena larghezza), corretto con un gruppo testo+foto compatto ancorato allo stesso margine delle sezioni sottostanti.

### Verifiche eseguite

- Confronto completo dell'elenco URL generati fra `master` (sito precedente) e `redesign-2026`, ripetuto a più riprese: zero permalink di post/categorie rimossi o modificati.
- Diff di `sitemap.xml` e `feed.xml` fra le due build.
- Build Jekyll pulita e verifica visiva (screenshot headless) su entrambi i temi colore, ad ogni modifica rilevante.

## [Non rilasciato] - 2026-08-13

### Ricerca interna potenziata

- `search.json` ora indicizza anche le pagine di contenuto (CV, Progetti, Contatti, pagine legali, indice blog, pagine categoria), non solo i post del blog, e porta con sé tag/categorie oltre a titolo e descrizione.
- Corretto un bug latente: i valori venivano inseriti nel JSON senza escaping (una virgoletta doppia in un titolo avrebbe rotto silenziosamente il file); ora si usa il filtro `jsonify` di Liquid.
- `search.js`: la query viene spezzata in parole con match "AND" su tutti i campi (titolo, descrizione, tag, categorie) invece della frase esatta su solo titolo/descrizione; punteggio semplice che privilegia i match nel titolo, risultati ordinati per rilevanza invece che per ordine cronologico, estratto (descrizione) mostrato sotto ogni risultato.
- **Bug fix — build rotta su GitHub Pages**: la pipeline "Deploy from a branch" builda con Jekyll 3.10.0 (gem `github-pages`), che non supporta `where_exp` con condizioni multiple in `or` usato per filtrare le pagine da indicizzare. Sostituito con tre `where` singoli (uno per layout) uniti via `concat` — sintassi base, stabile su qualunque versione di Jekyll.

## [Non rilasciato] - 2026-08-12

### Contesto

Il sito non veniva ricompilato da capo dal 2019: gli asset compilati (`static/assets/app-*.min.css/js`) erano congelati a quella data, mentre negli anni Dependabot ha continuato ad alzare le versioni dichiarate in `package.json` (Bootstrap 3→5, Chart.js 2→4, Font Awesome 4→5) senza che nessuno rieseguisse mai `npm run build`. Il sito pubblicato funzionava solo perché usava i vecchi bundle del 2019, non le dipendenze effettivamente dichiarate. Aggiornando i pacchetti e ricompilando per la prima volta dopo anni, sono emersi diversi bug dormienti dovuti a questo disallineamento.

### Aggiornamento dipendenze Ruby / Jekyll

- **Jekyll**: `4.2.2` → `4.4.1`. La 4.2.2 non era compatibile con Ruby 3.4 (mancavano `csv`/`bigdecimal` come dipendenze esplicite) e usava Liquid 4.0.3, che chiamava `String#tainted?`, rimosso da Ruby 3.2+.
- **Liquid**: aggiornato a `4.0.4` (fix del problema `tainted?`).
- **wdm** (watcher directory su Windows): vincolo rilassato da `~> 0.1.0` a `>= 0.1.0`, risolvendosi a `0.2.0`.
- Aggiunte dipendenze esplicite `logger` e `bigdecimal`, richieste da Ruby 3.4+ ma non più incluse di default.
- Rack `2.2.23` → `3.2.6`, Sass converter passato da `sassc`/libsass a `sass-embedded` (dart-sass) — verificato output CSS equivalente (differenze solo cosmetiche: `black`→`#000`, virgolette, BOM).
- `Gemfile.lock` rigenerato e coerente con l'ambiente Ruby 3.4 / Bundler 2.7.1 in uso.

### Aggiornamento dipendenze npm

- **Rimossi 9 pacchetti "morti"**, mai referenziati da nessun file del progetto (verificato con grep sull'intero repo), probabile residuo di vecchi `npm audit fix` che li avevano aggiunti come dipendenze dirette invece di usare `overrides`: `@npmcli/arborist`, `hosted-git-info`, `jsprim`, **`npm`** (il gestore pacchetti stesso, elencato per errore come dipendenza del progetto), `atob`, `purify-css`, `y18n`, `yargs-parser`, `popper.js`, `tar` (duplicato in `dependencies` e `devDependencies`, anch'esso inutilizzato).
- `colors` spostata da `dependencies` a `devDependencies` (serve solo allo script di build, non al sito pubblicato).
- **Vulnerabilità npm: 25 → 0** (`npm audit`), grazie soprattutto alla rimozione dei pacchetti morti; le 2 residue (`brace-expansion`, `minimatch`, transitive di `shelljs`) risolte con `npm audit fix`.
- Pacchetti installati: 431 → 40.
- Bootstrap e Chart.js aggiornati alle ultime versioni compatibili entro i rispettivi major.
- **jQuery lasciato a `3.7.1` intenzionalmente**: `metismenu@3.1.0` dichiara una peer-dependency su jQuery ≥4, ma bumpare jQuery a v4 rischierebbe di rompere `jquery-slimscroll`/`peity`/script custom del tema — non vale il rischio su un sito prossimo alla sostituzione.

### Bug fix — layout rotto (Bootstrap)

Il bundle CSS committato era compilato con **Bootstrap 3.4.1**; il markup dell'intero tema (`navbar-default`, `.features`, `col-lg-*`, ecc. in tutti i `_layouts`/`_includes`) è scritto per Bootstrap 3. `package.json` dichiarava però `^5.0.0` da anni (mai testato con una ricompilazione reale).

- `package.json`: `bootstrap` riportato a `^3.4.1`, coerente con il markup effettivo del tema.
- **Nota di sicurezza**: Bootstrap 3.4.1 è l'ultima release della serie 3 (EOL, nessuna patch futura) e porta con sé 2 vulnerabilità XSS moderate note in Popover/Tooltip/attributi `data-*` (nessun fix disponibile). Rischio pratico basso: il sito non inietta mai contenuto utente in tooltip/popover/data-*. Rischio accettato in attesa della sostituzione del sito con una nuova implementazione moderna.

### Bug fix — grafico radar delle competenze non visibile

`_includes/sections/skills.html` usava la sintassi di configurazione **Chart.js v2** (`options.scale`, `options.legend` in cima all'oggetto), incompatibile con Chart.js v4 (che richiede `options.scales.r` e `options.plugins.legend`).

- Aggiornata la sintassi nello snippet Liquid/JS alla API Chart.js v4, mantenendo la libreria aggiornata (`4.5.1`) invece di tornare a una versione EOL.

### Bug fix — bundle JavaScript vuoto/corrotto

`build/build.js` passava l'elenco dei path dei file direttamente a `UglifyJS.minify()`, assumendo che li leggesse da disco. **uglify-js 3.x ha cambiato API**: non fa più I/O su file, tratta ogni stringa dell'array come codice sorgente letterale. Il risultato era un bundle da 228 byte contenente i path stessi interpretati come espressioni JS (divisioni), invece di jQuery/Bootstrap/Chart.js/ecc. Il bug era presente da quando `uglify-js` era stato aggiornato alla v3 (anni fa), ma dormiente perché `npm run build` non veniva più eseguito dal 2019.

- `build/build.js`: `compressjs()` ora legge esplicitamente il contenuto di ogni file (`fs.readFileSync`) e passa a UglifyJS un oggetto `{filename: sorgente}`; aggiunto anche il controllo di `result.error` (prima ignorato silenziosamente).
- `build/files.conf.js`: corretto il path di Chart.js da `node_modules/chart.js/dist/Chart.js` (build ESM nella v4, matchato per caso solo per l'insensibilità al maiuscolo/minuscolo di Windows; su Linux/GitHub Pages non sarebbe nemmeno stato trovato) a `node_modules/chart.js/dist/chart.umd.js` (build UMD corretta, espone `window.Chart`).

### Bug fix — icone mancanti (Font Awesome)

`build/files.conf.js` referenziava `node_modules/components-font-awesome/css/font-awesome.css`, file che **non esiste più** in Font Awesome 5.9.0 (installato da tempo ma mai ricompilato): la 5.x ha ristrutturato i CSS in `all.css`, `v4-shims.css`, ecc. Il file mancante veniva ignorato silenziosamente da CleanCSS, lasciando tutte le icone (`fa fa-xxx`) senza font.

- `build/files.conf.js`: sostituito il path mancante con `node_modules/components-font-awesome/css/all.css` + `css/v4-shims.css` (lo shim che mappa i vecchi nomi classe FA4, usati in tutto il tema, alle icone FA5).
- `build/build.js`: aggiunta copia dei webfont (`node_modules/components-font-awesome/webfonts/*` → `static/webfonts/`), path richiesto dai riferimenti relativi `../webfonts/...` nel CSS di Font Awesome 5 rispetto al bundle compilato in `static/assets/`.

### Asset rigenerati

- `static/assets/app-<data>.min.css`, `app-<data>.min.js`, `blog-<data>.min.js`, `i18-<data>.min.js` ricompilati (i vecchi file datati `20190620` sono stati rimossi, come da comportamento normale dello script di build).
- Nuova cartella `static/webfonts/` con i font Font Awesome 5.

### Verifiche eseguite

- Build Jekyll pulita, confronto contenuto pre/post aggiornamento su tutte le pagine generate.
- Tutti i 10 permalink dei post del blog (`/blog/<categoria>/<slug>/`) invariati — nessun rischio per l'indicizzazione Google.
- Sitemap, feed RSS, pagine legali (`/about/disclaimer/`, `/about/privacy/`) generate correttamente.
- Server locale (`bundle exec jekyll serve`) testato manualmente in browser dall'utente: layout, timeline carriera, icone e grafico radar confermati funzionanti dopo i fix.

### Problemi noti, non risolti (pre-esistenti, fuori scope)

- `npm run dev` punta a `build/dev-server.js`, file inesistente nel repo — script già rotto prima di questo intervento.
- `build/files.conf.js` referenzia ancora `fork-awesome/css/fork-awesome.min.css` con un path relativo mai stato corretto (mancava già nel bundle del 2019): riferimento morto, nessuna icona del tema dipende da Fork Awesome, lasciato invariato.
- Bootstrap 3.4.1 è EOL: la migrazione del tema a Bootstrap 5 (ristrutturazione di classi in tutti i `_layouts`/`_includes`/`_sass`) è rimandata alla ricostruzione del nuovo sito.
