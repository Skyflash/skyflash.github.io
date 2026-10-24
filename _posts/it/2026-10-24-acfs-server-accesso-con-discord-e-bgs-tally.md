---
title: "ACFS Server, seconda parte: accesso con Discord, BGS-Tally e una roadmap senza confini"
layout: post
date: '2026-10-24 09:00:00'
description: "Come il server dell'ACFS BGS Tool è diventato dello squadrone: accesso con Discord senza bot e con i ruoli come permessi, chiavi BGS-Tally self-service filtrate sul PC del pilota, due bug trovati leggendo il codice del plugin, e quello che viene dopo."
intro: "Un server che ascolta la galassia è utile. Un server che sa chi sei, cosa puoi fare nello squadrone e cosa hai fatto ieri sera per la fazione è un'altra cosa. In una settimana sono sparite le password condivise, i piloti si sono collegati da soli, e la roadmap ha smesso di avere un fondo."
social:
  default: |-
    Un server che ascolta la galassia di Elite Dangerous è utile. Uno che sa chi sei nello squadrone è un'altra cosa.

    Seconda parte dell'ACFS Server: accesso con Discord senza bot, con i ruoli del server come permessi, e via tutte le password condivise. Poi il plugin BGS-Tally, che manda al server il lavoro dei piloti filtrato già sul loro PC.

    La lezione: due bug li abbiamo trovati solo leggendo il codice del plugin. I test passavano, perché simulavano il plugin come lo immaginavamo noi.

    Voi come gestite accessi e permessi nelle vostre community?
  threads: "Seconda parte dell'ACFS Server: accesso con Discord senza bot, i ruoli del server come permessi, via le password condivise, e il plugin BGS-Tally che manda il lavoro dei piloti filtrato sul loro PC. Due bug trovati solo leggendo il codice del plugin: i test simulavano il plugin come lo immaginavamo. Voi come gestite i permessi nelle community?"
image: "/static/assets/img/blog/acfs-server-discord-bgs-tally/cover.png"
lang: it_IT
categories:
- Progetti Personali
keywords: acfs server, elite dangerous, bgs, discord oauth2, accesso con discord, ruoli discord, bgs-tally, edmc, api, flotta stellare, claude code, chiavi api
tags:
- elite dangerous
- claude-code
- ia
- api
- sicurezza
- discord
permalink: "/it/blog/progetti-personali/:title/"
redirect_from: "/blog/progetti-personali/acfs-server-accesso-con-discord-e-bgs-tally/"
icon: fa-users
---

Nella [prima parte]({{ '/it/blog/progetti-personali/acfs-server-un-server-nostro-per-il-bgs-di-elite-dangerous/' | relative_url }}) ho raccontato come l'ACFS BGS Tool, lo strumento BGS del nostro squadrone di Elite Dangerous, si è trovato un server: un ascoltatore del flusso EDDN, un database, un'API in sola lettura. Qui racconto cosa succede quando quel server comincia a conoscere le persone.

* TOC
{:toc}

## Le password buttate lì

Prima del server il tool aveva tre modi di proteggere le cose, tutti imperfetti:

- la pagina degli **Ordini**, dove gli ufficiali scrivono gli ordini del giorno, si apriva con una frase condivisa controllata nel browser: chi sapeva aprire gli strumenti per sviluppatori poteva farne a meno;
- **"Assegna"**, che scrive nel foglio Google l'architetto di un sistema, aveva una password vera, controllata da uno script dal lato del foglio, ma era una sola per tutti gli ufficiali, da cambiare ogni volta che qualcuno usciva;
- le prime chiavi per il plugin BGS-Tally (ci arrivo fra poco) le generavo io sul server e le passavo a mano.

La richiesta era chiara: un vero pannello di accesso, senza password buttate lì a caso.

## Accesso con Discord, senza bot

