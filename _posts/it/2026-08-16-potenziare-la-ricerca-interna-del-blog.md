---
title: "Potenziare la ricerca interna del blog"
layout: post
date: '2026-08-16 15:32:00'
description: La ricerca del blog cercava solo in titolo e descrizione, ignorava le pagine statiche e non capiva le query a più parole. Come l'ho resa migliore senza librerie esterne.
intro: "A volte il miglioramento più utile non nasce da un bug, ma da un confronto: guardare come un altro progetto ha risolto lo stesso problema, e rubare le idee buone senza rubare anche le dipendenze."
lang: it_IT
categories:
- Progetti Personali
keywords: jekyll, ricerca, search, javascript, claude code
tags:
- jekyll
- claude-code
- ia
- javascript
- css
permalink: "/it/blog/progetti-personali/:title/"
redirect_from: "/blog/progetti-personali/potenziare-la-ricerca-interna-del-blog/"
icon: fa-search
---

Il sito è online da qualche giorno, le rifiniture principali sono fatte, e stavo scorrendo le funzionalità una per una per vedere cosa meritasse ancora attenzione. Mi sono fermato sulla lente di ricerca in alto a destra: funziona, ma non ho mai controllato davvero *quanto bene* funziona.

* TOC
{:toc}

## Cosa faceva, prima

La ricerca di questo blog è tutta lato client: alla build, Jekyll genera un `search.json` con titolo, URL e descrizione di ogni post; quando apri il pannello, un piccolo script scarica quel file una volta sola e, ad ogni tasto premuto, cerca la query come sottostringa dentro titolo e descrizione. Funzionale, ma con dei limiti concreti:

- **Le pagine statiche non c'erano.** Cercare "CV" non trovava la pagina CV, perché il JSON includeva solo `site.posts`.
- **Solo titolo e descrizione**, mai tag o categorie — un post taggato "kace" ma senza quella parola nel titolo non usciva cercando "kace".
- **Nessun match su più parole**: "claude code" veniva cercato come frase esatta, non come due parole da trovare entrambe, magari sparse fra campi diversi.
- **Nessun ranking**: i risultati uscivano nell'ordine cronologico dei post, non in base a quanto fossero pertinenti.

## Un confronto con un altro progetto

