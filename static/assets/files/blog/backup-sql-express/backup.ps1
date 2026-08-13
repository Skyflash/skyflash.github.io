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
