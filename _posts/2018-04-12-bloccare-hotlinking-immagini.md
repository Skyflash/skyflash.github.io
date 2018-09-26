---
layout: post
title:  "Come bloccare l'hotlinking delle immagini con .htaccess"
date:   2018-04-13
lang: it_IT
description: "L'hotlinking consiste nel mostrare una o più risorse (tipicamente immagini) all’interno di una pagina web, ad insaputa del proprietario del sito originale. Vediamo come impedirla, usando .htaccess e Apache"
intro: "
Quando si parla di hotlinking  ci si riferisce ad una pratica – molto abusata – che permette di mostrare una risorsa (tipicamente un’immagine) all’interno di una pagina web senza che questa sia presente all’interno del proprio spazio, sfruttando quindi la banda e le risorse del server esterno che la ospita"
image: /static/assets/img/blog/hotlinking-htaccess/NoHotlinking.jpg
keywords: "htaccess,apache,wordpress"
categories: [Wordpress,Apache]
permalink: /blog/wordpress/:title/
tags: [htaccess,apache,wordpress]
icon: fa-wordpress
---

* TOC 
{:toc}

# L’HOTLINKING DANNEGGIA IL TUO SITO

Facciamo un esempio. L’immagine che vedete qui sotto è stata caricata direttamente su un mio sito (ospite originale di questo articolo). Il server web non fa altro che andare a caricare una risorsa interna (l’immagine stessa) e mostrarla al visitatore, senza alcun carico elaborativo extra.

![Kenny]({{ site.img_path }}/hotlinking-htaccess/kenny-mccormick.jpg)

Il codice dell’immagine è il seguente:

```html
<img src="/wp-content/uploads/2012/05/kenny-mccormick.jpg" alt="" border="0" width="320" height="240" />
```

Un sito esterno, invece di effettuare il download dell’immagine e di caricarla sul proprio server (cosa che, oltretutto, è sempre consigliabile in quanto migliora moltissimo i tempi di caricamento e le prestazioni generali del sito), ottiene il collegamento diretto alla risorsa e lo include all’interno di una propria pagina.

```html
<img src="https://www.skyflash.it/wp-content/uploads/2012/05/kenny-mccormick.jpg" alt="" border="0" width="320" height="240" />
```

Il risultato sarà che il secondo sito, eterno al nostro, sfrutta l’immagine senza però sacrificare il proprio spazio web, mentre il nostro sito, su cui risiede l’immagine, sarà sottoposto ad un carico eccessivo (ed assolutamente non richiesto nè tanto meno gradito) sia per quanto riguarda la propria banda passante che per le risorse del server.

# COME PROTEGGERSI DA HOTLINKING

Sono sufficienti alcune righe da aggiungere al proprio, immancabile, file *.htaccess* e, se volete, un’immagine preparata per lo scopo, che servirà per sbattere in faccia al webmaster antipatico la dura verità :smile:

**ATTENZIONE:** la modifica di .htaccess, se fatta da persone non esperte e non particolarmente attente, può generare molti problemi al vostro sito WordPress, fino a **renderlo inaccessibile**. Assicuratevi quindi di fare **SEMPRE una copia di sicurezza** di .htaccess prima di cominciare le modifiche

Aprite in un qualsaisi editor di testo il vostro file *.htaccess* ed in coda (se usate WordPress, dovrebbero esserci solo le direttive di default) e **dopo ### END WordPress ###** aggiungete il seguente codice:

```apache
### Blocca l'hotlinking - Webmaster cattivo pussa via
RewriteEngineon
RewriteCond%{HTTP_REFERER}!^$
RewriteCond%{HTTP_REFERER}!^http(s)?://(www\.)?skyflash.it[NC]
RewriteCond%{HTTP_REFERER}!^http(s)?://(www\.)?google.com[NC]
RewriteCond%{HTTP_USER_AGENT}!googlebot[NC]
RewriteCond%{REQUEST_URI}!^hotlink.jpg$
RewriteRule\.(jpg|jpeg|png|gif|js|swf)$hotlink.jpg[NC,R,L]
```

## SPIEGAZIONE

Alla **terza riga** trovate:

```apache
RewriteCond%{HTTP_REFERER}!^$
```

Questa istruzione consente ai referrer che non forniscono informazioni di accedere al contenuto. Ciò è reso necessario in quanto molti visitatori (soprattutto quelli che si connettono dall’ufficio e si trovano dietro a proxy) sono protetti da un firewall che non rilascia informazioni al server per ragioni di sicurezza.

**Righe 4, 5 e 6:**

```apache
RewriteCond%{HTTP_REFERER}!^http(s)?://(www\.)?skyflash.it[NC]
RewriteCond%{HTTP_REFERER}!^http(s)?://(www\.)?google.com[NC]
RewriteCond%{HTTP_USER_AGENT}!googlebot[NC]
```

