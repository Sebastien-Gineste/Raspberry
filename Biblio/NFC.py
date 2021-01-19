import RPi.GPIO as GPIO
import os,time,threading,sys,signal
from Biblio.pn532 import *
from Biblio.lcd import Lcd
from Biblio.Button import Button
from datetime import datetime

#Thread qui va récuperer la valeur de la carte
class CardThread(threading.Thread):

	def __init__(self,C1,C2):
		threading.Thread.__init__(self)
		self.valCard = '' #La valeur de la carte sera mise ici
		self.C1 = C1 #code de la carte 1 
		self.C2 = C2 #code de la carte 2

	def run(self):
		cmd = "sudo python3 DetectCard.py "+self.C1+" "+self.C2 # prépare la commande pour récupèrer la valeur de la carte
		print(cmd) 
		res = os.popen(cmd) #lance la commande dans un autre processus
		self.valCard = res.read().split("\n") #Attends de recevoir la réponse

#Classe utilisant le composant lecteur NFC
class NFC:
	def __init__(self,hexaCarte1,hexaCarte2):
		self.C1 = hexaCarte1 #code de la carte 1
		self.C2 = hexaCarte2 #code de la carte 2

	#Fonction permettant de lancer le thread et de modifier l'affichage du LCD en fonction du temps passé à attendre
	#Elle renvoie la valeur de la carte mise sur le lecteur, ou -2 si le temps est dépassé 
	def ProgDetectCard(self):
		self.th = CardThread(str(self.C1),str(self.C2)) #Initialise le Thread
		self.th.start() #Le lance (sa fonction run())
		lcd = Lcd(1)
		butCache = Button(5)
		estAppuie = False
		afficheTemps = False
		tempsAttente = datetime.now()
		lcd.setText("En attente de   carte ...")
		lcd.setColor("bleu")
		while self.th.valCard == "": #Attends qu'il récupère sa valeur 
			if butCache.estAppuie() and not estAppuie:
				estAppuie = True
			elif not butCache.estAppuie() and estAppuie:
				return -2
			#Si ça fait déjà 4 secondes que le joueur n'a pas mit la carte on annonce que c'est bientôt fini
			elif not afficheTemps and 4 == int((datetime.now() - tempsAttente).total_seconds()):
				lcd.setText("Bientot fini...")
				lcd.setColor("rouge")
				afficheTemps = True
		print("test : ",self.th.valCard[2])
		if len(self.th.valCard[2]) > 2 : # Pas de carte au bout de 10 seconde
			return -2
		else :
			return self.th.valCard[2] #La retourne

	#Fonction qui attend que le joueur place une carte
	#Si au bout de 7 secondes, la fonction n'a toujours rien reçu, on arrête la fonction grâce au signal alarm.
	#Sinon affiche le numéro de carte (1 ou 2) placé par le joueur. 
	def DetectCard(self):
		try:
			pn532 = PN532_I2C(debug=False, reset=20, req=16)
			ic, ver, rev, support = pn532.get_firmware_version()
			print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

			# Configure PN532 to communicate with MiFare cards
			pn532.SAM_configuration()
			#Fonction du signal
			def fin_signal_ALRM(sig,ignore):
				print("ça fait 7 secondes, on kill")
				sys.exit()

			signal.signal(signal.SIGALRM,fin_signal_ALRM)
			signal.alarm(7) #Lance le signal alarm sur 7 secondes

			print('Waiting for RFID/NFC card...')
			# Check if a card is available to read
			while True :
				uid = pn532.read_passive_target(timeout=0.5) #Attend que le joueur place une carte
			
				if uid is None:
    					continue
				
				tabHexa = [hex(i) for i in uid]
		
				carte1 = self.C1[1:-1].split(",") # Transforme en tableau				
				carte2 = self.C2[1:-1].split(",") # Transforme en tableau
				estC1 = True	
				estC2 = True
	
				for i in range(len(tabHexa)):
					if tabHexa[i] != carte1[i]:	
						estC1 = False
					if tabHexa[i] != carte2[i]:
						estC2 = False
				
				if(estC1):
					print("1")
					return 1
				elif(estC2):
					print("2")
					return 2
				else:
					print("-1")
					return -1		
		except KeyboardInterrupt: #Ctrl C
			print("stop")
		except Exception as e:
			print(e)
		finally:
			GPIO.cleanup()
