---
title: "Il redesign di Ipui2Ipei"
layout: post
date: '2026-08-18 12:30:00'
description: "Jekyll 4, bilingue IT/EN, via Bootstrap e jQuery: come ho rifatto da zero un piccolo tool di conversione IPUI→IPEI usando lo stesso schema appena rodato sul sito principale."
intro: "Un tool che ho scritto per un problema mio, nel 2019, ha continuato silenziosamente ad aiutare sconosciuti che non ho mai incontrato. Quando ho ricostruito questo sito da zero, mi sono chiesto se non fosse ora di fare lo stesso anche lì."
image: "/static/assets/img/blog/ipuitoipei/redesign-convertitore.jpg"
image_dark: "/static/assets/img/blog/ipuitoipei/redesign-convertitore-dark.jpg"
lang: it_IT
categories:
- Progetti Personali
keywords: jekyll, redesign, ipui, ipei, dect, claude code, ia, bilingue
tags:
- jekyll
- redesign
- claude-code
- ia
- javascript
permalink: "/it/blog/progetti-personali/:title/"
redirect_from: "/blog/progetti-personali/il-redesign-di-ipui2ipei/"
icon: fa-refresh
---

Nel 2019 ho scritto [un post]({{ '/it/blog/tools/ipui-to-ipei/' | relative_url }}) su un problema piccolo e molto specifico: registrare un cordless Siemens su un centralino di un altro produttore richiede di convertire il suo codice IPUI in un codice IPEI standard. Per risolverlo avevo aggiustato [ipui2ipei](https://cristiancastellari.it/ipui2ipei/), un tool trovato su GitHub, e me n'ero sostanzialmente dimenticato.

* TOC
{:toc}

## Perché rifare un tool che quasi nessuno nota

Guardando Google Search Console per quel dominio, la cosa che salta all'occhio non sono i numeri assoluti — è uno strumento verticale per un problema di nicchia, il traffico è quello che ci si aspetta — ma **cosa** cercano le persone per arrivarci. Quasi nessuno digita "ipui2ipei", il nome del progetto: la query dominante è una variante diretta del problema, "ipui to ipei", seguita da "ipei", "ipei to ipui" e persino "ipui gigaset" — qualcuno che cerca partendo dalla marca del proprio telefono, non dal nome dello standard. Sono persone che non sanno che il mio tool esiste, sanno solo di avere in mano un cordless Siemens/Gigaset e un centralino che non lo riconosce.

La posizione media per queste query non-branded è comunque bassa, vicina alla decima — eppure il CTR resta sopra il 12%, niente male per un risultato che in teoria è sepolto in fondo alla prima pagina. Chi arriva, insomma, sa esattamente cosa vuole trovare.

C'è un altro modo di guardare la stessa cosa: fra tutte le pagine di destinazione da ricerca organica di `cristiancastellari.it`, quasi tre quarti dei click finiscono dritti su `/ipui2ipei/`. Il vecchio post del 2019 che lo racconta è il secondo — insieme, tool e articolo, si prendono quasi 9 click su 10 fra le pagine più cercate del sito. Uno strumento così merita di funzionare bene su schermi diversi da quello 2014 per cui era stato pensato, non di essere abbandonato solo perché nessuno se ne lamenta apertamente.

## Cosa c'era prima, e perché non bastava più

Il tool era un fork del 2014 di un progetto di Gorka Hernández, aggiustato da me negli anni fra il 2018 e il 2019: Bootstrap 3.2.0, jQuery, un CSS esterno ma niente di più. Funzionava — è ancora online da anni senza un solo bug segnalato — ma portava lo stesso tipo di debito tecnico da cui sono partito per [ricostruire il sito principale]({{ '/it/blog/progetti-personali/il-nuovo-sito-parte-1-perche-ripartire-da-zero/' | relative_url }}) poche settimane fa: una libreria CSS ferma al 2014, uno script scritto con variabili globali mai dichiarate con `var`, zero automazione — ogni modifica andava caricata a mano via FTP.

Con lo schema Jekyll 4 + GitHub Actions appena collaudato e documentato sul sito principale, riapplicarlo qui è stato più veloce che lasciare le cose come stavano.

## Stesso schema, aggiustamenti su misura

Non è stato un copia-incolla: ipui2ipei vive come *project page* sotto lo stesso dominio custom del sito principale (`cristiancastellari.it/ipui2ipei/`), quindi ha un `baseurl` diverso — ogni link e ogni asset passa dal filtro giusto di Jekyll per restare coerente sotto quel prefisso, cosa che sul sito principale (che vive alla radice del dominio) non serve.

Il vincolo più importante era però lo stesso di allora: **l'URL storico già indicizzato da anni doveva continuare a funzionare**. `https://cristiancastellari.it/ipui2ipei/` oggi fa da redirect verso la nuova pagina italiana — chi ha quel link salvato nei preferiti, o lo trova ancora citato da qualche parte, non nota nessuna differenza.

Ho anche colto l'occasione per renderlo bilingue, con pagine italiane e inglesi separate invece di uno switcher lato client: la maggior parte del traffico arriva da ricerca organica, e uno switcher JavaScript è invisibile a un motore di ricerca quanto lo è a chi digita "ipei to ipui" in inglese dall'altra parte del mondo.

## Riscrivere l'algoritmo senza cambiare un solo bit di output

La parte che mi metteva più a disagio era toccare `ipui2ipei.js`: è il cuore del tool, e un bug introdotto lì produce un IPEI sbagliato senza che nessuno se ne accorga finché qualcuno non prova a registrare un telefono che non si aggancia. L'ho riscritto da zero — via jQuery, via le variabili globali implicite dell'originale — ma **la matematica non doveva cambiare di una virgola**: stesso scarto del primo carattere, stessa suddivisione in due blocchi esadecimali, stesso zero-padding, stesso checksum secondo lo standard ETSI EN 300 175-6.

Per essere sicuro di non aver rotto nulla ho scritto un piccolo harness che esegue in parallelo l'algoritmo originale (trascritto tale e quale) e quello nuovo su una batteria di IPUI di prova — compreso un caso limite trovato apposta per forza bruta, quello in cui il checksum dà esattamente 10 e va sostituito con un asterisco secondo lo standard. Output identico su tutta la batteria, poi riconfermato aprendo davvero il tool in un browser headless, compilando il campo e premendo Converti via script, prima di fidarmi della riscrittura.

<img class="post-image post-image--on-light" src="{{ '/static/assets/img/blog/ipuitoipei/redesign-convertitore.jpg' | relative_url }}" alt="Il nuovo convertitore ipui2ipei">
<img class="post-image post-image--on-dark" src="{{ '/static/assets/img/blog/ipuitoipei/redesign-convertitore-dark.jpg' | relative_url }}" alt="Il nuovo convertitore ipui2ipei">

Un paio di dettagli che prima non c'erano: l'errore di validazione, che era un `alert()` bloccante del browser, è diventato un messaggio inline con bordo colorato; e il bottone Converti è ora un vero `type="submit"`, quindi premere Invio nel campo IPUI avvia la conversione da solo, senza dover cliccare — comportamento nativo del form, non uno script scritto apposta per intercettare il tasto.

## La palette: dal primo tentativo a quello buono

La prima proposta puntava su un'identità visiva totalmente indipendente dal sito principale, in ambra. L'ho rivista dopo essermela guardata per un po': il bottone Converti e il bordo di validazione dell'IPUI sono rimasti verdi in entrambi i temi — un richiamo diretto al vecchio `btn-success` di Bootstrap, l'unica cosa della palette originale che valeva la pena conservare — mentre testo ed evidenziazioni sono tornati sul blu del sito principale nel tema chiaro, con un arancione (un omaggio al mondo Gigaset/DECT di cui parla lo strumento) nel tema scuro.

Altri due dettagli minori ma fastidiosi da guardare, prima: nello switcher lingua e nel nav in alto, l'elemento su cui ti trovi già era discreto e quello cliccabile era colorato — esattamente il contrario di quello che ci si aspetta guardando una UI del genere. Ho invertito la gerarchia: ora "sei qui" è evidenziato con un pill pieno, il resto si accende solo al passaggio del mouse.

## Una nuova pagina Contatti

Lo strumento non aveva alcun modo per chi lo usa di contattarmi, se non intuendo che il progetto fosse mio da un link GitHub in fondo alla pagina. Ho aggiunto una pagina Contatti che replica la struttura di quella del sito principale — stesso saluto personale come titolo ("Ciao, sono Cristian!") al posto di un anonimo "Contatti", stessa griglia di card per canale.

<img class="post-image post-image--on-light" src="{{ '/static/assets/img/blog/ipuitoipei/redesign-contatti.jpg' | relative_url }}" alt="La nuova pagina Contatti di ipui2ipei">
<img class="post-image post-image--on-dark" src="{{ '/static/assets/img/blog/ipuitoipei/redesign-contatti-dark.jpg' | relative_url }}" alt="La nuova pagina Contatti di ipui2ipei">

Le icone però sono disegnate a mano in SVG invece di venire da un font di icone: reintrodurne uno solo per sei icone in una pagina avrebbe vanificato il senso di essersi liberati di Bootstrap e di tutto il resto in un colpo solo.

## Un bug trovato scrivendo la pagina Contatti

Controllando l'HTML generato per la nuova pagina mi sono accorto che il loop che genera i tag `apple-touch-icon` per le otto dimensioni richieste (57px, 72px, e così via) non funzionava come pensavo: lo split della stringa `"57,72,114,..."` avveniva *dentro* il ciclo invece che prima, quindi il loop girava una sola volta con l'intera stringa come valore unico, producendo un solo link con un nome file illeggibile invece di otto tag separati. Un bug presente fin dalla prima stesura del tema, mai notato perché nessuno controlla mai l'HTML generato per le icone del touch bar di iOS — finché non serve confrontarlo per una pagina nuova.

## Cosa mi porto a casa

Il sito principale aveva una scusa evidente per essere ricostruito: è il mio biglietto da visita, ci scrivo sopra, lo guardo ogni giorno. Ipui2ipei non ce l'aveva — è un tool che io stesso apro forse una volta all'anno. Eppure è probabilmente lo strumento che aiuta più sconosciuti, in silenzio, di qualsiasi altra cosa io abbia pubblicato: non genera conversazioni, non genera commenti, genera solo un telefono che finalmente si registra. Vale la pena curarlo con lo stesso standard delle cose che si vedono di più, non di meno — nessuno lo nota quando è fatto bene, ma qualcuno lo nota di sicuro quando è fatto male.
