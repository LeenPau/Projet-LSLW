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
from parsage import *
from sdd import *
from random import randint
from topologie import *


"""
Inscrit un joueur et initialise le robot pour la compétition

:param uid: identifiant utilisateur
:type uid:  chaîne de caractères str(UUID) 
    
:Example:
    
"0947e717-02a1-4d83-9470-a941b6e8ed07"
"""
def register_pooo(uid):
    logging.info('Entering register_pooo function...')
    global identifiant
    identifiant = uid

"""
Initialise le robot pour un match    

:param init_string: instruction du protocole de communication de Pooo (voire ci-dessous)
:type init_string: chaîne de caractères (utf-8 string)

:Example:
    
"INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"
"""
def init_pooo(init_string):
    data_init = decodage_init(init_string)

    global m
    m = Match(data_init)

    for cell in m.cellules.values() :
        print(cell.neighbours)

    
"""
Active le robot-joueur
"""
def play_pooo():
    logging.info('Entering play_pooo fonction from {} module...'.format(inspect.currentframe().f_back.f_code.co_filename))
    while True :
        msg=state_on_update()
        if 'STATE' in msg:
            logging.debug('[play_pooo] Received state: {}'.format(msg))
            data_state = decodage_state(msg)
            
            cells = data_state['cells'] #informations sur les cellules
            moves = data_state['moves'] #informations sur les mouvements

            #Mise à jour de la structure / INFOS MOVES
            if cells != 0:
                for cellule in cells:
                    cell_temp = m.cellules[cellule['cellid']]
                    cell_temp.update(cellule)

            if moves != 0:
                for move in moves:
                    time = etime()
                    m.moves_history[time] = move

        elif 'GAMEOVER' in msg: # on arrête d'envoyer des ordres. On observe seulement...
            order ('[{}]GAMEOVEROK'.format(identifiant))
            logging.debug('[play_pooo] Received game over: {}'.format(msg))
        elif 'ENDOFGAME' in msg: # on sort de la boucle de jeu
            logging.debug('[play_pooo] Received end of game: {}'.format(msg))
            break
        else:
            logging.error('[play_pooo] Unknown msg: {!r}'.format(msg))
    logging.info('>>> Exit play_pooo function')
            