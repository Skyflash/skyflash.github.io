---
title: "Il nuovo sito, parte 4: le ultime finiture"
layout: post
date: '2026-08-14 11:15:00'
description: Un menu che non portava dove prometteva, un indice di categorie per un blog destinato a crescere, bottoni di condivisione con link rotti e senza i colori dei social, un box dei commenti che si rompeva silenziosamente al primo caricamento, numeri di GitHub che andavano a capo per pochi pixel, e una hero in home che sembrava avere due blocchi scollegati. Il lavoro meno glamour ma più importante prima di andare online.
intro: "Non tutto il lavoro su un sito nuovo è fatto di decisioni grandi. Buona parte è fatta di questo: un menu che non porta dove promette, bottoni di condivisione che puntano a endpoint dismessi, un box commenti che si rompe in silenzio, tre pixel di troppo che fanno andare a capo un numero, uno spazio vuoto che cresce a dismisura fra un testo e una foto. Le ultime finiture, appunto."
image: "/static/assets/img/blog/nuovo-sito-2026/parte4-cover.jpg"
image_dark: "/static/assets/img/blog/nuovo-sito-2026/parte4-cover-dark.jpg"
lang: it_IT
categories:
- Progetti Personali
keywords: css, disqus, condivisione social, jekyll, claude code, accessibilità, navigazione, paginazione
tags:
- css
- claude-code
- ia
- debugging
- ux
permalink: "/blog/progetti-personali/:title/"
icon: fa-wrench
---

Le prime tre parti di questa serie ([1]({{ '/blog/progetti-personali/il-nuovo-sito-parte-1-perche-ripartire-da-zero/' | relative_url }}), [2]({{ '/blog/progetti-personali/il-nuovo-sito-parte-2-i-bug-nascosti-in-un-sito-nuovo/' | relative_url }}), [3]({{ '/blog/progetti-personali/il-nuovo-sito-parte-3-le-copertine-che-si-adattano-al-tema/' | relative_url }})) raccontano decisioni con un inizio, uno svolgimento e una fine chiara: ricostruire il sito, correggere i bug, inventarsi le copertine giuste. Questa parte è diversa. È la lista, un po' meno epica ma altrettanto necessaria, delle rifiniture fatte passando in rassegna il sito pezzo per pezzo prima di considerarlo pronto per andare online.

* TOC
{:toc}

## Un menu che non portava dove prometteva

La voce "Blog" nel menu principale apriva il sottomenu con le categorie — ma cliccandoci sopra direttamente, invece di finire su `/blog/` come ci si aspetterebbe, non succedeva nulla di utile. La voce del menu faceva doppio servizio: link e interruttore del sottomenu insieme, e il secondo comportamento vinceva sempre sul primo.

La correzione è stata separare le due responsabilità in due elementi distinti — un link vero verso `/blog/` e, accanto, un piccolo pulsante a freccia dedicato solo ad aprire o chiudere il sottomenu delle categorie:

{% raw %}```html
<li class="nav-item">
  <a class="nav-link" href="{{ '/blog/' | relative_url }}">Blog</a>
  <button type="button" class="nav-caret" aria-label="Mostra le categorie del blog" aria-expanded="false">
    <i class="fa fa-chevron-down" aria-hidden="true"></i>
  </button>
  <ul class="nav-submenu">
    {% for category in site.data.blog %}
    <li><a href="{{ category.href | relative_url }}">{{ category.name }}</a></li>
    {% endfor %}
  </ul>
</li>
```{% endraw %}

Un bug banale da leggere nel codice, ma invisibile finché non si prova davvero a cliccare "Blog" aspettandosi di arrivare al blog.

## Un indice per un blog che crescerà

