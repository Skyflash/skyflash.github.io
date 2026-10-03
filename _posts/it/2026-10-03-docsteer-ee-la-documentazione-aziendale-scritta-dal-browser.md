---
title: "DocSteer-EE: la documentazione aziendale, scritta dal browser"
layout: post
date: '2026-10-03 09:00:00'
description: "DocSteer-EE è il successore applicativo del tema Jekyll DocSteer: documentazione, knowledge base e FAQ per i team, con editor nel browser, cronologia delle versioni, revisione e accesso con Active Directory o single sign-on. È in alpha, e il piano gratuito basta già per usarlo in azienda."
intro: "Un tema Jekyll va benissimo finché chi scrive la documentazione ha accesso al repository. In azienda quasi mai è così. DocSteer-EE nasce da lì."
image: "/static/assets/img/blog/docsteer-ee/cover.png"
lang: it_IT
featured: true
categories:
- Progetti Personali
keywords: docsteer, docsteer-ee, documentazione, knowledge base, faq, wiki aziendale, active directory, ldap, oidc, single sign-on, sveltekit, postgres, open core, claude code
tags:
- docsteer
- documentazione
- open-source
- claude-code
permalink: "/it/blog/progetti-personali/:title/"
redirect_from: "/blog/progetti-personali/docsteer-ee-la-documentazione-aziendale-scritta-dal-browser/"
translation_key: docsteer-ee-alpha
icon: fa-compass
---

Un mese fa ho scritto di [DocSteer]({{ '/it/blog/progetti-personali/docsteer-un-tema-jekyll-per-la-documentazione/' | relative_url }}), un tema Jekyll per documentazione tecnica e knowledge base. Funziona bene per quello che è: pagine in Markdown in un repository, una build, un sito statico.

In azienda, però, la documentazione la scrivono persone che un repository non lo apriranno mai: l'helpdesk che aggiorna una procedura, l'ufficio qualità che corregge un manuale, il collega che vuole solo sistemare un refuso senza imparare Git. Per loro serve un'applicazione. **DocSteer-EE** è quell'applicazione, ed è in alpha.

* TOC
{:toc}

## Perché un'applicazione e non un tema

Ci sono quattro cose che chi la usa in azienda dà per scontate, e Jekyll non può darle. Non perché sarebbero difficili da fare: semplicemente il modello non le prevede.

- **Scrivere dal browser.** Serve un server che salvi a runtime, e un sito statico un runtime non ce l'ha.
- **Entrare con un account.** Serve una sessione e una decisione a ogni richiesta, mentre una pagina statica è pubblica dal momento in cui esiste su disco.
- **Sapere chi ha cambiato cosa e quando.** Git lo sa, ma solo per chi ha accesso al repository.
- **Permessi per sezione.** Un file pubblicato lo legge chiunque raggiunga l'indirizzo.

Quindi il motore cambia: SvelteKit e TypeScript sul server, i contenuti in PostgreSQL, tutto in un container Docker. Il design system di DocSteer invece resta: le skin, il tema chiaro e scuro, la barra laterale, l'indice, la ricerca da tastiera. Chi conosce il tema riconosce subito l'applicazione.

<img class="post-image post-image--on-light" src="{{ '/static/assets/img/blog/docsteer-ee/home-light.png' | relative_url }}" alt="La pagina iniziale di DocSteer-EE: titolo, ricerca in tutti gli spazi e le schede degli spazi di documentazione, knowledge base e FAQ">
<img class="post-image post-image--on-dark" src="{{ '/static/assets/img/blog/docsteer-ee/home-dark.png' | relative_url }}" alt="La pagina iniziale di DocSteer-EE: titolo, ricerca in tutti gli spazi e le schede degli spazi di documentazione, knowledge base e FAQ">

## Cosa fa già

