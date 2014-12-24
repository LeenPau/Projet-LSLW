# -*- coding: utf-8 -*-

"""
Robot-joueur de Pooo
    
Le module fournit les fonctions suivantes :
    register_pooo(uid)
    init_pooo(init_string)
    play_pooo()        
"""

__version__='0.1'
 
## chargement de l'interface de communication avec le serveur

from poooc import order, state, state_on_update, etime # import des fonctions de poooc
import logging # mieux que des print partout
import inspect # pour faire de l'introspection
from Decodage import Decodage #classe de Decodage des chaines de caractères
from Struct import *
from Game import *


"""
Inscrit un joueur et initialise le robot pour la compétition

:param uid: identifiant utilisateur
:type uid:  chaîne de caractères str(UUID) 
    
:Example:
    
"0947e717-02a1-4d83-9470-a941b6e8ed07"
"""
def register_pooo(uid):
    logging.info('Entering register_pooo function...')
    #Decoder uid
    #Stocker l'identifiant utilisateur dans la structure de données
    global game
    game = Game()
    game.setUid(uid)


"""
Initialise le robot pour un match    

:param init_string: instruction du protocole de communication de Pooo (voire ci-dessous)
:type init_string: chaîne de caractères (utf-8 string)

:Example:
    
"INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"
"""
def init_pooo(init_string):
    logging.info('Entering the init_pooo function...')
    #Récupérer la chaine de caractères init_string et la décoder 
    #initialiser la structure de données (création du graphe)
    init = decodage_init(init_string)
    """
    (
    'a8fc1dc8-4fc5-49c1-bac5-075b0b5c8540', '2', '1', '2',
    '7',   Nombre de cellules
    {
        0: {'cellid': '0', 'offsize': '30', 'y': '0', 'radius': '100', 'defsize': '8', 'prod': 'I', 'x': '0'}, 
        1: {'cellid': '1', 'offsize': '30', 'y': '5', 'radius': '100', 'defsize': '8', 'prod': 'I', 'x': '0'}, 
        2: {'cellid': '2', 'offsize': '30', 'y': '0', 'radius': '100', 'defsize': '8', 'prod': 'I', 'x': '5'}, 
        3: {'cellid': '3', 'offsize': '30', 'y': '5', 'radius': '200', 'defsize': '8', 'prod': 'II', 'x': '5'}, 
        4: {'cellid': '4', 'offsize': '30', 'y': '10', 'radius': '100', 'defsize': '8', 'prod': 'I', 'x': '5'}, 
        5: {'cellid': '5', 'offsize': '30', 'y': '5', 'radius': '100', 'defsize': '8', 'prod': 'I', 'x': '10'}, 
        6: {'cellid': '6', 'offsize': '30', 'y': '10', 'radius': '100', 'defsize': '8', 'prod': 'I', 'x': '10'}
    }, 
    {
        0: {'cellid2': '2', 'distance': '4800', 'cellid1': '0'}, 
        1: {'cellid2': '1', 'distance': '4800', 'cellid1': '0'}, 
        2: {'cellid2': '3', 'distance': '4700', 'cellid1': '2'}, 
        3: {'cellid2': '4', 'distance': '4700', 'cellid1': '3'}, 
        4: {'cellid2': '6', 'distance': '4800', 'cellid1': '4'}, 
        5: {'cellid2': '6', 'distance': '4800', 'cellid1': '5'}
    }
    )
    """
    game.setMatchId(init[0]) #Identifiant de la partie
    game.setNbPlayers(init[1]) #Nombre de joueurs de la partie
    game.setPersonalNumber(init[2]) #Identifiant du joueur
    game.terrain = Terrain()

    #Parcours de cellules
    cells = init[5]
    for ID,cell in cells.items():
        game.terrain.cellules[cell["cellid"]] = Cellule(name = ID,
                                                        capacity_Off = cell["offsize"],
                                                        prodRate_Off = cell["prod"],
                                                        capacity_Def = cell["defsize"],
                                                        prodRate_Def = 1)
        game.terrain.liste_adjacence[cell["cellid"]] = []
    
    liste_adj = init[6]
    for ID,cell in liste_adj.items():
        tmp = cell["cellid2"]    
        game.terrain.liste_adjacence[tmp].append(game.terrain.cellules[cell["cellid1"]])

    print(game.terrain.cellules)
 
    
"""
Active le robot-joueur
"""
def play_pooo():
    logging.info('Entering play_pooo fonction from {} module...'.format(inspect.currentframe().f_back.f_code.co_filename))
    ### Début stratégie joueur ### 
    # séquence type :
    # (1) récupère l'état initial
    # (2) TODO: traitement de init_state (e.g mise à jour de la structure de données avec l'état initial)
    # (3) while True : mise en place de la stratégie ICI
    
    while True :

        # (4) state = state_on_update()    
        state = state_on_update()

        # Decodage
        decode = decodage_state(state)
        
        #Parcours des informations obtenues
        moves = decode[4]
        cells = decode[3]
        
        #Mise à jour de la structure / INFOS MOVES
        if(moves != 0):
            for move in moves:
                print("init : ",move[0] , " finale : ", move[1], " nbUnits : ", move[2], "joueur : ", move[3], "timestamp : ", move[4])

        #Mise à jour de la structure / INFOS CELLS
        if(cells is not None):
            for cell in cells:
                game.terrain.cellules[cell[0]].player = cell[1]
                game.terrain.cellules[cell[0]].nbUnit_Off = cell[2]
                game.terrain.cellules[cell[0]].nbUnit_Def = cell[3]

                print("cellule : ", cell[0], "joueur : ", cell[1], "unitOff : ", cell[2], "unitDef : ", cell[3])


        # (5) TODO: traitement de state et transmission d'ordres order(msg)


    