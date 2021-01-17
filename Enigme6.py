#coding : utf-8
from Biblio.grovepi import *
from Biblio.Button import Button
from Biblio.lcd import Lcd
from Biblio.Led import Led
from Biblio.CapteurMvt import CaptMvt
import time
from datetime import datetime

def Enigme6(tLim) :
	Led1 = Led(7)
	lcd = Lcd(1)
	Button2 = Button(2)
	ButEstAppuie = False
	TabAvancer = [False,False,False] #0 : bouton enclenché, #1 : Capteur de présence enclenché, #2 Bouton réappuyé
	CapteurMvt1 = CaptMvt(8)
	tempsLimite = tLim 
	tempsCommence = -1
	LcdAffiche = False
	time.sleep(0.5)
	lcd.setText("Debut Enigme     finale")
	time.sleep(2)
	lcd.setColor("vert")
	lcd.setText("Appuyez sur un bouton :)")
	time.sleep(2)
	while True :
		if not TabAvancer[0]:
			if Button2.estAppuie() and not ButEstAppuie:
				ButEstAppuie = True
			elif not Button2.estAppuie() and ButEstAppuie:
				tempsCommence = datetime.now()
				lcd.setColor("vert")
				lcd.setText("Cette Led doit  s'allumer")
				time.sleep(1.5)
				TabAvancer[0] = True
		elif not TabAvancer[1] and (datetime.now() - tempsCommence).total_seconds() <= tempsLimite: 
			if CapteurMvt1.estPresence():
				lcd.setColor("vert")
				lcd.setText("1 etape sur 2   realisee")
				time.sleep(1.5)
				TabAvancer[1] = True
				ButEstAppuie = False
		elif TabAvancer[1] and not TabAvancer[2] and (datetime.now() - tempsCommence).total_seconds() <= tempsLimite:
			if Button2.estAppuie() and not ButEstAppuie:
				ButEstAppuie = True
			elif not Button2.estAppuie() and ButEstAppuie:
				Led1.turnOn()
				lcd.setColor("vert")
				lcd.setText("Led allumee bravo, Enigme finale reussie !")
				time.sleep(2)
				return True
		else : #Temps dépassé
			lcd.setColor("rouge")
			if not TabAvancer[1]:
				lcd.setText("Temps depasse, il manque 2 etapes !")
			else:
				lcd.setText("Temps depasse, il manque une etape ! ")		
			time.sleep(2)
			lcd.setColor("vert")
			return False
			#Lcd.setText("Réessayez !")
			#LcdAffiche = False

