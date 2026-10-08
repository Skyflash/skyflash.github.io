---
title: "ACFS BGS Tool: quattro giorni con Claude Code per il BGS di Elite Dangerous"
layout: post
date: '2026-10-08 09:00:00'
description: "Come ho costruito con Claude Code, in quattro giorni, l'ACFS BGS Tool per il mio squadrone di Elite Dangerous: un fork del progetto open source dei Canonn, dati Spansh aggiornati da GitHub Actions e le decisioni che l'AI non poteva prendere."
intro: "Non sono uno sviluppatore, e Angular non lo so scrivere. In quattro giorni, però, il mio squadrone di Elite Dangerous ha avuto il suo strumento per il BGS. Il codice l'ha scritto Claude Code. Le decisioni le ho prese io, e sono state la parte difficile."
social:
  default: |-
    Non sono uno sviluppatore, e Angular non lo so scrivere. In quattro giorni, però, il mio squadrone di Elite Dangerous ha avuto il suo strumento per il BGS: l'ACFS BGS Tool.

    Il codice l'ha scritto Claude Code, partendo dal progetto open source dei Canonn. Io ho deciso cosa doveva fare e ho visto girare ogni modifica prima di accettarla.

    La lezione più utile? Il codice può essere coerente e sbagliato allo stesso tempo. Quello che lo rende giusto è la conoscenza del dominio, e quella l'assistente non ce l'ha.

    Voi avete mai costruito uno strumento per una community o per un hobby? Con quali aiuti?
  threads: "In quattro giorni, con Claude Code, il mio squadrone di Elite Dangerous ha avuto il suo strumento per il BGS. Non sono uno sviluppatore: ho deciso io cosa doveva fare e ho verificato ogni modifica. La lezione: il codice può essere coerente e sbagliato. Voi avete mai costruito uno strumento per una community?"
image: "/static/assets/img/blog/acfs-bgs-tool/cover.png"
lang: it_IT
categories:
- Progetti Personali
keywords: acfs bgs tool, elite dangerous, bgs, background simulation, flotta stellare, claude code, sviluppo assistito, ia, spansh, github actions, github pages, angular, open source, canonn
tags:
- elite dangerous
- claude-code
- ia
- open-source
- api
- dati aperti
- github-actions
permalink: "/it/blog/progetti-personali/:title/"
redirect_from: "/blog/progetti-personali/acfs-bgs-tool-elite-dangerous-claude-code/"
icon: fa-rocket
---

