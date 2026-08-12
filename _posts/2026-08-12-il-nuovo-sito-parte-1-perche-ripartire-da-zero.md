---
title: "Il nuovo sito, parte 1: perché ho deciso di ripartire da zero (con un'IA come collega)"
layout: post
date: '2026-08-12 18:00:00'
description: Dalla manutenzione di un sito Jekyll del 2019 alla decisione di ricostruirlo completamente in poche ore, lavorando fianco a fianco con Claude Code. La storia di come è nata la versione 2.0 di questo sito.
intro: "Questa mattina ho aggiornato le dipendenze di questo sito. Nel pomeriggio l'ho buttato giù e ricostruito da zero. Ecco perché, e come ci sono arrivato in poche ore invece che in settimane."
image: "/static/assets/img/blog/nuovo-sito-2026/parte1-cover.jpg"
image_dark: "/static/assets/img/blog/nuovo-sito-2026/parte1-cover-dark.jpg"
lang: it_IT
categories:
- Progetti Personali
keywords: jekyll, redesign, claude code, ia, sviluppo assistito, minimal design
tags:
- jekyll
- redesign
- claude-code
- ia
- design
permalink: "/blog/progetti-personali/:title/"
icon: fa-paint-brush
---

Stamattina ho raccontato [come ho passato il pomeriggio a rimettere in sesto le dipendenze di questo sito]({{ '/blog/progetti-personali/manutenzione-sito-2026/' | relative_url }}) — Ruby, npm, Bootstrap, Chart.js, tutta roba ferma al 2019 che nessuno aveva mai più toccato davvero. Quel lavoro doveva essere la fine della giornata: sito sistemato, dipendenze pulite, tutti contenti.

Invece, mentre sistemavo l'ennesimo bug dormiente, mi sono fatto una domanda scomoda: *sto davvero curando questo sito, o sto solo rallentando la sua fine?*

* TOC
{:toc}

## Il momento in cui ho smesso di fare manutenzione

Il tema di partenza (derivato da [Jalpc](https://github.com/jarrekk/Jalpc)) era una landing page one-page con Bootstrap 3, jQuery e una manciata di plugin che oggi nessuno sceglierebbe più: un carosello hero, un menu mobile basato su Bootstrap 3 collapse, un grafico radar via Chart.js per le competenze. Funzionale, nel 2016. Nel 2026, con Bootstrap 3 a fine vita (due XSS moderate mai patchate, per dirne una) e un intero pomeriggio già speso a scoprire quanto debito tecnico si fosse accumulato, la domanda vera non era più "come lo sistemo" ma "vale ancora la pena sistemarlo?".

La risposta che mi sono dato: no. Non perché il contenuto non valesse — dieci anni di post tecnici, un CV, i miei progetti — ma perché il *contenitore* aveva fatto il suo tempo. Ho deciso di ricostruire il sito da zero, con un tema nuovo, scritto apposta per quello che sono oggi: un Infrastructure & Service Management Manager con un blog tecnico, non più un laptop pieno di plugin jQuery.

## Il vincolo che non potevo permettermi di rompere

C'era però una condizione non negoziabile: **ogni URL dei post del blog doveva restare esattamente identico**. Dieci anni di articoli tecnici, alcuni ancora citati o linkati da terzi, indicizzati da Google — un redesign che rompe i permalink è un redesign che butta via anni di posizionamento. Qualunque cosa avessi ricostruito, doveva convivere con questo vincolo dall'inizio, non come ripensamento finale.

Ho lavorato con **Claude Code**, l'assistente IA da riga di comando di Anthropic, che avevo già usato per il lavoro di manutenzione della mattina. La differenza, per un progetto di questa portata, è stata partire con un piano scritto invece che con il codice: prima abbiamo mappato cosa del sito esistente fosse contenuto reale (i miei progetti GitHub, il CV, gli articoli) e cosa fosse invece morto — funzionalità mai attivate (multilingua), sezioni con dati segnaposto mai personalizzati, categorie di blog senza un solo articolo. Poi abbiamo scritto un documento di piano vero e proprio: architettura delle pagine, sistema di design, quali file sarebbero spariti e quali sarebbero rimasti, come verificare che i permalink non si rompessero. Solo dopo, il codice.

Questo approccio — pianificare prima di scrivere, invece di scrivere e sistemare — è probabilmente il motivo per cui un lavoro che immaginavo su più giorni si è concluso in un pomeriggio.

## Le decisioni prese insieme

Alcune scelte le ho fatte io, altre le ho delegate, altre ancora le abbiamo discusse:

- **Stack**: restare su Jekyll. GitHub Pages lo supporta nativamente, la pipeline di build l'avevo appena sistemata la mattina stessa, e cambiare generatore avrebbe voluto dire rifare da capo anche quello.
- **Stile visivo**: minimal e professionale. Niente più carosello, niente animazioni jQuery — palette neutra, molto spazio bianco, il blu `#3385FF` mantenuto come accento (è già nel favicon, nei profili social collegati, non aveva senso perderlo).
- **Struttura**: da one-page a sito multi-pagina — Home, CV, Progetti, Blog, Contatti — più adatta a un sito che deve funzionare sia come portfolio professionale sia come blog tecnico.
- **Cosa buttare**: Bootstrap 3, jQuery e tutti i suoi plugin, l'intera pipeline npm di build (sostituita dalla compilazione Sass nativa di Jekyll, zero dipendenze front-end), il grafico radar Chart.js (sostituito da una lista di competenze raggruppate per area, più leggibile e coerente con lo stile minimal).

Il CV e le competenze, tra l'altro, li avevamo già aggiornati con i dati reali dal mio profilo LinkedIn qualche ora prima — quel lavoro è confluito direttamente nella nuova pagina `/cv/`.

## La velocità non è un compromesso sulla qualità

La parte che mi ha sorpreso di più non è stata la velocità in sé, ma il fatto che non sia arrivata a scapito della verifica. Ogni singolo pezzo — ogni layout, ogni pagina, ogni categoria del blog — è stato ricompilato e controllato prima di passare al successivo. Prima di considerare il lavoro finito, abbiamo fatto una cosa che a mano non avrei mai avuto la pazienza di fare: un confronto automatico, URL per URL, tra il sito vecchio e quello nuovo, per garantire zero permalink rotti. Il risultato: tre nuove pagine aggiunte (`/cv/`, `/progetti/`, `/contatti/`), **zero URL persi**.

Quello che un redesign di questo genere avrebbe richiesto in settimane — se fatto da solo, nei ritagli di tempo serali — si è concluso in un pomeriggio. Non perché il lavoro fosse meno, ma perché avere un collega che scrive codice, lo verifica, e lo ricontrolla in loop, senza stancarsi e senza saltare passaggi, cambia radicalmente i tempi.

Detto questo — e lo scoprirete nella prossima puntata — "veloce" non ha voluto dire "senza intoppi". Anche un sito costruito da zero, in poche ore, ha nascosto una manciata di bug genuinamente interessanti: uno di questi mi ha fatto finire a leggere il codice sorgente di Jekyll stesso.

**Continua nella [parte 2]({{ '/blog/progetti-personali/il-nuovo-sito-parte-2-i-bug-nascosti-in-un-sito-nuovo/' | relative_url }}): i bug nascosti in un sito nuovo di zecca.**
