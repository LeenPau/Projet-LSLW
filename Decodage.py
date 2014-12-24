import re

"""
Classe destinée à accueillir les fonctionnalités de decodage des string INIT et STATE
"""
class Decodage:
	"""
	Utilisation : 
	1) Creation d'un objet Decodage avec comme parametre la string a decoder
	2) La fonction __init__ se charge d'identifier le type de message a decoder
	3) On traite la chaine de caractere et on les stock dans un tableau

	ex : state = Decodage(state)
	state.state["method"] contient le nom de la methode 
	state.state["match_id"] contient l'identifiant du match
	...
	"""
	def __init__(self, toDecode):
		self.toDecode = toDecode		
		self.state = {}
		self.decodage_state(self.toDecode)
		
	def __str__(self):
		if self.state is not None:
			return str(self.state["method"] + "\n" + self.state["match_id"] + "\n" + self.state["nbPlayers"] + "\n" + str(self.state["cells"]) + "\n" +str(self.state["moves"]))

	"""
	Fonction d'affichage du contenu d'un dictionnaire
	"""
	def print_dict(dico):
		for key, value in dico.items():
			print(key, " : ", value)

	"""
	Fonction de decodage de la partie identification d'une chaine STATE
	"""
	def decodage_state(self, string):
		#Partie invariante tout au long de la partie on peut le sauvegarder une seule fois
		methode = re.search(r"(STATE)(.+?)IS([0-9]);", string)
		if methode is not None:
			self.state["method"]  = methode.group(1)
			self.state["match_id"] = methode.group(2)
			self.state["nbPlayers"] = methode.group(3)

		

		cells = []
		infos = re.search(r"([0-9]CELLS)([:,]?[0-9]\[[-]?[0-9]*\][0-9]*'[0-9]*[,]?)*", string)
		if infos is not None:
			complete = infos.group(0)
			first = complete.split(':')[1]
			second = first.split(',')

			for i in second:
				tmp = []
				cell = re.search(r"([0-9]*)\[([-]?[0-9]*)\]([0-9]*)'([0-9]*)", i)
				tmp.append(cell.group(1))
				tmp.append(cell.group(2))
				tmp.append(cell.group(3))
				tmp.append(cell.group(4))
				cells.append(tmp)
			self.state["cells"] = cells

		toAdd = ""
		moves = []
		initial = re.search(r"([0-9]*MOVES:)(([0-9]*[<>][0-9]*\[[-]?[0-9]\]@[0-9]*['][0-9]*)*[,]*)*", string)
		if initial is not None:
			premier_decoupage = initial.group(0).split(':')[1]
			inter = premier_decoupage.split(',')
			for element in inter:
				un = re.search(r"^[0-9]*", element)
				cellule_debut = un.group(0)

				last = re.search(r"[0-9]*$", element)
				cellule_fin = last.group(0)

				move = re.findall(r"[<>][0-9]*\[[0-9]\]@[0-9]*", element)
				if move is not None:
					for i in move:
						toAdd = []
						meta = re.search(r"([<>])([0-9]*)\[([0-9]*)\](@[0-9]*)", i)
						if meta is not None:
							if(meta.group(1) == "<"):
								toAdd.append(cellule_fin)
								toAdd.append(cellule_debut)
								toAdd.append(meta.group(2))
								toAdd.append(meta.group(3))
								toAdd.append(meta.group(4))
							else:
								toAdd.append(cellule_debut)
								toAdd.append(cellule_fin)
								toAdd.append(meta.group(2))
								toAdd.append(meta.group(3))
								toAdd.append(meta.group(4))
							moves.append(toAdd)
			self.state["moves"] = moves
		else:
			self.state["moves"] = 0

if __name__ == '__main__':
	nul = ""
	vide = Decodage(nul)
	print(vide.state)

	string = "STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]33'6;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3"

	obj = Decodage(string)
	print(obj.state)

	deux = "STATEee3c9806-5a88-496e-9964-18db09ce575eIS2;7CELLS:0[0]6'1,1[-1]6'0,2[-1]6'0,3[-1]12'0,4[-1]6'0,5[-1]6'0,6[1]6'1;0MOVES"

	snd = Decodage(deux)
	print(snd.state)
