---
title: Identificare e terminare processi zombie su Linux
layout: post
date: '2015-10-25'
description: Vediamo come uccidere, con un semplice script, eventuali processi zombie
  rimasti attivi sul nostro server Linux
intro: "Nei sistemi operativi Unix e Unix-like, un processo zombie o processo defunto è un processo informatico che, nonostante abbia terminato la propria esecuzione, possiede ancora un PID ed un process control block"
lang: it_IT
image: "/static/assets/img/blog/zombiesign.jpg"
keywords: linux,script,process,kill,zombie,server
categories:
- Linux
tags:
- Linux
- Scripting
- Process
- sicurezza
- script
icon: fa-linux
---

Recentemente ho avuto necessità di eseguire un pò di tuning su un server Linux, spesso infestato da processi zombie che lo portavano a raggiungere elevatissimi carichi operativi. Dalla descrizione di Wikipedia:

>Nei sistemi operativi Unix e Unix-like, un processo zombie o processo defunto è un processo informatico che, nonostante abbia terminato la propria esecuzione, possiede ancora un PID ed un process control block, necessario per permettere al proprio processo padre di leggerne il valore di uscita.

Girovagando alla ricerca di informazioni utili, mi sono imbattuto in un ottimo script, da copiare sui vostri server, in grado di identificare e killare lo zombie, oltre a lasciarne una traccia un un file di log apposito.

* TOC 
{:toc}

## LO SCRIPT KILL-ZOMBIE

Come prima cosa, creeremo (con i permessi di root) un nuovo file kill-zombie

```bash
cd /root
vi kill-zombies
```

In seguito copiamo il seguente codice ed incolliamolo nel file appena creato

```bash
#! /bin/bash
#
# Zombie processes killing script. Must be run under root.
 
case "$1" in
--admin)
stat=`ps ax | awk '{print $1}' | grep -v "PID" | xargs -n 1 ps lOp | grep -v "UID" | awk '{print"pid: "$3" *** parent_pid: "$4" *** status: "$10" *** process: "$13}' | grep ": Z"`
 
if ((${#stat} > 0));then
echo zombie processes found:
echo .
ps ax | awk '{print $1}' | grep -v "PID" | xargs -n 1 ps lOp | grep -v "UID" | awk '{print"pid: "$3" *** parent_pid: "$4" *** status: "$10" *** process: "$13}' | grep ": Z"
echo -n "Kill zombies? [y/n]: "
read keyb
if [ $keyb == 'y' ];then
echo killing zombies..
ps ax | awk '{print $1}' | grep -v "PID" | xargs -n 1 ps lOp | grep -v "UID" | awk '{print$4" status:"$10}' | grep "status:Z" | awk '{print $1}' | xargs -n 1 kill -9
fi
else
echo no zombies found!
fi
;;
--cron)
stat=`ps ax | awk '{print $1}' | grep -v "PID" | xargs -n 1 ps lOp | grep -v "UID" | awk '{print"pid: "$3" *** parent_pid: "$4" *** status: "$10" *** process: "$13}' | grep ": Z"`
if ((${#stat} > 0));then
ps ax | awk '{print $1}' | grep -v "PID" | xargs -n 1 ps lOp | grep -v "UID" | awk '{print$4" status:"$10}' | grep "status:Z" | awk '{print $1}' | xargs -n 1 kill -9
echo `date`": killed some zombie processes!" >> /var/log/zombies.log
fi
;;
*) echo 'usage: kill-zombies {--cron|--admin}'
;;
esac
exit 0
```

Ora rendiamolo eseguibile e spostiamolo in /usr/bin

```bash
chmod +x kill-zombies
mv kill-zombies /usr/bin
```

### FUNZIONAMENTO

Lo script viene evocato con un flag, che ne modifica il comportamento:

```bash
kill-zombies --admin
```

L’esecuzione avviene manualmente. Se vengono rilevati processi zombie l’utente ne viene informato e deve confermare l’operazione

```bash
kill-zombies --cron
```

Lo script **dovrà essere inserito nel crontab** e richiamato quindi a cadenze regolari dal server. I processi vengono killati in automatico e ne viene lasciata traccia in /var/log/zombies.log

### INSERIMENTO NEL CRONTAB

Richiamiamo l’editor del crontab con questo comando

```bash
crontab -e
```

Ed inseriamo questa riga:

```bash
*/10 * * * * /usr/bin/kill-zombies --cron
```

In questo modo, lo script verrà eseguito ogni 10 minuti a cadenza regolare. In caso si voglia modificare l’intervallo di tempo, sarà sufficiente cambiare ad esempio */10 in */5 (per 5 minuti)

[Download zombies.sh (1 KB)](https://www.skyflash.it/download/8205/)

Riferimenti:

* [Identificare ed uccidere processi zombie in un server Linux](https://www.skyflash.it/computer/linux-os/identificare-ed-uccidere-processi-zombie-in-un-server-linux/6076/)
* [CronHowTo](https://help.ubuntu.com/community/CronHowto)