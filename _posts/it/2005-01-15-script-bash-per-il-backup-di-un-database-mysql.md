---
layout: post
lang: it_IT
title: "Script bash per il backup di un database MySQL"
date: '2005-01-15 15:08:20'
description: "Uno script bash per automatizzare il backup giornaliero di un database MySQL su server Linux, con rotazione dei file per ogni giorno della settimana."
intro: "In passato ho avuto bisogno di uno script che, in modo automatico, mi facesse una serie di backup del database MySQL che gira sul nostro server in azienda."
image: "/static/assets/img/blog/backup-mysql/cover.jpg"
categories:
- Infrastruttura & Sistemi
keywords: bash, mysql, backup, linux, script
tags:
- bash
- mysql
- backup
- linux
- script
- database
permalink: "/it/blog/infrastruttura/:title/"
redirect_from:
  - "/2005/01/script-bash-per-il-backup-di-un-databse-mysql/"
  - "/blog/infrastruttura/script-bash-per-il-backup-di-un-database-mysql/"
icon: fa-linux
---
In passato ho avuto bisogno di uno script che, in modo automatico, mi facesse una serie di backup del database MySQL che gira sul nostro server in azienda.

Così mi sono messo un paio d'ore a studiare il linguaggio bash, che non conoscevo, ed ho "partorito" questo script:

Dopo alcune impostazioni iniziali, non fa altro che eseguire un dump del database e ne mette una copia nella home dell'utente, col nome `[database]_DAILY_[data_di_oggi]` e, nel caso ci sia, rinomina quello del giorno prima in `[database]_OLD`

Infine genera un ulteriore dump e lo piazza in una altra directory, che sul mio server corrisponde a `/dati` e lo nomina `Backup_db_[database]_[weekday]`, dove `[weekday]` è il giorno della settimana. In questo modo avremo sempre due copie del db nella nostra home (quella odierna e quella di ieri) e ben 7 copie, una per ogni giorno della settimana, in `/dati` (o altra directory).

E' molto grezzo, e chi volesse contribuire a migliorarlo è ben accetto 😉

```sh
#!/bin/bash
# Impostazioni dello script
# Qui comincia la sezione delle varibili utente da impostare
# Regolare questi valori secondo le proprie necessita'
# INIZIO SEZIONE IMPOSTAZIONE
#
# DIR -> Nome della directory home dell'utente.
# ATTENZIONE: DEVE TERMINARE CON "/"
#
# BACKUP -> Nome della directory dove andranno i backup.
# ATTENZIONE: DEVE TERMINARE CON "/"
#
# DATABASE -> Nome del database MySQL
#
# NAME -> Nome che verra' usato per generare il backup.
# ATTENZIONE: MANTENERE IL SUFFISSO "_DAILY_"
#
# OLD -> Nome che verra' usato per copiare il database
# del giorno prima. ATTENZIONE: MANTENERE IL SUFFISSO "_OLD"
#
DIR="/home/utente/"
BACKUP="/directory/"
DATABASE="NOME DATABASE"
NAME="NOME_DAILY_"
OLD="NOME_OLD"
#
# FINE DELLA SEZIONE DI IMPOSTAZIONE
#
# Queste sono le variabili di data e di ricerca
# in base al nome ricavato dalle variabili precedenti
#
OF=$(date +%d-%m-%Y)
IF=$(ls $DIR | grep $NAME)
DAY=$(date +%w_%a)
#
# Cambio il nome del file trovato
mv $DIR$IF $DIR$OLD.sql
#
# Eseguo il dump del database definito dalle variabili
#
# ALTRE IMPOSTAZIONI
# Cambiare [nome] con il nome utente e [password] con la password
# Cambiare [group] con il gruppo a cui appartiene l'utente (solitamente, uguale a [nome])
#
mysqldump --user=[nome] --password=[password] $DATABASE > $DIR$NAME$OF.sql
mysqldump --user=[nome] --password=[password] $DATABASE > $BACKUP"Backup_db_"$DATABASE"_0"$DAY.sql
#
# Cambio i permessi del dump nella mia home
# perche' sono fighetto e li voglio gia' accessibili al mio utente
#
chown [nome].[group] $DIR$NAME$OF.sql
#
echo Backup del database $DATABASE eseguito!
```

[Download backup-mysql.sh](/static/assets/files/blog/backup-database-mysql/backup-mysql.sh)

> **Nota:** passare la password con `--password=` la rende visibile a chiunque lanci `ps` sulla stessa macchina, oltre che nella cronologia della shell. Oggi è preferibile salvare le credenziali in un file `~/.my.cnf` (con permessi `chmod 600`) e lanciare `mysqldump` senza specificarle sulla riga di comando.

### Pianificazione automatica

Per eseguire il backup ogni notte senza doversene ricordare, basta aggiungerlo al crontab:

```bash
crontab -e
```

ed inserire una riga come questa, che lo esegue ogni giorno all'1:00 di notte:

```bash
0 1 * * * /home/utente/backup-mysql.sh
```
