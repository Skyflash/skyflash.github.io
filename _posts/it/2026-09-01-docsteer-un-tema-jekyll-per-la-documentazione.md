---
title: "DocSteer: un tema Jekyll per la documentazione"
layout: post
date: '2026-09-01 09:00:00'
description: "DocSteer è un tema Jekyll per documentazione tecnica, portali di supporto e knowledge base: ricerca live, sei skin con tema chiaro e scuro, indice automatico, lightbox e SEO. Senza framework, MIT, pubblicato come gem."
intro: "Una pagina di documentazione che esiste ma che nessuno riesce a trovare vale quanto una pagina che non è mai stata scritta. DocSteer è un tema Jekyll costruito attorno a quel problema."
image: "/static/assets/img/blog/docsteer/cover.png"
lang: it_IT
featured: true
categories:
- Progetti Personali
keywords: docsteer, jekyll, tema, documentazione, knowledge base, ricerca, dark mode, gem, github pages, claude code
tags:
- jekyll
- docsteer
- documentazione
- open-source
- claude-code
permalink: "/it/blog/progetti-personali/:title/"
redirect_from: "/blog/progetti-personali/docsteer-un-tema-jekyll-per-la-documentazione/"
translation_key: docsteer-jekyll-documentation-theme
icon: fa-compass
---

Chi lavora in IT passa una parte non piccola della giornata dentro documentazione: runbook, procedure, articoli di knowledge base, wiki interne che nessuno ha più aperto da un anno. E la parte difficile non è quasi mai scriverla — è farla ritrovare a chi ne ha bisogno mesi dopo, con un problema aperto e poca pazienza.

**DocSteer** è un tema Jekyll per esattamente quel tipo di sito: documentazione tecnica, portali di supporto, knowledge base interne. La barra laterale raggruppata, la ricerca e l'indice "In questa pagina" non sono decorazione — sono il motivo per cui il sito esiste.

* TOC
{:toc}

## Perché un altro tema per la documentazione

Di temi Jekyll per la documentazione ce ne sono già parecchi, e alcuni sono ottimi. Quello che volevo io era qualcosa di più stretto: un tema che si mettesse in piedi in un pomeriggio, che non trascinasse dentro una toolchain Node, e che non chiedesse di imparare un altro framework prima di poter scrivere la prima pagina.

Il tema di questo sito, che pure ho estratto e pubblicato a parte, non ci arrivava: è pensato per un sito personale bilingue con un CV, qualche pagina e un blog. La documentazione è un problema diverso. Serve una barra laterale raggruppata e collassabile, una ricerca che regga su decine di pagine, un indice costruito da solo, un pager avanti/indietro che segua l'ordine della navigazione. Sono tutte cose che si possono aggiungere a mano, una alla volta — ed è esattamente così che si finisce con un tema da blog pieno di pezze.

## Cosa fa

- **Sei skin di colore** — `aqua`, `violet`, `mint`, `ember`, `graphite`, `clay` — ognuna con variante chiara e scura, definite in un'unica mappa Sass ed emesse come custom property CSS. Il colore di brand di ogni skin supera il contrasto WCAG AA (4.5:1) sul proprio sfondo.
- **Tema scuro** che segue il sistema operativo, con toggle manuale salvato in `localStorage` e nessun lampo bianco al caricamento.
- **Ricerca live** — un indice JSON generato da Liquid e una modale da tastiera (<kbd>/</kbd> oppure <kbd>⌘K</kbd>), senza una sola libreria esterna.
- **Indice automatico** costruito dagli heading, con scroll-spy, e pager avanti/indietro che segue da solo l'ordine della navigazione.
- **Pagine FAQ** — `layout: faq` genera un accordion basato su `<details>` nativo, con un anchor per domanda, dati strutturati `FAQPage`, e ogni domanda indicizzata come risultato di ricerca a sé.
- **Lightbox immagini** con gallerie, didascalie e navigazione da tastiera.
- **Font Awesome 6.5.2 Free** incluso localmente di default, così il sito funziona offline e dietro i firewall aziendali. Il CDN resta un'opzione.
- **SEO** — `jekyll-seo-tag`, sitemap, feed RSS, Open Graph e JSON-LD.

