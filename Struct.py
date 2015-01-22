# -*- coding: utf-8 -*-
class Cellule() :

    """
    Initialise une cellule

    @param data : informations sur les cellules et obtenues grâce à la chaine d'initialisation qui a été récupérée puis parsée
    @param aretes : informations sur les voisins de chaque cellule 

    """

    
    def __init__(self, data, aretes) :
        
        self.cellid     = data['cellid']
        self.x          = data['x']
        self.y          = data['y']
        self.radius     = data['radius']
        self.player     = -1 # par défaut, la cellule est neutre
        
        self.offunits   = 0
        self.offsize    = data['offsize']
        self.offprod    = data['prod']
        
        self.defunits   = 0
        self.defsize    = data['defsize']
        self.defprod    = 1 # valeur unique pour chaque cellule

        self.neighbours = {}
        
        for arete in aretes :
            # Si la cellule est concernée, il y a deux cas possibles :
            # soit la cellule est en première position          
            if arete['cellid1'] == self.cellid :
                self.neighbours[arete['cellid2']] = arete['distance']

            # soit elle est en deuxième position
            if arete['cellid2'] == self.cellid :
                self.neighbours[arete['cellid1']] = arete['distance']


    def update(self, data) :
        self.defunits = data['defunits']
        self.offunits = data['offunits']
        self.player = data['owner']

    def __str__(self):
        return str(self.cellid) + "owner : " + str(self.player) + "\nUnité offensive : " + str(self.offunits) + "/" + str(self.offsize) + " \tCadence de production : " + str(self.offprod) + "\nUnité défensive : " + str(self.defunits) + "/" + str(self.defsize) + " \tCadence de production : " + str(self.defprod)

class Match():

    def __init__(self, data) :

        """ Initialise un match """

        self.matchid    = data['matchid']
        self.nbPlayers  = data['nbPlayers']
        self.me         = data['me']
        self.speed      = data['speed']
        
        self.cellules = {}
        self.moves_history = {}

        # Pour chaque cellule récupérée en décodant la chaine d'initialisation,
        # on crée un dictionnaire contenant des cellules et dont les clés sont les cellid des cellules.
        
        for cellule in data['cellules'] :
            self.cellules[cellule['cellid']] = Cellule(cellule, data['aretes'])
