---
layout: post
lang: it_IT
title: "Come proteggere un sito dagli attacchi - Parte 1 - I bad crawler"
date: '2012-05-07 11:36:11'
description: "Come creare una trappola (\"blackhole\") per bloccare i bad crawler che sovraccaricano il server, usando lo script Blackhole di Perishable Press."
intro: "Questo blog da alcuni giorni si trova sotto attacco dei cosiddetti \"bad crawler\", cioè di bot il cui scopo consiste nel download indiscriminato di ogni singolo elemento che componga il sito web."
image: "/static/assets/img/blog/bad-crawlers/cover.jpg"
categories:
- Infrastruttura & Sistemi
keywords: sicurezza, bad crawler, bot, blackhole, wordpress
tags:
- sicurezza
- bot
- bad crawler
- server
- php
- blackhole
permalink: "/it/blog/infrastruttura/:title/"
redirect_from:
  - "/2012/05/come-proteggere-il-proprio-sito-dagli-attacchi-dei-bad-crawlers-parte-1/"
  - "/blog/infrastruttura/come-proteggere-il-proprio-sito-dagli-attacchi-dei-bad-crawlers-parte-1/"
icon: fa-shield
---
Questo blog da alcuni giorni si trova sotto attacco dei cosiddetti "bad crawler", cioè di bot il cui scopo consiste nel download indiscriminato di ogni singolo elemento che componga il sito web.

