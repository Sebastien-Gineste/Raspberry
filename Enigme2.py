#coding : utf-8

from Biblio.lcd import Lcd
from Biblio.CapteurMvt import CaptMvt
from Biblio.DistUltrason import DUltraSon
import time
import random



def Enigme2(nbrEtape):
	
	lcd = Lcd(1)
	captMvt = CaptMvt(8) #Capteur de présence
	captUlt = DUltraSon(6) #Capteur de distance Ultrason
	tabCapt = [captMvt,captUlt]
	tabEstPresence = [False,False]
	indiceEtape = 0
	DistMaxPresence = 100 
	LcdAffiche = False
	
	time.sleep(0.5)
	lcd.setText("Debut Enigme2")
	time.sleep(2)
	
	while(indiceEtape < nbrEtape):
		if LcdAffiche == False : # affiche code à rentré
			capteurX = random.randint(0, 1) # Choisie entre capteur 1 et 2
			lcd.setText("Recepteur "+str(capteurX))
			LcdAffiche = True
			time.sleep(0.5)
		#S'il enlenche le mauvais capteur on recommence depuis le début
		if (tabCapt[0].estPresence() and 0 != capteurX) or (tabCapt[1].estPPD(DistMaxPresence) and 1 != capteurX):  
			indiceEtape = 0
			lcd.setColor("rouge")
			lcd.setText("Oups.. Perdu !")
			time.sleep(2)
			lcd.setColor("vert")
			lcd.setText("On recommence ! ")
			LcdAffiche = False
		if  not tabEstPresence[capteurX] and ((0 == capteurX and tabCapt[0].estPresence()) or (1 == capteurX and tabCapt[1].estPPD(DistMaxPresence))): #le détecteur la capté, on attend qu'il ressorte de la zone
			tabEstPresence[capteurX] = True
		elif tabEstPresence[capteurX] and ((0 == capteurX and not tabCapt[capteurX].estPresence()) or (1 == capteurX and not tabCapt[1].estPPD(DistMaxPresence))): #il est sortie de la zone
			print("Bravo")
			tabEstPresence[capteurX] = False
			indiceEtape+=1
			if nbrEtape == indiceEtape: # fini
				lcd.setText("BRAVO !\n Fini !")
				time.sleep(2)
				return True
			else : # reste des étapes
				LcdAffiche = False
				lcd.setText("Etape "+str(indiceEtape)+" reussie")
				time.sleep(2)
