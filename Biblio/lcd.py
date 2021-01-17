# coding: utf-8
import smbus
import time
import tty
import sys

DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

class Lcd:
	def __init__(self,port):
		self.bus = smbus.SMBus(port)  #1 pour I2C-1 (0 pour I2C-0)

	# Completez le code de la fonction permettant de choisir la couleur
	# du fond d'ecran, n'oubliez pas d'initialiser l'ecran
	def setRGB(self,rouge,vert,bleu):
		# rouge, vert et bleu sont les composantes de la couleur qu'on vous demande
		self.bus.write_byte_data(DISPLAY_RGB_ADDR,0x00,0x00)
		self.bus.write_byte_data(DISPLAY_RGB_ADDR,0x01,0x00)
		self.bus.write_byte_data(DISPLAY_RGB_ADDR,0x02,bleu)
		self.bus.write_byte_data(DISPLAY_RGB_ADDR,0x03,vert)
		self.bus.write_byte_data(DISPLAY_RGB_ADDR,0x04,rouge)
		self.bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xAA)
		#print("Couleur écran changée")

	def setColor(self,couleur):
		if(couleur == "rouge"):
			self.setRGB(255,0,0)
		elif(couleur == "bleu"):
			self.setRGB(0,0,255)
		elif(couleur == "vert"):
			self.setRGB(0,255,0)
		elif(couleur == "blanc"):
			self.setRGB(255,255,255)
		elif(couleur == "noir"):
			self.setRGB(0,0,0)
		else:
			self.setRGB(50,50,150)
		
	# Envoie  a l'ecran une commande concerant l'affichage des caracteres
	# (cette fonction vous est donnes gratuitement si vous
	# l'utilisez dans la fonction suivante, sinon donnez 2000€
	# a la banque et allez dictement en prison :)
	def textCmd(self,cmd):	
		time.sleep(0.1)
		self.bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

	def initScreen(self):
		self.textCmd(0x01)
		self.textCmd(0x0F)
		self.textCmd(0x38)

	def rewriteSecToFirstLigne(self,texte):
		time.sleep(2)
		self.initScreen()
		for ca in texte:
			self.bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(ca))
		self.textCmd(0xc0)
		return ""

	def setSecondLigne(self,texte):
		self.textCmd(0xC0)
		for c in range(15):
			if c > len(texte)-1:
				self.bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(" "))
			else :
				self.bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(texte[c]))

	# Completez le code de la fonction permettant d'ecrire le texte recu en parametre
	# Si le texte contient un \n ou plus de 16 caracteres pensez a gerer
	# le retour a la ligne
	def setText(self,texte):
		self.initScreen()
		# ...
		i = 0 #Nb de caracteres sur la ligne
		j = 0 #nb ligne
		StrMemoire = ""
		for c in texte:
			if c == '\n':
				if(j==1):
					StrMemoire = self.rewriteSecToFirstLigne(StrMemoire)
				else:
					self.textCmd(0xc0)
					j=1
				i=0 # Reset 
			elif j==1 and i==15:
				self.bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))
				StrMemoire+=c
				StrMemoire = self.rewriteSecToFirstLigne(StrMemoire)
				i=0
			elif i==15 :
				self.bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))
				self.textCmd(0xc0)
				i=0 # Reset
				j=1
			elif j==1 :
				StrMemoire+=c
				self.bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))
				i+=1
			else:
				self.bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))
				i+=1
