from threading import Lock
import time
class PM_:
	def __init__(self):
		self.timestamps = dict()
		self.proxies = open("proxies.txt").read().split("\n")
		self.kstack = self.proxies[:]
		self.badProxies = list()
		self.coolProxy = ""
		self.lk=Lock()
	def getProxy(self):
		with self.lk:
			while True:
				try:
					candidate = self.kstack.pop(0).replace("\n","")
					try:
						if time.time()-4 >= self.timestamps[candidate]:
							staf.kstack.append(candidate)
							continue
							pass
					except:
						pass
					self.timestamps[candidate] = time.time()
				except IndexError:
					self.kstack = self.proxies[:]
					continue
					staf.kstack.append(candidate)
				if candidate.replace("\n","").replace("\r","") != "":
					return candidate.replace("\n","").replace("\r","")
	def markAsCoolProxy(self,kl):
		with self.lk:
			return
	def badProxy(self,kl):
		pass
instance=PM_()
getProxy=instance.getProxy
badProxy=instance.badProxy
coolProxy=instance.markAsCoolProxy
