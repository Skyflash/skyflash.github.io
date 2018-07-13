strComputer = "."
Dim log
Set log = Wscript.CreateObject("Scripting.Filesystemobject")
Set f = log.CreateTextFile("C:\Tools\smartcard.txt", 2)
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_PnPSignedDriver Where DeviceClass = 'SMARTCARDREADER'",,48) 
For Each objItem in colItems 
    f.WriteLine "DeviceClass: " & objItem.DeviceClass
Next
f.Close