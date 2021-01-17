import time
from Biblio.grovepi import *

class Button:
	def __init__(self,port):
		self.port = port                                            
		pinMode(self.port,"INPUT")

	def estAppuie(self):
      		try:
        		return digitalRead(self.port) == 1
      		except IOError:
       			print("Error")
