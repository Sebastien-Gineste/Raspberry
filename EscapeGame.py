# coding: utf-8
import time,sys,signal
from Biblio.Led import Led
from Biblio.Button import Button
from Biblio.lcd import Lcd
from Biblio.BaseDonnees import BaseDonnees
from Biblio.CapteurLum import CapteurLum #Pour enigme 4
import DetectCode as dc
import Enigme1 as e1
import Enigme2 as e2
import Enigme3 as e3
import Enigme5 as e5
import Enigme6 as e6
from datetime import datetime
import time,sys

but3 = Button(3) # Permet de lancer la détection de code (Enigme 1 et 2)
estAppuie3 = False
but4 = Button(4) # Permet de lancer l'énigme 3 
estAppuie4 = False
butCache = Button(5) # Permet de lancer l'énigme 5 
estAppuieCacher = False
captLum = CapteurLum(0) # Permet de lancer l'énigme 4

tempsTotal = 600
tempsRestant = tempsTotal
lcd = Lcd(1)
strEnigmeFini = ["-","-","-","-","-","-"]
lcd.setText("Esc Game "+''.join(strEnigmeFini)+"   "+str(tempsTotal)+" secondes ")
lcd.setColor("vert")
time.sleep(1)

print('Entrez votre pseudo :')
pseudo = input()
tabScore = ["0","0","0","0","0","0"]

tempsGame = datetime.now()

continueGame = True
tabEnigmeFini = [False, False, False, False, False, False]

def Fin_prog(): #Fonction appellé lors de la fin du jeu
	bd = BaseDonnees()
	bd.envoiPost(pseudo,tabScore[0],tabScore[1],tabScore[2],tabScore[3],tabScore[4],tabScore[5])
	print("Fin du jeu")
	sys.exit(0)

def fin_signal_ALRM(sig,ignore): #Fonction appellé lorsqu'on a dépassé le temps limite
	lcd.setText("Esc Game "+''.join(strEnigmeFini)+"   Perdu ! HAHA")
	lcd.setColor("rouge")
	Fin_prog()

signal.signal(signal.SIGALRM, fin_signal_ALRM)
signal.alarm(tempsRestant) # après 600 seconde on lance la fonction qui arrête tout

