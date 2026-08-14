---
layout: post
lang: it_IT
title: "Backup automatizzato dei database su SQL Express"
date: '2012-05-24 17:03:37'
description: "Automatizzare il backup dei database su SQL Server Express, privo di SQL Agent: script T-SQL, pulizia in VBScript e attività pianificata di Windows."
intro: "SQL Server Express viene distribuito senza SQL Agent, quindi non è possibile schedulare internamente a SQL Server processi automatizzati, come ad esempio il backup."
categories:
- Infrastruttura & Sistemi
keywords: sql server, sql express, backup, database, vbscript
tags:
- database
- sql
- backup
permalink: "/it/blog/infrastruttura/:title/"
redirect_from:
  - "/2012/05/backup-automatizzato-dei-database-su-sql-express/"
  - "/blog/infrastruttura/backup-automatizzato-dei-database-su-sql-express/"
translation_key: sql-express-automated-backup
icon: fa-database
---
SQL Server Express viene distribuito senza SQL Agent, quindi non è possibile schedulare internamente a SQL Server processi automatizzati, come ad esempio il backup. E' però possibile aggirare questo ostacolo creando uno script ad-hoc, che si occupi dei vari job che vogliamo eseguire.

In questo articolo vedremo come creare uno **script per il backup di SQL Express** e, subito dopo, uno per la manutenzione dei backup, il cui compito sarà quello di tenere sempre le tre copie più recenti, cancellando di volta in volta quelli più vecchi.

> Tutto il lavoro verrà svolto all'interno della cartella **C:\SQL_Backup** e delle due sotto cartelle **scripts** e **Logs**, che dovranno quindi essere create preventivamente.
>
> Alla fine dell'articolo trovate i tre script già pronti da scaricare, con la stessa struttura di cartelle descritta qui sopra.

* TOC
{:toc}

## Lo script per il backup di SQL Express

Portiamoci all'interno di **C:\SQL_Backup\scripts** e creiamo un file che chiameremo **backupDB.sql** con questo contenuto:

```sql
DECLARE @dateString CHAR(12), @dayStr CHAR(2), @monthStr CHAR(2), @hourStr CHAR(2), @minStr CHAR(2)
--month variable
IF (SELECT LEN(CAST(MONTH(GETDATE()) AS CHAR(2))))=2
SET @monthSTR=CAST(MONTH(GETDATE()) AS CHAR(2))
ELSE
SET @monthSTR= '0' + CAST(MONTH(GETDATE()) AS CHAR(2))
--day variable
IF (SELECT LEN(CAST(DAY(GETDATE()) AS CHAR(2))))=2
SET @daySTR=CAST(DAY(GETDATE()) AS CHAR(2))
ELSE
SET @daySTR='0' + CAST(DAY(GETDATE()) AS CHAR(2))
--hour variable
IF (SELECT LEN(DATEPART(hh, GETDATE())))=2
SET @hourStr=CAST(DATEPART(hh, GETDATE()) AS CHAR(2))
ELSE
SET @hourStr= '0' + CAST(DATEPART(hh, GETDATE()) AS CHAR(2))
--minute variable
IF (SELECT LEN(DATEPART(mi, GETDATE())))=2
SET @minStr=CAST(DATEPART(mi, GETDATE()) AS CHAR(2))
ELSE
SET @minStr= '0' + CAST(DATEPART(mi, GETDATE()) AS CHAR(2))
--name variable based on time stamp
SET @dateString=CAST(YEAR(GETDATE()) AS CHAR(4)) + @monthStr + @dayStr + @hourStr + @minStr
--=================================================================
DECLARE @IDENT INT, @sql VARCHAR(1000), @DBNAME VARCHAR(200)
SELECT @IDENT=MIN(database_id) FROM SYS.DATABASES WHERE [database_id] > 0 AND NAME NOT IN ('TEMPDB')
WHILE @IDENT IS NOT NULL
BEGIN
SELECT @DBNAME = NAME FROM SYS.DATABASES WHERE database_id = @IDENT
/*Change disk location here as required*/
SELECT @SQL = 'BACKUP DATABASE '+@DBNAME+' TO DISK = ''C:\SQL_Backup\'+@DBNAME+'_db_' + @dateString +'.BAK'' WITH INIT'
EXEC (@SQL)
SELECT @IDENT=MIN(database_id) FROM SYS.DATABASES WHERE [database_id] > 0 AND database_id>@IDENT AND NAME NOT IN ('TEMPDB')
END
```

Lo script andrà a creare tanti backup quanti sono i database all'interno di SQL Express, ed aggiungerà una sorta di "timestamp" alla fine del nome, in modo da identificarli nel tempo, prima di terminare con l'estensione `.BAK`.

## Cancellazione dei backup vecchi

Sempre all'interno di **C:\SQL_Backup\scripts** creiamo un file **deleteoldsqlbaks.vbs** in cui scriveremo:

