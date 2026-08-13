---
layout: post
title: "Come proteggere un sito dagli attacchi - Parte 2 - Il file .htaccess"
date: '2012-05-08 16:05:48'
description: "Proteggere un sito web tramite il file .htaccess, con una serie di direttive in grado di intercettare e bloccare gli attacchi dei bot - 5G Blacklist 2012"
intro: "La tecnica della trappola vista nella parte 1 è molto efficiente, ma potrebbe non bastare a garantire una protezione di alto livello contro i bot che vanno alla ricerca di exploit e falle di sicurezza."
categories:
- Infrastruttura & Sistemi
keywords: sicurezza, htaccess, bad crawler, bot
tags:
- sicurezza
- htaccess
- bad crawler
- bot
- php
permalink: "/blog/infrastruttura/:title/"
redirect_from: "/2012/05/protezione-di-un-sito-parte-2-htaccess/"
icon: fa-shield
---
Ieri abbiamo illustrato un ottimo e "furbo" metodo per [ingabbiare i bad crawlers](/blog/infrastruttura/come-proteggere-il-proprio-sito-dagli-attacchi-dei-bad-crawlers-parte-1/). La tecnica della "trappola" illustrata è molto efficiente, ma potrebbe non bastare a garantire una protezione di alto livello. Esistono infatti anche bot maligni il cui scopo principale non è quello di effettuare il download indiscriminato di un intero sito web, ma che vanno alla ricerca di exploit, di falle di sicurezza e che magari tentano di eseguire script e simili.

In questi casi, diventa di fondamentale importanza dotarsi di un file *.htaccess* customizzato quel tanto che serve a bloccare la stragrande maggioranza degli attacchi. Negli ultimi giorni ho provato diverse modifiche al mio *.htaccess* e ritengo di aver trovato, grazie all'ottimo blog [Perishable Press](https://perishablepress.com), quella che ritengo una delle migliori soluzioni possibili.

Inoltre, particolare non di poco conto per quanto mi riguarda, l'autore della blacklist ha un blog basato su WordPress e ne testa personalmente il funzionamento proprio su quella piattaforma, garantendone in pratica il funzionamento.

* TOC
{:toc}

## .htaccess 5G Blacklist 2012

L'autore è giunto al quinto rilascio della sua blacklist, che prende quindi il nome attuale di "5G". E' già in fase avanzata di sviluppo la futura versione **6G**, che comprenderà ulteriori modifiche derivate dai suggerimenti degli utenti e dalla propria esperienza

## Cosa fa la Blacklist

La 5G è un set semplice e flessibile di direttive *.htaccess* che verificano tutte le richieste verso il web server e si occupano delle eventuali contromisure immediate, senza appesantire il carico del web server stesso, permettendoci quindi di risparmiare una grande quantità di banda e di risorse.

## Come si usa

Installare la blacklist è relativamente semplice. Sarà sufficiente aggiungere il codice necessario in fondo al proprio file *.htaccess*

> **Attenzione:** la modifica di .htaccess, se fatta da persone non esperte e non particolarmente attente, può generare molti problemi al vostro sito WordPress, fino a **renderlo inaccessibile**. Assicuratevi quindi di fare **sempre una copia di sicurezza** di .htaccess prima di cominciare le modifiche

Aprite il vostro file *.htaccess* ed in coda (se usate WordPress, dovrebbero esserci solo le direttive di default) e **dopo `### END WordPress ###`** aggiungete il seguente codice:

