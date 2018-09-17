---
title: Come importare un certificato CA su PC Windows con Kace 1000
layout: post
date: '2018-09-17 11:30:00'
description: Vediamo insieme come distribuire certificati Windows usando KACE 1000
lang: it_IT
image: "/static/assets/img/blog/ssl.png"
categories:
- Kace
keywords: kace,k1000,script,batch,ssl,certificate,certutil,kscript
tags:
- kace
- k1000
- script
- batch
- kscript
- ssl
- ca root
- certificate
- security
- sicurezza
icon: fa-floppy-o
intro: In un ambiente professionale, in cui è buona norma avere utenze Windows senza
  diritti di amministrazione del PC, anche l'installazione di una semplice CA può
  risultare difficoltosa in quanto è spesso richiesto l'intervento del reparto IT
  a cui è demandato il supporto utenti.
---

Per installare certificati in maniera trasparente possiamo usare diversi metodi, il più ovvio e diffuso dei quali è senza dubbio una _GPO_. Ma non è sempre detto che la GPO sia la soluzione più veloce (ad esempio: chi deve eseguire il deploy dei certificati non ha i permessi per lavorare sulle GPO, o il certificato deve essere installato su un numero esiguo di PC per cui chi dovrebbe fare la GPO non considera questa un'attività primaria da svolgere ed i tempi rischiano di allungarsi)

Andiamo quindi a vedere come **distribuire un certificato CA self-signed tramite KACE 1000**. In seguito andremo anche ad installare sui client, con la stessa procedura, un secondo certificato intermedio, validato a sua volta dalla CA.

* TOC
{:toc}

# L'utility certutil.exe
certutil.exe è una utility, presente in tutti i sistemi Windows, che ci permette di fare tante cose con i certificati.
Possiamo convertirli in caso il formato che abbiamo non sia quello che ci serve, possiamo importarli ed esportarli (sia in locale che su Active Directory), verificare la validità delle coppie di chiavi privata/pubblica eccetera.

Si usa da riga di comando e per la sintassi completa vi rimando [all'apposita pagina](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/certutil){:target="_blank"} sulla Knowledge Base Micorosoft

## Definizioni

- Entrambi i nostri certificati sono già in formato .cer
- Il certificato CA si chiama NGIRootCA01
- Il certificato intermedio si chiama NGISSLCA01.cer

## Importazione della CA tramite certutil.exe

Il comando di importazione, che possiamo eseguire da un qualsiasi prompt amministrativo, è il seguente

```batch
start /wait certutil -addstore Root NGIRootCA01.cer
```

Il parametro -addstore deifnisce il datastore in cui andremo ad installare il certificato. *Root* corrisponde a "**Autorità di certificazione radice attendibili**"


## Importazione del certificato intermedio

Il certificato intermedio (che chiameremo SSLCA01.cer) a cui si faceva riferimento poco fa si importerà nella stessa maniera, cambiando solamente il datastore di riferimento:

```msdos
start /wait certutil -addstore CA NGISSLCA01.cer
```


# Lo script (kscript) su Kace

Andiamo ora a riportare tutto su Kace 1000, creando uno script apposito.

## Riassunto delle Attività

- Impostazione dei parametri di base
- Importazione dei due certificati come dipendenze
- Creazione di un batch file
- Schedulazione

## Realizzazione 

1. Portiamoci in _Scripting / Scripts_ e creiamo un novo kscript ("_New_")  
2. Una volta definito un nome, portiamoci nella sezione _Operating Systems_ e clicchiamo su **Manage Operating Systems**, andando a selezionare tutti i SO Windows (e, visto che andremo a creare un batch file, **solo** quelli Windows) di nostro interesse  
  ![kscript Manage Operating Systems](/static/assets/img/blog/kace/cassl/oss.png)  
3. Verifichiamo che _Windows Run As_ sia impostato a **Local System**  
  ![kscript Run As](/static/assets/img/blog/kace/cassl/runas.png)  
4. Nella sezione **Dependencies** facciamo click su **+New Dependency...** e carichiamo:

   1. Il certificato Root
   2. Il certificato Intermedio  
   ![kscript Certificati](/static/assets/img/blog/kace/cassl/certificati.png) 
5. Facciamo ora click su **+Task...** nella sezione sottostante ed impostiamo i seguenti passi:

   1. **Verify** that the file "C:\Tools\certificato.ok" exists (questo ci servirà per fare un check sull'applicazione del certificato, che andremo a schedulare e qundi ad eseguire ad intervalli regolari; se il file _certificato.ok_ esiste allora lo script si interrompe). Per riferimento sul percorso scelto, potete vedere [questo mio precedente articolo](/blog/kace/k1000-report-pc-with-smartcard-reader/){:target="_blank"}
   2. **On Success**: nulla
   3. **Remediation**: Run the batch file "_Install_CA_Root_Script_" with params ""  
    ![kscript Script](/static/assets/img/blog/kace/cassl/script.png)  
    Codice:
    ```dosbatch
    @echo off
    start /wait certutil -addstore Root NGIRootCA01.cer
    start /wait certutil -addstore CA NGISSLCA01.cer
    exit
    ```  
   4. **On Remediaton Success** Launch a program...  
    ![kscript Remediation](/static/assets/img/blog/kace/cassl/remediation.png)  

6. Clicchiamo su **Save** per completare la creazione del kscript

## Schedulazione

In caso volessimo schedulare lo script, sarà sufficiente, una volta tornati in editing, andare ad impostare la finestra desiderata.
Ad esempio, nel nostro caso lo script verrà eseguito sui devices desiderati ogni tre ore secondo questa logica:

   1. Lo script viene eseguito la prima volta
   2. Al termine, lascia un file "_certificato.ok_", di dimensione 0 bytes, in C:\Tools\
   3. Dalla volta seguente (ogni tre ore...) se trova il file "certificato.ok" allora si interrompe e non fa null'altro

![kscript Schedule](/static/assets/img/blog/kace/cassl/schedule.png)  