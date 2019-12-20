---
title: Distribuire un aggiornamento di build di Windows 10 via Kace
layout: post
date: '2019-12-16 11:30:00'
description: Usiamo Kace per aggiornare un PC da Windows 7/8/10 all'ultima build di Windows 10
lang: it_IT
image: "/static/assets/img/blog/kace/smartcard/kace.jpg"
categories:
- Kace
keywords: kace,k1000,script,batch,windows,windows10,upgrade,kscript
tags:
- kace
- k1000
- script
- batch
- kscript
- windows
- windows 10
- upgrade
- aggiornamento
icon: fa-floppy-o
intro: Gli aggiornamenti di build di Windows 10, come "Fall Creators Update" o "April 2018 Update", non sono disponibili nel feed delle patch di KACE. In alternativa, questi aggiornamenti possono comunque essere distribuiti utilizzando una Managed Install. 
---

Gli aggiornamenti di build di Windows 10 non sono *patch* tradizionali, *rollup* o *service pack*. Dal punto di vista della distribuzione, sono progettati e si comportano come un aggiornamento del sistema operativo *"in-place"*, cioè senza toccare alcun dato od impostazione preesistente, rimuovere la versione di SO precedente e senza salvare nessun dato. Pertanto richiedono maggiore pianificazione e test rispetto alle patch tradizionali, oltre a maggiori risorse (capacità del disco per server e client, larghezza di banda, tempo di installazione, ecc.).

<small><b>NOTA: questa guida utilizza la versione 1903 di Ottobre 2019 come esempio di build nei passaggi seguenti</b></small>

* TOC
{:toc}

## Prima fase: Creare il pacchetto di installazione

Gli aggiornamenti di build devono essere ottenuti direttamente da Microsoft. Sono distribuiti in formato ISO e devono essere estratti e ripacchettizzati per la distribuzione tramite prodotti di terze parti come KACE Systems Management Appliance.

### Otteniamo una ISO ufficiale di Windows 10

Per ottenere la ISO di Windows 10 useremo **uno quasiasi** di questi **tre metodi**:

