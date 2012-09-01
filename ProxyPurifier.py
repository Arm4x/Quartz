#!/usr/bin/env python
from SyncPrint import *
import socks, threading, time, sys
proxies = open("list.txt").readlines()
def atest(x,a):
	while True:
		try:
			x = proxies.pop(0)
		except:
			sys.stderr.write("- Finished")
			return
		state = ""
		test = ["HTTP", "SOCKS4", "SOCKS5"]
		for mode in test:
			kmode = eval("socks.PROXY_TYPE_" + mode)
			try:
				s = socks.socksocket()
				s.settimeout(5)
				s.setproxy(kmode, x.split(":")[0], int(x.split(":")[1].replace("\n","")))
				s.connect(("www.ubuntu.com",80))
				s.sendall("GET / HTTP/1.1\r\nHost: www.ubuntu.com\r\n\r\n")
				kddt = s.recv(500)
				if kddt.find("Home | Ubuntu"):
					state = mode
					s.close()
					break
				s.close()
			except:
				pass
		if state != "":
			syncprint(state + "|" + x.replace("\n",""))
		
for xa in xrange(2000):
	t=threading.Thread(target=atest, args=(0,0))
	t.daemon=True
	t.start()
try:
	while True: 
		time.sleep(0.1)
		sys.stdout.flush()
except (KeyboardInterrupt, SystemExit):
	syncprint( '\nReceived keyboard interrupt, quitting!' )
	sys.exit()

