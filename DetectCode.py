# coding : utf-8

from Biblio.Button import Button
from Biblio.lcd import Lcd
import time

def DetectCode(code1,code2):
	lcd = Lcd(1)
	But1 = Button(2)
	But2 = Button(3)
	But3 = Button(4)
	LancementDirect = True
	tabB = [But1,But2,But3]
	tabEstAppuie = [False,False,False]
	codeEnigme1 = code1
	codeEnigme2 = code2
	tabCodeEntrer = [-1,-1,-1,-1]

	ContinueEntrerCode = True
	LcdAffiche = False
	while ContinueEntrerCode:
		if LancementDirect or (tabB[1].estAppuie() and LcdAffiche == False):
			lcd.setText("Rentre un code!")
			LcdAffiche=True
			LancementDirect = False
			i=0
			while(i < 4):
				if tabB[0].estAppuie() or tabB[1].estAppuie() or tabB[2].estAppuie():
					if(tabB[0].estAppuie()):
						tabEstAppuie[0] = True
					if(tabB[1].estAppuie()):
						tabEstAppuie[1] = True
					if(tabB[2].estAppuie()):
						tabEstAppuie[2] = True
				if(not tabB[0].estAppuie() and tabEstAppuie[0]): #relache le premier boutou
					tabCodeEntrer[i] = 0
					i+=1
					tabEstAppuie[0] = False
				if(not tabB[1].estAppuie() and tabEstAppuie[1]): #relache le deuxième bouton
					tabCodeEntrer[i] = 1
					i+=1
					tabEstAppuie[1] = False
				if(not tabB[2].estAppuie() and tabEstAppuie[2]): #relache le troisème bouton
					tabCodeEntrer[i] = 2
					i+=1
					tabEstAppuie[2] = False
			estCode1 = True
			estCode2 = True
			for j in range(4):
				if(tabCodeEntrer[j] != codeEnigme1[j]):
					estCode1 = False
				if(tabCodeEntrer[j] != codeEnigme2[j]):
					estCode2 = False
			if(estCode1):
				print("code 1")
				return 1
			elif(estCode2):
				print("code 2")
				return 2
			else:
				lcd.setText("Erreur !")
				lcd.setColor("rouge")
				time.sleep(1.5)
				lcd.setColor("vert")
				lcd.setText("But2 : restart\nBut3 : stop")
				LcdAffiche = False
		elif tabB[2].estAppuie() and LcdAffiche == False: #Veut arrêter
			lcd.setText("Arret ...")
			return -1
