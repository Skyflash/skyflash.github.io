---
title: "ACFS Colony Plotter: quali sistemi colonizzare in Elite Dangerous"
layout: post
date: '2026-11-21 09:00:00'
description: "Il Colony Plotter dell'ACFS BGS Tool: i sistemi da colonizzare entro 15 anni luce dalle stazioni di Flotta Stellare, con i motivi per cui valgono il viaggio, e il Ponte per arrivare a quelli lontani. Come è nato, cosa abbiamo sbagliato e cosa viene dopo."
intro: "Con la colonizzazione, in Elite Dangerous i giocatori possono reclamare un sistema disabitato e costruirci stazioni e porti. La parte difficile è scegliere dove piantare la prossima bandierina: attorno alle nostre stazioni ce ne sono quasi mille, e la maggior parte sono sassi. Il Colony Plotter serve a trovare quelli che non lo sono."
social:
  default: |-
    In Elite Dangerous si può prendere un sistema stellare vuoto e costruirci sopra stazioni, porti, basi. Il bello è sceglierlo. Il brutto è che attorno a ogni stazione ce ne sono decine, e quasi tutti sono sassi.

    Per il mio squadrone abbiamo fatto il Colony Plotter: ogni giorno guarda attorno alle nostre 265 stazioni e ti dice quali sistemi valgono il viaggio, e perché. Poi il Ponte, per arrivare a quelli lontani una tappa da 15 anni luce alla volta.

    La prima versione è nata in un giorno. Un mese dopo l'ho rifatta, perché era "un pochino confusionaria". Le parole sono mie.

    Voi, quando un vostro strumento funziona ma non vi piace, lo rifate o lo lasciate stare?
  threads: "In Elite Dangerous si può colonizzare un sistema vuoto. Il difficile è sceglierlo: attorno a ogni stazione sono decine, quasi tutti sassi. Per il mio squadrone abbiamo fatto il Colony Plotter, che ogni giorno ti dice quali valgono il viaggio e perché, più il Ponte per quelli lontani. Voi i vostri strumenti li rifate quando non vi piacciono più?"
image: "/static/assets/img/blog/acfs-colony-plotter/cover.png"
lang: it_IT
categories:
- Progetti Personali
keywords: acfs colony plotter, elite dangerous, colonizzazione, colonisation, trailblazers, bgs, spansh, colonisation plotter, bridging, ponte, flotta stellare, claude code, canonn colony finder
tags:
- elite dangerous
- claude-code
- ia
- open-source
- api
- dati aperti
permalink: "/it/blog/progetti-personali/:title/"
redirect_from: "/blog/progetti-personali/acfs-colony-plotter-colonizzare-elite-dangerous/"
icon: fa-flag
---

