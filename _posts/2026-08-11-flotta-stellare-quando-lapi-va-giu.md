---
title: "Quando l'API va giù: tenere aggiornata la mappa di flottastellare.it"
layout: post
date: '2026-08-11 18:30:00'
description: L'API di EDSM smette di rispondere e lascia a secco lo script che teneva aggiornata la tabella dei sistemi controllati dallo squadrone Flotta Stellare, su Elite Dangerous. La caccia a un'alternativa, uno scarto (Inara) e una sostituzione (Spansh) che fa anche di più di prima.
intro: "Non tutto quello che sistemo in una giornata finisce su questo blog sotto forma di articolo tecnico da manuale. A volte è solo uno script Python che smette di funzionare perché un servizio terzo è andato giù, e va sostituito prima che qualcuno se ne accorga."
image: "/static/assets/img/blog/flotta-stellare/cover.png"
image_dark: "/static/assets/img/blog/flotta-stellare/cover-dark.png"
lang: it_IT
categories:
- Fuori dall'Ufficio
keywords: elite dangerous, jekyll, python, api, dati aperti, bgs
tags:
- elite dangerous
- games
- jekyll
- python
- api
- dati aperti
permalink: "/blog/fuori-ufficio/:title/"
icon: fa-rocket
---

Fuori dall'orario di lavoro (e fuori dal [restyling di questo sito]({{ '/blog/progetti-personali/il-nuovo-sito-parte-1-perche-ripartire-da-zero/' | relative_url }}), di cui potete leggere qui) gioco a **Elite: Dangerous**, e faccio parte dell'**Alto Comando Flotta Stellare (ACFS)**, uno squadrone di comandanti indipendenti radunati attorno a una minor faction chiamata, per l'appunto, Flotta Stellare. Il sito dello squadrone, [flottastellare.it](https://flottastellare.it), è anche lui un sito Jekyll — e anche lui, come questo, ha bisogno ogni tanto di un po' di manutenzione.

* TOC
{:toc}

## Una tabella che si aggiorna da sola (di solito)

Nella pagina `about/index.md` del sito teniamo una tabella con tutti i sistemi stellari presidiati dalla fazione: governo, popolazione, alleanza, stato di controllo. Sono dati che si muovono di continuo — il **BGS** (Background Simulation) di Elite Dangerous fa evolvere ogni sistema in base a cosa i giocatori ci fanno dentro, giorno per giorno — quindi tenerla aggiornata a mano non è pensabile. Da qui uno script Python, lanciato ogni tanto dalla root del repository, che va a interrogare un'API pubblica e riscrive la tabella.

Il problema: lo script puntava a **EDSM**, e l'API di EDSM ha smesso di rispondere.

## Il candidato scartato

Prima di cercare un sostituto ho controllato se l'**API di Inara** — un altro grande database comunitario per Elite Dangerous — potesse coprire lo stesso bisogno. Risposta breve: no. È un'API pensata per essere **push-only** dal punto di vista di un comandante: riceve eventi come `addCommanderReputation` o `setCommanderRankPilot` dal client di gioco, non espone un modo per interrogare popolazione o fazioni presenti in un sistema arbitrario. Gli unici endpoint di lettura sono legati al profilo di un singolo comandante o alle community goal recenti — niente che aiuti a ricostruire lo stato di un sistema. Scartata.

## Il sostituto: Spansh

La soluzione arriva da [Spansh](https://spansh.co.uk/), un altro strumento molto popolare nella comunità di Elite Dangerous (più noto per il suo route planner), che espone un'**API pubblica non ufficiale** senza bisogno di alcuna chiave: una richiesta `GET` con il nome del sistema restituisce governo, popolazione, alleanza, stato di sicurezza e perfino le fazioni minori presenti con la relativa influenza.

Il nuovo script, `spansh_sync.py`, non si limita a rimpiazzare quello vecchio funzione per funzione — fa qualcosa in più:

- **Aggiunge le righe mancanti**, in ordine alfabetico, per i sistemi che lo squadrone ha conquistato ma che non erano ancora in tabella.
- **Aggiorna i campi esistenti** solo quando il dato live di Spansh è effettivamente diverso da quello in tabella (un sistema passa da Controllato a Non Controllato, cambia governo, l'alleanza si sposta) — e stampa un log riga per riga di cosa è cambiato.
- **Lascia invariate le righe non trovate** su Spansh (es. sistemi visitati ma non ancora presenti nei dump pubblici), invece di cancellarle per errore.
- **Aggiorna da solo `last_modified_at`** nel front matter a ogni esecuzione.
- **Ricalcola il totale** nella frase "Governiamo su **N** abitanti", sommando la popolazione di tutti i sistemi con stato Controllato.

## I bug trovati passando i dati al setaccio

Il primo lancio contro dati reali, come spesso succede, ha fatto emergere problemi che uno script "silenzioso" aveva lasciato indisturbati per chissà quanto:

- Una riga con il nome **duplicato per errore**: "V0502 V0502 Ophiuchii" invece di "V0502 Ophiuchii" — non abbastanza simile al nome vero perché Spansh la riconoscesse, quindi mai più aggiornata da anni.
- Una **riga doppia per lo stesso sistema** ("Misir"), con due valori di Governo diversi tra loro — probabilmente il risultato di due inserimenti manuali in momenti diversi.
- Un file `__pycache__/edsm_fetcher.cpython-314.pyc` **finito nel repository per sbaglio** in un commit precedente — rimosso, e `__pycache__` aggiunto finalmente a `.gitignore`.

## Il risultato

Il primo run completo con Spansh ha aggiunto **98 sistemi** che mancavano del tutto dalla tabella e ha aggiornato popolazione, governo, alleanza e stato su gran parte delle righe esistenti. Lo script `edsm_fetcher.py` originale resta nel repository come fallback, per il giorno — se mai arriverà — in cui l'API di EDSM tornerà raggiungibile.

Niente di paragonabile, per portata, al lavoro fatto in questi giorni su questo sito. Ma è lo stesso tipo di soddisfazione: uno script che si era rotto in silenzio, un'alternativa scartata a ragion veduta, una sostituzione che funziona meglio dell'originale. Anche gestire una flotta virtuale di comandanti spaziali, alla fine, è una questione di infrastruttura da tenere in ordine.
