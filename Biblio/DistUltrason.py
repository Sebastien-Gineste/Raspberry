import time
from Biblio.grovepi import *

class DUltraSon:
	def __init__(self,port):
		self.port = port
	
	def estDansZone(self, cmMin, cmMax): # estEntreDistance cmMin et cmMax
		try:
			valUltra = ultrasonicRead(self.port)
			print("Dist : ",valUltra)
			return valUltra < cmMax and valUltra > cmMin
		except IOError:
			print("Error")

	def estPPD(self, cmMax): #estPlusPetiteDistance
      		try:
        		return ultrasonicRead(self.port) < cmMax
      		except IOError:
       			print("Error")

	def estPGD(self, cmMin): #estPlusGrandeDistance
		try:
			return ultrasonicRead(self.port) > cmMin
		except IOError:
			print("Error")
