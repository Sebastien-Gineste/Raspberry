import time
from Biblio.grovepi import *

class CapteurLum :
	def __init__(self,port):
		self.port = port
		pinMode(self.port,"INPUT")

	def PresenceLumiere(self,seuil): #seuil peut-etre à mettre en variable
		try:
			sensor_value = analogRead(self.port)
			if (sensor_value == 0):
				sensor_value = 0.1
			resistance = (float)(1023 - sensor_value) * 10 / sensor_value
			if(resistance > seuil):
				return False # ne capte pas assez de lumiere
			else:
				return True # capte assez de lumiere
		except IOError:
			print("Error")
