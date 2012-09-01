#!/usr/bin/env python
from SyncPrint import *
import socks, threading, time, sys
proxies = open("list.txt").readlines()
def atest(x,a):
	while True:
		try:
			x = proxies.pop(0)
		except:
			sys.exit(0)
		s = socks.socksocket()
		s.settimeout(5)
		state = False
		try:
			s.setproxy(socks.PROXY_TYPE_SOCKS4, x.split(":")[0], int(x.split(":")[1].replace("\n","")))
			s.connect(("www.minecraft.net",80))
			s.send("GET / HTTP/1.1\r\nHost: www.minecraft.net\r\n\r\n")
			if s.recv(1024).find("Minecraft is a game about placing blocks to build anything") != -1:
				state = True
		except:
			pass
		s.close()
		if state == True:
			syncprint(x.replace("\n",""))
for xa in xrange(1000):
	t=threading.Thread(target=atest, args=(0,0))
	t.daemon=True
	t.start()
try:
	while True: time.sleep(1000)
except (KeyboardInterrupt, SystemExit):
	syncprint( '\nReceived keyboard interrupt, quitting!' )
	sys.exit()

