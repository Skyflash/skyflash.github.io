# Changelog

Tutte le modifiche rilevanti al sito sono documentate in questo file.

## [2.8.1] - 2026-08-18 — Fix testo invisibile di Disqus dopo un cambio tema

Segnalato un bug: il banner "Regolamento dei commenti" di Disqus, leggibile in tema scuro, diventava praticamente invisibile (restavano visibili solo link e bottone) passando al tema chiaro con lo switcher del sito. Non è un'impostazione lato Disqus: Disqus decide se disegnarsi chiaro o scuro leggendo il colore di sfondo che eredita **una sola volta**, al momento in cui l'embed viene caricato — cambiare tema dopo, senza ricaricare la pagina, lo lascia con lo schema colori sbagliato per il nuovo sfondo (testo bianco su sfondo ormai chiaro).

- `assets/js/theme.js`: alla selezione di un nuovo tema, se l'embed Disqus è già stato caricato (`window.DISQUS` esiste, cioè l'utente ha dato consenso "terze parti" su un post con commenti), viene invocato `DISQUS.reset({ reload: true, config: disqus_config })` per forzare una nuova rilevazione del colore di sfondo sul tema appena scelto, riusando la stessa configurazione di pagina (`page.url`/`page.identifier`) già definita in `_includes/comments.html` — nessun nuovo thread, solo un ridisegno.

## [2.8.0] - 2026-08-17 — Migrazione a Jekyll 4 + GitHub Actions (preparata, non ancora attiva)

Sostituita, sul branch `explore/github-actions-jekyll4`, la gem `github-pages` (che fissa Jekyll a 3.10.0 e libSass 1.x per la pipeline legacy "Deploy from a branch") con Jekyll 4.4.1 e i plugin dichiarati direttamente nel `Gemfile`, in vista del passaggio alla pubblicazione tramite GitHub Actions. **La pubblicazione in produzione resta quella legacy finché non si cambia manualmente il source in Settings → Pages → Build and deployment**: questo aggiornamento da solo non cambia nulla sul sito live.

### Migrazione Jekyll 4 e nuovi workflow

- `Gemfile`: `jekyll ~> 4.3` (risolto a 4.4.1) e `jekyll-sass-converter ~> 3.0` (Dart Sass, al posto della libSass 1.5.2 deprecata) dichiarati direttamente, non più tramite `github-pages`; aggiunta `kramdown-parser-gfm` (prima arrivava come dipendenza transitiva).
- Verificata l'assenza di regressioni con un confronto completo, file per file, fra l'output della build legacy (Jekyll 3.10/libSass) e quello della nuova pipeline (Jekyll 4.4.1/Dart Sass): pagine HTML identiche byte per byte, CSS semanticamente identico (solo differenze cosmetiche di minificazione fra i due compilatori Sass), unica differenza reale un file CSS orfano (`style.css`, mai referenziato da alcuna pagina, residuo dei temi bundlati in `github-pages`) che la build legacy includeva per errore anche nella sitemap e che Jekyll 4 non genera più.
- Due nuovi workflow GitHub Actions:
  - `.github/workflows/build-check.yml`: build + `html-proofer` (link interni, immagini, anchor) su ogni push/pull request di ogni branch — solo verifica, nessuna pubblicazione.
  - `.github/workflows/pages.yml`: build + deploy vero e proprio su GitHub Pages (`actions/upload-pages-artifact`, `actions/deploy-pages`), attivo su push a `master`, manualmente, e ogni giorno alle 5:00 UTC — il rebuild schedulato serve a pubblicare da soli i post con data futura una volta arrivato il loro turno (Jekyll esclude i post futuri ad ogni build; senza un rebuild periodico resterebbero invisibili finché non arriva un push manuale). **Il job di deploy non ha alcun effetto finché il source di Pages non viene cambiato manualmente in Settings.**

### Bug scovati (e corretti) dai nuovi controlli

