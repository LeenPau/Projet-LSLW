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
		
		if(toDecode.contains("STATE")):
			self.state = {}

			tmp = state_beg(string)
			self.state["method"] = tmp[0]
			self.state["match_id"] = tmp[1]
			self.state["nbPlayers"] = tmp[2]

			cells = state_cells(string)
			self.state["cells"] = cells

			moves = state_moves(string)
			self.state["moves"] = moves

	def __str__(self):
		return str(self.state["method"] + "\n" + self.state["match_id"] + "\n" + self.state["nbPlayers"] + "\n" + self.state["cells"] + "\n" +self.state["moves"])

	"""
	Fonction d'affichage du contenu d'un dictionnaire
	"""
	def print_dict(dico):
		for key, value in dico.items():
			print(key, " : ", value)

	"""
	Fonction de decodage de la partie identification d'une chaine STATE
	"""
	def state_beg(string):
		"""
		Decodage de la première partie de la string STATE
		"""
		methode = re.search(r"(STATE)(([0-9]{2})(([a-z0-9]{4,}[-;]*){5}))IS([0-9]);", string)
		method = methode.group(1)
		match_id = methode.group(2)
		nbPlayers = methode.group(6)
		return (method, match_id, nbPlayers)

	"""
	Fonction de decodage de la partie CELLS de la string STATE
	"""
	def state_cells(string):
		cells = []
		infos = re.search(r"([0-9]CELLS)([:,]?[0-9]\[[0-9]*\][0-9]*'[0-9]*[,]?)*", string)
		complete = infos.group(0)
		first = complete.split(':')[1]
		second = first.split(',')

		for i in second:
			cell = re.search(r"([0-9]*)\[([0-9]*)\]([0-9]*)'([0-9]*)", i)
			tmp = cell.group(1)+","+cell.group(2)+","+cell.group(3)+","+cell.group(4)
			cells.append(tmp)
		return cells

	"""
	Fonction de decodage de la partie MOVES de la string STATE
	"""
	def state_moves(string):
		toAdd = ""
		moves = []
		initial = re.search(r"([0-9]MOVES:)(([0-9]*[<>][0-9]*\[[0-9]\]@[0-9]*['][0-9]*)*[,]*)*", string)
		premier_decoupage = initial.group(0).split(':')[1]
		inter = premier_decoupage.split(',')

		for element in inter:
			un = re.search(r"^[0-9]*", element)
			cellule_debut = un.group(0)

			last = re.search(r"[0-9]*$", element)
			cellule_fin = last.group(0)

			move = re.findall(r"[<>][0-9]*\[[0-9]\]@[0-9]*", element)

			for i in move:
				meta = re.search(r"([<>])([0-9]*)\[([0-9]*)\](@[0-9]*)", i)

				if(meta.group(1) == "<"):
					toAdd = cellule_fin+","+meta.group(1)+","+cellule_debut+","+meta.group(2)+","+meta.group(3)+","+meta.group(4)
				else:
					toAdd = cellule_debut+","+meta.group(1)+","+cellule_fin+","+meta.group(2)+","+meta.group(3)+","+meta.group(4)
				moves.append(toAdd)
		return moves

	"""
	Fonction de constitution et d'affichage des informations d'une string STATE
	"""
	def decode_state(string):
		"""
		STATE<matchid>IS<#players>;<#cells>CELLS:<cellid>[<owner>]<offunits>'<defunits>,...;\
		<#moves>MOVES:<cellid><direction><#units>[<owner>]@<timestamp>'...<cellid>,...

		STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]33'6;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3
		"""

		#Définition du dictionnaire de stockage des informations
		state = {}

		tmp = state_beg(string)
		state["method"] = tmp[0]
		state["match_id"] = tmp[1]
		state["nbPlayers"] = tmp[2]

		cells = state_cells(string)
		state["cells"] = cells

		moves = state_moves(string)
		state["moves"] = moves


		#affichage du dictionnaire
		print_dict(state)