Niente framework CSS, nessuno step di build Node: circa 7 kB di JavaScript vanilla in tutto, tutto `defer`, CSS compresso e Sass compilato da Jekyll.

Chiaro e scuro non sono due temi da mantenere in parallelo: sono la stessa mappa di custom property con valori diversi. Qui la pagina di configurazione tagliata a metà — chiaro a sinistra, scuro a destra — con barra laterale, indice e blocco di codice con pulsante di copia:

<img class="post-image" src="{{ '/static/assets/img/blog/docsteer/light-dark.png' | relative_url }}" alt="La stessa pagina di documentazione di DocSteer divisa a metà: tema chiaro a sinistra, tema scuro a destra">

Le sei skin si scelgono dal menu a tavolozza nella navbar, e ognuna ha la sua variante chiara e scura:

<img class="post-image post-image--on-light" src="{{ '/static/assets/img/blog/docsteer/skins-menu.png' | relative_url }}" alt="Il menu a tavolozza di DocSteer aperto nella navbar, con le sei skin: Aqua, Violet, Mint, Ember, Graphite, Clay">
<img class="post-image post-image--on-dark" src="{{ '/static/assets/img/blog/docsteer/skins-menu-dark.png' | relative_url }}" alt="Il menu a tavolozza di DocSteer aperto nella navbar, con le sei skin: Aqua, Violet, Mint, Ember, Graphite, Clay">

Cambiarla non tocca una riga di markup, solo delle custom property. Questa è la stessa identica pagina con la skin Violet:

<img class="post-image post-image--on-light" src="{{ '/static/assets/img/blog/docsteer/docs-violet.png' | relative_url }}" alt="La stessa pagina di documentazione con la skin Violet: accenti viola su barra laterale, indice e link">
<img class="post-image post-image--on-dark" src="{{ '/static/assets/img/blog/docsteer/docs-violet-dark.png' | relative_url }}" alt="La stessa pagina di documentazione con la skin Violet: accenti viola su barra laterale, indice e link">

La ricerca è la parte a cui tengo di più, perché è quella che decide se una knowledge base è consultabile o è solo un archivio. Si apre da tastiera e raggruppa i risultati per sezione mentre si digita:

<img class="post-image post-image--on-light" src="{{ '/static/assets/img/blog/docsteer/search.png' | relative_url }}" alt="La ricerca live di DocSteer: risultati raggruppati per sezione, con i termini cercati evidenziati">
<img class="post-image post-image--on-dark" src="{{ '/static/assets/img/blog/docsteer/search-dark.png' | relative_url }}" alt="La ricerca live di DocSteer: risultati raggruppati per sezione, con i termini cercati evidenziati">

## Perché "DocSteer"