- **Spazi di tre tipi**: documentazione, knowledge base, FAQ. Convivono nella stessa installazione, ognuno con la sua visibilità: pubblico, riservato a chi ha un account, o ristretto a chi ha un ruolo su quello spazio.
- **Due editor sullo stesso testo.** Uno in Markdown, con anteprima affiancata, e uno visuale per chi il Markdown non lo vuole vedere. Il testo salvato resta sempre Markdown, e una pagina che il visuale non saprebbe rappresentare fedelmente resta in Markdown: l'editor lo dice, invece di convertirla in silenzio.
- **Cronologia completa.** Ogni pubblicazione è una versione, e nessuna viene mai cancellata o riscritta. Si confrontano due versioni qualsiasi e se ne ripristina una vecchia, che diventa una versione nuova.
- **Revisione, se la si vuole.** Un'opzione per spazio: le modifiche passano da un revisore diverso dall'autore, che approva o rimanda indietro con una nota.
- **Segnalazioni** al posto dei commenti: chi legge una procedura sbagliata lo segnala a chi se ne occupa, con il link alla versione che ha letto.
- **Allegati e una galleria** per ogni spazio, con l'indicazione di dove ogni file è usato.
- **Ricerca** su tutto il sito o dentro uno spazio, che mostra solo quello che chi cerca può leggere.
- **Il proprio marchio**: logo, favicon, colori, nome e testi si cambiano dal pannello, senza toccare un file di configurazione.
- **Lingue dell'interfaccia** in file PO: si scaricano, si traducono con Poedit e si ricaricano.

La documentazione del prodotto è scritta dentro il prodotto, come uno spazio fra gli altri:

<img class="post-image post-image--on-light" src="{{ '/static/assets/img/blog/docsteer-ee/versioni-light.png' | relative_url }}" alt="Una pagina della guida di DocSteer-EE, Cronologia e versioni: barra laterale, breadcrumb, autore e numero di versione sotto il titolo, indice della pagina a destra">
<img class="post-image post-image--on-dark" src="{{ '/static/assets/img/blog/docsteer-ee/versioni-dark.png' | relative_url }}" alt="Una pagina della guida di DocSteer-EE, Cronologia e versioni: barra laterale, breadcrumb, autore e numero di versione sotto il titolo, indice della pagina a destra">

## Entrare con l'account aziendale

Un'applicazione interna che chiede di creare l'ennesima password parte già in salita. Per questo DocSteer-EE si collega a quello che l'azienda usa già:

- **LDAP e Active Directory**, provati contro OpenLDAP e contro un vero controller di dominio Samba 4, che risponde con gli stessi codici d'errore di AD, risolve i gruppi annidati e rifiuta le password in chiaro come un dominio configurato con criterio.
- **Single sign-on con OpenID Connect**: Entra ID, Keycloak, Okta. L'autenticazione a più fattori la gestisce il provider.

Gli account locali restano, e vengono prima della directory: l'amministratore che configura LDAP non rischia di restare chiuso fuori.

Poi c'è la questione di *chi* può entrare. Non so voi, ma io con i filtri LDAP non ho mai fatto pace. Basta chiedere una cosa ragionevole come "solo le persone vere, solo gli account attivi, niente account di servizio" e ci si ritrova a contare parentesi alle undici di sera, a cercare per l'ennesima volta che cosa voglia dire `1.2.840.113556.1.4.803` (spoiler: è un AND bit a bit, ovviamente) e a scoprire il giorno dopo di aver lasciato fuori mezzo ufficio acquisti.

Per questo il filtro si costruisce spuntando delle caselle. Si scelgono le condizioni, si aggiunge se serve un gruppo, compresi i gruppi annidati, e il filtro si scrive da solo sotto gli occhi. "Conta le persone" dice quante ne trova prima di salvare. Chi preferisce le parentesi può sempre scriverlo a mano, e un filtro già esistente viene riletto e mostrato con le caselle che gli corrispondono. Semplifica la costruzione delle query e, con un po' di fortuna, anche il vostro sonno.

