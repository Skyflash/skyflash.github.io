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