- `_posts/it/2019-12-13-aggiornare-windows10-k1000.md`: un link Microsoft andava a capo dentro l'URL in markdown, producendo uno spazio letterale nell'URL renderizzato — tollerato in silenzio dalla pipeline legacy, ma non da `jekyll-target-blank` (vedi sotto), che è andato in errore alla build. Corretto unendo le righe.
- `_posts/it/` e `_posts/en/2018-02-14-k1000-report-pc-with-smartcard-reader.md`: link interno `#the-kscript` che puntava a un anchor inesistente — l'heading reale ("The KScript (smarcard.vbs)") genera l'id `the-kscript-smarcardvbs`. Trovato da `html-proofer`, corretto in entrambe le lingue.
- `Gemfile`: la gem `wdm` (solo Windows) era condizionata con `if Gem.win_platform?`, un `if` Ruby valutato alla lettura del Gemfile — su CI Linux la gem sparisce dal Gemfile mentre resta nel lockfile, mandando in conflitto la modalità frozen usata in CI ("Some dependencies were deleted from your gemfile"). Corretto con `platforms: [:windows]`, il meccanismo nativo di Bundler per questo caso.
- `Gemfile.lock`: generato solo su Windows (piattaforma `x64-mingw-ucrt`), mancava la piattaforma `x86_64-linux` necessaria ai runner Ubuntu di GitHub Actions — `bundle install` falliva subito in CI. Aggiunta con `bundle lock --add-platform x86_64-linux`.

### Nuovi plugin e piccoli miglioramenti

- `jekyll-target-blank`: link esterni con `target="_blank" rel="noopener noreferrer"` automatico, in tutto il sito.
- Campo front matter manuale `last_modified_at` sui post, mostrato in `_layouts/post.html` come "Aggiornato il" quando diverso dalla data di pubblicazione — **volutamente manuale**, non calcolato automaticamente dal log Git (`jekyll-last-modified-at`, scartato): la migrazione multilingua IT/EN di agosto ha riscritto quasi tutti i post storici, un calcolo automatico avrebbe segnato "aggiornato" quasi ogni articolo del blog alla stessa data, anche dove nulla è cambiato nel merito.
- `fetchpriority="high"` sulle immagini sopra la piega (avatar in home, post in evidenza nell'indice blog, copertina dell'articolo) — le uniche tre posizioni del tema dove compare un'immagine "hero"; non toccato `project-card.html`, che è sotto la piega e ha già `loading="lazy"`.
- `html-proofer`, oltre ai due fix sopra, configurato con `--no-enforce-https` (alcuni post storici linkano risorse esterne rimaste solo in `http://`, non link rotti) e `--ignore-urls` sui `mailto:?subject=...&body=...` dei pulsanti "condividi via email" (nessun destinatario di proposito, falso positivo del controllo).
- Nuovo `static/assets/img/favicon.jpg` (sostituisce il vecchio, generato da `favicon.svg`) e nuovo `favicon.png` con sfondo trasparente.

## [2.7.2] - 2026-08-16 — Google Analytics 4 con caricamento subordinato al consenso

Sostituito il vecchio script Universal Analytics (`analytics.js`, dismesso da Google a luglio 2023 e già disattivato qui) con Google Analytics 4 (`gtag.js`), seguendo lo stesso schema già collaudato su ed-acfs.github.io. A differenza della vecchia integrazione, lo script GA ora si carica solo dopo il consenso esplicito dell'utente, non incondizionatamente.

