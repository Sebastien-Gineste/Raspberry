#coding : utf-8
from Biblio.grovepi import *
from Biblio.DistUltrason import DUltraSon
from Biblio.lcd import Lcd
from Biblio.Led import Led
from Biblio.NFC import NFC
import time
import random
from datetime import datetime

def Enigme3(tLim,nbTour,zone) :
	captUlt = DUltraSon(6)
	lcd = Lcd(1)
	led = Led(7)

	#Cartes NFC
	codestr1 = "['0x9e','0xb8','0x0','0x0']"
	codestr2 = "['0x1f','0xf5','0x90','0x0']"
	nfc = NFC(codestr1,codestr2) #Initialisation du NFC

	time.sleep(0.5)
	lcd.setText("Debut Enigme3")
	time.sleep(2)

	val = nfc.ProgDetectCard() #test carte
	print(val)
	if val == "1": #bonne carte
		i = 0
		while i < nbTour :
			Dist = random.randint(10,200) #Button aléatoire entre 10 et 400 (centimetre)
			time.sleep(0.1)
			lcd.setColor("vert")
			lcd.setText("Dist : "+str(Dist)+"cm..")
			led.blinkPlus(tLim)
			if captUlt.estDansZone(Dist-zone,Dist+zone): #si le joueur est dans la bonne distance
				lcd.setText(" -- Bravo! --   Etape "+str(i)+" finie")
				time.sleep(1.5)
				i=i+1
			else:
				time.sleep(1)
				lcd.setColor("rouge")
				lcd.setText("Mauvaise distance !")
				i = 0
				time.sleep(1.5)
				lcd.setText("On recommence !")
				time.sleep(1)
		led.turnOff()
		return True
	elif val == "-2":
		lcd.setText("Plus de temps")
		return False
	else: #mauvaise carte
		lcd.setText("mauvaise carte ..")
		return False