Questo genere di attacco provoca un enorme spreco di banda passante (nel nostro caso, si sono viste punte anche di **2Gb/sec di upload verso Internet per diverse ore**, reiterati più volte nell'arco della giornata) ed un impegno della CPU del server che molto spesso raggiunge il 100%, arrivando a bloccare così non solo il sito colpito, ma tutti quanti si trovano ospitati all'interno della stessa macchina.

Infatti, negli ultimi 4 giorni la media delle visite su www.skyflash.it si è quasi dimezzata, arrivando a punte minime davvero non abituali per questo blog, proprio a causa dei frequenti blocchi del server, incapace di soddisfare tutte le richieste a cui era sottoposto. Nei giorni passati sono state ovviamente prese alcune contromisure, la cui bontà è ancora in fase di testing. Alcune di queste sembrano più efficaci di altre che sono quindi state scartate, o che devono ancora ricevere il necessario tuning.

> Questo è il primo articolo dedicato alla protezione di un sito Internet basato su WordPress, a cui ne seguirà [un altro](/it/blog/infrastruttura/protezione-di-un-sito-parte-2-htaccess/), basato sulla nostra esperienza diretta e su una discreta quantità di informazioni recepita in rete in questi giorni.

* TOC
{:toc}

## Una trappola per i bots maligni

Il primo passo da compiere consiste nel **realizzare una trappola in grado di ingabbiare i crawlers**. Un web crawler non fa altro che collegarsi tramite una richiesta HTTP al sito da colpire, iniziando a scaricare tutto quanto trovi in quella pagina, in modo ricorsivo seguendo ogni singolo link che viene rilevato all'interno della stessa.

L'idea, quindi, consiste nel fargli trovare un link invisibile ad un normale visitatore, che lo faccia puntare ad una specifica directory, che contiene la trappola stessa. La trappola altro non è che uno script php in grado di bannare l'IP del crawler, impedendogli di conseguenza ogni possibile accesso in futuro.

Un crawler normale (come ad esempio googlebot, bing eccetera) non sarà interessato a seguire il link nascosto, e non accederà mai alla trappola in quanto la stessa viene negata all'interno del file robots.txt (file che viene normalmente letto ed interpretato da qualsiasi bot "legale" ed ovviamente ignorato da chi ha intenzioni malevole)

## Creiamo la trappola

Per la creazione della trappola, dopo aver provato un paio di script, ho deciso di adottare Blackhole di PerishablePress.

In realtà ci sarebbe anche l'ottimo ZB Block, ma devo ancora finire di approfondirne la conoscenza, e quando l'ho installato e provato per 60 minuti circa, il risultato è stato il blocco anche di visitatori normali, tutti provenienti da ADSL Telecom Italia con IP dinamico. Quindi, per il momento, ZB Block non verrà ulteriormente citato.

**Step 1:** Innanzi tutto, procediamo a scaricare l'ultima versione dello script dalla [pagina ufficiale di Blackhole su Perishable Press](https://perishablepress.com/blackhole-bad-bots/) e scompattiamo lo zip da qualche parte sul nostro computer

**Step 2:** Carichiamo quindi via FTP la directory */blackhole/* nella root del nostro sito

**Step 3:** Verifichiamo che il file */blackhole/* sia regolarmente scrivibile (impostare i permessi a 755)

**Step 4:** Inserire il seguente codice in cima ad ogni pagina del sito. Nel caso di WordPress, la soluzione migliore è l'inserimento in prima posizione all'interno del file *wp-load.php*, **ricordandosi però di andare a rieseguire la modifica ad ogni aggiornamento**:

```php
<?php include($_SERVER['DOCUMENT_ROOT'] . "/blackhole/blackhole.php"); ?>
```

Lo script *blackhole.php* controlla l'IP richiedente all'interno della blacklist contenuta nel file *blackhole.dat*. Se viene trovata una corrispondenza, la richiesta viene bloccata e viene mostrato un breve messaggio (personalizzabile).

**Step 5:** La trappola vera e propria! Aggiungere al *footer.php* del proprio template, questo codice:

```html
<a style="display: none;" href="http://example.com/blackhole/" rel="nofollow">Do NOT follow this link or you will be banned from the site!</a>
```

Questo è il link reso invisibile tramite CSS che i bad crawlers seguiranno diligentemente come tanti topolini seguono il Pifferaio Magico. Essendo reso invisibile, nessun visitatore lo vedrà mai e quindi non esiste il pericolo che possa venire cliccato inavvertitamente.

> Sostituite `http://example.com` con l'indirizzo del vostro sito

**Step 6:** Passo fondamentale, da eseguire assolutamente.
Apriamo il nostro **robots.txt** ed aggiungiamo:

```
User-agent: *
Disallow: /blackhole/*
```

Come detto, i bot "legali" interpretano correttamente il file **robots.txt** quindi, grazie a questa regola, saranno direttamente esclusi dalla directory contenente la trappola e non correranno quindi il rischio di venire bloccati per errore.

## Alcune personalizzazioni

Il file **index.php** richiede un minimo di configurazione. Aprire **/blackhole/index.php** ed eseguire le seguenti modifiche:

* **Riga #54:** Il percorso del nostro file robots.txt
* **Riga #56:** Il percorso della nostra pagina per i contatti
* **Righe #140/141:** L'indirizzo email del mittente e del destinatario della notifica che riceveremo per ogni nuovo bot blacklistato da Blackhole
* Nel file **blackhole/blackhole.php** modificare la **Riga #53** con le nostre informazioni di contatto esterne al sito

## Whitelisting dei bot

Lo script Blackhole si preoccupa, a scanso di errori, di eseguire il whitelisting dei principali bot di indicizzazione. In questa versione, la whitelist comprende:

* googlebot (Google)
* msnbot (MSN/Bing)
* yandex (Yandex)
* teoma (Ask)
* slurp (Yahoo)

E' possibile eventualmente inserirne altri, modificando manualmente la **riga #40** all'interno del file **blackhole.php**

> **Aggiornamento:** se installato su un CMS, come Joomla o WordPress, potreste ricevere un errore del tipo "Error opening file...". Per risolvere il problema, aprite il file **blackhole.php** e modificate la riga evidenziata, immettendo il percorso assoluto del file **blackhole.dat** all'interno del vostro server:

```php
$filename = "/var/www/example/web/blackhole/blackhole.dat"; // scan to prevent duplicates
$fp = fopen($filename, "r") or die("Error opening file...");
while ($line = fgets($fp)) {
    if (!preg_match("/(googlebot|slurp|msnbot|teoma|yandex)/i", $line)) {
        $u = explode(" ", $line);
        if ($u[0] == $_SERVER['REMOTE_ADDR']) ++$badbot;
    }
}
```

Via | [Perishable Press](https://perishablepress.com/blackhole-bad-bots/)
