import time
from Biblio.grovepi import *

class Buzzer:
	def __init__(self,port):
		self.port = port
		pinMode(self.port,"OUTPUT")

	def turnOn(self):
		digitalWrite(self.port,1)

	def turnOff(self):
		digitalWrite(self.port,0)

	def blink(self,times,nbrBlink):
		for i in range(nbrBlink):
			try:
				self.turnOn()
				time.sleep(times)
				self.turnOff()
				time.sleep(times)
			except KeyboardInterrupt:
				self.turnOff()
				break
			except IOError:
				print("Error") 
