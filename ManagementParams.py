#Classe gérant les paramètres sauvegarder du jeu
class ManagParams :
	def __init__(self):
		self.url = "config.txt"
	
	#Fonction renvoyant la valeur du paramètre identifier par la varibale "champs", si elle n'est pas présente, elle renvoie false
	def get(self, champs):
		try :
			i = 0
			dict = {}
			indexLigne = -1
			with open(self.url, 'r') as fichier:
				params = fichier.readlines()
				for param in params:
					tab = param.split("=")
					if tab[0] == champs:	
						indexLigne = i
					i+=1
					dict[tab[0]] = tab[1][0:-1]
			if indexLigne != -1 : # si ça existe
				if "-" not in dict[champs]: 
					return int(dict[champs])
				else :
					return [int(i) for i in dict[champs].split("-")] #tableau des codes
			else:
				return False
		except Exception as e:
			print(e)
			print("il y a eu une erreur")
			return False

	#Fonction qui enregistre une valeur dans le config.txt
	def enregistre(self,id,reponse):
		file = open(self.url,"r")
		lignes = file.readlines()
		file.close()
		tab = lignes[id].split("=")
		lignes[id]=tab[0]+"="+reponse+"\n" # modifie ligne 
		file = open(self.url,"w")
		file.writelines(lignes)	
		file.close()
		print("Valeur modifiée !")

	#Fonction qui modifie une valeur dans le fichier conservant les valeurs des paramètres
	def modif(self, id):
		if id == 10 or id == 11:
			print("nouveau code : (ex: 1-0-0-0) avec des valeurs entre 0 et 2")
		else :
			print("nouvelle Valeur :")
		reponse = input()
		try :
			if id == 10 or id == 11: #Modif Code
				tabVerif = [int(i) for i in reponse.split("-")]
				if len(tabVerif) == 4: #Code de longeur 4 
					for code in tabVerif:
						if(code < 0 or code>2): # nombre du code >0 et <2
							print("Mauvais code")
							return False
					self.enregistre(id,reponse)
				else :
					print("Mauvais code")
					return False
			elif isinstance(int(reponse), (int)): # si c'est un int
				if int(reponse) <= 0 :
					print("Ce n'est pas une valeur autorisé")
					return False
				else:
					self.enregistre(id,reponse)
			else :
				print("Ce n'est pas une valeur autorisé")
				return False
		except Exception as e:
			print("Ce n'est pas une valeur autorisé")
			return False

	#Fonction qui va demander si l'utilisateur veut modifier les paramètres, si oui elle les modifies
	def modifParams(self):
		print("Bonjour, voulez-vous modifiez les paramètres de l'escape Game avant de le lancer ? (0:non, 1:oui)")
		reponse = input()
		if reponse == "1" :
			strAffiche = ""
			i = 0
			with open(self.url, 'r') as fichier:
				params = fichier.readlines()
				dict = {}
				for param in params:
					tab = param.split("=")
					strAffiche += "---- "+str(i)+" > "+tab[0]+" : "+tab[1][0:-1]+" ----\n"
					i+=1
					dict[tab[0]] = tab[1][0:-1]
				print(strAffiche) #Affiche l'ensemble des paramètres
			print("Que voulez-vous modifiez ? (entrez l'id d'un paramètre ou un non présent pour arrêter)")
			reponse = input()
			while(int(reponse) >= 0 and int(reponse) < 12):
				self.modif(int(reponse))
				print("Que voulez-vous modifiez ? (entrez l'id d'un paramètre ou un non présent pour arrêter)")
				reponse = input()
			print("Gestion des paramètres finie! Bon jeu :)\n")
		else :
			print("Très bien, Bon jeu :) !\n")


   

