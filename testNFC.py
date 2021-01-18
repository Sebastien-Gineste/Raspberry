import os,time,threading

from Biblio.NFC import NFC
codestr1 = "['0x9e','0xb8','0x0','0x0']"
codestr2 = "['0x1f','0xf5','0x90','0x0']"

nfc = NFC(codestr1,codestr2)

print(nfc.ProgDetectCard())
