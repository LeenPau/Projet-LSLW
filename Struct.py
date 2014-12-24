# -*- coding: utf-8 -*-

class Cellule :

    """
    Fonction d'initialisation de la classe Cellule

    @param name (chaine de caractères) : le nom de la cellule (pour l'affichage)
    
    @param player (entier) : le joueur qui possède la cellule, 0 si neutre
    
    @param nbUnit_Off (entier) : le nombre d'unité offensive que possède la cellule
    @param capacity_Off (entier) : le nombre maximal d'unité offensive que peut contenir la cellule
    @param prodRate_Off (entier) : la cadence de production d'unité offensive de la cellule
        (initialisée à 0 par défaut, car une cellule neutre ne produit pas d'unité)

    @param nbUnit_Def (entier) : le nombre d'unité defensive que possède la cellule
    @param capacity_Def (entier) : le nombre maximal d'unité defensive que peut contenir la cellule
    @param prodRate_Def (entier) : la cadence de production d'unité defensive de la cellule
        (initialisée à 0 par défaut, car une cellule neutre ne produit pas d'unité)
    
    """
    def __init__(self,
                 name,
                 player = 0,
                 nbUnit_Off = 0, capacity_Off = 0, prodRate_Off = 0,
                 nbUnit_Def = 0, capacity_Def = 0, prodRate_Def = 0
                 ) :

        self.name = name # pour l'affichage (voir fonction " __str__(self) : "
        
        self.player = player
        
        self.nbUnit_Off     = nbUnit_Off
        self.capacity_Off   = capacity_Off
        self.prodRate_Off   = prodRate_Off
        
        self.nbUnit_Def     = nbUnit_Def
        self.capacity_Def   = capacity_Def
        self.prodRate_Def    = prodRate_Def


    """
    Fonction d'affichage par défaut de la classe Cellule
    """
    def __str__(self) :
        return self.name \
               + "\nUnité offensive : " + str(self.nbUnit_Off) + "/" + str(self.capacity_Off) + "\t Cadence de production : " + str(self.prodRate_Off) \
               + "\nUnité défensive : " + str(self.nbUnit_Def) + "/" + str(self.capacity_Def) + "\t Cadence de production : " + str(self.prodRate_Def) \
               + "\n"

    """
    Fonction de mise à jour de l'attribut name d'une Cellule
    @param name (string) : nouveau nom de la cellule
    """
    def setName(self, name):
        self.name = name

    """
    Fonction de mise à jour de l'attribut player d'une Cellule
    @param player (string) : nouveau propriétaire de la cellule
    """
    def setPlayer(self, player):
        self.player = player

    """
    Fonction de mise à jour de l'attribut nbUnit_Off d'une Cellule
    @param nb (int) : nouveau nombre d'unités offensives de la cellule
    """
    def setNbUnitOff(self, nb):
        self.nbUnit_Off = nb

    """
    Fonction de mise à jour de l'attribut capacity_Off d'une Cellule
    @param capacity (int) : nouvelle capacité offensive de la cellule
    """
    def setCapacityOff(self, capacity):
        self.capacity_Off = capacity
    """
    Fonction de mise à jour de l'attribut prodRate d'une Cellule
    @param prodRate (int) : nouveau taux de production de la cellule
    """
    def setProdRateOff(self, prodRate):
        self.prodRate_Off = prodRate

    """
    Fonction de mise à jour de l'attribut nbUnit_Def d'une Cellule
    @param nb (string) : nouveau nombre d'unités défensives de la cellule
    """
    def setNbUnitDef(self, nb):
        self.nbUnit_Def = nb

    """
    Fonction de mise à jour de l'attribut capacity_Def d'une Cellule
    @param capacity (string) : nouveau nombre maximal d'unités défensives de la cellule
    """
    def setCapacityDef(self, capacity):
        self.capacity_Def = capacity

    """
    Fonction de mise à jour de l'attribut name d'une Cellule
    @param name (string) : nouveau nom de la cellule
    """
    def setProdRateDef(self, prodRate):
        self.prodRate_Def = prodRate


class Terrain :
    """
    Fonction d'initialisation de la classe Terrain (graphe)
    
    @param cellules (dictionnaire python) : contient les cellules du terrain ainsi que leurs caractéristiques
    @param liste_adjacence (dictionnaire python) : contient la liste d'adjacence du terrain
        
    """
    def __init__(self, cellules = {}, liste_adjacence = {}) :
        self.cellules = cellules
        self.liste_adjacence  = liste_adjacence
        self.size = len(self.cellules)

    def __str__(self) :
        chaine = ""
        i = 1
        while i <= len(self.liste_adjacence) :
            chaine_voisins = ""
            for voisins in self.liste_adjacence[i] :
                chaine_voisins += (voisins.name + "; ")
            chaine += (str(self.cellules[i]) + "Liste des voisins : " + chaine_voisins + "\n\n")
            i += 1
        return chaine

def main() :
    c1 = Cellule(name = "1", player = 1, nbUnit_Off = 0, capacity_Off = 10, prodRate_Off = 3, nbUnit_Def = 0, capacity_Def = 10, prodRate_Def = 1)
    c2 = Cellule(name = "2")
    c3 = Cellule(name = "3")
    c4 = Cellule(name = "4")
    c5 = Cellule(name = "5")
    c6 = Cellule(name = "6")
    c7 = Cellule(name = "7", player = 2, nbUnit_Off = 0, capacity_Off = 10, prodRate_Off = 3, nbUnit_Def = 0, capacity_Def = 10, prodRate_Def = 1)
    
    cellules = {
        1 : c1,
        2 : c2,
        3 : c3,
        4 : c4,
        5 : c5,
        6 : c6,
        7 : c7
    }
    liste_adjacence = {
        1 : [c2, c4],
        2 : [c1, c3, c4],
        3 : [c2, c5],
        4 : [c1, c2, c5, c6],
        5 : [c3, c4, c7],
        6 : [c4, c7],
        7 : [c5, c6]
    }


    
    terrain = Terrain(cellules, liste_adjacence)
    
    print(terrain)

if __name__ == '__main__' :
    main()