**/dɒkˈstɪə/** — *dok-STÌR*, accento sulla seconda sillaba, in rima con l'inglese *beer*.

Il nome è la descrizione del mestiere. *To steer* vuol dire guidare, condurre: la barra laterale, il campo di ricerca e l'indice esistono solo per portare chi legge all'unica pagina che stava cercando. Una documentazione che non lo fa è una cartella di file Markdown con sopra un foglio di stile.

Il resto l'ho scoperto dopo: *steer*, in inglese, è anche un giovane bue. Non era assolutamente il piano. Ma come descrizione di qualcosa che si trascina dietro una pila enorme di documentazione senza mai lamentarsi è difficile darle torto, e ormai ci ho fatto pace.

## Come si usa

Due strade. **Come gem**, aggiungendola al `Gemfile`:

```ruby
gem "jekyll-theme-docsteer", "~> 1.0"
```

e poi nel `_config.yml`:

```yaml
theme: jekyll-theme-docsteer
plugins:
  - jekyll-seo-tag
  - jekyll-sitemap
  - jekyll-feed
```

Oppure **clonando il repo** come starter, per partire da un sito già popolato e svuotarlo man mano. La gem sta [su RubyGems](https://rubygems.org/gems/jekyll-theme-docsteer).

Tutte le opzioni del tema vivono sotto un'unica chiave `docsteer:` nel `_config.yml` — skin, tema, ricerca, lightbox e il resto:

```yaml
docsteer:
  skin: aqua          # aqua | violet | mint | ember | graphite | clay
  mode: auto          # auto (segue il sistema) | light | dark
  skin_switcher: true # mostra il menu a tavolozza nella navbar
  search:
    enabled: true
    collections: [docs]
    hotkey: true      # "/" e Cmd/Ctrl-K aprono la ricerca
  lightbox:
    enabled: true
```

La navigazione — navbar in alto e barra laterale raggruppata — sta tutta in `_data/navigation.yml`:

```yaml
sidebar:
  - title: Getting started
    icon: fa-solid fa-rocket
    children:
      - { title: Introduction, url: /docs/introduction/ }
      - { title: Installation, url: /docs/installation/ }
```

Il pager in fondo a ogni pagina segue da solo l'ordine di questo file: riordini la navigazione e "precedente/successivo" si aggiusta di conseguenza. Il deploy va su GitHub Pages (via Actions), Netlify, Vercel o Cloudflare Pages.

Demo dal vivo e documentazione completa su **[cristiancastellari.it/docsteer](https://cristiancastellari.it/docsteer/)**; codice su **[GitHub](https://github.com/Skyflash/docsteer)**.

## Come l'ho costruito

Mi sono fatto dare una mano da **Claude Code** (e da tanti, tanti token in Opus 5). La regola che mi sono dato è la stessa con cui ho [ricostruito questo sito]({{ '/it/blog/progetti-personali/il-nuovo-sito-parte-1-perche-ripartire-da-zero/' | relative_url }}) qualche settimana fa: prima il piano scritto, poi il codice. Quali layout servivano (`default`, `home`, `doc`, `page`), come strutturare l'indice di ricerca, cosa doveva restare configurabile da un solo file — deciso e messo nero su bianco prima di aprire un editor.

Poi l'implementazione un pezzo alla volta, ricompilando e guardando il risultato prima di passare al successivo. Non è pignoleria: su un tema, quando salti la verifica, il bug non lo trovi tu — lo trova chi lo installa.

Il che non vuol dire che ne sia uscito perfetto. DocSteer ha già due release alle spalle nello stesso giorno della 1.0.0, e sono tutte cose che si vedono solo *usando* il tema, non costruendolo: il burger della navbar non apriva niente fuori dalle pagine di documentazione, i tag in fondo agli articoli erano badge inerti invece di aprire la ricerca, e l'indice di ricerca poteva arrivare dalla cache del browser anche dopo aver pubblicato pagine nuove. Le ho sistemate nella 1.1.0 e nella 1.1.1.

## Cosa manca ancora

Per onestà, due cose che so già.

I sorgenti Sass usano ancora `@import`. Dart Sass stampa avvisi di deprecazione — la build è per il resto pulita — e la migrazione a `@use`/`@forward` è pianificata, ma tocca ventuno file e in un tema l'output visivo *è* il prodotto: una regressione su una delle sei skin, in chiaro o in scuro, resta invisibile finché non la segnala qualcuno. Preferisco farla con calma.

E gli anchor delle domande nelle pagine FAQ derivano dal testo della domanda: riformularla cambia il frammento URL e rompe i deep link già condivisi. Correggere un refuso è sicuro, riscrivere una domanda va pesato.

## Perché è gratis

Il tema è MIT, per uso personale e commerciale, senza obbligo di attribuzione: il credito in fondo si toglie da configurazione.

Le cose che ho fatto gratis — la [traduzione di Morrowind]({{ '/it/blog/fuori-ufficio/la-traduzione-di-morrowind-e-bloodmoon/' | relative_url }}), [quella di Twitter]({{ '/it/blog/fuori-ufficio/twittero-in-italiano-anche-io/' | relative_url }}), un [convertitore per telefoni DECT]({{ '/it/blog/tools/ipui-to-ipei/' | relative_url }}) che apro forse una volta all'anno — sono quelle che alla fine hanno aiutato più persone, e quasi sempre in silenzio: nessun commento, nessuna mail, solo qualcuno dall'altra parte del mondo che ha risolto il suo problema e ha chiuso la scheda.

Un tema per la documentazione ha esattamente lo stesso profilo. Se fa risparmiare una giornata a qualcuno che non incontrerò mai, è già valsa la pena scriverlo — e se vuole [offrirmi un caffè](https://www.buymeacoffee.com/cristiancastellari), tanto meglio.
