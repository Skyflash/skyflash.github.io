---
layout: post
title:  "Blocco delle applicazioni con K1000"
date:   2018-07-11
description: "Come utilizzare KACE 1000 per il controllo ed il blocco dei software non autorizzati sui PC - Una breve guida."
intro: "In seguito alla creazione della lista di blocco quando l’utente tenterà di aprire un software non autorizzato riceverà invece un avviso nell’angolo basso a destra dello schermo. "
lang: it_IT
image: /static/assets/img/blog/kace/smartcard/kace.jpg
keywords: "kace,k1000,script,vbs,visualbasic,smartcard,security,encryption"
categories: [Kace]
tags: [kace,script,vbs,smartcard,security,encryption]
icon: fa-unlock
---

In questa veloce guida si dà per scontato che il lettore abbia già una buona conoscenza dell'ambiente KACE 1000 (KACE SMA) e del funzionamento delle etichette (_Labels_)

* TOC 
{:toc}

# Il blocco delle applicazioni tramite K1000, passo per passo

Il blocco delle applicazioni su Kace funziona con una doppia logica:

1. Una [_Label_](#la-label), in grado di controllare e bloccare i software

2. Uno o più Software marcati come [_Not Allowed_](#i-software-da-bloccare)

Per funzionare, è necessario che **entrambe** le condizioni siano **vere**

## La Label

Kace mette a disposizione una Label già preconfezionata, secondo i parametri di default.

Useremo quindi questa per illustrare il funzionamento del blocco applicativo.

![Screenshot 1 - Default Application Control Label]({{ site.img_path }}/kace/appcontrol/K1000_appcontrol.png)

1. Portarsi in _Home_ ed in seguito in _Label Management_ e selezionare **Labels**

2. La nostra etichetta di default si chiama **“ApplicationControlDevices”** ed è così impostata:  

![Screenshot 2 - Appcontrol Label Details]({{ site.img_path }}/kace/appcontrol/appcontrol_label.png)

### Significato della Label

Illustriamo velocemente il significato dei vari flag:

* Device Inventory: La Label si applica all'Inventario dei devices (quindi: ai PC)
    * Allow Application Control:    La Label è in grado di controllare l'avvio delle applicazioni
* Resources (Processes, Services, Startup Items):   La Label si può applicare anche a processi e servizi
* Catalog:  La Label si applica al Catalogo Software (**essenziale** per il buon funzionamento del meccanismo di blocco!)
* Software: Come sopra, ma per i software non normalizzati dal catalogo

## I software da bloccare

Portiamoci nel **Software Catalog** (*Inventory* -> *Software Catalog*), che racchiude e “normalizza” tutti i software rilevati e riconosciuti, all’interno di un unico nome. Più chiaramente, avremo ad esempio “iTunes 12.x”, che contiene tutte le revisioni di iTunes 12 (es: 12.1, 12.4, 12.74 e via dicendo).

_Lavorare nel Catalogo Software ci consente di bloccare o monitorare un software indipendentemente dagli aggiornamenti che riceve._

![Screenshot 3]({{ site.img_path }}/kace/appcontrol/appcontrol_software_catalog.png)

Una volta trovato il nostro software (prendiamo sempre ad esempio iTunes 12.x), selezioniamo il checkbox e da menu “Choose Action” scegliamo “**Mark Not Allowed**”  
  
In alternativa, è possibile spuntare “**Not Allowed**” all’interno della pagina del software di nostro interesse. L’autosave è automatico nel momento del cambio di selezione del checkbox.  
  
![Screenshot 4]({{ site.img_path }}/kace/appcontrol/software_catalog_detail.png)

## I PC e la loro Label

Ora che abbiamo capito come funzionano sia la Label (che si applica ai PC) che il marker di blocco (relativo ai software), possiamo metterli insieme ed ottenere l’effetto desiderato.

**NOTA BENE:** *il meccanismo di Kace bloccherà l’apertura dei programmi SOLO sui PC a cui abbiamo applicato la Label “ApplicationControlDevice” e solo a loro*. In questa fase sperimentale l’etichetta NON VIENE applicata di default a tutti i device in inventario e l’operazione dovrà quindi essere fatta manualmente.

**Un pc che ha un software bloccato ma che non appartiene alla Label continuerà ad eseguire quel software come se nulla fosse, senza alcun problema.**

* 1 Otteniamo il nome od i nomi dei PC che ci interessa inserire nella Label. Per fare ciò abbiamo diverse strade, tutte corrette:  
    1. Lo conosciamo e lo troviamo direttamente in Inventario
    2. Dal Catalogo Software clicchiamo sul numero nella colonna “Installed”, che ci porterà alla lista di tutti i PC con quel software  

![Screenshot 5]({{ site.img_path }}/kace/appcontrol/appcontrol_locked.png)

* 2 Selezioniamo il checkbox a fianco del o dei PC di nostro interesse e da menu “**Choose Action**” facciamo click su “**Apply Labels**”  

![Screenshot 6]({{ site.img_path }}/kace/appcontrol/apply_label.png)

* 3 Scegliamo quindi la Label “**ApplicationControlDevices**” e trasciniamola nella parte destra della finestra, cliccando poi su “**Apply Labels**”

![Screenshot 7]({{ site.img_path }}/kace/appcontrol/labels_list.png)

## L’Inventario

Abbiamo fatto le regole. Abbiamo applicato le Labels. Manca ancora qualcosa?

Uno dei punti di forza dell’agente Kace è quello di lavorare sostanzialmente offline: si collega una volta al server, riceve tutte le regole, le informazioni e gli script e poi continua a lavorare, da solo, senza più bisogno di dialogare col server. E continua a fare tutto ciò che gli è stato detto di fare fino a prova contraria. Questo meccanismo si chiama “Inventario” e nel nostro caso viene eseguito una volta ogni 8 ore (almeno) da ogni singolo computer inventariato.

*Le nuove regole di blocco, quindi, verranno applicate al PC al suo prossimo contatto (cioè al prossimo inventario)*. Le potremo forzare manualmente (click sul box del device e poi “**Force Inventory**”) ma, in condizioni normali, il frutto delle nostre regole si vedrà solo dopo alcune ore (ed un riavvio del PC) e non in tempo reale.

# Il risultato finale

![Screenshot 8]({{ site.img_path }}/kace/appcontrol/final_result.png)

In seguito alla creazione della lista di blocco (alcuni software in questa immagine sono solo puramente a scopo di esempio e non si intende veramente bloccarli), all’assegnazione della Label al PC ed al propagarsi delle regole tramite inventario, una volta che l’utente tenterà di aprire il software riceverà un alert nell’angolo basso a destra dello schermo, come questo:

![Screenshot 9]({{ site.img_path }}/kace/appcontrol/messagebox.png)
