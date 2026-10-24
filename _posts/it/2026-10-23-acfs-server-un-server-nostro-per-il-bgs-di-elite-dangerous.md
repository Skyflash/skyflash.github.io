---
title: "ACFS Server: un server nostro, a zero euro, per il BGS di Elite Dangerous"
layout: post
date: '2026-10-23 09:00:00'
description: "Perché l'ACFS BGS Tool è passato da un sito statico a un server sempre acceso: ascoltatore EDDN, SQLite, Docker e Caddy su Oracle Cloud Free, aggiornamento automatico da GitHub, avvisi su Discord e un'API che oggi alimenta anche la mappa 3D dello squadrone."
intro: "Un sito statico aggiornato da GitHub Actions ha retto due settimane. Poi le domande dello squadrone sono diventate più veloci dei dati. In un fine settimana, con Claude Code, è nato un server tutto nostro: ascolta la galassia in diretta, ricorda quello che vede e lo racconta a chi ne ha bisogno."
social:
  default: |-
    Ho costruito un tool per il mio squadrone di Elite Dangerous, un simulatore spaziale che riproduce in scala 1:1 l'intera Galassia.
    Doveva essere un progettino da weekend. È diventato decisamente di più.

    Qualche settimana fa io e Claude ci siamo messi a creare uno strumento che ci dicesse dove conviene operare ogni giorno. La nostra passione è il BGS: una simulazione politica interna al gioco che permette alle fazioni di espandersi e "esistere davvero" in game.

    In quattro giorni avevamo un sito statico che si aggiornava da solo. Perfetto.
    Peccato che GitHub, ogni tanto, considerasse "ogni mezz'ora" un concetto filosofico.

    E il dato più importante? Il punteggio di guerre ed elezioni.
    Nessuna fonte affidabile. Zero.

    Quindi abbiamo fatto quello che una persona sana eviterebbe:
    un server tutto nostro, che ascolta in diretta i dati che i giocatori mandano mentre volano.
    La prima notte aveva già visto tutto quello che aveva visto Spansh… più i punteggi che Spansh non conserva.

    Poi ci siamo fatti prendere la mano:
    – login con Discord (basta password urlate in chat)
    – plugin dei piloti filtrato direttamente sul loro PC
    – solo i dati utili alla squadra

    La parte più divertente?
    Due bug invisibili ai test. Li abbiamo trovati solo aprendo il codice del plugin.
    Mai fidarsi delle supposizioni.

    E voi? Avete mai costruito qualcosa per una community o un hobby? Mi piacerebbe leggere le vostre storie.

    Ho raccontato tutto in due puntate: la prima è qui 👇
  threads: "Doveva essere un progettino da weekend per il mio squadrone di Elite Dangerous. È diventato un server tutto nostro, che ascolta in diretta i dati dei giocatori, con login Discord e i dati dei piloti filtrati sul loro PC. E due bug invisibili ai test, trovati solo aprendo il codice del plugin. Voi avete mai costruito qualcosa per una community? 👇"
image: "/static/assets/img/blog/acfs-server/cover.png"
lang: it_IT
categories:
- Progetti Personali
keywords: acfs server, elite dangerous, bgs, eddn, zeromq, sqlite, docker, docker compose, caddy, oracle cloud free, api, flotta stellare, claude code, healthchecks.io, discord webhook
tags:
- elite dangerous
- claude-code
- ia
- api
- docker
- database
- backup
- dati aperti
permalink: "/it/blog/progetti-personali/:title/"
redirect_from: "/blog/progetti-personali/acfs-server-un-server-nostro-per-il-bgs-di-elite-dangerous/"
icon: fa-server
---