try : 
	while continueGame:
		if not tabEnigmeFini[0] or not tabEnigmeFini[1]:
			if but3.estAppuie():
				estAppuie3 = True
			elif not but3.estAppuie() and estAppuie3:  #lancementDetectCode
				resultCode = dc.DetectCode()
				if resultCode == 1 and not tabEnigmeFini[0]: #commence Enigme 1
					lcd.setText("Bravo ! code 1")
					time.sleep(2)
					if e1.Enigme1(8,5,0.5) :
						strEnigmeFini[0] = "X"
						tempsRestant = tempsTotal - int((datetime.now()-tempsGame).total_seconds())
						tabScore[0] = str(tempsRestant) #On met le temps qu'il reste après la fin de l'énigme
						lcd.setText("Esc Game "+''.join(strEnigmeFini)+"   "+str(tempsRestant)+" secondes ")
						time.sleep(2)
						tabEnigmeFini[0] = True
				elif resultCode == 2 and not tabEnigmeFini[1]: #commence Enigme 2
					lcd.setText("Bravo ! code 2")
					time.sleep(2)
					if e2.Enigme2(8):
						strEnigmeFini[1] = "X"
						tempsRestant = tempsTotal - int((datetime.now()-tempsGame).total_seconds())
						tabScore[1] = str(tempsRestant) #On met le temps qu'il reste après la fin de l'énigme
						lcd.setText("Esc Game "+''.join(strEnigmeFini)+"   "+str(tempsRestant)+" secondes ")
						time.sleep(2)				
						tabEnigmeFini[1] = True					
				elif resultCode == 2 or resultCode == 1:
					print("Déja fait")
				else :
					print("Enigme : echouer")
				estAppuie3 = False
		
		if not tabEnigmeFini[2]:
			if but4.estAppuie():
				estAppuie4 = True
			elif not but4.estAppuie() and estAppuie4:  #lancement Enigme 3
				if e3.Enigme3(8,5,30):
					strEnigmeFini[2] = "X"
					tempsRestant = tempsTotal - int((datetime.now()-tempsGame).total_seconds())
					tabScore[2] = str(tempsRestant) #On met le temps qu'il reste après la fin de l'énigme
					lcd.setText("Esc Game "+''.join(strEnigmeFini)+"   "+str(tempsRestant)+" secondes ")
					time.sleep(2)
					tabEnigmeFini[2] = True
				else:
					time.sleep(1)
					lcd.setColor("vert")
					estAppuie4 = False			

		if not tabEnigmeFini[3]: #Pas encore fini
			if captLum.PresenceLumiere(6): #Si le joueur allume le capteur
				lcd.setText("Enigme 4 Fini ! ")
				time.sleep(2)
				strEnigmeFini[3] = "X"
				tempsRestant = tempsTotal - int((datetime.now()-tempsGame).total_seconds())
				tabScore[3] = str(tempsRestant) #On met le temps qu'il reste après la fin de l'énigme	
				lcd.setText("Esc Game "+''.join(strEnigmeFini)+"   "+str(tempsRestant)+" secondes ")
				time.sleep(1)
				tabEnigmeFini[3] = True
		
		if not tabEnigmeFini[4]:
			if butCache.estAppuie() and not estAppuieCacher: #Appuie sur le bouton caché
				estAppuieCacher = True
			elif not butCache.estAppuie() and estAppuieCacher: #Relache le bouton caché
				if e5.Enigme5(5) : # Si l'énigme5 est réussie
					strEnigmeFini[4] = "X"
					tempsRestant = tempsTotal - int((datetime.now()-tempsGame).total_seconds())
					tabScore[4] = str(tempsRestant)
					lcd.setText("Esc Game "+''.join(strEnigmeFini)+"   "+str(tempsRestant)+" secondes ")
					time.sleep(1)
					tabEnigmeFini[4] = True
				else : 
					time.sleep(0.5)
					estAppuieCacher = False # On réinitalise le bouton
		
		if not tabEnigmeFini[5] and tabEnigmeFini[0] and tabEnigmeFini[1] and tabEnigmeFini[2] and tabEnigmeFini[3] and tabEnigmeFini[4]: #Une fois toutes les énigmes finis
			if but3.estAppuie():
				estAppuie3 = True
			elif not but3.estAppuie() and estAppuie3:  #lancementEnigme3
				if e6.Enigme6(20) :
					strEnigmeFini[5] = "X"
					tempsRestant = tempsTotal - int((datetime.now()-tempsGame).total_seconds())
					tabScore[5] = str(tempsRestant)
					lcd.setText("Esc Game "+''.join(strEnigmeFini)+"   "+str(tempsRestant)+" secondes ")
					time.sleep(1)
					tabEnigmeFini[5] = True
					lcd.setText("Bravooooo!")
					time.sleep(1)
					Fin_prog()
				else:
					estAppuie3 = False
		if tempsRestant > tempsTotal - int((datetime.now()-tempsGame).total_seconds()):
			tempsRestant = tempsTotal - int((datetime.now()-tempsGame).total_seconds())
			lcd.setText("Esc Game "+''.join(strEnigmeFini)+"   "+str(tempsRestant)+" secondes ")
		elif tempsTotal - int((datetime.now()-tempsGame).total_seconds()) <= 0:
			lcd.setColor("rouge")
			lcd.setText("Esc Game "+''.join(strEnigmeFini)+"   Perdu ! HAHA")
			break;

except KeyboardInterrupt: #Si on fait Ctrl + C
	Fin_prog()
	#Envoie le score du joueur sur le google form
except IOError: # Si problème de connexion au Grove
	print("Problème avec le Grove")