Ad agosto ho raccontato di [quando l'API di EDSM è andata giù]({{ '/it/blog/fuori-ufficio/flotta-stellare-quando-lapi-va-giu/' | relative_url }}) e ho dovuto rifare lo script che aggiorna la mappa di [flottastellare.it](https://flottastellare.it), il sito dello squadrone di Elite Dangerous di cui faccio parte, l'**Alto Comando Flotta Stellare**. Allora la soluzione era stata Spansh. Questa volta Spansh è il punto di partenza di qualcosa di più grande: uno strumento che lo squadrone usa ogni giorno.

* TOC
{:toc}

## La domanda dopo il tick

Elite Dangerous è un simulatore spaziale, nonché la fedele riproduzione del campo di gioco più grande di sempre: la nostra galassia, riprodotta in scala 1:1. In quella galassia la politica la decide il **[BGS](https://flottastellare.it/bgs/)** (Background Simulation), il meccanismo con cui il gioco simula il potere delle fazioni: ogni sistema stellare ne ha diverse, e quello che i giocatori fanno lì dentro sposta la loro influenza. Una volta al giorno il gioco fa i conti, il cosiddetto *tick*. Chi ha più influenza controlla il sistema. Quando due fazioni si avvicinano troppo, scoppia una guerra o un'elezione.

La nostra fazione, Flotta Stellare, è presente in 399 sistemi, ne controlla 253 e si sta espandendo nel quattrocentesimo. Dopo ogni tick c'è sempre la stessa domanda: **dove lavoriamo oggi?** Per rispondere si aprivano Inara, Spansh e il foglio di monitoraggio dello squadrone, si confrontavano le percentuali sistema per sistema e si scrivevano a mano gli ordini del giorno su Discord.

Dal 4 ottobre la risposta la dà l'**[ACFS BGS Tool](https://flottastellare.it/acfs-bgs-tool/)**: una tabella con tutti i nostri sistemi, ordinati per priorità da P1 a P5, con il motivo di ogni priorità scritto accanto. La storia raccontata per i piloti è [sul sito dello squadrone](https://flottastellare.it/blog/acfs-bgs-tool/). Qui racconto l'altra metà: come ci si arriva in quattro giorni senza essere uno sviluppatore.

## Partire dal lavoro di altri

Non sono partito da zero. Il **Canonn Research Group** è uno dei gruppi di giocatori più grandi di Elite Dangerous, votato alla ricerca scientifica e alla mappatura dei sistemi, tanto da essere entrato a far parte della lore del gioco. Fra i tanti strumenti che mettono a disposizione della comunità, avevano pubblicato con licenza MIT anche quello per seguire il BGS delle loro fazioni, [Canonn Colony Operations](https://github.com/canonn-science/canonn-colony-operations): un'applicazione Angular che faceva per loro più o meno quello che serviva a noi.

Prima di toccare il codice ho fatto una sessione di analisi in chat con Claude, e ne è uscito un documento di passaggio: cosa c'era nel progetto, cosa era scritto apposta per i Canonn (i nomi delle loro due fazioni, i loro sistemi, le regole che confrontano una fazione con l'altra), cosa era già deciso e cosa restava da verificare. Da lì è partito Claude Code.

Il repository è un progetto indipendente, non un fork su GitHub, ma quello dei Canonn resta collegato come sorgente da cui recuperare eventuali correzioni. La licenza MIT conserva la loro nota di copyright, e i crediti sono scritti nel README.

## Come ho lavorato

Lo stesso metodo con cui avevo [ricostruito questo sito]({{ '/it/blog/progetti-personali/il-nuovo-sito-parte-1-perche-ripartire-da-zero/' | relative_url }}) e con cui sto scrivendo [DocSteer-EE]({{ '/it/blog/progetti-personali/docsteer-ee-la-documentazione-aziendale-scritta-dal-browser/' | relative_url }}): prima le decisioni per iscritto, poi il codice.

- **Una roadmap con le decisioni datate.** Ogni scelta finisce in un file del repository, con il giorno e le alternative scartate. Quando una regola cambia, resta scritto perché.
- **Un file di istruzioni per l'assistente.** Lavoro da due PC, a casa e in ufficio, e la memoria locale di Claude resta su una macchina sola. Il file `CLAUDE.md` viaggia con il repository: convenzioni, cose da non fare, come funziona il BGS spiegato da me.
- **Una modifica, un branch.** E nessuna modifica accettata solo perché i test sono verdi: prima la vedo girare in locale.
- **Il push lo decido io.** Il repository è pubblico, e un push sul ramo principale pubblica il sito vero nel giro di mezz'ora.

Il ritmo è stato quello che non mi aspettavo: un centinaio di commit e una trentina di pull request fra il 4 e il 7 ottobre. La sera del 4 il tool era online, il 7 è uscita la versione 1.0.

## Le decisioni che l'AI non poteva prendere

Questa è la parte che mi è servita di più. Un assistente scrive codice coerente con le regole che ha davanti. Se le regole sono quelle di un altro, il codice è coerente e sbagliato.

**SPOCS 253.** Nei primi giorni il tool lo dava in P5, "tutto tranquillo", proprio accanto a due semafori rossi: 35,7% di influenza e 15,6 punti di vantaggio sulla seconda fazione. Il calcolo della priorità era quello dei Canonn e non guardava i semafori, che sono un'abitudine del nostro squadrone. Nessun test poteva accorgersene, perché i test controllavano proprio quel calcolo. Saltava all'occhio solo guardando la tabella. Dalla versione 1.1 i semafori fanno da pavimento alla priorità, e con i dati di quel giorno 32 sistemi sono saliti di fascia.

**"Ultima su quattro fazioni".** Una regola ereditata metteva in P1 qualunque sistema in cui fossimo ultimi fra quattro o più fazioni. Il 7 ottobre erano 10 dei 16 sistemi in P1, compreso uno al 13,9% di influenza, lontanissimo dal pericolo reale. Le strade erano tre: eliminarla, limitarla o lasciarla. Ho scelto di limitarla sotto il 5%.

**"Un conflitto è sempre prioritario".** Una guerra o un'elezione di Flotta Stellare resta in P1 anche dove non controlliamo il sistema. Non è una regola che si ricava dai dati: è come gioca lo squadrone.

E poi le cose che servono solo a chi gioca: la scala di priorità da P1 a P5 (i Canonn partivano da P0, noi no), il fatto che un'espansione compaia in tutti i sistemi della fazione ma parta da uno solo, il punteggio di un conflitto da scrivere sempre dal nostro punto di vista. Le ho spiegate una volta, e sono finite in `CLAUDE.md`.

## I dati: quello che c'è e quello che manca

Il tool legge **Spansh**, che non accetta chiamate dirette da un browser. Quindi niente server: uno script scarica i dati di tutti i nostri sistemi, una pipeline di **GitHub Actions** lo esegue ogni 30 minuti e il sito su **GitHub Pages** viene ricompilato solo se i dati sono cambiati.

Sulla carta, 48 controlli al giorno. Il 5 ottobre GitHub ne ha eseguiti 3: le esecuzioni programmate partono in ritardo o saltano quando i suoi server sono carichi. Per ora basta, perché Spansh stesso si aggiorna solo quando un giocatore passa nel sistema. Ma è finito nella roadmap, per il giorno in cui servirà un aggiornamento più regolare.

Per il punteggio dei conflitti, cioè i giorni vinti in una guerra o in un'elezione, Spansh non basta. Ho valutato con Claude Code tutte le fonti possibili:

- **EliteBGS** ce l'ha, ma il suo database non risponde da giorni, e dal repository si capisce che succede spesso;
- **Inara** risponde alle richieste automatiche con un blocco anti-bot;
- l'**API ufficiale di Frontier** restituisce solo i dati del singolo comandante che fa il login;
- una piattaforma per squadroni già pronta avrebbe voluto dire affidare a terzi i nostri dati.

Il tool chiede il punteggio a EliteBGS e, quando non risponde (cioè quasi sempre), rimanda a Inara. Meglio un rimando onesto che un numero inventato. Lo stesso vale per l'età del dato: ogni riga dice quanto è vecchia, invece di fingere che sia aggiornata.

Per le informazioni che deve gestire lo squadrone, come gli architetti dei sistemi colonizzati e la lista dei sistemi da tenere d'occhio, il database è un **Google Sheet**. GitHub Pages pubblica pagine statiche e non offre un database, e per un gruppo delle nostre dimensioni un foglio condiviso va più che bene.

## Tre lingue in una sera

Pochi giorni dopo l'uscita, il link è arrivato a un giocatore tedesco. La sera del 7 ottobre la parte di consultazione parlava italiano, tedesco e inglese. I testi stanno in un dizionario per lingua, con l'italiano come riferimento, e una traduzione mancante blocca la compilazione: è il modo più semplice per non dimenticarsene la prossima volta che si aggiunge una frase. I nomi degli stati del BGS restano in inglese, come nel gioco. Il tedesco lo rivedrà proprio quel giocatore.

## E adesso

Il tool è diventato il primo posto in cui lo squadrone guarda dopo il tick. Nella roadmap ci sono un report automatico su Discord dopo ogni tick, un elenco dei sistemi importanti ancora fermi a prima del tick, da girare a chi è in volo, e la mappa 3D del sito che legge direttamente i dati del tool.

Il tool è qui: **[flottastellare.it/acfs-bgs-tool](https://flottastellare.it/acfs-bgs-tool/)**. Il racconto per i piloti è [sul sito dello squadrone](https://flottastellare.it/blog/acfs-bgs-tool/).

Voi avete mai costruito uno strumento per una community, un'associazione o un hobby, senza farlo di mestiere? Con quali aiuti, e dove vi siete fermati?
