---
title: "Il nuovo sito, parte 5: breadcrumb, metainfo riordinate e un post in vetrina"
layout: post
date: '2026-08-14 22:00:00'
description: Un breadcrumb con dati strutturati per Google, la riga data/lettura riposizionata e un post in evidenza in cima al blog — con una lezione su come non ritagliare una cover.
intro: "Le prime quattro parti raccontavano la ricostruzione, i bug, le copertine, le rifiniture. Questa è la prima puntata del \"dopo\": tre modifiche pensate per rendere il sito più facile da navigare e più leggibile per chi legge — e, di riflesso, anche per chi indicizza."
image: "/static/assets/img/blog/nuovo-sito-2026/parte5-cover.png"
image_dark: "/static/assets/img/blog/nuovo-sito-2026/parte5-cover-dark.png"
lang: it_IT
categories:
- Progetti Personali
keywords: seo, breadcrumb, json-ld, ux, navigazione, jekyll, claude code
tags:
- css
- claude-code
- ia
- ux
- seo
permalink: "/it/blog/progetti-personali/:title/"
redirect_from: "/blog/progetti-personali/il-nuovo-sito-parte-5-breadcrumb-metainfo-e-un-post-in-vetrina/"
icon: fa-compass
---

Le prime quattro parti di questa serie ([1]({{ '/it/blog/progetti-personali/il-nuovo-sito-parte-1-perche-ripartire-da-zero/' | relative_url }}), [2]({{ '/it/blog/progetti-personali/il-nuovo-sito-parte-2-i-bug-nascosti-in-un-sito-nuovo/' | relative_url }}), [3]({{ '/it/blog/progetti-personali/il-nuovo-sito-parte-3-le-copertine-che-si-adattano-al-tema/' | relative_url }}), [4]({{ '/it/blog/progetti-personali/il-nuovo-sito-parte-4-le-ultime-finiture/' | relative_url }})) coprivano la ricostruzione, i bug, le copertine, le rifiniture prima del lancio. Il sito è online da un po', ora — ed è arrivato il momento di lavorare su cose che si notano solo se funzionano bene: come ci si orienta dentro un articolo, cosa si legge per primo, e come si scopre un contenuto che altrimenti sarebbe sepolto in mezzo a tutti gli altri.

* TOC
{:toc}

## Un breadcrumb, per chi legge e per chi indicizza

L'idea di partenza era semplice: aggiungere un breadcrumb (Home / Blog / Categoria / Titolo) sopra ogni articolo, per dare un punto di riferimento durante la lettura. Ma il breadcrumb visibile è solo metà del valore — l'altra metà è dati strutturati che Google usa per sostituire l'URL nudo con un percorso leggibile nei risultati di ricerca, a patto di marcarli con lo schema `BreadcrumbList` in JSON-LD.

`jekyll-seo-tag`, il plugin che già genera buona parte dei meta tag del sito, non lo fa in autonomia — verificato leggendo l'HTML compilato: produce solo `BlogPosting`, `WebSite` e `Person`. Serviva un secondo blocco `application/ld+json` indipendente (pratica comune: più blocchi JSON-LD sulla stessa pagina sono validi), generato dagli **stessi identici dati** del breadcrumb visibile, per non rischiare che i due finiscano per raccontare percorsi diversi.

Liquid, però, non ha letterali per gli hash — non puoi scrivere al volo un array di coppie `{etichetta, url}`. La soluzione più pulita è stata usare due array paralleli, costruiti con `push` (lo stesso filtro già usato altrove nel sito per i post correlati):

{% raw %}```liquid
{% assign crumb_labels = "" | split: "" %}
{% assign crumb_urls = "" | split: "" %}
{% assign crumb_labels = crumb_labels | push: i18n.nav_home[short_lang] %}
{% assign crumb_urls = crumb_urls | push: home_url %}
{% assign crumb_labels = crumb_labels | push: i18n.nav_blog[short_lang] %}
{% assign crumb_urls = crumb_urls | push: blog_url %}
{% include breadcrumb.html labels=crumb_labels urls=crumb_urls %}
```{% endraw %}

e dentro l'include, un solo ciclo genera sia gli `<a>` che gli `<li>` del JSON-LD, scorrendo gli stessi due array:

{% raw %}```liquid
{
  "@type": "ListItem",
  "position": {{ forloop.index }},
  "name": {{ label | jsonify }}
  {% unless forloop.last %},"item": {{ url | absolute_url | jsonify }}{% endunless %}
}
```{% endraw %}

