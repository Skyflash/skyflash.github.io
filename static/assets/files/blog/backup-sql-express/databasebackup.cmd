@echo off
REM Lancio il backup e scrivo il log
sqlcmd -S SERVER\SQLEXPRESS -E -i C:\SQL_Backup\scripts\backupDB.sql -o C:\SQL_Backup\Logs\backuplog.txt

REM Lancio lo script di pulizia e aggiorno cleanuplog.txt
C:\SQL_Backup\scripts\deleteoldsqlbaks.vbs
