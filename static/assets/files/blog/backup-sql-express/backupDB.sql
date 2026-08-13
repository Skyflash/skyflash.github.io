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