```apache
# 5G BLACKLIST/FIREWALL
# @ http://perishablepress.com/5g-blacklist/

# 5G:[QUERY STRINGS]

RewriteEngine On
RewriteBase /
RewriteCond %{QUERY_STRING} (environ|localhost|mosconfig|scanner) [NC,OR]
RewriteCond %{QUERY_STRING} (menu|mod|path|tag)\=\.?/? [NC,OR]
RewriteCond %{QUERY_STRING} boot\.ini [NC,OR]
RewriteCond %{QUERY_STRING} echo.*kae [NC,OR]
RewriteCond %{QUERY_STRING} etc/passwd [NC,OR]
RewriteCond %{QUERY_STRING} \=\\%27$ [NC,OR]
RewriteCond %{QUERY_STRING} \=\\\'$ [NC,OR]
RewriteCond %{QUERY_STRING} \.\./ [NC,OR]
RewriteCond %{QUERY_STRING} \? [NC,OR]
RewriteCond %{QUERY_STRING} \: [NC,OR]
RewriteCond %{QUERY_STRING} \[ [NC,OR]
RewriteCond %{QUERY_STRING} \] [NC]
RewriteRule .* - [F]

# 5G:[USER AGENTS]

SetEnvIfNoCase User-Agent ^$ keep_out
SetEnvIfNoCase User-Agent (casper|cmsworldmap|diavol|dotbot) keep_out
SetEnvIfNoCase User-Agent (flicky|ia_archiver|jakarta|kmccrew) keep_out
SetEnvIfNoCase User-Agent (libwww|planetwork|pycurl|skygrid) keep_out
SetEnvIfNoCase User-Agent (purebot|comodo|feedfinder|turnit) keep_out
SetEnvIfNoCase User-Agent (zmeu|nutch|vikspider|binlar|sucker) keep_out

Order Allow,Deny
Allow from all
Deny from env=keep_out

# 5G:[REQUEST STRINGS]

RedirectMatch 403 (https?|ftp|php)\://
RedirectMatch 403 /(cgi|https?|ima|ucp)/
RedirectMatch 403 /(Permanent|Better)$
RedirectMatch 403 (\=\\\'|\=\\%27|/\\\'/?|\)\.css\()$
RedirectMatch 403 (\,|//|\)\+|/\,/|\{0\}|\(/\(|\.\.\.|\+\+\+|\||\\\"\\\")
RedirectMatch 403 \.(cgi|asp|aspx|cfg|dll|exe|jsp|mdb|sql|ini|rar)$
RedirectMatch 403 /(contac|fpw|install|pingserver|register)\.php$
RedirectMatch 403 (base64|crossdomain|localhost|wwwroot|e107\_)
RedirectMatch 403 (eval\(|\_vti\_|\(null\)|echo.*kae|config\.xml)
RedirectMatch 403 \.well\-known/host\-meta
RedirectMatch 403 /function\.array\-rand
RedirectMatch 403 \)\;\$\(this\)\.html\(
RedirectMatch 403 proc/self/environ
RedirectMatch 403 msnbot\.htm\)\.\_
RedirectMatch 403 /ref\.outcontrol
RedirectMatch 403 com\_cropimage
RedirectMatch 403 indonesia\.htm
RedirectMatch 403 \{\$itemURL\}
RedirectMatch 403 function\(\)
RedirectMatch 403 labels\.rdf
RedirectMatch 403 /playing.php
RedirectMatch 403 muieblackcat

# 5G:[BAD IPS]

Order Allow,Deny
Allow from all
# uncomment/edit/repeat next line to block IPs
# Deny from 123.456.789
```

## Alcune note

Se sul vostro sito ospitate dei download, fate molta attenzione a questa riga:

```apache
RedirectMatch 403 \.(cgi|asp|aspx|cfg|dll|exe|jsp|mdb|sql|ini|rar)$
```

che contiene un filtro contro, fra gli altri, i files .rar

In caso quindi alcuni dei vostri downloads siano compressi con questo formato, rimuovete semplicemente l'eccezione "rar" dalla regola:

```apache
RedirectMatch 403 \.(cgi|asp|aspx|cfg|dll|exe|jsp|mdb|sql|ini)$
```

Via | [5G Blacklist 2012](https://perishablepress.com/5g-blacklist-2012/)
