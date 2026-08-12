---
title: "Il nuovo sito, parte 3: le copertine che si adattano al tema (senza una riga di JavaScript)"
layout: post
date: '2026-08-13 10:00:00'
description: La storia in diretta di come una semplice richiesta — "usa uno screenshot del vecchio e uno del nuovo sito come copertina" — sia diventata un piccolo rabbit hole fatto di browser headless, dissolvenze fallite e un trucco CSS per far apparire l'immagine giusta a seconda del tema del lettore.
intro: "A volte il post più interessante da scrivere è quello sulla cosa appena successa. Questa è la storia, in diretta, di come le copertine di questa stessa serie di articoli abbiano imparato a cambiare da sole a seconda che tu stia leggendo in chiaro o in scuro."
image: "/static/assets/img/blog/nuovo-sito-2026/parte1-cover.jpg"
image_dark: "/static/assets/img/blog/nuovo-sito-2026/parte1-cover-dark.jpg"
lang: it_IT
categories:
- Progetti Personali
keywords: css, dark mode, jekyll, claude code, image processing, headless browser
tags:
- css
- claude-code
- ia
- design
permalink: "/blog/progetti-personali/:title/"
icon: fa-image
---

Nelle prime due parti di questa serie ([1]({{ '/blog/progetti-personali/il-nuovo-sito-parte-1-perche-ripartire-da-zero/' | relative_url }}), [2]({{ '/blog/progetti-personali/il-nuovo-sito-parte-2-i-bug-nascosti-in-un-sito-nuovo/' | relative_url }})) ho raccontato perché ho ricostruito questo sito e i bug scoperti subito dopo. Poi mi serviva un'ultima cosa, piccola: una copertina per quei due articoli. Ci è voluto più tempo di quanto vorrei ammettere, ed è successo letteralmente mentre scrivevo — quindi eccolo qui, come terzo capitolo.

* TOC
{:toc}

## L'idea di partenza

Volevo una copertina che raccontasse visivamente il passaggio dal vecchio sito al nuovo: uno screenshot di ciascuna versione, uniti in un'unica immagine — due terzi vecchio e un terzo nuovo per la prima parte, il contrario per la seconda.

Nessun tool di editing immagini a disposizione, solo la riga di comando. Ho installato Pillow (Python) per comporre le immagini, e usato Microsoft Edge in **modalità headless** per catturare gli screenshot: sia del sito vecchio, ancora online in produzione, sia del nuovo, in locale.

```
msedge --headless --disable-gpu --window-size=1600,1400 --screenshot=old.png https://cristiancastellari.it/
```

Fin qui, facile.

## Tre tentativi, tre problemi

**Primo tentativo**: dissolvenza larga tra le due immagini. Risultato: i testi delle due pagine, sovrapposti nella zona di sfumatura, diventavano illeggibili — un doppio esposizione confusa, non una transizione elegante.

**Secondo tentativo**: ho ristretto il ritaglio a soli 300 pixel in alto, giusto l'header. Risultato: si vedeva solo lo sfondo animato a particelle del vecchio sito, senza alcun indizio che si trattasse davvero di un sito diverso. Contenuto zero, contesto zero.

**Terzo tentativo**: ritaglio più alto (750px, header più una porzione di contenuto reale) e un taglio netto con una linea di accento blu invece della dissolvenza. Finalmente qualcosa di leggibile e riconoscibile — ma mancava ancora qualcosa.

## L'osservazione che ha cambiato tutto

A quel punto ho notato una cosa banale ma rivelatrice: la copertina, da sola, non "sapeva" se sarebbe stata vista su una pagina chiara o scura. Un'immagine con il nuovo sito fotografato in tema scuro, su una pagina già scura, si mimetizza — poco contrasto, poco impatto. La stessa immagine su una pagina chiara, invece, risalta.

La soluzione ovvia, una volta vista: **due copertine per articolo**, una con il nuovo sito fotografato in chiaro e una in scuro, mostrate in alternativa a seconda del tema con cui il lettore sta guardando il sito in quel momento — sempre quella che fa più contrasto.

## Catturare uno screenshot "in chiaro" quando il browser insiste per lo scuro

Qui la parte tecnicamente più interessante. Il sistema su cui lavoro preferisce il tema scuro, quindi ogni screenshot headless usciva scuro di default. Ho provato i flag "giusti" di Chromium per forzare il tema chiaro:

```
--force-prefers-color-scheme=light
--blink-settings=preferredColorScheme=1
```

Nessuno dei due ha funzionato con questa versione di Edge headless — lo screenshot continuava a uscire scuro, senza errori, semplicemente ignorando il flag.

La soluzione che ha funzionato: **imposta la preferenza attraverso il sito stesso, non attraverso il browser**. Il selettore di tema di questo sito salva la scelta in `localStorage`. Ho creato una micro-pagina temporanea che imposta quel valore e reindirizza alla home:

{% raw %}```html
<script>
localStorage.setItem('theme', 'light');
location.href = '/';
</script>
```{% endraw %}

...e l'ho aperta con Edge headless usando un **profilo persistente** (`--user-data-dir`), in due passaggi separati: prima la micro-pagina (per scrivere il valore), poi lo screenshot della home vera e propria, riusando lo stesso profilo — così `localStorage` sopravviveva tra i due lanci del browser. Non elegantissimo, ma affidabile al 100%.

## L'implementazione finale: zero JavaScript

Con gli screenshot giusti in mano, l'ultimo pezzo è stato mostrare l'immagine corretta in base al tema — usando lo stesso meccanismo, puramente CSS, con cui questo sito gestisce già i tre stati automatico/chiaro/scuro:

```scss
.post-image--on-dark {
  display: none;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    .post-image--on-light { display: none; }
    .post-image--on-dark { display: block; }
  }
}

:root[data-theme="dark"] {
  .post-image--on-light { display: none; }
  .post-image--on-dark { display: block; }
}
```

Il markup diventa semplicemente due tag `<img>`, uno per variante:

{% raw %}```html
<img class="post-image post-image--on-light" src="cover.jpg">
<img class="post-image post-image--on-dark" src="cover-dark.jpg">
```{% endraw %}

Il browser scarica entrambe le immagini (un piccolo costo, accettabile per due JPEG leggeri) ma ne mostra sempre una sola, decisa dal CSS in base al tema corrente — nessun JavaScript aggiuntivo, nessun flash, nessuna richiesta extra.

## Cosa mi porto a casa, di nuovo

La versione finale delle copertine — quella che stai vedendo proprio ora, in cima a questo articolo — è il quinto tentativo, non il primo. Nessuno dei tentativi precedenti era "sbagliato" in senso tecnico: producevano tutti un'immagine valida. Erano semplicemente poco convincenti, ed è stato solo continuando a guardarli con occhio critico — mio, non del codice — che è emerso il problema vero: un'immagine statica non può sapere in che contesto verrà mostrata, a meno che non gliene costruisci due e lasci decidere il CSS.

Anche questo, alla fine, è un dettaglio che nessuno noterà consciamente. Ma se il sito regge bene sia in chiaro che in scuro, è anche per questo pomeriggio passato a litigare con i flag di un browser headless.

**Nella [parte 4]({{ '/blog/progetti-personali/il-nuovo-sito-parte-4-le-ultime-finiture/' | relative_url }})**, l'ultima di questa serie: le rifiniture minori ma necessarie trovate ripassando il sito pezzo per pezzo.