Con dieci post il problema non si pone, ma prima o poi la lista cronologica in `/blog/` smetterà di bastare da sola. Ho aggiunto due cose pensando in avanti: un indice di categorie navigabile in cima alla pagina, con il conteggio degli articoli per categoria, e la paginazione vera e propria — quindici post per pagina, tramite il plugin `jekyll-paginate` (il cui comportamento tutt'altro che intuitivo, con quattro pagine che scrivevano tutte sullo stesso file, è raccontato nella [parte 2]({{ '/blog/progetti-personali/il-nuovo-sito-parte-2-i-bug-nascosti-in-un-sito-nuovo/' | relative_url }})).

{% raw %}```liquid
<nav class="category-index" aria-label="Categorie del blog">
  {% for category in site.data.blog %}
  <a class="category-pill" href="{{ category.href | relative_url }}">
    {{ category.name }}
    <span class="category-pill__count">{{ site.categories[category.name].size | default: 0 }}</span>
  </a>
  {% endfor %}
</nav>
```{% endraw %}

Ho scartato di proposito l'idea di una tag cloud: con una manciata di categorie ben curate, le pillole già rispondono alla domanda "cosa trovo qui dentro" in un colpo d'occhio — una nuvola di tag avrebbe aggiunto rumore visivo senza aggiungere informazione.

## I bottoni di condivisione erano fermi al 2016

Ogni post ha dei bottoni per condividerlo sui social. Non li avevo toccati durante la ricostruzione — funzionavano, quindi perché guardarli? Guardandoli davvero, la lista dei problemi è stata più lunga del previsto:

- **Twitter era ancora Twitter.** Dominio e testo non aggiornati a X.
- **LinkedIn usava un endpoint dismesso.** `shareArticle` non è più quello raccomandato da anni: quello attuale è `sharing/share-offsite`.
- **Reddit era in `http://`**, non `https://`, e non passava nemmeno il titolo del post.
- **Nessun parametro era codificato per l'URL.** Il titolo di un articolo con un apostrofo — capita spesso, in italiano — poteva rompere silenziosamente il link di condivisione.
- **Il testo dell'email era in inglese** ("Check out this site") in mezzo a un sito interamente in italiano.
- **Mancavano Bluesky, WhatsApp e Telegram**, probabilmente più rilevanti oggi di Reddit per un pubblico italiano.

La correzione più istruttiva è quella dell'URL encoding. Senza:

{% raw %}```liquid
https://x.com/intent/tweet?text={{ page.title }}&url={{ page_url }}
```{% endraw %}

Con un titolo tipo *"...dell'Infrastruttura IT..."*, quell'apostrofo tipografico finiva letteralmente dentro l'URL, rompendo la struttura dei parametri. Basta un filtro:

{% raw %}```liquid
https://x.com/intent/tweet?text={{ page.title | url_encode }}&url={{ page_url | url_encode }}
```{% endraw %}

Un dettaglio che non si nota mai, finché non capita il titolo sbagliato.

## Il colore dei social, recuperato dal sito vecchio

Nella nuova versione i bottoni di condivisione erano tutti uguali: bordo neutro, colore d'accento del sito. Corretto, ma anonimo — nel sito vecchio ogni icona aveva il proprio colore di brand, e passandoci sopra con il mouse il bottone si riempiva di quel colore invertendo il testo in bianco. Un dettaglio che aiuta a riconoscere le icone a colpo d'occhio, prima ancora di leggerle.

Il file che conteneva quei colori l'avevo cancellato durante la ricostruzione, ma la cronologia Git non dimentica:

```
git show master:_sass/_social.scss
```

Da lì ho recuperato le tonalità esatte (Facebook `#3b5998`, LinkedIn `#0077b5`, Reddit `#ff5700`...) e le ho riapplicate, aggiungendo i colori ufficiali delle tre piattaforme nuove. Per X, che oggi non usa più l'uccellino ma un logo che Font Awesome — fermo al 2016 — non conosce, ho dovuto disegnare l'icona a mano con un piccolo SVG inline, esattamente come già fatto per Bluesky nella parte 3.

## Il box dei commenti che si rompeva in silenzio

Questo è stato il bug più subdolo dell'intera rifinitura. Un lettore mi ha segnalato che, aprendo certi articoli, il box dei commenti restava vuoto — a meno di ricaricare la pagina, dopodiché funzionava perfettamente.

La causa era in una singola riga, rimasta invariata probabilmente dal giorno in cui questo sito ha adottato Disqus:

```js
cookieValue = document.cookie.match(/(;)?cookiebar=([^;]*);?/)[2];
```

Se il cookie `cookiebar` non esiste ancora — cioè alla primissima visita, prima che l'utente interagisca col banner dei cookie — `document.cookie.match()` restituisce `null`. E leggere `[2]` da `null` non restituisce `undefined`: **lancia un errore JavaScript** che interrompe l'intero script sul colpo. Disqus non veniva nemmeno provato a caricare. Solo un secondo caricamento della pagina, con il cookie ormai presente, faceva ripartire lo script da capo — da qui il "funziona solo dopo il reload".

La correzione è una manciata di righe più difensive:

```js
var cookieMatch = document.cookie.match(/(?:^|; )cookiebar=([^;]*)/);
var cookieValue = cookieMatch ? decodeURIComponent(cookieMatch[1]) : null;
```

Ne ho approfittato per allineare l'imbottitura di Disqus alla configurazione raccomandata attuale — URL e identificatore di pagina dichiarati esplicitamente invece di lasciarli dedurre automaticamente — e per passare da un URL "protocol-relative" (`//...disqus.com/embed.js`) a un più corretto `https://` esplicito.

## Tre pixel di troppo

Ultima segnalazione, la più piccola: nella pagina Progetti, il numero di fork su GitHub andava a capo su una riga propria invece di stare accanto alle stelle, per pochi pixel. Corretto allargando leggermente il contenitore generale del sito (1280 → 1360px, un aumento del 6% impercettibile ovunque tranne che dove serviva) e riducendo il padding orizzontale delle pillole statistiche. Verificato sul caso peggiore — il repository di questo stesso sito, con oltre cento stelle — che ora sta comodamente su una riga sola.

## Il vuoto fra il testo e la foto, in home

Ultima segnalazione, arrivata guardando la home su uno schermo largo: nella hero, il blocco di testo a sinistra e la mia foto a destra sembravano due isole scollegate, con un vuoto enorme in mezzo che restringere la finestra non risolveva. Colpa di `justify-content: space-between` su un contenitore largo quanto l'intera pagina (1360px): spinge i due elementi ai bordi opposti a prescindere da quanto sia effettivamente largo il testo — più lo schermo è ampio, più cresce il vuoto.

Primo tentativo, sbagliato: dare alla hero un `max-width` proprio e centrarla, per tenere testo e foto più vicini. Il risultato sembrava due blocchi sovrapposti, perché le sezioni sotto (Progetti, Blog) restavano larghe quanto tutta la pagina e non più allineate al bordo sinistro della hero. Corretto tornando alla larghezza piena e sostituendo `space-between` con `justify-content: flex-start` più un gap fisso: testo e foto restano un gruppo compatto, ancorato allo stesso margine di tutto il resto della pagina.

Ultimo dettaglio, puramente estetico, che ha richiesto tre tentativi: prima un alone sfumato nel colore d'accento dietro la foto ("sembro una divinità scesa dal cielo", bocciato giustamente), poi un cerchio piatto più discreto nello stesso colore delle card sotto, e alla fine — con lo spazio ormai risolto dal fix di layout — nessun elemento decorativo. La foto non ne aveva più bisogno: il problema era il vuoto intorno, non l'assenza di uno sfondo.

## Perché questa parte conta

Nessuna di queste correzioni cambia in modo visibile il sito per un visitatore distratto. Ma sommate, sono la differenza tra un sito che "sembra pronto" e uno che lo è davvero: link che portano dove devono, un box commenti che funziona sempre e non solo a volte, un dettaglio di colore che aiuta a riconoscere un'icona senza doverla leggere. Le parti divertenti di ricostruire un sito sono le prime tre. Questa è quella che, silenziosamente, fa la differenza quando qualcuno lo usa sul serio.
