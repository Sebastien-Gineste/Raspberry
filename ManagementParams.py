import sys

class ManagParams :
  def __init__(self):
    self.url = "config.txt"

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
        return int(dict[champs])
      else:
        return False
    except Exception as e:
      print(e)
      print("il y a eu une erreur")
      return False

  
  def modif(self, id):
    print("nouvelle Valeur :")
    reponse = input()
    try :
      if isinstance(int(reponse[:-1]), (int)): # si c'est un int
          file = open(self.url,"r")
          lignes = file.readlines()
          file.close()
          tab = lignes[id].split("=")
          lignes[id]=tab[0]+"="+reponse+"\n" # modifie la ligne 
          file = open(self.url,"w")
          file.writelines(lignes)
          file.close()
          print("Valeur modifiée !")
      else :
        print("Ce n'est pas une valeur autorisé")
        return False
    except Exception as e:
      print("Ce n'est pas une valeur autorisé")
      return False
  
  def modifParams(self):
    print("Bonjour, voulez-vous modifiez les paramètres de l'escape Game ? (0:non, 1:oui)")
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
        print(strAffiche)
       
        print("Que voulez-vous modifiez ? (entrez l'id)")
        reponse = input()
        while(int(reponse) >= 0 and int(reponse) < 10):
          self.modif(int(reponse))
          print("Que voulez-vous modifiez ? (entrez l'id)")
          reponse = input()

    else :
      print("Très bien, au revoir")
      sys.exit()


   

