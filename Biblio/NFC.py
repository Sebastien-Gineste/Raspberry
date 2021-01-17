import RPi.GPIO as GPIO
import os,time,threading,sys,signal
from Biblio.pn532 import *
from Biblio.lcd import Lcd
from Biblio.Button import Button


class myThread(threading.Thread):

	def __init__(self,C1,C2):
		threading.Thread.__init__(self)
		self.valCard = ''
		self.C1 = C1
		self.C2 = C2

	def run(self):
		self.PID = os.getpid()
		cmd = "sudo python3 DetectCard.py "+self.C1+" "+self.C2
		print(cmd)
		res = os.popen(cmd)
		self.valCard = res.read().split("\n")

class NFC:
	def __init__(self,hexaCarte1,hexaCarte2):
		self.C1 = hexaCarte1
		self.C2 = hexaCarte2

	def ProgDetectCard(self):
		self.th = myThread(str(self.C1),str(self.C2)) #Initialise un Thread
		self.th.start() #Le lance
		lcd = Lcd(1)
		butCache = Button(5)
		estAppuie = False
		lcd.setText("En attente de   carte ...")
		lcd.setColor("bleu")
		while self.th.valCard == "": #Attends qu'il récupère sa valeur
			if butCache.estAppuie() and not estAppuie:
				estAppuie = True
			elif not butCache.estAppuie() and estAppuie:
				self.th.tuer()
				return -2 #Quitte le programme : le joueur abandonne
		print("test : ",self.th.valCard[2])
		return self.th.valCard[2] #La retourne

	def DetectCard(self):
		try:
			pn532 = PN532_I2C(debug=False, reset=20, req=16)
			ic, ver, rev, support = pn532.get_firmware_version()
			print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

			# Configure PN532 to communicate with MiFare cards
			pn532.SAM_configuration()
	
			print('Waiting for RFID/NFC card...')
			while True:
				# Check if a card is available to read
				uid = pn532.read_passive_target(timeout=0.5)
				
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
