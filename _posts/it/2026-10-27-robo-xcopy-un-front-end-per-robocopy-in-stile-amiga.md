---
title: "Robo-XCopy: un front end per robocopy in stile Amiga, scritto in Rust in due ore e mezza"
layout: post
date: '2026-10-27 09:00:00'
description: "Robo-XCopy è un programma gratuito e open source per Windows che mette robocopy dietro una schermata in stile X-Copy dell'Amiga: un solo .exe da 5 MB, anteprima con DRY RUN, costruttore dei flag e log. Com'è nato in due ore e mezza con Claude Code, e cosa ha scoperto la prova su robocopy vero."
intro: "Robocopy è il miglior strumento di copia che Windows abbia già dentro, e nessuno ricorda i suoi parametri. Ieri ho passato due ore e mezza a dargli una faccia: quella dell'X-Copy dell'Amiga."
social:
  default: |-
    Robocopy è il miglior strumento di copia che Windows abbia già dentro, e nessuno ricorda i suoi parametri.

    Ieri, in due ore e mezza di lavoro con Claude Code, è nato Robo-XCopy: un front end grafico in Rust, con la schermata dell'X-Copy dell'Amiga. Un solo .exe da 5 MB, nessun installer, DRY RUN per vedere cosa succederebbe prima di toccare qualcosa, e il comando esatto sempre sotto gli occhi.

    La parte che mi è piaciuta di più: i test lanciano robocopy vero, e così sono saltati fuori comportamenti che nessuna documentazione dice chiaramente.

    È gratuito, open source (MIT) e c'è anche una versione "Classic" in nero, argento e verde.

    Voi che strumento da riga di comando vorreste vedere con una faccia più amichevole?
  threads: "Robocopy è il miglior strumento di copia di Windows e nessuno ricorda i suoi parametri. Ieri ho scritto, con Claude Code, Robo-XCopy: un front end in Rust con la schermata dell'X-Copy dell'Amiga. Un .exe da 5 MB, gratuito e open source. Quale strumento da riga di comando vorreste vedere con un'interfaccia?"
image: "/static/assets/img/blog/roboxcopy/cover.png"
lang: it_IT
featured: true
categories:
- Progetti Personali
keywords: robo-xcopy, robocopy, front end robocopy, gui robocopy, interfaccia grafica robocopy, amiga, x-copy, rust, egui, windows, claude code, open source
tags:
- robo-xcopy
- robocopy
- rust
- amiga
- claude-code
- open-source
permalink: "/it/blog/progetti-personali/:title/"
redirect_from: "/blog/progetti-personali/robo-xcopy-un-front-end-per-robocopy-in-stile-amiga/"
translation_key: robo-xcopy
icon: fa-copy
---

**Robocopy** è lo strumento di copia che Windows ha già dentro, ed è il migliore che ci sia: copia, specchia, sposta, riprova se la rete cade, conserva permessi e date. Il guaio è che i suoi parametri non li ricorda nessuno. Chi lo usa lo fa con una pagina di appunti aperta accanto, e il giorno in cui sbaglia un `/MIR` si accorge che cancella anche quello che non voleva.

