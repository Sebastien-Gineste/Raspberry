import requests

class BaseDonnees:
	def __init__(self):
		self.BASE_URL = "https://docs.google.com/forms/d/"
		self.id = "1b1uHK1Qg8GL7v4iSsgbHH78e9UmYEmBcRiO9MHRSHWA"

	def envoiPost(self,pseudo,x1,x2,x3,x4,x5,x6):
		myobj = {'entry.507353568' : pseudo,'entry.1281000' : x1,'entry.868785079' : x2,'entry.1460687400': x3, 'entry.664422064':x4,'entry.51431724':x5,'entry.1665534565':x6}
		requests.post(self.BASE_URL+self.id+"/formResponse?ifq&submit=Submit", data = myobj)
