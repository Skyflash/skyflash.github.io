---
title: IPUI to IPEI
layout: post
date: '2019-01-24 12:30:00'
description: Cosa è un codice IPUI e come convertirlo facilmente in IPEI per registrare un telefono DECT Siemens su un centralino di un altro produttore.
intro: non tutti i produttori di telefoni DECT usano la stessa notazione IPEI. Più
  precisamente, il principale produttore di telefoni DECT di fascia consumer al mondo,
  Siemens, utilizza un proprio codice chiamato IPUI, che differisce dal primo in modo
  piuttosto evidente
image: "/static/assets/img/blog/ipuitoipei/ipui2ipei.jpg"
categories:
- HTML
- Tools
keywords: html,ipui,ipei,dect,siemes,conversione,tool,converter
tags:
- telefonia
- cordless
- siemens
- dect
- ipui
- ipei
- conversione
permalink: "/blog/tools/:title/"
icon: fa-refresh
---

Talvolta (prendiamo ad esempio le installazioni aziendali) diventa necessario registrare sull'impianto DECT un telefono di produttore diverso da quello del centralino, vuoi per mancanza di disponibilità del prodotto voluto, vuoi per pure e semplici ragioni di budget (un cordless **Siemes** costa mediamente fra i 50 e i 70€, mentre un terminale ad esempio **Spectralink** o **Avaya** supera allegramente i 250€).

L'operazione è comunque veloce ed indolore per ogni tipo di terminale che supporti ovviamente lo standard DECT/GAP in quanto, come detto, è sufficiente l'IPEI del telefono che intendiamo registrare ed il gioco è fatto.
Con Siemens, invece, ci servirà un passaggio in più, proprio per via della loro scelta di utilizzare IPUI, che ha una diversa notazione ed una diversa struttura e non viene quindi riconosciuto come IPEI valido.

* TOC 
{:toc}

## Cosa è il codice IPEI?

L'IPEI è un codice numerico di identificazione, simile al codice IMEI dei telefoni cellulari, dei telefoni DECT/GAP (i cosiddetti "telefoni cordless").

* IPEI è un codice numerico di 13 caratteri
* IPUI è un codice alfanumerico di 10 caratteri

### Come convertire il codice IPEI in IPUI?

La conversione consiste nella divisione di IPUI in due parti separate, con conseguente trasformazione dei due valori esadecimanli in decimali e qualche altro calcolo più o meno divertente. 
Oppure, molto più semplicemente, si può utilizzare un tool di conversione come quello indicato di seguito.

## Ipui2Ipei: strumento di conversione da IPUI a IPEI
Al questo link è possibile trovare [ipui2ipei](https://cristiancastellari.it/ipui2ipei/), un tool web che ho trovato su GitHub e che ho poi provveduto a modificare e migliorare (si spera) secondo le mie esigenze.

Il suo utilizzo è semplicissimo: è sufficiente scrivere nel primo campo il codice IPUI estratto dal telefono Siemens seguendo la procedura indicata successivamente e premere il bottone Converti.

![Conversione da IPUI a IPEI](/static/assets/img/blog/ipuitoipei/conversione.jpg)

Un attimo dopo avrete il risultato desiderato, con tanto di spiegazione sul tipo di calcoli che sono stati eseguiti.

![Calcolo IPUI a IPEI](/static/assets/img/blog/ipuitoipei/calcolo.jpg)

## Informazioni aggiuntive

### Come trovare il codice IPUI di un telefono SIEMENS?

  col portatile in stand-by, bisogna premere la seguente sequenza di tasti:
  **Tasto MENU'** seguito da [\*] [#] 0 6 [#]

### Note ulteriori

* Il codice IPEI è composto da 13 caratteri: i primi 12 sono il codice vero e proprio, mentre il tredicesimo è un carattere di controllo. 
* A seconda del produttore del vostro centralino o server DECT dovrete inserirli tutti o solo i primi 12.
* La conversione potrebbe portare ad un risultato con *quattordici* numeri in quanto il codice di controllo può essere un qualsiasi numero compreso fra 1 e 10. In questo caso trasfromate il 10 in "asterisco" [\*]

## Riferimenti

* [Strumento di conversione Ipui 2 Ipei](https://cristiancastellari.it/ipui2ipei/)
* [Pagina GitHub del progetto](https://github.com/skyflash/ipui2ipei)
* [Progetto originale](https://github.com/StrongeLeeroy/ipui2ipei)