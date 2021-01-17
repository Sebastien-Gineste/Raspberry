#coding : utf-8

from Biblio.Button import Button
from Biblio.lcd import Lcd
import time
import random
from datetime import datetime



def Enigme1(nbrEtape,tLim,valTempsDiminu):
	
	lcd = Lcd(1)
	But1 = Button(2)
	But2 = Button(3)
	But3 = Button(4)

	tabB = [But1,But2,But3]
	tabEstAppuie = [False,False,False]
	indiceEtape = 0
	tempsLimite = tLim
	tempsCommence = -1

	LcdAffiche = False
	
	time.sleep(0.5)
	lcd.setText("Debut Enigme1")
	time.sleep(2)
	
	while(indiceEtape < nbrEtape):
		if LcdAffiche == False : # affiche code à rentré
			butX = random.randint(0, 2) # entre bouton 0, 1 et 2
			tabCode = ["0","0","0"]
			tabCode[butX] = "X"
			time.sleep(0.1)
			lcd.setText("-".join(tabCode))
			LcdAffiche = True
			tempsCommence = datetime.now()
		#S'il appuie sur les autre boutons ou que le temps est fini on recommence depuis le début
		if (datetime.now()-tempsCommence).total_seconds() > tempsLimite or (tabB[0].estAppuie() and 0 != butX) or (tabB[1].estAppuie() and 1 != butX)or (tabB[2].estAppuie() and 2 != butX):
			indiceEtape = 0
			tempsLimite = tLim
			lcd.setColor("rouge")
			if (datetime.now()-tempsCommence).total_seconds() > tempsLimite :
				lcd.setText("Temps dépasse ! ")
			else :
				lcd.setText("Oups.. Perdu !")
			time.sleep(2)
			lcd.setColor("vert")
			lcd.setText("On recommence ! ")
			LcdAffiche = False
		if tabB[butX].estAppuie():
			tabEstAppuie[butX] = True
		elif not tabB[butX].estAppuie() and tabEstAppuie[butX] and (datetime.now()-tempsCommence).total_seconds() <= tempsLimite: #il a appuyé sur le bon bouton à temps
			print("Bravo ! ")
			tabEstAppuie[butX] = False
			indiceEtape+=1
			if nbrEtape == indiceEtape: # fini
				lcd.setText("BRAVO !\n Fini !")
				time.sleep(2)
				return True
			else : # reste des étapes
				tempsLimite-=valTempsDiminu
				LcdAffiche = False
				lcd.setText("Etape"+str(indiceEtape)+" reussie")
				time.sleep(1)
