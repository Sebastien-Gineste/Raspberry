import time
from Biblio.grovepi import *

class DUltraSon:
	def __init__(self,port):
		self.port = port
	#Renvoi vrai si la distance détecter est entre cmMin et cmMax
	def estDansZone(self, cmMin, cmMax): # estEntreDistance cmMin et cmMax
		try:
			valUltra = ultrasonicRead(self.port)
			print("Dist : ",valUltra)
			if valUltra == 516: #Erreur capteur
				return True
			return valUltra < cmMax and valUltra > cmMin
		except IOError:
			print("Error")
	#Renvoi vrai si la distance détecter est plus petite que cmMax
	def estPPD(self, cmMax): #estPlusPetiteDistance
      		try:
        		return ultrasonicRead(self.port) < cmMax
      		except IOError:
       			print("Error")
	#Renvoi vrai si la distance détecter est plus grande que cmMin
	def estPGD(self, cmMin): #estPlusGrandeDistance
		try:
			return ultrasonicRead(self.port) > cmMin
		except IOError:
			print("Error")
