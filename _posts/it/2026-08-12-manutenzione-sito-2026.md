---
title: "Manutenzione straordinaria del sito: quando aggiornare le dipendenze rompe tutto (e perché non si era mai rotto prima)"
layout: post
date: '2026-08-12 14:00:00'
description: Cosa succede quando aggiorni sul serio, per la prima volta dal 2019, le dipendenze di un sito Jekyll. Tre bug dormienti, un tema compilato con la libreria sbagliata da anni, e come li ho trovati e sistemati tutti in un pomeriggio.
intro: "Oggi ho aggiornato le dipendenze di questo sito (Ruby, Jekyll, npm, Bootstrap, Chart.js) per la prima volta sul serio dal 2019. Risultato: il sito si è rotto quasi subito. La cosa interessante non è che si sia rotto, ma perché non si era mai rotto prima."
image: "/static/assets/img/blog/manutenzione-sito-2026/cover.jpg"
lang: it_IT
categories:
- Progetti Personali
permalink: "/it/blog/progetti-personali/:title/"
redirect_from:
  - "/blog/progetti-personali/manutenzione-sito-2026/"
  - "/blog/tools/manutenzione-sito-2026/"
keywords: jekyll, npm, bootstrap, chart.js, dependency update, manutenzione, dependabot, uglify-js
tags:
- jekyll
- npm
- ruby
- bootstrap
- chart.js
- dependabot
- manutenzione
- debugging
icon: fa-wrench
---

Questo sito gira su Jekyll da anni, con un tema (Jalpc) basato su Bootstrap, jQuery e qualche libreria JS per grafici e animazioni. Come capita spesso ai side-project personali, negli ultimi anni l'ho tenuto vivo solo dal punto di vista dei contenuti, lasciando che Dependabot aprisse pull request di aggiornamento dipendenze in automatico, quasi sempre mergiate a scatola chiusa perché "tanto sono solo numeri di versione".

Oggi ho deciso di fare pulizia sul serio: verificare gemme Ruby e pacchetti npm, aggiornarli davvero, e assicurarmi che il sito continuasse a funzionare. Quello che è successo è stata una piccola lezione di archeologia informatica.

* TOC
{:toc}

## Il problema di partenza: una build congelata dal 2019

La prima cosa che ho scoperto è che gli asset compilati del sito (i file CSS/JS minificati in `static/assets/`) portavano tutti la data **20190620** nel nome. Sei anni di pull request di Dependabot avevano alzato pian piano i numeri di versione dichiarati in `package.json` — Bootstrap da 3 a 4 a 5, Chart.js da 2 a 4, Font Awesome da 4 a 5 — ma **nessuno aveva mai più eseguito `npm run build`** da allora.

Il sito pubblicato, quindi, funzionava benissimo per un motivo molto semplice: stava ancora servendo i bundle compilati nel 2019, con le librerie di allora. `package.json` diceva una cosa, i file effettivamente in produzione ne dicevano un'altra. Due sistemi paralleli che non si parlavano da anni.

Appena ho lanciato una build vera, questa finzione è crollata tutta insieme.

## Aggiornare Ruby e Jekyll

Prima ostacolo: Jekyll 4.2.2 (versione dichiarata nel `Gemfile.lock`) non partiva più su Ruby 3.4, l'unica installata sulla macchina. Ruby 3.4 ha smesso di includere `csv`, `logger` e `bigdecimal` come gemme di default, e Jekyll 4.2.2 le usava senza dichiararle esplicitamente. Anche risolto quello, Liquid 4.0.3 (il motore dei template di Jekyll) chiamava `String#tainted?`, un metodo rimosso da Ruby 3.2 in poi.

Soluzione: aggiornare Jekyll a 4.4.1, che dichiara correttamente le sue dipendenze, e Liquid alla patch 4.0.4 che risolve il problema di `tainted?`.

## Ripulire npm: 25 vulnerabilità, quasi tutte fantasma

Sul lato npm la sorpresa è stata diversa. `npm audit` segnalava **25 vulnerabilità**, ma scavando ho trovato che il `package.json` conteneva pacchetti come `@npmcli/arborist`, `hosted-git-info`, `jsprim` e persino **`npm` stesso**, elencato come dipendenza del progetto. Nessuno di questi veniva mai usato da una riga di codice del sito: erano tutti finiti lì, probabilmente, come effetto collaterale di vecchi `npm audit fix` che avevano promosso dipendenze transitive a dipendenze dirette invece di usare gli `overrides`.