Un mese fa, chiudendo la [seconda parte sull'ACFS Server]({{ '/it/blog/progetti-personali/acfs-server-accesso-con-discord-e-bgs-tally/' | relative_url }}), avevo messo in fondo a una lista di idee "il Colony Plotter, per trovare i sistemi da colonizzare vicino alle nostre stazioni". Sembrava una di quelle cose da fare "prima o poi". È uscito il giorno dopo, ed è diventato la parte dell'[ACFS BGS Tool]({{ '/it/blog/progetti-personali/acfs-bgs-tool-elite-dangerous-claude-code/' | relative_url }}) su cui abbiamo lavorato di più.

* TOC
{:toc}

## Colonizzare, in due parole

Da quando è arrivata la colonizzazione, in Elite Dangerous non si gioca più solo nei sistemi che esistono già. Si può prendere un sistema disabitato, posarci un segnale (il *beacon*), e nelle quattro settimane successive portarci abbastanza materiale da costruire il primo porto. Da lì in poi il sistema è vivo: ci si costruiscono altre stazioni, basi a terra, installazioni, e arriva gente ad abitarlo.

Sul sito dello squadrone ci abbiamo scritto una guida in cinque capitoli, dal perché farlo fino a un caso pratico: se volete partire dalle basi, il [primo capitolo](https://flottastellare.it/blog/colonizzazione-parte1/) è il posto giusto. Qui mi limito all'essenziale.

Le regole che contano per noi sono tre:

- si parte da una stazione che abbia il **Contatto di Colonizzazione**, e il sistema da reclamare deve stare entro **15 anni luce**;
- costa **25 milioni di crediti**, che non tornano indietro, e un sistema reclamato e lasciato a metà resta lì a guardarti;
- il sistema nuovo non nasce vuoto di politica. Se parti da una stazione di Flotta Stellare, la nostra fazione ci entra con il **60%** dell'influenza. Se parti dalla stazione di qualcun altro, quel 60% va a lui.

L'ultima regola è quella che ha fatto nascere il Colony Plotter. Per uno squadrone che fa BGS, colonizzare vuol dire allargare la fazione. Ma solo se si parte dal posto giusto.

## Il problema: sono quasi tutti sassi

Attorno a ogni nostra stazione, entro 15 anni luce, ci sono di solito decine di sistemi liberi. La maggior parte sono una stella qualunque con qualche pianeta di roccia. Ci si può costruire, certo, ma non è per quelli che uno spende 25 milioni e un mese di viaggi da cargo.

Quelli che fanno gola sono altri: un **Earth-like world** o un **Water world**, che sono rari e portano popolazione; un sistema con **due o più stelle**; pianeti con **anelli** con riserva *Pristine*, dove andare a caccia nelle RES; **biologia** sulla superficie, che dà bonus ad alcune economie (questa me l'ha fatta notare un contrammiraglio, non ci sarei arrivato da solo); sistemi enormi, con più di 40 corpi.

Trovarli a mano vuol dire aprire Spansh o Inara, cercare attorno a una stazione, scorrere sistema per sistema, aprire i corpi, prendere appunti. Per una stazione si fa. Per 265 no.

## L'idea dei Canonn, di nuovo

Come per il BGS Tool, anche qui c'era già qualcuno che ci aveva già pensato: i **Canonn**, con il loro [Colony Finder](https://canonn-science.github.io/canonn_colony_finder/). Una bella tabella di circa 4.700 sistemi da colonizzare attorno alle loro stazioni, con i corpi interessanti scritti accanto.

Guardandolo da vicino, però, aveva alcuni limiti, che per la nostra necessità non lo rendevano ottimale. 

1. Viene generato leggendo di volta in volta l'archivio completo della galassia di Spansh (ben 117 GB!), e soprattutto viene aggiornato a mano (l'ultima volta, quando l'ho guardato, era di due settimane prima). 
2. Non sa niente di BGS, che invece per noi è fondamentale.
3. Il codice non ha una licenza esplicita, il che ci avrebbe potuto portare problemi futuri.

La sorpresa è arrivata in seguito, provando Spansh: la sua ricerca dei sistemi, quella normale che usa chiunque dal sito, restituisce anche i sistemi disabitati, con tutti i corpi e con lo stato della colonizzazione. Attorno alla prima stazione che abbiamo provato ne sono usciti 27. _Quindi l'archivio da 117 GB non serviva_: bastava fare una ricerca attorno a ogni nostra stazione, una alla volta e con calma, per non pesare su Spansh.

## E venne il 25 ottobre

La prima versione del Colony Plotter è nata il 25 ottobre, in una giornata sola. Il motore principale si trova in un [repository a parte](https://github.com/ed-acfs/acfs-colony-plotter), pubblico e con licenza MIT, perché non c'è niente di segreto e magari serve a qualcun altro. Funziona in questo modo:

1. prende tutte le stazioni controllate da Flotta Stellare (ma non gli insediamenti di Odyssey: non hanno un _Colonisation Contact_ da cui acquistare il beacon);
2. per ognuna chiede a Spansh i sistemi entro 15 anni luce, più i corpi con gli anelli, che la ricerca dei sistemi non dice;
3. tiene quelli liberi, segna quelli già reclamati da qualcuno, e per ogni sistema scrive **perché è interessante**, corpo per corpo;
4. calcola da quali nostre stazioni ci si arriva, dalla più vicina, e con quali fazioni nascerebbe il sistema nuovo.

Il tutto viene fatto girare dal server dello squadrone una volta al giorno. Inoltre, la pagina è visibile solo da chi ha un ruolo specifico all'interno del nostro Discord: i membri dello squadrone e, con un ruolo pensato appositamente, anche amici ed ospiti. Oggi, mentre scrivo, i sistemi liberi attorno alle nostre stazioni sono 919 (più 112 già reclamati da qualcuno). Di questi, 34 hanno biologia, 101 anelli *Pristine* e 22 almeno un hotspot. Altro che "per una stazione si fa".

Per capire a cosa è "adatto" un sistema (raffineria, industria, estrazione, agricoltura, turismo) mi sono fatto leggere la **Colonization Mega Guide** di CMDR Mechan, un documento enorme che chiunque colonizzi in Elite prima o poi apre. Da lì è uscito un riassunto di poche pagine, che il motore usa per i suoi punteggi. Come un corpo decide l'economia di un porto l'abbiamo spiegato nel [terzo capitolo della nostra guida](https://flottastellare.it/blog/colonizzazione-parte3/). Una cosa l'ho dovuta correggere io: la guida dice che il sistema nuovo dà il 13% anche alla fazione dello squadrone. Se però la stazione di partenza è già nostra, Flotta Stellare ha già il 60%, e il 13% non le arriva una seconda volta. Sono le cose che si imparano giocando, non leggendo.

La prova del fuoco è stata una richiesta precisa di un mio compagno di gioco: voleva i sistemi con gli anelli buoni per trovare future RES (zone di comabttimento in cui fare taglie, convertibili in comoda Influenza, in modo piuttosto semplice e veloce). Come esempio aveva portato _Col 285 Sector ZZ-Y d79_, uno dei nostri sistemi, con sei corpi con anelli *Pristine* e un hotspot di Void Opal: ne voleva altri così. Nella stessa zona, per dire, c'è Col 285 Sector ZZ-Y d91: libero, con sette corpi con anelli, tutti *Pristine*.

<img class="post-image" src="{{ '/static/assets/img/blog/acfs-colony-plotter/scheda-anelli.png' | relative_url }}" alt="La scheda di Col 285 Sector ZZ-Y d91 nel Colony Plotter, tema scuro: stato Libero, 29 corpi, riserva Pristine; le ragioni di interesse (sei giganti gassosi di classe I, un pianeta ad alto contenuto metallico, sette corpi con anelli Pristine); la partenza da Col 285 Sector ZZ-Y d43 a 14,68 anni luce con le fazioni del sistema nuovo, 60% Flotta Stellare; l'elenco degli anelli e a cosa è adatto il sistema: estrazione, industria, High Tech">

Ogni sistema ha la sua scheda così: perché è interessante, da quale nostra stazione partire e con che fazioni nascerebbe, gli anelli uno per uno e a cosa è adatto.

## "Un pochino confusionario"

Il Colony Plotter funzionava, e lo usavamo. Ma ogni volta che lo aprivo mi veniva il mal di testa. L'avevo impostato come il Colony Finder dei Canonn, con tutti i corpi interessanti in fila nella riga di ogni sistema, e il risultato era un muro di etichette colorate. Il 20 novembre l'ho scritto così, testuale: "un pochino confusionario, molto tabellare". Come riferimento ho indicato [edbubbles.com](https://edbubbles.com), che ha un'aria molto più pulita.

Avevo tre strade possibili: rifare tutto con uno stile nuovo, passare a schede grandi per i sistemi migliori, oppure riordinare la tabella. Ho scelto la terza, la meno spettacolare. Le schede grandi hanno senso solo quando il punteggio dei sistemi sarà tarato bene, e oggi non lo è ancora del tutto.

Il riordino, in pratica:

- la pagina si apre con due schede, **Obiettivi entro 15 ly** e **Ponte** (ci arrivo fra poco);
- i filtri che si usano sempre stanno in vista, gli altri in un riquadro **Altri filtri** che, da chiuso, dice quanti ne hai attivi. Così non ti chiedi più perché vedi solo tre sistemi;
- nella riga resta un dato per colonna, e al posto del muro di etichette pochi segni **In evidenza** con un'icona e un numero. Ci passi sopra e ti dice quali corpi o quali specie; ci clicchi e si apre la scheda del sistema, già al punto giusto;
- il nome si copia con l'icona accanto, come su Inara, perché in gioco il nome del sistema lo devi incollare nella mappa galattica, e a fine riga dava fastidio.

<img class="post-image" src="{{ '/static/assets/img/blog/acfs-colony-plotter/in-evidenza-chiaro.png' | relative_url }}" alt="La tabella degli obiettivi del Colony Plotter nel tema chiaro: per ogni sistema distanza, numero di corpi, scopo più adatto e i segni In evidenza. Sulla riga di LTT 18046 il segno 2 specie è aperto e mostra i corpi 6 c e 6 d con Bacterium Vesicula e Fonticulua Campestris">

Poi i colori. Lo scuro è diventato un grigio ardesia, un po' bluastro, lo stesso di questo blog. Ed è arrivato il tema chiaro, con lo stesso selettore che usate qui (automatico, chiaro o scuro). Lo scuro nuovo mi piaceva così tanto che l'ho voluto in tutto il tool, non solo nel Colony Plotter.

<img class="post-image post-image--side" src="{{ '/static/assets/img/blog/acfs-colony-plotter/telefono.png' | relative_url }}" alt="Il Colony Plotter sullo schermo di un telefono, tema scuro: ogni sistema è una scheda compatta con il nome in testa, il menu in alto a destra, il sistema di partenza, distanza, corpi, scopo più adatto e i segni In evidenza">

E siccome c'è chi lo apre dal telefono mentre è in gioco sull'altro schermo, l'ultima modifica è stata per quello: al telefono la riga diventa una scheda compatta, con il nome in testa e il menu in alto a destra.

Due dettagli che mi sono rimasti in mente:

- **I grassetti finti.** I nomi dei sistemi su fondo scuro sembravano impastati. Il motivo: il tool scarica il font Roboto solo fino a un certo spessore, e oltre quello il browser il grassetto se lo inventa, ingrossando le lettere. Bastava usare lo spessore che c'era già.
- **L'accessibilità.** Ho fatto passare tutte le viste nei due temi da axe-core, lo stesso controllo che usa Lighthouse. Prima ogni vista aveva da quattro a sei regole violate (contrasti, focus da tastiera, bersagli troppo piccoli da toccare). Dopo, nessuna. Non è una gara, ma un arancio che non si legge sul bianco non serve a nessuno.

## Il Ponte: spazio, ultima frontiera

I 15 anni luce sono un limite stretto. Se il sistema che vi piace sta a 80 anni luce dalla stazione più vicina, l'unico modo di arrivarci è un **ponte**: una catena di sistemi colonizzati uno dopo l'altro, ognuno entro 15 anni luce dal precedente, dove ogni tappa diventa il punto di partenza della successiva. È lavoro di squadra per forza, e la tempistica conta: quando il porto di una tappa è finito, per mezz'ora può reclamare da lì solo l'architetto, poi per quasi un giorno tutto il suo squadrone, poi chiunque. Il pilota successivo deve essere pronto.

La catena la calcola già Spansh, con il suo Colonisation Plotter. Il nostro Ponte gliela chiede attraverso il server e ci aggiunge quello che a noi serve sapere: per ogni tappa se è **nostra**, **da colonizzare**, **in costruzione** o **già colonizzata** da altri, quale è la **prossima tappa**, un pulsante per copiare tutta la rotta e un link da mandare in chat che apre lo stesso ponte. Spansh a volte ci mette più di un minuto, e la pagina ve lo dice invece di lasciarvi lì a chiedervi se si è bloccata.

Verso Hyades Sector LY-X a2-0, per esempio, il tool parte da Col 285 Sector ZZ-Y d79, il nostro sistema più vicino, e Spansh trova otto salti per 91 anni luce, tutti in sistemi ancora da colonizzare.

<img class="post-image" src="{{ '/static/assets/img/blog/acfs-colony-plotter/ponte.png' | relative_url }}" alt="La scheda Ponte del Colony Plotter, tema scuro: arrivo Hyades Sector LY-X a2-0, partenza il nostro sistema più vicino. In alto 8 salti da Col 285 Sector ZZ-Y d79, 8 tappe da colonizzare, 91 anni luce e la prossima tappa, Col 285 Sector VO-X b2-2; sotto le nove tappe numerate con salto, distanza dall'arrivo, corpi e stato, la prima segnata come nostra e le altre da colonizzare, e i pulsanti Copia il link e Copia la rotta">

L'introduzione del Ponte nella pagina comincia con *"Spazio, ultima frontiera. Questi sono i viaggi di Flotta Stellare…"*. Con un nome così, era il minimo.

## Cosa ha fatto Claude, cosa ho fatto io

Il metodo è quello di sempre. Claude Code ha scritto il codice, ha letto Spansh e la Mega Guide, ha fatto le prove e mi ha portato le proposte. Io ho fatto il giocatore: ho deciso cosa è interessante e cosa no, ho corretto le regole quando non tornavano con quello che vedo in gioco, e ho detto "no, così non mi piace" quando non mi piaceva. Che, ve lo assicuro, è più difficile di quanto sembri: bisogna capire *perché* non ti piace.

Il Colony Plotter era partito da una frase precisa: volevo "un bel prodotto una volta finito", non uno strumento cucito su misura per la prossima operazione dello squadrone e poi dimenticato. Il 20 novembre, con la versione 1.9.0 del BGS Tool, è uscito dalla beta. Non è ancora 100% finito, ma comincia ad assomigliare a quello che avevo in testa.

## E adesso?

Nella roadmap ci sono già le prossime cose:

- **un indirizzo tutto suo**, tipo `colonyplotter.flottastellare.it` e la PWA da installare sul telefono come un'app;
- **la taratura dei punteggi**: oggi la raffineria vince troppo spesso, solo perché i pianeti rocciosi sono tanti. Va rivista sui sistemi veri, insieme agli Architetti;
- **l'avanzamento dei cantieri**, con le consegne prese dal plugin BGS-Tally dei piloti, per sapere quanto manca senza chiederlo in chat;
- **un Ponte tutto nostro**, che fra due tappe possibili preferisca quella con i corpi più utili invece della più corta.

Se colonizzate in Elite, mi interessa sapere come scegliete i vostri sistemi: a occhio, con un foglio, con uno strumento? E se avete in mente un criterio che il Colony Plotter non guarda, scrivetemelo: è così che sono arrivati gli anelli e la biologia.
