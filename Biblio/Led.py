import time
from datetime import datetime
from Biblio.grovepi import *
from Biblio.lcd import Lcd

class Led:
	def __init__(self,port):
		self.port = port
		pinMode(self.port,"OUTPUT")
	
	def turnOn(self):
		digitalWrite(self.port,1)

	def turnOff(self):
		digitalWrite(self.port,0)

	def blinkPlus(self, timeMax):
		try:	
			LcdAffiche = True
			lcd = Lcd(1)
			lcd.setSecondLigne(" En position !")
			lcd.setColor("bleu")
			tempsCommence = datetime.now()
			while (datetime.now()-tempsCommence).total_seconds() < timeMax : #Tant qu'il reste du temps
				tempsRest = (datetime.now()-tempsCommence).total_seconds() #0,1,2,3,4,...,timeMAx
				if tempsRest < (timeMax/2): # si il reste + de la moitié du temps
					self.blink(timeMax/10,1)
				elif LcdAffiche: # il reste la moitié
					lcd.setSecondLigne("   En cours...")
					LcdAffiche = False
				if tempsRest < (2*timeMax/4) and tempsRest > (timeMax/2): # il reste entre 25% ET 50% DE TEMPS
					self.blink(timeMax/20,1)
				elif tempsRest < timeMax and tempsRest > (2*timeMax/4): # il reste entre 0% et 25%
					self.blink(timeMax/30,1)
			lcd.setColor("vert")
			lcd.setSecondLigne(" Traitement..")
			self.turnOn()
			time.sleep(1)
							
		except KeyboardInterrupt:
			self.turnOff()
		except IOError:
			print("Error")
		
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