Rimuovendo i pacchetti morti (verificato con una ricerca sull'intero repository, zero riferimenti):

```
25 vulnerabilità → 0
431 pacchetti installati → 40
```

Nessun codice toccato, solo pulizia.

## Il sito si rompe: colpa di Bootstrap 5 (che in realtà non esiste)

Con le dipendenze pulite e aggiornate, ho lanciato per la prima volta in anni una vera ricompilazione degli asset. Il sito è diventato illeggibile: menu di navigazione non collassato, sezioni impilate senza layout, icone sparite.

La causa: il bundle CSS compilato nel 2019 conteneva **Bootstrap v3.4.1**. Tutto il markup del tema — layout, header, sezioni della landing page — è scritto con classi Bootstrap 3 (`navbar-default`, `navbar-fixed-top`, `col-lg-*`...). Ma `package.json` dichiarava da tempo `bootstrap: "^5.0.0"`, mai realmente compilato contro quel markup. Il numero "5" in `package.json` era, di fatto, una bugia mai verificata.

Ho riportato Bootstrap a `^3.4.1`, l'unica versione compatibile con il tema così com'è. Bootstrap 3 è però a fine vita: porta con sé due vulnerabilità XSS moderate in popover/tooltip mai patchate. Rischio pratico basso (il sito non inserisce mai contenuto utente in quei componenti), ma è un compromesso consapevole, in attesa di una revisione più profonda del tema.

## Il grafico delle competenze sparito: Chart.js v2 vs v4

Nella sezione "Cosa so fare" della home c'è un grafico radar (Chart.js) con le mie competenze. Dopo la ricompilazione, spazio vuoto. Il codice della pagina configurava il grafico così:

```js
options: {
    scale: { ticks: {min: 0, max: 100}, pointLabels: {fontSize: 14} },
    legend: { display: false },
}
```

Sintassi di **Chart.js 2**. Nella versione 4 (quella effettivamente installata da tempo) la configurazione è cambiata: `scale` è diventato `scales.r`, `legend` è finito dentro `plugins`. La vecchia sintassi non generava errori, semplicemente veniva ignorata in silenzio, e il grafico non si disegnava.

```js
options: {
    responsive: true,
    scales: { r: { min: 0, max: 100, pointLabels: {font: {size: 14}} } },
    plugins: { legend: { display: false } },
}
```

Cinque righe, e il radar è tornato visibile.

## Il bundle JavaScript da 228 byte

Questo è stato il bug più subdolo. Lo script di build (`build/build.js`) passa a **UglifyJS** l'elenco dei percorsi dei file da minificare e concatenare — jQuery, Bootstrap, Chart.js, eccetera. Dopo la ricompilazione, il file JS finale pesava **228 byte** invece delle solite centinaia di KB, e conteneva, testuale:

```
node_modules,jquery,dist,jquery.js,static,js,bs3,typeahead.js,node_modules,bootstrap,...
```

I percorsi dei file, non il loro contenuto. UglifyJS li aveva interpretati come *codice sorgente* — ogni `/` letto come operatore di divisione tra variabili — invece di leggerli da disco. Il motivo: **UglifyJS 3.x ha cambiato API**. Nella versione 2 (quella in uso nel 2019), passare un array di percorsi significava "leggi questi file da disco". Nella 3.x, un array di stringhe viene trattato come codice sorgente letterale: bisogna leggere i file esplicitamente e passare un oggetto `{nomefile: contenuto}`.

Il bug è nato probabilmente anni fa, quando `uglify-js` è stato aggiornato alla v3 da una PR di Dependabot — ma è rimasto dormiente, invisibile, perché nessuno rieseguiva più la build. Corretto leggendo i file esplicitamente prima di passarli a UglifyJS, e aggiunto un controllo sugli errori che prima veniva ignorato silenziosamente.

## Le icone sparite: Font Awesome 4 vs 5

Ultimo tassello: le iconcine sui bottoni (Linux, Apple, i social nella sezione "Chi sono") erano vuote. Lo script di build puntava a `node_modules/components-font-awesome/css/font-awesome.css` — file che **non esiste più** in Font Awesome 5, che ha riorganizzato i CSS in `all.css` più uno shim (`v4-shims.css`) per la retrocompatibilità con i vecchi nomi di classe (`fa fa-linux`, usati ovunque nel tema). Il riferimento al file mancante veniva ignorato silenziosamente dal compressore CSS, proprio come il resto.

Corretto puntando ai file giusti e copiando i webfont di Font Awesome 5 nella cartella corretta (un dettaglio non banale: i percorsi relativi dentro il CSS compilato si risolvono rispetto alla posizione del bundle finale, non rispetto alla posizione originale dei file sorgente — un'altra assunzione implicita che nessuno aveva mai verificato).

## Il filo conduttore

Quattro bug, quattro cause diverse, ma un solo colpevole comune: **una pipeline di build che nessuno eseguiva più**. Dependabot aggiornava fedelmente i numeri di versione, il sito pubblicato continuava a funzionare (perché serviva asset compilati anni prima), e il divario fra "quello che il progetto dichiara" e "quello che il progetto effettivamente pubblica" cresceva silenzioso, versione dopo versione.

Nessuno di questi bug avrebbe causato danni se qualcuno avesse rilanciato una build ogni tanto. La lezione, come spesso capita, non è tecnica ma di processo: gli aggiornamenti automatici delle dipendenze sono utili, ma senza una build (e magari un deploy) che li verifichi regolarmente, si accumula un debito invisibile che esplode tutto insieme, il giorno che qualcuno ricomincia a guardare.

## E adesso?

Il sito torna a funzionare com'era prima, con le dipendenze aggiornate dove ha senso farlo (Ruby, Jekyll, npm) e bloccate dove non lo ha, come Bootstrap 3, in attesa di qualcosa di più definitivo: sto lavorando a una versione completamente nuova di questo sito, con un aspetto più moderno, mantenendo però intatti tutti i permalink degli articoli del blog per non perdere l'indicizzazione su Google. Ne parlerò presto.
