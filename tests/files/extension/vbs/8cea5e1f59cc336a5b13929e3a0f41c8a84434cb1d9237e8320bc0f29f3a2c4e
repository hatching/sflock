Attribute VB_TEST = FOO

strComputer = "."
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\cimv2")
Set colProcesses = objWMIService.ExecQuery _
    ("Select * from Win32_Process Where Name = 'Dfrgntfs.exe'")
If colProcesses.Count = 0 Then
    Wscript.Echo " Dfrgntfs.exe is not running."
Else
    Wscript.Echo " Dfrgntfs.exe is running."
End If

For i = 1 to 5
    Wscript.echo i
Next

Public Sub hello()
    If 1
        Wscript.Echo "hello"
End Sub

Function hello2()
    Dim var1
End Function