Lo squadrone vive su Discord, e lì ci sono già i membri e i ruoli: Ammiraglio, Vice Ammiraglio, Contrammiraglio, Membro Flotta, Cadetto. Bastava farli valere anche per il tool.

Discord permette a un'applicazione di chiedere, con il consenso dell'utente, chi è e quali ruoli ha in un server. Si fa con OAuth2 e due permessi (`identify` e `guilds.members.read`), senza installare nessun bot. Il pilota preme "Accedi con Discord", autorizza l'applicazione "ACFS BGS Tool", e il nostro server riceve identità e ruoli. Apre una sessione di sette giorni, con un cookie che JavaScript non può leggere, e nel database ne salva solo l'impronta. I token di Discord non si conservano: un cambio di ruolo vale dal login successivo.

Ne escono tre livelli:

| Livello | Chi | Cosa può fare |
|---|---|---|
| **Collegato** | Chiunque sia nel server Discord dello squadrone | Generarsi la chiave per BGS-Tally |
| **Membro** | Membro Flotta e Cadetto | Leggere gli Ordini pubblicati e la pagina Attività |
| **Ufficiale** | Ammiraglio, Vice Ammiraglio, Contrammiraglio | Scrivere gli Ordini, "Assegna", gestire le chiavi dei piloti |

Chi perde un ruolo perde l'accesso, senza che nessuno debba cambiare una password. La password di "Assegna" esiste ancora, ma la conosce solo il server: gli ufficiali non devono più ricordarla, e il nome di chi assegna è quello di Discord.

C'è anche un limite, scritto nella roadmap invece che nascosto. Senza un bot il server controlla i ruoli solo al momento dell'accesso, e non sa chi esce dal server Discord. Una chiave BGS-Tally, quindi, non si revoca da sola: lo fanno gli ufficiali, da una pagina apposita. Un bot nella stessa applicazione Discord potrà farlo in automatico, più avanti.

## BGS-Tally: il lavoro dei piloti, senza copia e incolla

