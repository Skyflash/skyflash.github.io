---
title: "Il nuovo sito, parte 2: i bug nascosti in un sito nuovo di zecca"
layout: post
date: '2026-08-12 18:20:00'
description: "Cinque bug scoperti dopo il lancio del nuovo sito: non debito tecnico ereditato, ma difetti nati lo stesso pomeriggio. Cascata CSS, rate limit di GitHub e un bug di Jekyll."
intro: "Un sito nuovo di zecca, costruito da zero in poche ore, dovrebbe essere pulito. Il mio ha nascosto cinque bug tutt'altro che banali — scoperti uno alla volta, nelle ore successive al lancio, mentre lo usavo davvero."
image: "/static/assets/img/blog/nuovo-sito-2026/parte2-cover.jpg"
image_dark: "/static/assets/img/blog/nuovo-sito-2026/parte2-cover-dark.jpg"
lang: it_IT
categories:
- Progetti Personali
keywords: jekyll, debugging, css, jekyll-paginate, github api, dark mode, claude code
tags:
- jekyll
- debugging
- claude-code
- css
- ia
permalink: "/it/blog/progetti-personali/:title/"
redirect_from: "/blog/progetti-personali/il-nuovo-sito-parte-2-i-bug-nascosti-in-un-sito-nuovo/"
icon: fa-bug
---

Nella [prima parte]({{ '/it/blog/progetti-personali/il-nuovo-sito-parte-1-perche-ripartire-da-zero/' | relative_url }}) ho raccontato perché ho deciso di ricostruire questo sito da zero, insieme a Claude Code, e come l'intero lavoro si sia concluso in un pomeriggio invece che in settimane. Quello che non ho detto è che, appena ho iniziato a usare il sito nuovo per davvero — cliccando in giro, cambiando tema, aggiungendo contenuti — sono saltati fuori bug che il codice, da solo, non avrebbe mai rivelato. Codice scritto quel pomeriggio stesso, non debito ereditato dal 2019.

Qui ci sono i cinque più interessanti.

* TOC
{:toc}

## 1. Il bottone sottolineato che non voleva saperne

Il primo problema evidente: il bottone "Scarica il CV in PDF" con il testo sottolineato, bruttissimo, in mezzo a un componente che doveva essere un bottone pieno. Stessa cosa era già successa sulle card della pagina Contatti.

La causa: le pagine come CV e Contatti avvolgono il loro contenuto in un contenitore `.prose`, pensato per lo stile tipografico degli articoli del blog (dove i link *devono* essere sottolineati, per leggibilità e accessibilità). La regola CSS era:

```scss
.prose a {
  text-decoration: underline;
}
```

Il problema è che un bottone (`<a class="btn">`) o una card cliccabile (`<a class="card">`), quando si trovano dentro un paragrafo `<p>` dentro `.prose` — come capita spesso, per semplice comodità di markup — vengono presi in pieno da questa regola, che ha più specificità della classe del componente stesso. Ho ristretto la regola al vero testo discorsivo:

```scss
.prose p a:not(.btn):not(.pill):not(.card),
.prose li a:not(.btn):not(.pill):not(.card),
.prose blockquote a:not(.btn):not(.pill):not(.card) {
  text-decoration: underline;
}
```

Non basta scrivere "solo i link nei paragrafi vanno sottolineati" — bisogna anche escludere esplicitamente i componenti che, per comodità di impaginazione, finiscono dentro un paragrafo pur non essendo testo.

## 2. Il tema chiaro che si perdeva a ogni pagina

Avevo costruito un selettore Automatico/Chiaro/Scuro con uno script che, nell'`<head>`, legge la preferenza salvata e la applica *prima* del disegno della pagina, per evitare il classico "flash" del tema sbagliato. Cliccavo "Chiaro", funzionava. Cambiavo pagina, tornava scuro.