Ieri ho costruito **Robo-XCopy**: una piccola interfaccia grafica per robocopy, con la schermata dell'**X-Copy** dell'Amiga, il programma con cui si copiavano i dischetti. È gratuito, open source, e si scarica da [roboxcopy.com](https://roboxcopy.com/).

* TOC
{:toc}

## Cos'è e come si usa

Un solo file `.exe` da circa 5 MB, senza installer e senza niente da installare prima. Si scelgono cartella di origine e di destinazione, si spuntano le opzioni e si preme **START**.

<img class="post-image" src="{{ '/static/assets/img/blog/roboxcopy/cover.png' | relative_url }}" alt="La schermata di Robo-XCopy nel tema Modern Amiga">

Le cose che ho voluto fin dall'inizio:

- **DRY RUN.** Mostra cosa farebbe robocopy (è il suo `/L`) senza toccare niente. Prima di uno specchio è l'unico pulsante da premere.
- **Il comando sempre visibile.** Ogni scelta cambia la riga di comando che il programma sta per lanciare, e la stessa riga è stampata in cima al log. Chi vuole imparare robocopy lo impara guardando.
- **Il COPY BUILDER.** Ogni flag di `/COPY` e `/DCOPY` con una frase che spiega cosa fa, invece di lettere da ricordare (`DATSOU`).
- **Avanzamento in diretta**: un file contato alla volta nella griglia delle tracce, come nell'originale.
- **Il log dove si vuole**, e il programma che sa quando servono i diritti di amministratore e, se serve, si riavvia da solo.

<img class="post-image" src="{{ '/static/assets/img/blog/roboxcopy/builder.png' | relative_url }}" alt="Il COPY BUILDER di Robo-XCopy: ogni flag con la sua descrizione">

*Mirror* è l'opzione pericolosa: cancella nella destinazione quello che non c'è nell'origine. Il programma lo dice a chiare lettere, e la strada consigliata è sempre la stessa: prima DRY RUN.

## Due temi, perché l'Amiga era così

Con il pulsante **THEME** si passa da *Modern Amiga* (blu) a *Classic X-Copy*: nero, argento e verde, con le caselle della griglia riempite di zeri come sullo schermo di un tempo. La scelta viene ricordata fra un avvio e l'altro.

<img class="post-image" src="{{ '/static/assets/img/blog/roboxcopy/classic.png' | relative_url }}" alt="La schermata di Robo-XCopy nel tema Classic X-Copy">

Del programma originale ho preso solo l'idea della schermata. Il logo e la grafica sono altre cose, e l'icona (un dischetto con una X arancione) è disegnata a pixel in un file di testo, da cui si generano icona del programma, favicon e immagini del sito.

## Due ore e mezza, e come ci si arriva

Il codice l'ha scritto Claude Code, in Rust. Il metodo è quello degli altri progetti di questi mesi, dal [nuovo sito]({{ '/it/blog/progetti-personali/il-nuovo-sito-parte-1-perche-ripartire-da-zero/' | relative_url }}) all'[ACFS BGS Tool]({{ '/it/blog/progetti-personali/acfs-bgs-tool-elite-dangerous-claude-code/' | relative_url }}): decido io cosa deve fare e come deve sembrare, lui scrive, io guardo girare ogni modifica prima di accettarla. Il risultato sono circa 2.100 righe di Rust, e una suite di test che ne verifica il comportamento.

Le scelte tecniche, per chi è curioso:

- **egui**, con widget disegnati a mano su un'area di 640×330 che scala con la finestra. I pulsanti, le lampadine dei drive e le griglie non sono controlli di Windows: sono rettangoli e testo dipinti pixel per pixel, ed è per questo che la schermata è identica ovunque.
- **Nessuna libreria in più per parlare con Windows.** Servono poche chiamate (aprire un indirizzo web, sapere se il programma è elevato, riavviarlo come amministratore) e sono scritte direttamente.
- **Il programma non reinventa robocopy.** Lo lancia e ne legge l'output. I file si riconoscono dalla *forma* della riga (campi separati da tabulazione, una dimensione numerica) e non dal testo, perché robocopy stampa nella lingua di Windows: su un sistema italiano scrive "Nuovo file". Così funziona con qualsiasi lingua.

## Quello che ha insegnato robocopy vero

La parte che mi è piaciuta di più. I test sono 20, e molti non simulano robocopy: lo **lanciano davvero**, con tutte le opzioni che il costruttore può produrre. Sono saltate fuori cose che nessuna guida dice chiaramente:

- `/IPG` (la pausa fra i blocchi) insieme a `/MT` (più thread) fa uscire robocopy con errore 16 e **non copia niente**. Ora, se si imposta una pausa, il programma passa a un solo thread.
- `/B` (modalità backup) e il flag `U` di `/COPYALL` senza diritti di amministratore fanno rifiutare l'avvio. Su questo si basa la finestra che propone di riavviare come amministratore.
- `/XO` salta il file anche quando la copia di destinazione ha la *stessa* data, non solo una più recente.
- Un backslash prima delle virgolette di chiusura (`C:\`) rompe i parametri: i percorsi vengono normalizzati.

Una cosa invece l'ho trovata solo dopo la pubblicazione. La versione 0.1.0 importava `vcruntime140.dll`, cioè richiedeva il Visual C++ Redistributable, che un Windows appena installato non ha: da me partiva, altrove poteva non partire. L'ho scoperto elencando i nomi delle DLL dentro l'exe. Nella 0.1.1, uscita la sera stessa, la libreria C è collegata staticamente e l'exe cresce da 4,9 a 5,0 MB. È il tipo di errore che il computer dello sviluppatore non mostra mai.

## Limiti e prossimi passi

Il programma **non è ancora firmato**, quindi Windows può mostrare l'avviso di SmartScreen alla prima esecuzione (*Ulteriori informazioni*, poi *Esegui comunque*). Ogni versione pubblicata ha l'impronta SHA-256 e l'attestazione di build di GitHub, con cui si verifica che l'exe sia davvero quello compilato dal codice del repository. La firma è in preparazione, e la [pagina sulla firma del codice](https://roboxcopy.com/signing.html) spiega a che punto è.

Nella lista delle cose da fare ci sono un avanzamento complessivo vero (con una scansione iniziale per contare file e dimensione totale), i profili salvabili, una notifica a fine copia, il trascinamento delle cartelle sulla finestra, l'interfaccia in italiano e inglese, e un installer. Più avanti, in una fase a parte, vorrei valutare una modalità per clonare e cancellare dischi, con tutte le protezioni del caso.

## Provarlo

Il programma è su [roboxcopy.com](https://roboxcopy.com/), con una [guida passo passo](https://roboxcopy.com/howto.html). Il codice è su [GitHub](https://github.com/Skyflash/RoboXCopy), con licenza MIT.

È nato ieri e ha ancora pochissimi utenti. Se lo provate e qualcosa non va, o se c'è un'opzione di robocopy che vi manca nella schermata, scrivetemelo: è esattamente quello che mi serve. E voi, quale strumento da riga di comando vorreste vedere con una faccia più amichevole?
