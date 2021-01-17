#coding : utf-8
from Biblio.grovepi import *
from Biblio.Button import Button
from Biblio.lcd import Lcd
from Biblio.NFC import NFC
import time
import random
from datetime import datetime

def Enigme5(tLim) :
	But0 = Button(2)
	But1 = Button(3)
	But2 = Button(4)
	ButCacher = Button(5) # Permet de quitter l'énigme si le joueur n'y arrive pas
	EstAppuieCacher = False 
	lcd = Lcd(1)
	
	#Cartes NFC
	codestr1 = "['0x9e','0xb8','0x0','0x0']"
	codestr2 = "['0x1f','0xf5','0x90','0x0']"
	nfc = NFC(codestr1,codestr2) #Initialisation du NFC
	nfcActive = False #N'est pas activé encore pour le joueur	

	tabB = [But0,But1,But2]
	tabEstAppuie = [False,False,False]
	tempsLimite = tLim
	tempsCommence = -1

	LcdAffiche = False
	time.sleep(0.5)
	lcd.setText("Debut Enigme5")
	time.sleep(2)
	while True :
		if ButCacher.estAppuie() and not EstAppuieCacher:
			EstAppuieCacher = True
		if not ButCacher.estAppuie() and EstAppuieCacher: #Le joueur à réappuyer sur le bouton caché : il veut quitté l'énigme
			return False
		if not nfcActive : #NFC non activé encore
			if LcdAffiche == False :
				butX = random.randint(0,2) #Button aléatoire entre 0, 1 et 2
				butX2 = random.randint(0,2)
				while butX == butX2: # tant que c'est les mêmes, on refait un tirage
					butX = random.randint(0,2)		
				tabCode = ["0","0","0"]
				tabCode[butX] = "X"
				tabCode[butX2] = "X"
				time.sleep(0.1)
				lcd.setColor("vert")
				lcd.setText("-".join(tabCode)+"  Activer le lecteur!")
				tempsCommence = datetime.now()
				LcdAffiche = True
			# On a cliqué le mauvais bouton, ou le temps a été dépassé
			if (datetime.now()-tempsCommence).total_seconds() > tempsLimite or (tabB[0].estAppuie() and (0 != butX and 0 != butX2)) or (tabB[1].estAppuie() and (1 != butX and 1 != butX2)) or (tabB[2].estAppuie() and (2 != butX and 2 != butX2)):
				lcd.setColor("rouge")
				if (datetime.now()-tempsCommence).total_seconds() > tempsLimite :	
					lcd.setText("Temps depasse ! ")
				else :	
					lcd.setText("Oups.. Mauvais Code!")
				time.sleep(2)
				lcd.setColor("vert")
				#lcd.setText("Essaye encore ! ")
				#LcdAffiche = False
				return False
			if tabB[butX].estAppuie() and tabB[butX2].estAppuie() :
				tabEstAppuie[butX] = True
				tabEstAppuie[butX2] = True
			elif not tabB[butX].estAppuie() and tabEstAppuie[butX] and not tabB[butX2].estAppuie() and tabEstAppuie[butX2] and (datetime.now()-tempsCommence).total_seconds() <= tempsLimite: #il a appuyé sur les bon bouton à temps
				lcd.setColor("vert")
				lcd.setText("   Lecteur   \n NFC  active!")
				time.sleep(2)
				tabEstAppuie[butX] = False
				tabEstAppuie[butX2] = False
				nfcActive = True
		else : 
			val = nfc.ProgDetectCard() 
			print(val)
			if val == "2": #Si le NFC est activé et qu'il donne la bonne carte : Enigme fini
				lcd.setColor("vert")
				lcd.setText("Enigme 5 réussie")
				time.sleep(2)
				return True
			elif val == "-2":
				return False #Le joueur à abandonné
			else:
				lcd.setText("mauvaise carte ..")
				time.sleep(2)
				lcd.setColor("Vert")
				return False