1. Scaricare la ISO dalla propria **MSDN Library** (richiede una licenza MSDN attiva), assicurandosi di ottenere la versione appropriata per il proprio scopo (es: Home, Professional, eccetera)
2. Usare il **Media Creation Tool** di Microsoft, scaricandolo da questo indirizzo: [https://www.microsoft.com/en-us/software-download/windows10](https://www.microsoft.com/en-us/software-download/windows10)
     1. Una volta scaricato, esegui il Tool
     2. Quando ti viene richiesto cosa vuoi fare, scegli "**Crea supporti di installazione (unità flash USB, DVD o file ISO) per un altro PC**" e clicca **Avanti**
     3. Verifica che le opzioni raccomandate (linuga, versione ed architettura) siano corrette in base alle tue necessità e prosegui
     4. In "Scegli il supporto da usare" seleziona **File ISO** e clicca **Avanti**
     5. Scegli un nome per il file (esempio: **Windows10_1903_Italiano_x64.iso**) e prosegui. Inizierà il download della ISO configurata così come hai deciso nelle opzioni precedenti
     6. Clicca **Fine** al completamento per chiudere il wizard
3. *Metodo Alternativo: Scaricare la ISO direttamente da [https://www.microsoft.com/en-us/software-download/windows10ISO](https://www.microsoft.com/en-us/
software-download/windows10ISO), visitando la URL con un computer **non Windows** (OS X o Linux)*

### Montare la ISO e creare un file .zip

1. In Windows 10, la ISO può essere montata facendo clic con il pulsante destro del mouse sul file e scegliendo "**Monta**" o semplicemente facendo doppio clic sul file ISO.
2. Assicurati di avere 7-Zip installato. 7-Zip è una condizione essenziale, quindi se non lo hai procuratelo da [qui](https://www.7-zip.org/a/7z1604.exe)
3. Una volta montata, **seleziona tutti i file all'interno della ISO** (non la directory / unità, ma i file al suo interno), quindi fai clic con il pulsante destro del mouse e scegli "**7-Zip > Aggiungi all'archivio...**"
![Screenshot 1 - 7-Zip > Add to Archive...]({{ site.img_path }}/kace/w10upgrade/KB_1-547AMZ0_AddToArchive.png)
4. **Nota:** visto che la ISO è ovviamente read-only, scegli un percorso di salvataggio dello zip esterno, da qualche parte sul tuo hard disk
5. Al termine della compressione, il file zip verrà creato nella posizione selezionata con un nome generato automaticamente (esempio: setup.zip). Rinomina in modo appropriato (esempio: **Windows10_1903_Italiano_x64.zip**). Questo file verrà utilizzato nei seguenti passaggi
6. Smonta la ISO (fai clic con il pulsante destro del mouse sull'unità ed espelli) e fanne ciò che preferisci. Per questa guida non ne avremo più bisogno

## Seconda fase: Upload del pacchetto su KACE SMA

Per via delle limitazioni sulla massima dimensione uploadabile di un file via interfaccia web, il pacchetto zip deve essere caricato su Kace tramite la **condivisione samba *clientdrop***. La dimensione massima del file per il caricamento tramite l'interfaccia utente Web di SMA è infatti di 2GB (versione 8.0 e precedenti) o 4 GB (versione 8.1 e successive), mentre gli aggiornamenti di build tendono ad essere leggermente troppo grandi rispetto a questi limiti. Il metodo Samba evita del tutto il limite di upload e, opinione personale, è anche più veloce e pratico.

### Verifica dell'attivazione di Samba

1. Se Samba non è abilitato, abilitalo (Samba può essere disabilitato dopo che il pacchetto è stato caricato e importato al passaggio 3). Le impostazioni di abilitazione / disabilitazione di Samba si trovano in **Settings > Security Settings** all'interno dell'interfaccia di Amministrazione. Per abilitare Samba, verifica che sia abilitato il checkbox "**Enable organization file shares**"
![Screenshot 2 - Samba Shares]({{ site.img_path }}/kace/w10upgrade/KB_1-547AMZ0_w10bu_samba.png)
2. Assicurati anche che la condivisione sia abilitata anche a **livello di organizzazione** e di conoscere le credenziali per la share **clientdrop**. In caso contrario la password può essere reimpostata nella pagina **Settings > General Settings** nell'interfaccia utente di amministrazione (specifica dell'organizzazione per sistemi multi-org)
![Screenshot 3 - Samba Shares]({{ site.img_path }}/kace/w10upgrade/KB_1-547AMZ0_w10bu_samba_share.png)

### Caricamento dell'archivio nella clientdrop

1. Collegati alla share **clientdrop**. Puoi farlo facilmente aprendo un Esplora Risorse e digitando l'indirizzo UNC della tua appliance Kace (esempio: __\\\KBOX\clientdrop__, sostituendo _KBOX_ con il nome del tuo host SMA).
![Screenshot 4 - KACE SMA clientdrop]({{ site.img_path }}/kace/w10upgrade/KB_1-547AMZ0_w10bu_clientdrop.png)
2. Trascina all'interno della **clientdrop** il file .zip creato nella [Fase Uno](#prima-fase-creare-il-pacchetto-di-installazione)
3. ![Screenshot 5 - KACE SMA clientdrop]({{ site.img_path }}/kace/w10upgrade/KB_1-547AMZ0_w10bu_clientdrop_copy.png)
4. Concluso con successo il caricamento, passiamo allo Step 3

## Terza Fase: Mappare il pacchetto di installazione all'interno dell'Inventario

### Scenario Operativo

Per ragioni di performance, andremo a creare un **Custom Software Title** all'interno del **Software Inventory**, tralasciando invece il **Software Catalog**. Questa scelta è dovuta alla grande quantità di versioni e revisioni di Windows 10 all'interno del Catalog che andrebbero ad impattare fortemente sulle prestazioni del database di Kace ad ogni interrogazione dello stesso da parte della Managed Install che andremo a vedere verso la fine di questa guida.

Creeremo anche una apposita **regola di inventario personalizzato** ("*Custom Inventory Rule*"), in modo da avere un controllo più preciso e granulare sul processo di aggiornamento attuale e futuro.

### Creazione di un Custom Software

1. Nell'interfaccia di amministraizone, vai su **Inventory > Software**
2. Dal menu **Choose Action** seleziona **New**
3. Compila i campi **Name**, **Version**, **Publisher** e **Notes** come preferisci. Ad esempio:
![Screenshot 6 - Custom Inventory Title]({{ site.img_path }}/kace/w10upgrade/customsoftware.png)
4. Nel campo **Custom Inventory Rule** inseriamo una regola che andrà a verificare una precisa chiave di registro, situata in **HKLM\Software\Microsoft\Windows NT\CurrentVersion**, per identificare la verisone della build.
![Screenshot 7 - Custom Inventory Rule]({{ site.img_path }}/kace/w10upgrade/cir1903.png)  
Codice:
```dosbatch
RegistryValueEquals(HKLM64\SOFTWARE\Microsoft\Windows NT\CurrentVersion,ReleaseId,1903)
```
5. Associamo finalmente il nostro file zip, creato in precendenza e copiato nella condivisione clientdrop, al Custom Software. Per far ciò andremo a scegliere dal menu a tendina **Upload and Associate Client Drop File** il file, salvando al termine.
![Screenshot 8 - Media Upload]({{ site.img_path }}/kace/w10upgrade/mediaupload.png)

## Quarta Fase: Creazione e deploy del processo di aggiornamento

Ora che abbiamo tutti i pezzi del puzzle, dobbiamo solo unirli nel passaggio finale. Andremo a creare una **Installazione Gestita** (*Managed Install*) che avrà il compito di distrubire la nuova build di Windows 10 nei PC target.<br>
Andremo a dettagliare i passaggi uno per uno ma chi avesse già esperienza con le Managed Install può saltare direttamente alla fine.

### Creazione della Managed Install

1. Nel pannello di Amministrazione, vai in **Distribution > Managed Installations**
2. Seleziona **Choose Action > **New**
3. Digita un nome per la Managed Install, ad esempio "Windows 10 1903 Upgrade"
4. Imposta l'opzione di esecuzione desiderata in base ai tuoi requisiti. Se tieni il campo con valore "Disabled" la MI non verrà eseguita
5. In **Inventory** scegli **Software**
6. Nel menu a discesa **Software**, scegli il software title che hai creato nello [Step 3](#terza-fase-mappare-il-pacchetto-di-installazione-allinterno-dellinventario) ed a cui hai associato lo zip
7. Verifica che sia selezionato **Use associated file** e che il fle mostrato sia il tuo zip
![Screenshot 9 - Managed Install - General Settings]({{ site.img_path }}/kace/w10upgrade/mi-general.png)
8. Se lo desideri (consigliato), seleziona **Delete downloaded files**
9. **Installation Options:**
   1.  Seleziona **Override default installation** ed inserisci questa stringa  
  Codice:
  ```dosbatch
  setup.exe /auto upgrade /DynamicUpdate disable /showoobe none
  ```
   2.  Verifica che sia spuntato il selettore **Don't prepend msiexec.exe**  
![Screenshot 10 - Managed Install - Opzioni]({{ site.img_path }}/kace/w10upgrade/mi-options.png)
    * **Nota**: Puoi trovare una spiegazione esaustiva riguardo tutti i parametri di **setup.exe** tu technet di Microsoft, qui: [https://blogs.technet.microsoft.com/home_is_where_i_lay_my_head/2015/09/14/windows-10-setup-command-line-switches/](https://blogs.technet.microsoft.com/home_is_where_i_lay_my_head/2015/09/14/windows-10-setup-command-line-switches/)

### Deploy

1. Nella sezione **Deploy**, assegna alla Managed Install le **Labels** che ritieni più opportune (*è **fortemente raccomandato** eseguire uno o più test preliminari su un numero ristretto di computer*)
2. Configura la sezione di **Notifica**, inserendo un messaggio chiaro e che rispecchi le tue necessità
![Screenshot 11 - Managed Install - Schedule]({{ site.img_path }}/kace/w10upgrade/mi-schedule.png)
3. Configura la **Schedulazione**, anche qui in base alle tue specifiche (*Nota: non è consigliabile regolare la finestra di distribuzione, poiché le MIs vengono eseguite solo durante l'intervallo di inventario. Se la finestra è configurata in modo tale da non essere aperta abbastanza a lungo da consentire a tutti i sistemi di eseguire un intervallo di inventario, i sistemi interessati non riceveranno mai l'aggiornamento.*)
![Screenshot 12 - Managed Install - Schedule]({{ site.img_path }}/kace/w10upgrade/mi-deployment.png)
4. Premi **Save** per completare il lavoro. Abbiamo finito, buon aggiornamento di build 

(ricorda: **PROVA SEMPRE PRIMA DI DISTRIBUIRE!!!**)