Il primo tentativo aveva però un difetto invisibile finché non lo si guarda affiancato al resto della pagina: il breadcrumb, inserito appena sopra `<header class="post-header">`, restava ancorato al bordo dell'intero container da 1360px — mentre il titolo sotto vive dentro `.post-header`, che ha un suo `max-width: 760px` centrato, la colonna di lettura usata in tutto il sito. Risultato: su schermi larghi il breadcrumb partiva più a sinistra del titolo che gli stava proprio sotto, uno sfasamento che si nota a colpo d'occhio ma che in isolamento — guardando solo il breadcrumb, o solo il titolo — è del tutto invisibile. Bastava spostare l'include dentro l'header per farlo ereditare la stessa colonna.

## La riga con data e tempo di lettura, spostata due volte

Volevo che la riga con data, numero di parole e tempo di lettura stesse fra il titolo e il contenuto, non sopra al titolo com'era prima. Mi sono ispirato al layout di un altro blog Jekyll — titolo, poi immagine di copertina, poi metainfo, poi contenuto — e ho spostato tutto lì.

Sbagliato: quel layout metteva le metainfo *dopo* l'immagine, io le volevo *subito sotto* il titolo. Un malinteso mio nell'interpretare il riferimento, corretto non appena fatto notare — la differenza è di poche righe di Liquid, ma cambia parecchio la gerarchia visiva della pagina.

Sistemata la posizione, è rimasto un problema di affollamento: sotto al titolo si accalcavano tre elementi tutti "di servizio" — il breadcrumb appena sopra, la pill della categoria, la riga della meta-info — e la pill era ridondante: la stessa categoria è già visibile nel breadcrumb, una riga più in alto. L'ho spostata sotto la riga meta invece che sopra, e ho stretto lo spazio fra breadcrumb e titolo (24px → 8px, che da solo bastava a far sembrare tutto più affollato di quanto fosse davvero).

## Un post in vetrina, e la lezione sulle immagini con testo dentro

L'ultima modifica: un post per lingua, marcato `featured: true` nel front matter, compare come card grande in cima all'indice del blog — escluso dalla griglia normale sotto, per non mostrarlo due volte. Anche qui, ispirazione presa da come altri blog Jekyll gestiscono l'articolo in evidenza.

{% raw %}```liquid
{% assign featured_post = lang_posts | where: "featured", true | first %}
{% assign grid_posts = "" | split: "" %}
{% for post in lang_posts %}
  {% unless featured_post and post.url == featured_post.url %}
    {% assign grid_posts = grid_posts | push: post %}
  {% endunless %}
{% endfor %}
```{% endraw %}

La parte interessante è stata l'immagine di copertina. Primo tentativo: `object-fit: cover` con un rapporto fisso 16:9, per dare alla card un'altezza prevedibile. Sembrava ragionevole finché non ho provato con la copertina del post su WireGuard: il ritaglio tagliava via la parte alta dell'immagine, portandosi via il titolo "WireGuard" disegnato dentro la grafica stessa. Ho stretto l'altezza pensando bastasse un `object-position: top` — e ho provato con un'altra copertina, un banner panoramico (rapporto 4:1) per l'articolo sulla Flotta Stellare. Risultato anche peggiore: il testo "Alto Comando Flotta Stellare" tagliato ai lati, illeggibile.

Il problema non era la posizione del ritaglio, era il ritaglio in sé. Le copertine di questo blog sono quasi sempre grafiche con testo integrato — non fotografie — a proporzioni imprevedibili e con il testo in posizioni diverse ogni volta. Nessun `object-position` fisso avrebbe funzionato per tutte. La soluzione è stata smettere di ritagliare: l'immagine mantiene le sue proporzioni naturali, esattamente come già succede per le copertine dentro ai singoli articoli. Card più alte o più basse a seconda del post, ma mai un titolo tagliato a metà.

Un'ultima rifinitura, via feedback diretto: la badge "In evidenza" era troppo timida — sfondo tenue, poco riconoscibile — sostituita con uno sfondo pieno, colore d'accento, e un'iconcina a stella.

## Perché questa parte conta

Con una manciata di articoli, breadcrumb e post in evidenza sono quasi decorazione. Non lo sono più a lungo andare: più il blog cresce, più contano i punti di riferimento — sapere dove si è, tornare indietro di un livello senza usare il tasto back del browser, scoprire un articolo importante senza doverlo cercare fra dieci schede uguali nella griglia. Sono le stesse rifiniture "poco glamour" della [parte 4]({{ '/it/blog/progetti-personali/il-nuovo-sito-parte-4-le-ultime-finiture/' | relative_url }}), applicate un livello più in alto: non più "il sito funziona", ma "il sito si lascia usare bene".