Il colpevole: **Brave**. Il browser blocca, per motivi di privacy, gli script inline (come quello nell'`<head>`) in certe condizioni, pur lasciando passare i file `.js` esterni. Il pulsante mostrava comunque "Chiaro" come selezionato — perché quello stato veniva letto correttamente da `localStorage` da un file esterno — ma nessuno riapplicava davvero l'attributo sulla pagina.

La correzione: non fidarsi che lo script inline avesse fatto il suo lavoro. Il file esterno ora riapplica sempre l'attributo all'avvio, invece di limitarsi ad aggiornare l'aspetto del pulsante:

```js
var initialChoice = currentChoice();
applyAttribute(initialChoice);   // non solo updateButtons(initialChoice)
updateButtons(initialChoice);
```

Ridondante, se lo script inline funziona. Indispensabile, quando (per qualsiasi motivo, non solo Brave) non funziona.

## 3. Le stelline di GitHub sparite

Le card dei miei progetti mostrano stelle e fork presi in diretta dalla GitHub API. Funzionava, poi improvvisamente tutti i numeri sono spariti, sostituiti da un trattino.

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 0
```

L'API pubblica di GitHub, senza autenticazione, concede **60 richieste all'ora per indirizzo IP**. Tra i miei test e i ricaricamenti della pagina durante lo sviluppo, l'avevamo esaurita — e con 5 repository interrogati a ogni caricamento della pagina Progetti, in produzione sarebbero bastate 12 visite in un'ora per rifare lo stesso danno.

Non un bug da correggere, ma un limite strutturale da progettare meglio: ho aggiunto una cache lato client di 6 ore in `localStorage`, così visite ripetute non richiamano l'API ogni volta.

## 4. Le pillole delle categorie che puntavano nel vuoto

Dopo aver rinominato le categorie del blog — "Kace" è rimasta "Kace", ma "Tools" è diventata "Strumenti", "ITIL" è diventata "Filosofia di Lavoro" — le pillole colorate sulle card dei post (quelle che mostrano la categoria e ci si clicca sopra) hanno iniziato a puntare a URL che non esistevano. Il codice faceva semplicemente:

{% raw %}```liquid
<a class="pill" href="{{ category | downcase | prepend: '/' | relative_url }}">
```{% endraw %}

Funzionava per puro caso quando il nome della categoria coincideva con lo slug dell'URL (`Kace` → `/kace/`). Rinominando "Strumenti" (URL reale: `/tools/`), quella logica ha iniziato a generare `/strumenti`, una pagina inesistente. La correzione: cercare davvero l'URL configurato, invece di indovinarlo:

```liquid
{% raw %}{% assign cat_data = site.data.blog | where: "name", category | first %}
<a class="pill" href="{{ cat_data.href | relative_url }}">{% endraw %}
```

Una riga di scorciatoia che ha funzionato per caso finché i nomi non sono cambiati — il tipo di bug che resta invisibile finché qualcuno, mesi dopo, decide di rinominare qualcosa.

## 5. Quattro pagine, un solo file (quello di Jekyll)

Questo è stato il più tosto. Volevo la paginazione degli articoli del blog (utile quando supereranno i 15 post), e ho aggiunto il plugin `jekyll-paginate`. Impostato tutto, build pulita, nessun errore — ma abbassando temporaneamente il numero di post per pagina per testare davvero il meccanismo, Jekyll ha iniziato ad avvisarmi:

```
Conflict: The following destination is shared by multiple files.
  C:/.../blog/index.html
   - blog/index.html
   - blog/index.html
   - blog/index.html
   - blog/index.html
```

Quattro pagine diverse (pagina 1, 2, 3, 4), tutte scritte nello stesso identico file. Ho dovuto leggere il codice sorgente di Jekyll stesso per capire perché: la mia pagina `blog/index.html` aveva un `permalink: /blog/` esplicito nel front matter. Il plugin di paginazione crea copie della pagina per ogni "numero" (assegnando a ciascuna una diversa sotto-cartella), ma se il file ha un permalink fisso nel front matter, **quel valore vince sempre**, a prescindere dalla cartella assegnata alla copia — perché nel codice di Jekyll, il metodo che calcola l'URL di una pagina dà priorità assoluta al permalink esplicito:

```ruby
# jekyll/page.rb
def permalink
  data.nil? ? nil : data["permalink"]
end
```

Tutte e quattro le copie, leggendo lo stesso file sorgente, ereditavano lo stesso permalink fisso. La correzione, una volta capita la causa, è stata la più semplice di tutte: **togliere** il permalink esplicito. Il file si chiama `index.html` e vive nella cartella `blog/` — Jekyll gli assegna già `/blog/` da solo, senza bisogno di forzarlo, e a quel punto le pagine successive (`/blog/pagina2/`, `/blog/pagina3/`...) si generano correttamente.

## Cosa mi porto a casa

Nessuno di questi cinque bug era debito tecnico ereditato — erano tutti in codice scritto quello stesso pomeriggio. La lezione non è "l'IA scrive codice pieno di bug": è che **qualsiasi codice, scritto da chiunque, va usato davvero per scoprire dove si rompe**. La differenza, lavorando con Claude Code, è stata la velocità con cui ogni bug — dalla sottolineatura CSS al codice sorgente di Jekyll — è stato isolato, spiegato e corretto, quasi sempre nell'arco della stessa conversazione in cui l'ho segnalato.

Un sito nuovo, costruito in un pomeriggio, con la stessa attenzione ai dettagli che normalmente richiederebbe settimane. Continuo a scoprirne di nuovi, probabilmente — ma per ora, il sito che vedete è quello.

**C'è anche una [parte 3]({{ '/it/blog/progetti-personali/il-nuovo-sito-parte-3-le-copertine-che-si-adattano-al-tema/' | relative_url }})**, più leggera: la storia di come sono nate le copertine di questi stessi articoli.