<img class="post-image" src="{{ '/static/assets/img/blog/docsteer-ee/filtro-ldap.png' | relative_url }}" alt="Il costruttore del filtro LDAP di DocSteer-EE: caselle per solo persone, solo account attivi, esclusione degli account con password che non scade e solo chi ha un indirizzo email, ricerca di un gruppo, e il filtro risultante scritto sotto, con il pulsante Conta le persone">

## Come ci sto lavorando

Come per il tema, con **Claude Code**, questa volta dentro VS Code e con Opus 5.5. Il metodo è lo stesso: prima le decisioni per iscritto, poi il codice. C'è un documento di architettura che raccoglie ogni scelta, con le alternative scartate e il motivo, e un file di stato aggiornato a fine sessione, che serve a riprendere il giorno dopo senza ricostruire tutto da capo.

Le parti delicate, come l'autenticazione, le versioni e i permessi, hanno i loro test, e quelle che parlano con un sistema esterno si provano contro un sistema vero in Docker, non contro una simulazione. Un'integrazione con Active Directory scritta senza un Active Directory davanti è codice che sembra funzionare.

## Cosa è gratis e cosa no

DocSteer-EE è **open core**: il nucleo è AGPL-3.0, e le funzionalità di amministrazione avanzata richiedono una licenza. Dove passa il confine è stata la decisione più ragionata di tutto il progetto, e la regola è una sola: **si limitano le funzionalità, mai i volumi.**

Nessun piano ha un tetto su spazi, documenti, articoli o FAQ. Un limite sul numero di pagine colpirebbe esattamente chi sta usando di più il prodotto, nel momento in cui ci si sta affidando.

Il pannello di amministrazione lo mostra così:

<img class="post-image" src="{{ '/static/assets/img/blog/docsteer-ee/funzionalita.png' | relative_url }}" alt="La pagina Funzionalità del pannello di amministrazione di DocSteer-EE: accesso con email e password, LDAP / Active Directory e single sign-on OIDC segnati come Sempre inclusa; sincronizzazione della directory e più directory insieme segnate come Funzionalità Premium">

**Sempre incluso, senza chiave:** scrittura e lettura senza limiti, editor, cronologia e confronto, revisione, ricerca, allegati, il proprio marchio, ruoli globali, spazi pubblici e riservati a chi ha un account, il registro delle attività, l'export dei propri contenuti. E soprattutto l'accesso con **LDAP / Active Directory** e con **single sign-on OIDC**: entrare con l'identità che l'azienda ha già non è un'integrazione da vendere, è il modo normale di entrare.

**Con una licenza:** la sincronizzazione periodica della directory (chi lascia l'azienda viene disattivato da solo), più directory insieme, la mappatura dei gruppi AD sui ruoli, gli spazi ristretti con permessi per singolo spazio, l'export del registro per la conformità, la reportistica, l'importazione da Confluence e da DOCX, e la rimozione del credito "Built with DocSteer" in fondo alla pagina.

In pratica: **un'azienda può installare la versione gratuita e usarla in produzione**, con i suoi utenti che entrano con le credenziali di dominio, senza limiti e senza scadenze. La licenza serve quando le persone diventano troppe per seguirle a mano, cioè quando c'è un'organizzazione da amministrare. E una licenza scaduta non può togliere nulla di quello che è gratuito.

## A che punto è

È un'**alpha** e non è ancora pubblica: il repository è privato finché non è pronta una prima versione installabile. Le basi ci sono tutte: permessi, flusso editoriale, sincronizzazione della directory e mappatura dei gruppi sui ruoli. Mancano ancora alcune delle funzionalità di amministrazione, come l'importazione da altri sistemi e la reportistica.

Nel frattempo il progetto da cui tutto è partito resta lì, MIT e su **[GitHub](https://github.com/Skyflash/docsteer)**.

Prima di aprirla mi interessa soprattutto capire cosa manca a chi la documentazione aziendale la gestisce tutti i giorni. Voi cosa usate oggi? E cos'è che, alla fine, vi fa abbandonare una wiki interna?