Ho anche un altro sito Jekyll che curo, quello del mio squadrone di **Elite: Dangerous** ([flottastellare.it](https://flottastellare.it) — ne ho scritto [qualche giorno fa]({{ '/it/blog/fuori-ufficio/flotta-stellare-quando-lapi-va-giu/' | relative_url }}), a proposito di un altro script rotto). Ha anche lui un motore di ricerca interno, decisamente più maturo: usa [Simple-Jekyll-Search](https://github.com/christian-fei/Simple-Jekyll-Search), una libreria di terze parti con qualche anno sulle spalle, con un `search.json` che include tag, categorie e data oltre a titolo e descrizione, e persino una tag cloud in fondo alla pagina di ricerca.

Idee valide, ma non tutte da copiare così come sono. Questo sito ha una regola precisa, dichiarata anche nel README ora che il tema è open source: **zero JavaScript di terze parti**. Aggiungere una libreria — per quanto piccola — solo per la ricerca avrebbe rotto quella regola per un guadagno che potevo ottenere anche scrivendo poche righe in più a mano.

## Cosa ho portato, e come

**Più contenuto indicizzato.** Il `search.json` ora include, oltre ai post, tutte le pagine che usano un layout "di contenuto" (`page`, `category`, `blog-index`) — CV, Progetti, Contatti, le pagine legali, l'indice del blog e tutte le pagine categoria. Cercare "CV" ora trova la pagina CV.

**Ricerca su più campi.** Ogni voce del JSON porta con sé anche tag e categorie (uniti in una stringa), non solo titolo e descrizione. La funzione di match adesso guarda dentro tutti questi campi.

**Query a più parole, in AND.** La query viene spezzata in parole; un elemento risulta un match solo se *ogni* parola è presente da qualche parte (titolo, descrizione, tag o categoria) — non serve più che compaiano vicine o nell'ordine esatto.

**Un ranking minimo, ma sensato.** Ogni parola trovata nel titolo vale 3 punti, ogni parola trovata altrove ne vale 1; i risultati sono ordinati per punteggio decrescente. Cercare "kace" fa uscire per prima la pagina categoria Kace e i post che hanno "Kace" nel titolo, poi quelli che ce l'hanno solo nei tag — invece dell'ordine cronologico casuale di prima.

{% raw %}```js
function scoreItem(item, words) {
  var title = (item.title || '').toLowerCase();
  var rest = [item.description, item.tags, item.categories]
    .filter(Boolean).join(' ').toLowerCase();

  var score = 0;
  for (var i = 0; i < words.length; i++) {
    var inTitle = title.indexOf(words[i]) !== -1;
    var inRest = rest.indexOf(words[i]) !== -1;
    if (!inTitle && !inRest) return null; // AND: una parola assente esclude il risultato
    score += inTitle ? 3 : 1;
  }
  return score;
}
```{% endraw %}

**Un estratto sotto ogni risultato**, non più solo il titolo nudo — così si capisce perché quel risultato è uscito, prima ancora di cliccarci sopra.

## Un bug silenzioso trovato per strada

Scrivendo il nuovo `search.json` ho notato che quello vecchio inseriva titolo e descrizione nel JSON senza nessun escaping:

{% raw %}```liquid
"title" : "{{ post.title }}",
```{% endraw %}

Nessuno dei titoli attuali contiene virgolette doppie, quindi non si era mai rotto — ma sarebbe bastato un titolo con un `"` dentro per generare un JSON non valido e far fallire silenziosamente `fetch('/search.json').then(r => r.json())` su tutto il sito, senza errori visibili se non aprendo la console. Corretto usando il filtro `jsonify` di Liquid, che serializza il valore in JSON corretto invece di inserirlo come stringa grezza:

{% raw %}```liquid
"title" : {{ post.title | jsonify }},
```{% endraw %}

## Verificare uno script che scarica dati e aggiorna il DOM, da terminale

L'ultima parte è stata la più scomoda, nel senso buono: come si verifica in automatico — senza aprire davvero un browser e digitare — che una ricerca javascript funzioni? Ho scritto una pagina di prova temporanea che apre il pannello, digita "kace" nel campo e scrive i risultati nel DOM, poi l'ho fotografata con Microsoft Edge headless.

Primo tentativo, fallito: uno screenshot semplice cattura la pagina subito dopo il caricamento, senza aspettare che i `setTimeout` dello script di prova (e la vera chiamata `fetch` al `search.json` reale) abbiano il tempo di completarsi — risultato, uno screenshot con la casella di ricerca ancora vuota. Secondo tentativo: alzare il "budget di tempo virtuale" di Chromium (`--virtual-time-budget`) a un valore abbondante, cosa che permette al browser di far avanzare timer e rete anche in modalità headless prima di scattare la foto. Con margine sufficiente (6 secondi virtuali), lo script ha avuto tutto il tempo di aprire il pannello, scaricare `search.json` davvero e mostrare i risultati — verificati poi anche con lo stile reale del sito, non solo con la logica nuda.

## Cosa mi porto a casa

Non è stato un lavoro nato da una segnalazione o da un bug in produzione — è nato da una domanda pigra ("come funziona quell'altro sito?") che si è rivelata utile. A volte il modo più veloce per migliorare qualcosa non è inventarsi la soluzione da zero, ma guardare come l'ha già risolta un progetto simile, capire cosa vale la pena portare a casa e cosa no — e nel farlo, trovare pure un bug che dormiva lì da mesi senza che nessuno se ne accorgesse.