specificano i domini che invece possono effettuare l’hotlinking e quindi visualizzare le immagini presenti sul server. Quindi scriveremo il nostro dominio internet e, in caso vogliate farvi indicizzare le immagini, Google. Tutti gli altri sono fuori.

**Riga 7:**

```apache
RewriteCond%{REQUEST_URI}!^hotlink.jpg$
```

Se proprio qualcuno vuole rubare qualche immagine, allora lasciamogli prendere quella che abbiamo preparato per segnalare gli hotlinker. Questa riga ci assicura che l’immagine sia sempre visualizzabile.

**Riga 8:**
```apache
RewriteRule\.(jpg|jpeg|png|gif|js|swf)$hotlink.jpg[NC,R,L]
```

Specifica il formato dei file protetti dall’hotlinking (non solo le immagini ne sono soggette) e sostituisce le richieste con un’immagine statica.

Ovviamente potrete specificare l’immagine che desiderate, ma assicuratevi che questa non sia protetta (vedi riga precedente) oppure, ancora meglio, caricatela su una risorsa esterna come [Dropbox](http://db.tt/wgafhzXi), o il risultato sarà un loop infinito!

### CONCEDERE L’ACCESSO A BING, YAHOO E FACEBOOK

Esattamente come abbiamo fatto per Google, aggiungiamo al nostro *.htaccess* le seguenti direttive:

```apache
RewriteCond%{HTTP_REFERER}!msn.[NC]
RewriteCond%{HTTP_REFERER}!yahoo.[NC]
RewriteCond%{HTTP_REFERER}!^https?://(www\.)?facebook\.com[NC]
RewriteCond%{HTTP_USER_AGENT}!facebookplatform[NC]
RewriteCond%{HTTP_USER_AGENT}!msnbot[NC]
RewriteCond${HTTP_USER_AGENT}!slurp[NC]
```

## CONCLUSIONI

Il risultato finale sarà quindi il seguente:

```apache
### Blocca l'hotlinking - Webmaster cattivo pussa via

RewriteEngineon
RewriteCond%{HTTP_REFERER}!^$
RewriteCond%{HTTP_REFERER}!^http(s)?://(www\.)?skyflash.it[NC]
RewriteCond%{HTTP_REFERER}!^http(s)?://(www\.)?google.com[NC]
RewriteCond%{HTTP_REFERER}!msn.[NC]
RewriteCond%{HTTP_REFERER}!yahoo.[NC]
RewriteCond%{HTTP_REFERER}!^https?://(www\.)?facebook\.com[NC]
RewriteCond%{HTTP_USER_AGENT}!googlebot[NC]
RewriteCond%{HTTP_USER_AGENT}!facebookplatform[NC]
RewriteCond%{HTTP_USER_AGENT}!msnbot[NC]
RewriteCond${HTTP_USER_AGENT}!slurp[NC]
RewriteCond%{REQUEST_URI}!^hotlink.jpg$
RewriteRule\.(jpg|jpeg|png|gif|js|swf)$hotlink.jpg[NC,R,L]
```

Chi dovesse linkare ad una risorsa con estensione jpg, jpeg, png, gif, js o swf sul sito così "trattato", come unico risultato avrà la visualizzazione della seguente immagine

![Hotlink-Monkey]({{ site.img_path }}/hotlinking-htaccess/hotlink.jpg)

Se guardando le statistiche del vostro spazio web avete notato un consumo eccessivo di banda in uscita o se state rilevando una grande quantità di accessi esterni alle stesse immagini, probabilmente siete hotlinkati da qualcuno. Ora sapete come difendervi.

Risorse esterne:

- [Stop bandwith thief using rewrite rules on .htaccess file](http://www.istanto.net/stop-bandwith-thief-using-rewrite-rules-on-htaccess-file.html)
- [Prevent hotlinking of images – how to hotlink protect](http://www.htaccesstools.com/hotlink-protection/)
- [Smarter Way To Prevent Image Hotlinking With .Htaccess](http://www.hongkiat.com/blog/smarter-way-to-prevent-image-hotlinking-with-htaccess/)
- [Impedire l’hotlinking delle immagini con il file .htaccess](http://gabrieleromanato.com/2012/03/impedire-hotlinking-immagini-htaccess/)
- [Proteggiamoci dall’hotlinking con un semplice file](http://vincenzodibiaggio.it/2008/07/11/proteggiamoci-dallhotlinking-con-un-semplice-file-htaccess/)
- [Stop image hotlinking with .htaccess](http://www.thewebsqueeze.com/web-design-tutorials/stop-image-hotlinking-with-htaccess.html)
- [Il post originale](https://www.skyflash.it/internet-reti/sicurezza/come-bloccare-lhotlinking-delle-immagini-tramite-htaccess/6552/)