```vb
On Error Resume Next
Dim fso, folder, files, sFolder, sFolderTarget
Set fso = CreateObject("Scripting.FileSystemObject")

'location of the database backup files
sFolder = "C:\SQL_Backup\"

Set folder = fso.GetFolder(sFolder)
Set files = folder.Files

'used for writing to textfile - generate report on database backups deleted
Const ForAppending = 8

'you need to create a folder named "scripts" for ease of file management &
'a file inside it named "LOG.txt" for delete activity logging
Set objFile = fso.OpenTextFile(sFolder & "\Logs\cleanuplog.txt", ForAppending)

objFile.Write "================================================================" & VBCRLF & VBCRLF
objFile.Write " DATABASE BACKUP FILE REPORT " & VBCRLF
objFile.Write " DATE: " & FormatDateTime(Now(),1) & "" & VBCRLF
objFile.Write " TIME: " & FormatDateTime(Now(),3) & "" & VBCRLF & VBCRLF
objFile.Write "================================================================" & VBCRLF

'iterate thru each of the files in the database backup folder
For Each itemFiles In files
'retrieve complete path of file for the DeleteFile method and to extract
'file extension using the GetExtensionName method
a=sFolder & itemFiles.Name

'retrieve file extension
b = fso.GetExtensionName(a)
'check if the file extension is BAK
If uCase(b)="BAK" Then

'check if the database backups are older than 3 days
If DateDiff("d",itemFiles.DateCreated,Now()) >= 3 Then

'Delete any old BACKUP files to cleanup folder
fso.DeleteFile a
objFile.WriteLine "BACKUP FILE DELETED: " & a
End If
End If
Next

objFile.WriteLine "================================================================" & VBCRLF & VBCRLF

objFile.Close

Set objFile = Nothing
Set fso = Nothing
Set folder = Nothing
Set files = Nothing
```

Il compito di questo script sarà quello di posizionarsi nella cartella in cui abbiamo salvato i backup, "contare" i backup presenti e tenere i tre più recenti, cancellando gli altri. Inoltre, scrive un log delle operazioni eseguite.

## I file di log

Portiamoci in `C:\SQL_Backup\Logs` e creiamo due file vuoti, che chiameremo `backuplog.txt` e `cleanuplog.txt`

## Esecuzione

Creiamo il file **databasebackup.cmd**

```batchfile
@echo off
REM Lancio il backup e scrivo il log
sqlcmd -S SERVER\SQLEXPRESS -E -i C:\SQL_Backup\scripts\backupDB.sql -o C:\SQL_Backup\Logs\backuplog.txt

REM Lancio lo script di pulizia e aggiorno cleanuplog.txt
C:\SQL_Backup\scripts\deleteoldsqlbaks.vbs
```

L'unica modifica da fare sarà l'inserimento del nome e della istanza del vostro server, sostituendo **SERVER\SQLEXPRESS** con i vostri dati corretti (presumibilmente, l'istanza si chiama sempre **SQLEXPRESS** ma cambia il nome del server)

## Schedulazione

Non resta che creare una **Operazione pianificata** dal **Pannello di controllo di Windows**, il cui semplice compito consisterà nell'esecuzione di **C:\SQL_Backup\scripts\databasebackup.cmd**, impostando un orario ed una ricorrenza secondo le proprie necessità.

## Aggiornamento (2026): la versione moderna con PowerShell

A 14 anni di distanza, l'approccio di fondo (uno script esterno più un'operazione pianificata, visto che SQL Express non ha mai guadagnato SQL Agent) resta valido, e lo script **backupDB.sql** funziona ancora così com'è. Quello che è invecchiato è il resto della catena: Microsoft ha avviato la **deprecazione di VBScript**, con rimozione pianificata da Windows nelle prossime versioni, quindi non ha più senso scrivere nuovo codice che ci si appoggia.

Al posto di `deleteoldsqlbaks.vbs` e `databasebackup.cmd` basta un unico script **PowerShell**, che richiama `backupDB.sql` tramite `sqlcmd` (nessuna dipendenza aggiuntiva da installare) e si occupa della pulizia mantenendo solo le ultime copie più recenti *per ciascun database*, invece del semplice "cancella tutto ciò che ha più di 3 giorni" dello script originale:

```powershell
# backup.ps1 - versione moderna, sostituisce deleteoldsqlbaks.vbs + databasebackup.cmd
# Richiede solo sqlcmd (incluso in SQL Server / SQL Server Express, oppure
# installabile a parte tramite gli "SQL Server Command Line Utilities")

$SqlInstance = "SERVER\SQLEXPRESS"
$BackupPath  = "C:\SQL_Backup"
$KeepCopies  = 3

# 1. Backup: richiama lo script T-SQL backupDB.sql, invariato
sqlcmd -S $SqlInstance -E -i "$BackupPath\scripts\backupDB.sql" -o "$BackupPath\Logs\backuplog.txt"

# 2. Pulizia: tiene solo le ultime $KeepCopies copie per ciascun database
Get-ChildItem -Path $BackupPath -Filter "*.BAK" |
    Group-Object { $_.Name -replace '_db_\d{12}\.BAK$', '' } |
    ForEach-Object {
        $_.Group | Sort-Object LastWriteTime -Descending | Select-Object -Skip $KeepCopies
    } |
    ForEach-Object {
        Remove-Item $_.FullName -Force
        "$(Get-Date -Format s)  BACKUP FILE DELETED: $($_.FullName)" | Add-Content "$BackupPath\Logs\cleanuplog.txt"
    }
```

Nell'Operazione pianificata, l'azione da eseguire diventa quindi `powershell.exe -ExecutionPolicy Bypass -File C:\SQL_Backup\scripts\backup.ps1` al posto del vecchio `databasebackup.cmd`.

## Download

- [backupDB.sql](/static/assets/files/blog/backup-sql-express/backupDB.sql)
- [backup.ps1](/static/assets/files/blog/backup-sql-express/backup.ps1) — versione consigliata (2026)
- [deleteoldsqlbaks.vbs](/static/assets/files/blog/backup-sql-express/deleteoldsqlbaks.vbs) — script originale del 2012
- [databasebackup.cmd](/static/assets/files/blog/backup-sql-express/databasebackup.cmd) — script originale del 2012

Via | [mssqltips.com](https://www.mssqltips.com/sqlservertip/1486/automate-sql-server-express-backups-and-deletion-of-older-backup-files/)
