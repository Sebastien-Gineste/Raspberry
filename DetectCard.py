# coding: utf-8
import sys

from Biblio.NFC import NFC

tabHexa = ['',''] # code des 2 cartes

if len(sys.argv) == 3:
	for i,elt in enumerate(sys.argv):
		if i != 0:
			tabHexa[i-1] = elt


	#nfc = NFC(['0x9e', '0xb8', '0x0', '0x0'],['0x1f', '0xf5', '0x90', '0x0'])
	
	nfc = NFC(tabHexa[0],tabHexa[1])
	nfc.DetectCard()
else:
	print("error argument")