Due settimane fa ho raccontato l'[ACFS BGS Tool]({{ '/it/blog/progetti-personali/acfs-bgs-tool-elite-dangerous-claude-code/' | relative_url }}), lo strumento con cui l'**Alto Comando Flotta Stellare**, lo squadrone di Elite Dangerous di cui faccio parte, decide dove lavorare dopo ogni tick. Era un sito statico su GitHub Pages, con i dati scaricati da Spansh ogni mezz'ora. Finiva così: "nella roadmap ci sono un report automatico su Discord dopo ogni tick…".

Il report è arrivato, ma non nel modo previsto. Nel frattempo è arrivato un server.

* TOC
{:toc}

## Dove un sito statico non arriva

Il tool funzionava, e lo squadrone lo usava ogni giorno. Proprio per questo i suoi limiti hanno cominciato a vedersi:

- **I cron di GitHub saltano.** Sulla carta 48 aggiornamenti al giorno; in pratica GitHub esegue le pianificazioni quando ha tempo, e in certi giorni ne faceva tre.
- **Spansh arriva dopo.** Si alimenta dal flusso dei giocatori, ma lo elabora con il suo ritmo: un cambio di controllo poteva comparire nel tool ore dopo.
- **Il punteggio dei conflitti non c'era.** Spansh non lo conserva, EliteBGS ce l'ha ma il suo database cade di continuo (segnalato a mano, rimesso in piedi a mano, giù di nuovo dopo poche ore), Inara blocca le richieste automatiche.
- **Le password stavano nel browser.** La pagina degli Ordini era protetta da una frase condivisa controllata in JavaScript: un deterrente, non una protezione. Di questo parlo nel prossimo articolo.

La spinta finale è venuta dai **Canonn**, gli stessi da cui il tool era partito. Il 17 ottobre ci hanno girato un messaggio del loro bot Discord: "Canonn lost control of Lyncis Sector CL-Y d68", con influenze, architetto e fazione preferita. Leggendo i loro repository pubblici si ricostruiva la catena: dall'11 ottobre avevano un ascoltatore sempre acceso, un database proprio, un'API e una tabella di eventi. La strada c'era, e qualcuno l'aveva già percorsa.

## Da dove arrivano i dati

<img class="post-image post-image--side" src="{{ '/static/assets/img/blog/acfs-server/tron-flusso.jpg' | relative_url }}" alt="Illustrazione in stile Tron: una figura in tuta nera con linee luminose, a braccia alzate su una piattaforma circolare, investita da una pioggia di dati blu e arancioni">

Il gioco non ha un'API pubblica per la galassia. I dati li portano i giocatori stessi: programmi come EDMC leggono il diario di volo (il *journal*) e, se il pilota lo permette, inviano a **[EDDN](https://github.com/EDCD/EDDN)**, l'Elite Dangerous Data Network, ogni salto, ogni attracco, ogni mercato visitato.

Il risultato è un fiume. Migliaia di comandanti, in ogni angolo della galassia e a ogni ora, riversano lì quello che vedono. EDDN non conserva niente e non risponde a domande: trasmette e basta. Chi vuole i dati si mette in ascolto e li prende come arrivano. Spansh, Inara ed EliteBGS fanno così, e da adesso anche noi.

Ogni salto in un sistema popolato porta con sé l'elenco delle fazioni, con influenze, stati e conflitti. E nei conflitti c'è un campo, `WonDays`, con i giorni vinti da ciascuna parte: il punteggio che cercavamo da settimane. Bastava ascoltare.

## L'ascoltatore, una notte di prova

La sera del 17 ottobre, con Claude Code, è nato un ascoltatore in **Node**, poche centinaia di righe: si collega al flusso con **ZeroMQ** e tiene solo i messaggi dei circa 390 sistemi in cui è presente la nostra fazione, salvandoli in **SQLite**. Per quel volume di dati, qualche megabyte all'anno, un database server non serve: Node 24 ha SQLite integrato.

Prime misure: circa 1.300 messaggi al minuto da tutta la galassia, una settantina di salti in sistemi popolati. In una prova di due minuti, tutti i messaggi con un conflitto avevano il punteggio.

