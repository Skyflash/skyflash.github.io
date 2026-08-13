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