- `_includes/analytics.html` rimosso, sostituito da `_includes/tracking.html`: definisce `loadAnalytics()` (gtag.js con `anonymize_ip: true`) solo se `site.ga.id` è impostato, ma non la esegue.
- `_includes/cookieconsent.html`: nuova categoria `analytics` nel banner, con `onConsent`/`onChange` che invocano `loadAnalytics()` solo se l'utente ha accettato quella categoria. Aggiornate le traduzioni IT/EN del banner e del pannello preferenze.
- `_includes/head.html` include `tracking.html` (definizione della funzione, presto in pagina); `_includes/footer.html` non include più il vecchio `analytics.html`.
- `_config.yml`: rimosso il blocco `go:` (Google Optimize, dismesso da Google nel 2023); impostato `ga.id` con il Measurement ID della nuova proprietà GA4 creata per `cristiancastellari.it`.
- `it/about/privacy.md`: aggiunta la categoria "Analisi (statistica)" tra i cookie descritti e una voce dedicata a Google Analytics nella sezione "Cookie di terze parti" (dati raccolti, anonimizzazione IP, luogo di trattamento, modalità di opt-out).
- Verificato con build locale (`bundle exec jekyll build`) che lo script GA venga generato correttamente con il Measurement ID reale, e che resti comunque subordinato al consenso (nessuna chiamata a `loadAnalytics()` finché l'utente non accetta la categoria "analytics" nel banner).

## [2.7.1] - 2026-08-16 — Massimo 3 post correlati in "Potrebbe interessarti anche"

`_layouts/post.html` mostrava fino a 4 post correlati in una griglia a 3 colonne (`grid--3`): il quarto andava a capo da solo, rompendo la griglia. Ridotto `maxRelated` da 4 a 3 per riempire sempre la riga senza aggiungere una quarta colonna. Verificato in locale con `bundle exec jekyll serve` che, su un post con almeno 3 correlati per tag, la sezione mostri esattamente 3 card allineate.

## [2.7.0] - 2026-08-14 — Recuperate le cover originali di 4 post storici

Ritrovato un backup completo (non solo il dump del database) del vecchio blog WordPress, comprensivo della cartella `wp-content/uploads` con i file media originali — fino ad oggi si pensava che le immagini fossero perse per sempre dopo l'attacco ransomware. Da qui recuperate le immagini "in evidenza" originali (il campo WordPress separato dal contenuto del post, non un semplice `<img>` nel testo — per questo erano sfuggite a un primo controllo basato solo sul contenuto) di 4 post storici che sul sito nuovo risultavano senza cover:

- "Backup automatizzato dei database su SQL Express" (IT+EN): foto stock di un hard disk aperto; recuperato anche lo screenshot originale di Task Scheduler, reinserito nel punto del testo in cui compariva ("Schedulazione").
- "Script bash per il backup di un database MySQL": la maglietta "I just took a HUGE mySQL DUMP".
- "Come proteggere un sito dagli attacchi - Parte 1 - I bad crawler": il robottino "We want all your keywords".
- "Come proteggere un sito dagli attacchi - Parte 2 - Il file .htaccess": l'illustrazione "BAD ROBOT".

## [2.6.0] - 2026-08-14 — Link al feed RSS nell'indice del blog

`feed.xml` esisteva già (feed custom, non dal plugin `jekyll-feed`) ma era raggiungibile solo dalla piccola icona nel footer. Aggiunto un link "Feed RSS" ben visibile, allineato a destra sulla stessa riga del titolo "Blog".

- `_layouts/blog-index.html`: nuovo link icona+testo verso `/feed.xml`, riusando la stringa i18n `footer_aria_feed` già presente per il link del footer.
- `_sass/_layout.scss`: nuovo modificatore `.section-header--blog` (flex, titolo a sinistra e link a destra) e stile `.rss-link` con il classico arancione RSS.
- Verificato in locale che `/feed.xml` sia XML valido, si rigeneri ad ogni build con tutti i post in ordine cronologico corretto e rifletta subito le modifiche al front matter (es. i title della voce precedente).

## [2.5.0] - 2026-08-14 — Audit SEO e social sharing dei post

Verifica sistematica di meta tag, description e immagini di condivisione su tutti i 31 post (IT+EN), confrontando front matter dichiarato e HTML effettivamente generato da `jekyll-seo-tag`.

- `_config.yml`: `twitter:card` da `summary` a `summary_large_image` — con `summary` le anteprima su X/Twitter mostravano un'immagine piccola e quadrata, sprecando le cover panoramiche presenti sulla maggior parte dei post.
- Riscritte le `description` di 15 post (IT+EN) troppo lunghe (fino a 419 caratteri, praticamente il primo paragrafo incollato) o troppo corte (<70 caratteri), portandole nella fascia utile prima del troncamento su Google/social.
- Accorciati 5 title fuori misura (fino a 118 caratteri) rimuovendo i sottotitoli tra parentesi che li allungavano oltre la soglia di troncamento nei risultati Google; i title solo leggermente sopra soglia sono stati lasciati invariati per non alterare inutilmente la voce dei post.
- **Post senza immagine propria non avevano alcun `og:image`/`twitter:image`**: verificato nel sorgente del plugin (`jekyll-seo-tag`, `image_drop.rb`) che non esiste un fallback automatico — chi condivideva quei post sui social vedeva una card senza anteprima. Aggiunta un'immagine placeholder generica (`static/assets/img/blog/blog-cover-generic.png`) come default via `defaults:` in `_config.yml` (scope `_posts`) per ogni post privo di `image`; in attesa di cover dedicate per i post più vecchi.
- `_layouts/post.html`: la cover placeholder è esclusa esplicitamente dal rendering della hero image in pagina (mostrata solo nei meta tag social), per non far comparire un banner di branding generico dentro vecchi articoli tecnici che non ne avevano mai avuto uno.

## [2.4.0] - 2026-08-14 — Post in evidenza nell'indice del blog

Ispirato da [jekyllpad.com/blog](https://www.jekyllpad.com/blog): un post per lingua può essere marcato `featured: true` nel front matter per comparire in una card grande in cima all'indice del blog (solo prima pagina), escluso dalla griglia normale sottostante per non duplicarlo. Nessun post è featured di default: è una scelta editoriale esplicita, non calcolata automaticamente sull'ultimo pubblicato.

- `_layouts/blog-index.html`: individua il post `featured` (per lingua) via `where: "featured", true`, lo esclude dalla lista normale ricostruendo l'array con `push` (stesso idioma già usato per i post correlati in `post.html` — niente `where_exp`, evitato di proposito: causa nota di instabilità con condizioni multiple su Jekyll 3.10, vedi voce 2.0.1 più sotto).
- Nuovo componente `.featured-post` in `_sass/_blog.scss`: immagine a sinistra (42% larghezza) e testo a destra su desktop, impilati su mobile; badge "In evidenza"/"Featured" con sfondo pieno e icona stella (prima versione, con sfondo tenue, giudicata poco visibile).
- **Iterazioni sul ritaglio dell'immagine**: un primo tentativo con `object-fit: cover` e altezza fissata (poi rapporto 16:9) tagliava il testo incorporato nelle grafiche di copertina — prima il titolo "WireGuard" in alto, poi un banner panoramico ("Alto Comando Flotta Stellare", proporzioni 4:1) illeggibile perché tagliato ai lati. Le copertine di questo blog sono spesso grafiche con testo a posizioni imprevedibili, non foto: nessun `object-position` fisso va bene per tutte. Risolto abbandonando il ritaglio, lasciando ogni immagine alle sue proporzioni naturali (`height: auto`) — stesso approccio già usato da `.post-image` sugli articoli.

## [2.3.0] - 2026-08-14 — Breadcrumb su articoli e pagine categoria

### Navigazione e SEO: breadcrumb con dati strutturati

Aggiunto un breadcrumb (Home / Blog / Categoria / Titolo) sugli articoli del blog e sulle pagine categoria (Home / Blog / Categoria), sia come nav visibile sia come JSON-LD `BreadcrumbList` — utile per la navigazione e perché Google lo usa per sostituire l'URL nudo con un percorso leggibile nei risultati di ricerca. `jekyll-seo-tag` (già in uso per SEO/Open Graph) non genera breadcrumb di suo: verificato sull'output compilato, produce solo schema `BlogPosting`/`WebSite`/`Person`. Aggiunto quindi un secondo blocco `application/ld+json` indipendente (pratica comune, pagine con più blocchi JSON-LD sono valide).

- Nuovo `_includes/breadcrumb.html`: genera nav visibile e JSON-LD dagli stessi due array (`labels`/`urls`) passati dal layout chiamante, cosicché i due non possano mai disallinearsi. Costruiti con il filtro `push` (già usato in `post.html` per i post correlati) invece di serializzazioni testuali fragili — Liquid non supporta letterali hash, ma supporta array reali.
- Wired in `_layouts/post.html` e `_layouts/category.html`; nuovo stile `.breadcrumb` in `_sass/_components.scss`.

### Riordino header articolo

Diverse iterazioni sul posizionamento di meta-info (data/parole/tempo di lettura) e categoria nell'header di `_layouts/post.html`, con verifica visiva ad ogni passaggio (screenshot chiaro/scuro/mobile):

- La riga meta-info, prima sopra il titolo, ora sta subito sotto (nuova classe `.post-meta` in `_sass/_blog.scss`, stessa colonna di lettura da 760px di titolo/testo — motivo del primo tentativo fallito: il breadcrumb, inserito fuori da `.post-header`, restava ancorato al bordo dell'intero container da 1360px invece che alla colonna centrata, disallineato dal titolo).
- La pill della categoria, ridondante subito sotto al breadcrumb (che la mostra già), spostata sotto la riga meta invece che sopra.
- Spaziatura fra breadcrumb e titolo ridotta (24px → 8px, sembrava eccessiva).

## [2.2.1] - 2026-08-14 — Layout dedicato per la pagina Progetti

### Griglia dei progetti troppo stretta — layout dedicato in stile Blog

La pagina Progetti (`en/projects.html`, `it/progetti.html`) riusava `layout: page`, pensato per contenuti testuali lunghi (CV, Contatti): il contenuto veniva avvolto in `.prose`, con `max-width: 760px` per la leggibilità del testo. Applicato a una griglia a 3 colonne di card, il vincolo schiacciava ogni card a ~245px di larghezza, rendendo le descrizioni strette su 4-5 righe.

Primo tentativo (poi scartato): un flag `wide` in `layout: page` che allargava il container a 1600px e saltava `.prose` solo per quella pagina — funzionante ma una toppa su un layout condiviso con CV/Contatti/Privacy, e con un effetto collaterale: il titolo "Progetti" risultava disallineato rispetto al titolo delle altre pagine su viewport di larghezza intermedia (1360–1600px), dove il container standard restava centrato con margine mentre quello allargato no.

Sostituito con un layout dedicato, `_layouts/projects.html`, sul modello di `_layouts/blog-index.html` (che non ha mai sofferto il problema, non passando da `.prose`): titolo e griglia nello stesso `.container` standard (1360px), senza alcun vincolo aggiuntivo. Le card ora hanno la stessa larghezza (~420px) di quelle del Blog, il titolo è allineato a tutte le altre pagine del sito, e `_layouts/page.html` è tornato alla sua forma originale, senza condizionali.

### Rifinitura testi delle descrizioni progetti

Titoli e descrizioni in `_data/index/projects.yml` chiariti (es. "Italian Translation Project" per l'ITP) e punteggiatura uniformata.

## [2.2.0] - 2026-08-14 — Cookie consent, SEO social e favicon configurabile

### Cookie consent: da cookie-bar.eu a CookieConsent v3

`cookie-bar.eu` (script caricato in `_includes/cookieconsent.html`) è fermo alla versione 1.10.3, pubblicata il 17 luglio 2023 — oltre tre anni senza aggiornamenti. Sostituito con [CookieConsent v3](https://cookieconsent.orestbida.com/) (orestbida, MIT, ultimo push a fine luglio 2026), scelto rispetto a `tarteaucitron.js` (alternativa altrettanto valida) principalmente per il peso: ~23KB minificati contro ~87KB, coerente con un sito che si dichiara "senza JavaScript di terze parti" nel proprio README.

- Due categorie di consenso: `necessary` (readonly) e `thirdparty` (per Disqus, estendibile a futuri embed). Testi del banner e del pannello preferenze in italiano/inglese nativi nella libreria, con `autoDetect: 'document'` che legge la `<html lang>` già impostata da ogni pagina — zero codice di i18n aggiuntivo.
- **Bug fix — il consenso granulare non faceva mai caricare Disqus**: con la vecchia libreria, `_includes/comments.html` controllava solo il cookie generico "accetta tutto" (`cookiebar=CookieAllowed`), ignorando il cookie granulare per le terze parti. Un visitatore che sceglieva "accetto solo le terze parti" — la categoria esatta a cui appartiene Disqus — non vedeva comunque i commenti. Risolto passando al meccanismo dichiarativo di CookieConsent (`manageScriptTags`): lo script di embed di Disqus è ora un `<script type="text/plain" data-category="thirdparty" data-src="...">`, attivato dalla libreria stessa in base alla categoria realmente accettata.
- Nuovo `_sass/_cookieconsent.scss`: rimappa le variabili CSS della libreria (`--cc-bg`, `--cc-btn-primary-bg`, ecc.) sui token del sito (`--color-*` in `_tokens.scss`), così banner e pannello preferenze ereditano automaticamente chiaro/scuro/automatico senza bisogno della classe `.cc--darkmode` della libreria né di JS aggiuntivo.
- Aggiunto un link "Preferenze cookie" nel footer (`_includes/footer.html`, nuova chiave `footer_cookie_prefs` in `_data/i18n.yml`) che riapre il pannello preferenze in qualsiasi momento — poter revocare/cambiare il consenso con la stessa facilità con cui lo si dà è un requisito delle linee guida del Garante Privacy (giugno 2021), non solo una comodità.

### SEO: i profili social non comparivano mai nel JSON-LD della home

Il blocco `social: {name, links}` in `_config.yml` esisteva da tempo ma non produceva **mai** output: `jekyll-seo-tag` considera "home" solo le pagine con url esattamente `/` o `/about/` (vedi `HOMEPAGE_OR_ABOUT_REGEX` nel gem), mentre le home di questo sito vivono sotto `/it/` ed `/en/` per via del routing bilingue — quella regex non scattava mai, quindi `sameAs`/tipo `WebSite` non venivano mai emessi nel JSON-LD, a prescindere da cosa contenesse `social.links`. Verificato confrontando il JSON-LD generato prima/dopo in `_site/it/index.html`.

- Aggiunto un override esplicito `seo: {type: WebSite, links: [...]}` nel front matter di `it/index.html` ed `en/index.html` (unico modo per bypassare il bug della regex), con l'elenco profili aggiornato — includeva Bluesky, mai aggiunto a `social.links` nonostante fosse già presente in `author.bluesky` e nel footer.
- Rimosso il blocco `social:` da `_config.yml`, ormai ridondante e senza alcun consumer.

### Rebrand X (ex Twitter)

`jekyll-seo-tag` 2.8.0 (versione fissata dalla gem `github-pages` usata per il deploy) non ha alcuna chiave "x": genera ancora `twitter:card`/`twitter:site`/`twitter:creator` (nomi invariati anche dopo il rebrand, X li supporta così). Aggiornato quello che è codice nostro, non del plugin:

- Link footer e pagine Contatti (IT/EN) da `twitter.com` a `x.com`.
- Nuova icona SVG dedicata (`_includes/icons/x.html`) al posto di `fa-twitter` — Fork Awesome è un fork di Font Awesome 4 (2015), mai aggiornato dopo il rebrand X del 2023: il logo non esiste nel set.

### Favicon configurabile e ridisegnata

Portata da [my-personal-resume-and-blog](https://github.com/Skyflash/my-personal-resume-and-blog) la stessa idea: nuova chiave `favicon:` in `_config.yml`, usata da `_includes/head.html` e `404.html` al posto del path hardcoded — un fork cambia la favicon in un punto solo.

- Nuovo `static/assets/img/favicon.svg`: monogramma "C" (le iniziali di nome e cognome coincidono) disegnato come singolo arco, con un trattino a fianco che richiama il cursore di un prompt di terminale — nod al contenuto del blog (VPN, KACE, backup, script). Colore `#3385ff`/`#5b9dff` (accent chiaro/scuro del sito) con variante automatica via `prefers-color-scheme` incorporata nell'SVG stesso.
- Sostituisce il vecchio `favicon.jpg`, in uso da circa vent'anni; il file resta nel repo ma non è più referenziato da nulla.

## [2.1.2] - 2026-08-14 — Sitemap pulita e icone nelle card dei post

### Sitemap — pagine tecniche e redirect duplicati esclusi

`sitemap.xml` includeva per errore pagine non-contenuto (`assets/css/main.css`, `search.json`, `feed.xml`, `404.html`, nessuna delle quali aveva mai impostato `sitemap.exclude` nel front matter) e, soprattutto, tutte le pagine di redirect generate da `jekyll-redirect-from`: il plugin le marca già con `sitemap: false`, ma il template controllava solo il formato annidato `sitemap.exclude == "yes"`, ignorando il flag booleano — corretto aggiungendo `or page.sitemap == false` alla condizione. URL totali nel sitemap generato: 104 → 55. Disattivata anche la generazione di `redirects.json` (`redirect_from: {json: false}` in `_config.yml`): non è referenziato da nessuna pagina/script del sito ed era comunque in conflitto con il `Disallow: /*.json` di `robots.txt`.

### Icona per-post nelle card del blog

Il front matter di quasi ogni post porta da sempre un campo `icon:` (classe Fork Awesome, es. `fa-lock`), eredità del vecchio sito WordPress — sopravvissuto alla ricostruzione 2.0.0 ma mai consumato da nessun layout/include. Aggiunto il rendering in `_includes/post-card.html`: l'icona compare in basso a destra della card (`.card__footer`), allineata alla pill della categoria, colorata con `--color-accent`. Prima versione provata accanto al titolo — scartata dopo verifica visiva (stesso colore del testo del titolo, poco leggibile/efficace); provata anche con colore muted prima di stabilizzarsi sull'accento.

## [2.1.1] - 2026-08-13 — Fix paginazione blog e limite home

### Bug fix — post in un'altra lingua nel blog

`_layouts/blog-index.html` per la lingua IT usava `paginator.posts` di `jekyll-paginate`, che pagina **tutti** i `site.posts` senza modo di filtrare per lingua — appena sono comparsi i primi post inglesi, sono spuntati anche nell'elenco del blog italiano. Il plugin è stato rimosso del tutto (era usato solo lì) e sostituito con paginazione manuale filtrata per `page.lang`, implementata con i parametri `offset:`/`limit:` del tag `{% for %}` (non un filtro — vedi sotto). `_config.yml`: tolto `jekyll-paginate` dai plugin e `paginate`/`paginate_path`, aggiunta la chiave `blog_posts_per_page`.

### Bug fix — "Ultimi articoli" in home mostrava tutti i post

`{{ site.posts | where: ... | limit: 6 }}` non troncava nulla: **`limit` non esiste come filtro Liquid** (esiste solo come parametro del tag `{% for %}`, es. `{% for x in y limit:3 %}`), quindi in modalità non-strict di Jekyll veniva ignorato silenziosamente e la sezione mostrava tutti e 23 i post italiani invece di un numero limitato — bug presente fin dall'introduzione della sezione, mascherato dal fatto che con pochi post il risultato "sembrava" quasi giusto. Sostituito con il filtro `slice: 0, 6`, che tronca davvero l'array. Portato anche il numero di articoli mostrati in home da 3 a 6.

## [2.1.0] - 2026-08-13 — Sito multilingua (IT/EN)

### Contesto

Il sito era mono-lingua (italiano). Aggiunto l'inglese per chrome, pagine principali (Home, CV, Progetti, Contatti) e blog **da qui in avanti**: i 23 post storici (e quelli già schedulati) restano solo in italiano, senza traduzione retroattiva. GitHub Pages builda in modalità "safe" con una whitelist di plugin che non include soluzioni i18n standard per Jekyll (`jekyll-polyglot`, `jekyll-multiple-languages-plugin`), quindi tutto è stato gestito con Liquid/front matter puri, riusando i meccanismi già presenti nel sito. (Il tedesco era stato implementato in un primo momento e poi rimosso prima del rilascio: manteneva a parità la complessità architetturale ma raddoppiava il lavoro di traduzione, senza un pubblico target chiaro per ora.)

### Permalink e redirect

- Entrambe le lingue vivono sotto prefisso: `/it/`, `/en/`. Gli URL italiani precedenti (senza prefisso) diventano redirect verso l'equivalente `/it/...`, via `jekyll-redirect-from` (già usato per i redirect dal vecchio WordPress) — nessun URL storico rotto.
- Slug della sezione `/en/` tradotti in inglese dove ha senso (`/en/projects/`, `/en/contact/`, `/en/infrastructure/`, `/en/work-philosophy/`, `/en/personal-projects/`, `/en/outside-office/` — non `/en/progetti/`), lasciati invariati solo per parole già neutre o nomi propri (`tools`, `kace`).
- `404.html` resta l'unica pagina non prefissata (vincolo GitHub Pages: dev'essere in root) ed è stata resa bilingue inline.

### Architettura

- Nuovo `_data/i18n.yml`: dizionario di stringhe UI condivise (nav, bottoni social, paginazione, badge "Attuale", 404, ecc.), consumato via `site.data.i18n.<chiave>[short_lang]`.
- `_data/index/careers.yml`, `projects.yml`, `skills.yml`: campi testo passati da scalare a mappa `{it, en}` — sostituito lo scaffold `{detail, i18n}` mai attivato che era già presente (nessun `language.yml` di supporto, zero riferimenti a `.i18n` in `_layouts`/`_includes`).
- `_data/blog.yml`: da lista flat `{name, href}` a una riga per lingua per categoria (12 righe totali); zero cambi alla logica di match esistente (`site.categories[page.category]`, `where: "name", category`).
- Nuovo include condiviso `_includes/i18n-alternates.html`: calcola le versioni sorelle della pagina corrente tramite `translation_key` in front matter, usato uniformemente sia per i post sia per le pagine (home/CV/Progetti/Contatti/categorie) — niente prefix-swap dell'URL, dato che con slug tradotti (es. `/it/progetti/` vs `/en/projects/`) la sola sostituzione del prefisso `/it|en/` non basta più. Riusato sia da `head.html` (tag `hreflang`) sia da `nav.html` (switcher IT/EN visibile).
- `_config.yml`: nuova chiave `default_lang` (lingua di fallback quando una pagina/post non imposta `lang`) invece di ripetere il valore hardcoded in ogni template.
- Blog IT resta paginato (`/it/blog/pagina:num/`, unico consumer di `jekyll-paginate` nel sito — il plugin supporta un solo indice paginato per l'intero sito). EN non è paginato per ora: volume iniziale basso, si aggiungerà paginazione se/quando servirà.
- Ricerca interna (`search.json`/`search.js`): aggiunto un campo `lang` per ogni voce, filtro sulla lingua della pagina corrente.
- Post correlati (`_layouts/post.html`): il match ora richiede anche `post.lang == page.lang`, per non suggerire un articolo in un'altra lingua come "correlato".

### Fuori scope (intenzionale)

- Nessuna traduzione retroattiva dei 23 post esistenti.
- `disclaimer.md`/`privacy.md` restano solo in italiano (spostati sotto `/it/about/...` per coerenza di struttura, con redirect dagli URL precedenti) — testo legale/regolatorio specifico per l'Italia.
- `feed.xml` resta un unico feed globale bilingue misto.

## [2.0.1] - 2026-08-13 — Ricerca interna potenziata

### Ricerca interna potenziata

- `search.json` ora indicizza anche le pagine di contenuto (CV, Progetti, Contatti, pagine legali, indice blog, pagine categoria), non solo i post del blog, e porta con sé tag/categorie oltre a titolo e descrizione.
- Corretto un bug latente: i valori venivano inseriti nel JSON senza escaping (una virgoletta doppia in un titolo avrebbe rotto silenziosamente il file); ora si usa il filtro `jsonify` di Liquid.
- `search.js`: la query viene spezzata in parole con match "AND" su tutti i campi (titolo, descrizione, tag, categorie) invece della frase esatta su solo titolo/descrizione; punteggio semplice che privilegia i match nel titolo, risultati ordinati per rilevanza invece che per ordine cronologico, estratto (descrizione) mostrato sotto ogni risultato.
- **Bug fix — build rotta su GitHub Pages**: la pipeline "Deploy from a branch" builda con Jekyll 3.10.0 (gem `github-pages`), che non supporta `where_exp` con condizioni multiple in `or` usato per filtrare le pagine da indicizzare. Sostituito con tre `where` singoli (uno per layout) uniti via `concat` — sintassi base, stabile su qualunque versione di Jekyll.

## [2.0.0] - 2026-08-12 — Ricostruzione completa del sito

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

## [1.1.0] - 2026-08-12 — Manutenzione dipendenze sul vecchio tema

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