Quasi tutti i piloti dello squadrone usano [BGS-Tally](https://github.com/aussig/BGS-Tally), un plugin di EDMC che legge il diario di volo e tiene il conto del lavoro BGS: missioni, taglie, bond di combattimento, zone di conflitto, commercio. Il lavoro si riporta su Discord copiando a mano il testo preparato dal plugin, in un canale apposito.

Non tutti lo usano (io, per esempio, no), quindi il canale resta. Ma BGS-Tally può anche mandare i dati a un server scelto dal pilota, con una chiave. È lì che il nostro server è diventato utile in un modo nuovo.

**Solo il lavoro per Flotta Stellare.** Era la condizione, ed è stata la parte più interessante da progettare. Quando il plugin si collega, il server gli dice quali eventi vuole e con quali filtri: salti solo nei sistemi dove c'è la nostra fazione, mercato solo nelle sue stazioni, missioni solo se toccano la sua influenza. Quello che non ci riguarda **non parte nemmeno dal PC del pilota**. Il server poi ricontrolla tutto e del riepilogo del tick, che arriva intero, tiene solo la nostra voce.

**Chiavi self-service.** Chi è collegato con Discord si genera, rigenera e revoca la chiave da solo, dal menu dell'account. Ogni chiave ha un nome ricavato da quello su Discord, che è anche l'inizio della chiave: nelle impostazioni del plugin e nei registri si capisce a colpo d'occhio di chi è. Nel database, come per le sessioni, solo l'impronta. Il primo pilota si è collegato da solo, senza passare da un ufficiale, la sera stessa in cui la funzione è uscita.

**La pagina Attività.** Il lavoro ricevuto, per tick, sistema e pilota, sul modello delle categorie di BGS-Tally. In beta solo per gli ufficiali, dal 20 ottobre aperta a tutti i membri.

## Due bug che i test non potevano vedere

Il server ha i suoi test, e passavano. Ma due cose non tornavano con i dati veri:

- **Il riepilogo del tick veniva rifiutato.** Il server lo aspettava con una richiesta `POST`; leggendo il codice del plugin è venuto fuori che arriva con `PUT`.
- **Le zone di conflitto non si contavano.** Il server le cercava come `spacecz` e `groundcz`; nel plugin si chiamano `czspace` e `czground`.

In tutti e due i casi i test erano verdi perché simulavano il plugin come lo immaginavamo noi, non com'è. È la stessa lezione del tool, vista da un'altra parte: il codice può essere coerente e sbagliato. Lì serviva la conoscenza del gioco, qui il codice di qualcun altro. Leggerlo è stato il lavoro più utile di Claude Code in questa fase: il plugin è open source, e le risposte erano lì.

Lo stesso codice ha spiegato anche perché le prime chiavi non funzionavano: il plugin toglie dalla chiave tutto ciò che non è una lettera o una cifra, e le prime chiavi potevano contenere un trattino. Ora le chiavi sono fatte solo di lettere e cifre.

## Gli Ordini, finalmente condivisi

Con i ruoli, gli Ordini sono diventati un documento condiviso: una bozza sul server che gli ufficiali scrivono insieme, con un avviso se qualcun altro l'ha cambiata nel frattempo, e un pulsante per pubblicarla ai membri.

Il primo editor era a moduli: un campo per ogni sistema, ogni priorità, ogni tipo di intervento. Funzionava, ma lasciava troppi campi all'autore, e gli ordini li scrivevo più in fretta in VS Code. Il 22 ottobre è diventato un editor di testo, con l'anteprima com'è su Discord e una barra delle emoji. Anche questa è una decisione che nessun test poteva prendere: lo strumento giusto era quello più semplice.

## Il limite è la fantasia

Una settimana fa il server non esisteva. Oggi è il punto in cui si incontrano il tool, la mappa del sito, Discord e i plugin dei piloti. Ogni idea nuova parte già con un database, un'API, un accesso e i dati di chi gioca. Nella roadmap, in ordine sparso:

- **Avviso dei dati fermi.** Dal 19 ottobre Crowfor è rimasto senza dati per giorni, mentre Inara mostrava un'elezione in arrivo: nessuno ci passava con l'invio a EDDN attivo. Un messaggio dirà quando un sistema importante non riceve dati da più di 24 ore, perché qualcuno ci faccia un salto.
- **I salti di BGS-Tally come seconda fonte**, accanto a EDDN, per i piloti che non inviano a EDDN.
- **Gli Ordini dentro il gioco.** BGS-Tally può ricevere dal server degli obiettivi di squadrone e mostrarli in sovrimpressione mentre si vola, con l'avanzamento calcolato dal plugin.
- **Le classifiche del lavoro**, per tick, settimana, mese e campagna, per categoria e senza un punteggio unico. Sommare crediti di commercio, bond e taglie premierebbe chi fa numeri, non chi aiuta il BGS.
- **La Pattuglia**: i sistemi importanti ancora fermi a prima del tick, con la spunta automatica appena l'ascoltatore vede passare uno scout.
- **Il Colony Plotter**, per trovare i sistemi da colonizzare vicino alle nostre stazioni, e l'avanzamento delle colonie in costruzione.
- **Un plugin EDMC nostro**, per mostrare nel gioco la priorità del sistema in cui ci si trova, l'architetto e gli ordini del giorno.

Non tutto si farà, e non tutto subito. Ma è cambiata la domanda: non più "si può fare?", ma "serve allo squadrone?".

Molte di queste idee vengono dagli strumenti che i Canonn pubblicano da anni per tutta la comunità: guardare come hanno risolto loro lo stesso problema è servito più di qualsiasi documentazione. Se gestite un gruppo, in Elite o altrove, e avete risolto in un altro modo accessi, permessi o raccolta dei dati dei membri, mi piacerebbe sapere come. E voi, cosa mettereste in cima a quella lista?