Poi l'ho lasciato acceso sul PC tutta la notte, quasi dieci ore. La mattina dopo il confronto con Spansh: nello stesso intervallo Spansh aveva aggiornato 57 dei nostri sistemi, l'ascoltatore 59, compresi tutti i 57 di Spansh. In più, il punteggio di sette conflitti, fra cui l'elezione di Crowfor: 4-0 per noi. Crowfor è passata a Flotta Stellare, e la cronaca della conquista è [sul sito dello squadrone](https://flottastellare.it/blog/crowfor-roccaforte-edmund-mahon/).

Una notte di dati ha deciso la cosa più importante: valeva la pena di metterlo su un server.

## Dove farlo girare

Il traffico non era un problema: poche decine di utenti e un flusso in entrata gratuito ovunque. Servivano una CPU e un gigabyte di memoria, sempre accesi. Il confronto, fatto con Claude in una sessione di analisi, ha messo in fila VPS a pagamento (OVH, Hetzner, Hostinger), i piani gratuiti dei grandi cloud, le piattaforme a container (che spengono il container quando nessuno lo visita, cioè fermerebbero l'ascoltatore) e un Raspberry Pi a casa.

La scelta è stata **Oracle Cloud Free**: una macchina ARM a Francoforte, gratis senza scadenza. Con i suoi rischi, scritti nella roadmap prima di cominciare: niente assistenza, istanze gratuite poco usate che Oracle può recuperare, account chiusi senza preavviso. Oracle offre di evitare il recupero passando al piano a consumo, gratis entro i limiti, ma chiedeva un'autorizzazione di 93 euro sulla carta, e ho preferito di no. Il rimedio è un altro: tutto sta in un `docker-compose.yml` con i backup fuori dalla macchina, quindi ricominciare su una VPS qualsiasi è questione di un'ora o due.

## Com'è fatto

Il 18 ottobre il server era in produzione. Oggi sono cinque container:

| Container | Cosa fa |
|---|---|
| `listener` | Ascolta EDDN, salva le osservazioni, ricava gli eventi, manda gli avvisi su Discord |
| `api` | L'API in sola lettura su `api.flottastellare.it` |
| `auth` | L'accesso con Discord (nel prossimo articolo) |
| `tally` | La ricezione dei dati del plugin BGS-Tally (anche questa nel prossimo articolo) |
| `caddy` | HTTPS davanti a tutti, con i certificati Let's Encrypt rinnovati da soli |

Il codice sta in un repository privato, separato da quello del tool. La decisione era precisa: il server deve poter servire anche altro, non solo il BGS.

Il tool legge dall'API fazioni, influenze, stati, controllo e punteggi, quando il server li ha visti dopo Spansh. Se il server non risponde entro sei secondi, usa i dati di sempre. È la regola che ha guidato tutto il resto: **un server fermo deve rendere il tool meno fresco, non rotto**.

## Le cose che non si vedono

Un servizio sempre acceso ha bisogno di cure che un sito statico non chiede. Sono la parte meno spettacolare, ed è quella che mi fa dormire tranquillo:

- **Ricollegamento.** Con ZeroMQ una connessione può restare aperta senza ricevere più niente. Dopo due minuti di silenzio l'ascoltatore la chiude e ne apre un'altra. L'idea viene dai contatori pubblici dei Canonn, che fanno lo stesso.
- **Battito.** Ogni cinque minuti l'ascoltatore avvisa [healthchecks.io](https://healthchecks.io), ma solo se sta davvero ricevendo messaggi. Se il battito manca arriva un'email. Non su Discord: quel canale è dello squadrone, e un avviso tecnico lì sarebbe solo rumore.
- **Backup.** Ogni notte una copia compressa del database, sette giorni sul server e una nel bucket di Oracle, caricata con un link di sola scrittura. Il ripristino l'ho provato prima di fidarmi.
- **Aggiornamento da GitHub.** Ogni cinque minuti il server controlla se il ramo principale ha un commit nuovo e, se sì, ricostruisce i container. Se la ricostruzione fallisce, i vecchi restano accesi. Il server legge GitHub con una chiave di sola lettura, e su GitHub non c'è nessuna chiave che apra il server.
- **`bgslogs`.** Un comando per guardare il server dal vivo dopo l'accesso SSH: l'ascoltatore che riceve, gli eventi, gli scarichi da Spansh, gli aggiornamenti. Con `bgslogs stato` la salute di tutto in una schermata, con `bgslogs cerca Crowfor` tutto quello che i servizi hanno scritto su un sistema. Legge soltanto i log, senza toccare niente.

## Eventi: il report che è arrivato da un'altra parte

Il report su Discord previsto nella roadmap del tool doveva partire da GitHub Actions, confrontando due scarichi di Spansh. Con il server la strada è cambiata: l'ascoltatore confronta ogni osservazione nuova di un sistema con la precedente e ne ricava gli **eventi**. Controllo preso o perso, conflitto in arrivo, iniziato o finito, con vincitore e punteggio, la nostra fazione entrata o uscita da un sistema, influenza sotto la soglia della ritirata.

Quelli che ci riguardano partono come riquadri colorati nel canale del BGS dello squadrone, pochi secondi dopo il salto del giocatore che li ha rivelati, invece che ore dopo con Spansh. Su quel canale c'è stata una sola regola: niente rumore. Gli stati globali come l'espansione, per esempio, non si mandano: comparirebbero in tutti i sistemi insieme.

## Un'API per più strumenti

Fin dal primo giorno l'API è stata pensata per più utilizzatori, non solo per il tool: versione nel percorso (`/v1/…`), formato documentato, sistemi identificati dal loro id64 come testo, perché come numero supera gli interi sicuri di JavaScript.

Il secondo utilizzatore è arrivato oggi: la **mappa 3D** di [flottastellare.it](https://flottastellare.it/map/). Prima si aggiornava lanciando a mano uno script Python. Ora il server scarica da sé Spansh ogni ora e pubblica `/v1/site`, con i sistemi già uniti: coordinate, popolazione e servizi delle stazioni da Spansh, controllo e fazioni da chi li ha visti più di recente. La mappa lo legge dal browser; se il server non risponde, ripiega sul file del tool e poi sull'ultima copia salvata. La stessa regola di prima.

Nella prova, il totale degli abitanti dei sistemi controllati è venuto identico, al singolo abitante, a quello della pagina dello squadrone calcolato con lo script vecchio: 25.822.439.448. È il tipo di controllo che dà fiducia nel passaggio.

## Come ho lavorato

Lo stesso metodo del tool, con una differenza. Il tool è un sito: se sbaglio, pubblico una pagina sbagliata. Il server è una macchina accesa su Internet, con chiavi, porte aperte e dati dei piloti. Ogni passo è passato da una decisione scritta nella roadmap, con la data e le alternative scartate, prima di diventare codice. Claude Code ha scritto il codice, proposto le architetture e letto i repository dei Canonn per capire come avevano fatto loro. Dove riprendere, riscrivere o lasciare stare l'abbiamo deciso guardando le licenze.

Le decisioni che contano, però, non erano tecniche. Quanto rumore accettare su Discord. Se rischiare la carta di credito con Oracle. Che cosa un ufficiale deve poter fare senza conoscere una password. Sono le domande che un assistente può aiutare a formulare, ma a cui risponde chi conosce lo squadrone.

## E adesso

Il server è in produzione da cinque giorni, e ha già cambiato il modo in cui il tool e il sito ricevono i dati. Il prossimo articolo racconta come è diventato dello squadrone: l'accesso con Discord, i dati del plugin BGS-Tally e quello che c'è nella roadmap.

Voi avete un progetto personale che a un certo punto ha avuto bisogno di un server sempre acceso? Dove lo fate girare, e cosa vi ha fatto scegliere?
