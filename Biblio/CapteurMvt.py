import time
from Biblio.grovepi import *

class CaptMvt:
	def __init__(self,port):
		self.port = port                                            
		pinMode(self.port,"INPUT")

	def estPresence(self):
      		try:
        		return digitalRead(self.port) == 1
      		except IOError:
       			print("Error")
