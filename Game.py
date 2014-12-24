# -*- coding: utf-8 -*-

from Struct import *
import re

"""
Classe chargée d'abstraire le fonctionnement d'une partie, elle va contenir les informations concernant la partie
de manière à ce qu'on puisse y accéder de manière centralisée

@param terrain (Terrain) : graphe contenant les cellules représentant le terrain de jeu d'une partie

@param uid (string) : Chaine de caractères identifiant l'utilisateur aucours de la partie

@param match_id (string) : Chaine de caractère identifiant la partie en elle-même

@param nbPlayers (int) : Nombre de joueurs dans la partie en cours

"""
class Game:
	def __init__(self, terrain = None, uid = None, match_id = None, nbPlayers = None, personalNumber = None):
		self.terrain = terrain
		self.uid = uid
		self.match_id = match_id
		self.nbPlayers = nbPlayers
		self.personalNumber = personalNumber

	"""
	Fonction de mise à jour de l'identifiant d'une partie
	"""
	def setUid(self, newUid):
		self.uid = newUid

	"""
	Fonction de mise à jour du terrain
	"""
	def setTerrain(self, newTerrain):
		self.terrain = newTerrain

	"""
	Fonction de mise à jour de l'identifiant de la partie
	"""
	def setMatchId(self, newMatchId):
		self.match_id = newMatchId

	"""
	Fonction de mise à jour du nombre de joueurs de la partie
	"""
	def setNbPlayers(self, nbPlayers):
		self.nbPlayers = nbPlayers

	"""
	Fonction de mise à jour du nombre de joueurs de la partie
	"""
	def setPersonalNumber(self, nb):
		self.personalNumber = nb

def decodage_init(init_string) :
    #init_string = "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"

    # On commence par diviser la chaine en plusieurs parties, chacunes des parties étant séparées par un ";"
    parties = re.split(';', init_string)

    chaine_decodee = {}

    
    """
    ----------------------------------------------------------------------------
    On traite la première partie de la chaine

    INIT<matchid>TO<#players>[<me>];
    ----------------------------------------------------------------------------
    """
    decodagePartie1 = re.search(r'INIT(.+)TO([0-9]+)\[([0-9]+)\]', parties[0])
    if decodagePartie1 :
        matchid = decodagePartie1.group(1)
        nbPlayer = decodagePartie1.group(2)
        me = decodagePartie1.group(3)




    """
    ----------------------------------------------------------------------------
    On traite la deuxième partie de la chaine

    <speed>;
    ----------------------------------------------------------------------------
    """
    speedi = parties[1]
    if speedi :
        speed = speedi



    """
    ----------------------------------------------------------------------------
    On traite la troisième partie de la chaine
    
    <#cells>CELLS:<cellid>(<x>,<y>)'<radius>'<offsize>'<defsize>'<prod>,...;
    ----------------------------------------------------------------------------
    """
    nbCELLS = re.search(r'([0-9]+)CELLS', parties[2])
    if nbCELLS :
        nbCELLS = nbCELLS.group(1)


    # cellulesBruts = liste contenant les infos sur chacunes des cellules, mais sous un format brut
    cellulesBruts = re.findall(r'[0-9]+\([0-9]+,[0-9]+\)\'[0-9]+\'[0-9]+\'[0-9]+\'I+', init_string)

    # cellulesDecodees = cellulesBruts + traitement des données
    cellulesDecodees = {}
    i = 0
    
    for i in range(len(cellulesBruts)) :
        # rappel : <cellid>(<x>,<y>)'<radius>'<offsize>'<defsize>'<prod>
        decodageCellules = re.search(r'([0-9]+)\(([0-9]+),([0-9]+)\)\'([0-9]+)\'([0-9]+)\'([0-9])\'(I+)', cellulesBruts[i])
        
        if decodageCellules :
            celluleEnCours = {}
            celluleEnCours['cellid']    = decodageCellules.group(1)
            celluleEnCours['x']         = decodageCellules.group(2)
            celluleEnCours['y']         = decodageCellules.group(3)
            celluleEnCours['radius']    = decodageCellules.group(4)
            celluleEnCours['offsize']   = decodageCellules.group(5)
            celluleEnCours['defsize']   = decodageCellules.group(6)
            celluleEnCours['prod']      = decodageCellules.group(7)

            cellulesDecodees[i] = celluleEnCours

    cellules = cellulesDecodees




    """
    ----------------------------------------------------------------------------
    On traite la dernière partie de la chaine

    <#lines>LINES:<cellid>@<dist>OF<cellid>,...
    ----------------------------------------------------------------------------
    """
    nbLINES = re.search(r'([0-9]+)LINES', parties[3])
    if nbLINES :
        nbLINES = nbLINES.group(1)


    # aretesBruts = liste contenant les infos sur chacunes des aretes, mais sous un format brut
    aretesBruts = re.findall(r'[0-9]+@[0-9]+OF[0-9]+', init_string)

    # aretesDecodees = aretesBruts + traitement des données
    aretesDecodees = {}
    i = 0
    
    for i in range(len(aretesBruts)) :
        # rappel : <cellid>@<dist>OF<cellid>
        decodageAretes = re.search(r'([0-9]+)@([0-9]+)OF([0-9]+)', aretesBruts[i])
        
        if decodageAretes :
            areteEnCours = {}
            areteEnCours['cellid1']     = decodageAretes.group(1)
            areteEnCours['distance']    = decodageAretes.group(2)
            areteEnCours['cellid2']     = decodageAretes.group(3)

            aretesDecodees[i] = areteEnCours

    aretes = aretesDecodees


    return (matchid, nbPlayer, me, speed, nbCELLS, cellules, aretes)

"""
Fonction de parsage de la chaine de caractère STATE

@param string (string) : Chaine de caractère à parser

@return : tuple contenant les valeurs extraites de la chaine de caractère
"""
def decodage_state(string):
		#Initialisation
		cells = []
		moves = []

		#Partie invariante tout au long de la partie on peut le sauvegarder une seule fois
		methode = re.search(r"(STATE)(.+?)IS([0-9]);", string)
		if methode is not None:
			method  = methode.group(1)
			match_id = methode.group(2)
			nbPlayers = methode.group(3)

		#======================================================================================================

		#Parsage de la partie CELLS
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

		#======================================================================================================

		#Parsage de la partie MOVES 
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
		else:
			moves = 0

		#======================================================================================================

		return (method, match_id, nbPlayers, cells, moves)