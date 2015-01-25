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
from struct import *
from random import randint
from topologie import dijkstra, set_rang


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
    aide = {}

    #Initialise le dictionnaire d'aide pour toutes les cellules à 0 (il va servir à déterminer les cellules ayant besoin d'aide pour contenir une attaque)
    for cellule in m.cellules.values():
        aide[cellule.cellid] = 0

    while True:
        msg=state_on_update()
        if 'STATE' in msg:
            logging.debug('[play_pooo] Received state: {}'.format(msg))
            data_state = decodage_state(msg)
            
            cells = data_state['cells'] #informations sur les cellules
            moves = data_state['moves'] #informations sur les mouvements

            #Mise à jour des informations concernant les cellules en fonction du state reçu
            if cells != []:
                for cellule in cells:
                    cell_temp = m.cellules[cellule['cellid']]
                    cell_temp.update(cellule)
            
            #Mise à jour de la structure en fonction des moves reçus
            if moves != []:
                for move in moves:
                    time = etime()
                    m.moves_history[time] = move

            #Affichage de toutes les cellules
            for key,value in m.cellules.items():
                print(value)
                print("cellule : ", key, "voisins : ", value.neighbours)


            #On crée un dictionnaire qui va servir à appliquer l'algorithme de dijkstra et ainsi déterminer les rangs des différentes cellules
            matrice = {}
            for key,value in m.cellules.items():
                matrice[key] = value.neighbours

            #création d'un tableau des cellules alliées
            ally = []
            for cle,cellule in m.cellules.items():
                if cellule.player == m.me:
                    ally.append(cle)
            print("ally : ", ally)

            #création d'un tableau des cellules ennemies
            ennemy = []
            for cle,cellule in m.cellules.items():
                if (cellule.player != m.me and cellule.player != -1):
                    ennemy.append(cle)
            print("ennemy : ", ennemy)
            
            # (5) TODO: traitement de state et transmission d'ordres order(msg) 
            rangs = {}
            fronts, ravitailleurs = {}, {}

            #Mise à jour du rang de toutes les cellules alliées
            for c_alliee in ally:
                rang_minimum = -1
                for c_ennemie in ennemy:
                    if (set_rang(c_alliee, c_ennemie, matrice) < rang_minimum) or (rang_minimum == -1):
                        rang_minimum = set_rang(c_alliee, c_ennemie, matrice)
                        rangs[c_alliee] = rang_minimum

            #En fonction du rang qui leur est affecté, les cellules divisées en deux catégories 
            #Les ravitailleurs : qui ne sont pas au contact des ennemies
            #Les fronts : qui sont à exactement 1 "saut" d'un ou plusieurs ennemis
            for cellule, rang in rangs.items():
                if rang == 1:
                    fronts[cellule] = rang
                else:
                    ravitailleurs[cellule] = rang

            #Affichage des cellules du front
            for cellule_front,rang in fronts.items():
                print("fronts : ", cellule_front, " rang : ", rang)

            #Affichage des cellules ravitailleuses
            for cellule_ravit,rang in ravitailleurs.items():
                print("ravitailleurs : ", cellule_ravit, " rang : ", rang)


            """
            =====================================================================================================================
                        ======================================= STRATEGIE =======================================
            =====================================================================================================================
            """
            # on commence par les cellules du front pour savoir si elles ont besoins d'aides avant de commencer à gérer les cellules ravitailleuses
            for cellule in fronts.keys() :
                est_attaque = False
                max_temps = 0 
                nb_attaquants = 0

                # On cherche si il y a des déplacements offensifs vers la cellule considérée
                for move in moves :
                    if (move['destination'] == cellule) and (move['owner'] != m.me) : # On cherche si il y a des déplacements aggressifs vers notre cellule
                        est_attaque == True
                        nb_attaquants += move.nbUnits # si c'est le cas, on compte le nombre d'attaquants total

                        #max_temps, on regarde si on arrive à stopper toutes les attaques, on prend l'attaquant le plus éloigné pour le calcul
                        if move['timestamp'] > max_temps :
                            max_temps = move['timestamp']


                if est_attaque == True : # si je suis attaqué.
                    capacite_reception = (m.cellules[cellule].offunits + m.cellules[cellule].defunits + (max_temps * m.cellules[cellule].offprod) )
                    if capacite_reception < nb_attaquants : # les attaquants sont plus forts
                        # Il faut demander de l'aide : la différence entre les attaquants et la capacité de reception + 1
                        aide[cellule] = ( nb_attaquants - (m.cellules[cellule].offunits + m.cellules[cellule].defunits + (max_temps * m.cellules[cellule].offprod) ) +1 )
                        
                    elif capacite_reception + 1 > nb_attaquants : # On est plus fort, on peut utiliser le surplus pour attaquer
                        # il y a au moins 2 unités, d'où le "+ 1" :
                        # une pour garder le controle de la cellule
                        # et une autre au minimum pour faire une attaque

                        # On détermine la cellule la plus rentable
                        target = 100000000
                        d = 0

                        #enlever les cellules alliées lors du parcours
                        for cel,distance in m.cellules[cellule].neighbours.items():
                            if (target > (distance + m.cellules[cel].offunits + m.cellules[cel].defunits) * m.cellules[cel].coeff) and m.cellules[cel].player != m.me:
                                target = (distance + m.cellules[cel].offunits + m.cellules[cel].defunits) * m.cellules[cel].coeff
                                cible = cel
                                d = distance
                        
                        print("target : ", target, " / cible", cible)
                        
                        envoi = (capacite_reception + 1) - nb_attaquants

                        # order avec comme pourcentage : envoi/cellule.offunits
                        toSend = round((envoi / m.cellules[cellule].offunits)*100)
                        order_string = "[" + str(identifiant) + "]MOV" + str(toSend) + "FROM" + str(cellule) + "TO" + str(cible)
                        print("order string : ", order_string)
                        order(order_string)
                    
                    else : # égalite, mais il faut au moins 1 de plus pour garder la cellule
                        aide[cellule.cellid] = 1
                        


                else : # je ne suis pas attaqué donc j'attaque le plus rentable
                    target = 100000000
                    d = 0

                    #enlever les cellules alliées lors du parcours
                    for cel,distance in m.cellules[cellule].neighbours.items():
                        if (target >= (distance + m.cellules[cel].offunits + m.cellules[cel].defunits) * m.cellules[cel].coeff) and m.cellules[cel].player != m.me:
                            target = (distance + m.cellules[cel].offunits + m.cellules[cel].defunits) * m.cellules[cel].coeff
                            cible = cel
                            d = distance
                    
                    print("target : ", target, " / cible", cible)
                    
                    envoi = m.cellules[cellule].offunits -1

                    # order avec comme pourcentage : envoi/cellule.offunits
                    toSend = round((envoi / m.cellules[cellule].offunits)*100)
                    order_string = "[" + str(identifiant) + "]MOV" + str(toSend) + "FROM" + str(cellule) + "TO" + str(cible)
                    print("order string : ", order_string)
                    order(order_string)
                #Appel à order : ici --> constituer la string pour pouvoir l'envoyer ensuite


            # On gère maintenant les cellules dont le rôle est de ravitailler
            # On commence par les plus éloignées, comme ca une fois qu'elles ont envoyées leurs unités, les cellules du rang juste en dessous peuvent prendre en compte cela
            max_rang = 0
            min_rang = 10000
            for cell, rang in ravitailleurs.items():
                max_rang = max(max_rang,rang)
                min_rang = min(min_rang,rang)

            rang_en_cours = max_rang
            cellules_en_cours = []

            while rang_en_cours >= min_rang :
                for cellule, rang in ravitailleurs.items() :
                    if rang == rang_en_cours :
                        cellules_en_cours.append(cellule)

                #Pour toutes les cellules du rang en cours
                for cellule in cellules_en_cours :
                    calme = True # il n'y a pas de demande d'aide

                    for cel_id, nb_units in aide.items():
                        if (nb_units != 0):
                            calme = False

                    if calme == False : # on doit aider
                        #choisir laquelle cellule aider
                        #   - envoyer à la voisine la plus proche, qui elle meme enverra à la voisine la plus proche ? parait bien, on ravitaille plus vite
                        #   - envoyer à la plus grosse demande ? peut etre dangereux s'il y a pleins de cellules, on pourrait ne sauver que celle avec la plus grosse demande
                        #       et perdre toutes celles avec des petites demandes
                        #   - envoyer vers les plus petites demandes => on pourrait en sauver plus
                        #   => tenir compte dans tous les cas de la production des cellules attaquées aussi
                        
                        #on récupère les id de cellules qui ont besoin d'aide
                        toHelp = []
                        for cle, help in aide.items():
                            if help > 0:
                                toHelp.append(cle)

                        for cel in toHelp:
                            pred = dijkstra(cellule, cel, matrice)
                            cible = pred[cellule]
                            if aide[cel] > (m.cellules[cellule].offunits - 1):
                                envoi = round((m.cellules[cellule].offunits - 1 / m.cellules[cellule].offunits)*100)
                            order_string = "[" + str(identifiant) + "]MOV" + str(toSend) + "FROM" + str(cellule) + "TO" + str(cible)
                            order(order_string)


                    else : # Pas de demande d'aide
                        # On cherche à savoir si on possède déjà toutes les cellules voisines de la cellule
                        # On a deux choix :
                        #   - si on ne possède pas toutes les voisines, on peut se permettre de les capturer afin d'augmenter notre production
                        #   - soit on ravitaille au front
                        toutes_alliees = True
                        for cel, dist in m.cellules[cellule].neighbours.items() :
                            if m.cellules[cel].player != m.me :
                                toutes_alliees = False

                        #Les cellules voisines ne sont pas toutes alliées
                        if toutes_alliees == False :
                            # On détermine la cellule la plus rentable
                            target = 100000000
                            d = 0

                            #enlever les cellules alliées lors du parcours
                            for cel,distance in m.cellules[cellule].neighbours.items():
                                if (target > (distance + m.cellules[cel].offunits + m.cellules[cel].defunits) * m.cellules[cel].coeff) and m.cellules[cel].player != m.me:
                                    target = (distance + m.cellules[cel].offunits + m.cellules[cel].defunits) * m.cellules[cel].coeff
                                    cible = cel
                                    d = distance
                            
                            if (m.cellules[cible].player == -1):
                                envoi = m.cellules[cellule].offunits -1
                            else:
                                #On détermine les troupes à envoyer
                                max_envoi = int(round(m.cellules[cible].offsize - ( m.cellules[cible].offunits + ( (d * m.cellules[cible].offprod) * m.speed/1000 ) + m.cellules[cible].offprod)))

                                # On regarde cb d'unités on va envoyer en faisant gaffe à ne pas dépasser la capacité maximale d'envoi (max_envoi)
                                if m.cellules[cellule].offunits <= max_envoi :
                                    envoi = m.cellules[cellule].offunits - 1
                                else :
                                    envoi = max_envoi - 1 #par securite, a voir si necessaire 

                            # order avec comme pourcentage : envoi/cellule.offunits
                            toSend = round((envoi / m.cellules[cellule].offunits)*100)
                            order_string = "[" + str(identifiant) + "]MOV" + str(toSend) + "FROM" + str(cellule) + "TO" + str(cible)
                            order(order_string)

                        else :
                            #Si les cellules sont toutes alliées autout de nous : on envoie à la cellule alliée la plus proche et de rang inférieur
                            c_possibles = []
                            for cel, dist in m.cellules[cellule].neighbours.items():
                                c_possibles.append((cel, dist))

                            cible_alliee = -1
                            dist_min = c_possibles[0][1]
                            for cel in c_possibles:
                                if (dist_min >= cel[1] and rangs[cel[0]] < rangs[cellule]):
                                    dist_min = cel[1]
                                    cible_alliee = cel[0]

                            if cible_alliee != -1:
                                # la capacité maximale d'unités offensives que peut avoir la cellule (voisine.cel.offsize)
                                # moins le nombre d'unité offensives déjà présentes (voisine.cel.offunits)
                                # moins la production qu'aura fait la cellule le temps du trajet ( (voisine.dist*voisine.cell.offprod)*m.speed/1000 ) => tiens compte de la vitesse de jeu
                                # moins la production effectuée en 2 sec (pour etre sur de ne pas dépasser la limite et perdre d'unités)
                                #On détermine les troupes à envoyer
                                max_envoi = int(round(m.cellules[cible_alliee].offsize - ( m.cellules[cible_alliee].offunits + ( (d * m.cellules[cible_alliee].offprod) * m.speed/1000 ) + m.cellules[cible_alliee].offprod)))

                                # On regarde cb d'unités on va envoyer en faisant gaffe à ne pas dépasser la capacité maximale d'envoi (max_envoi)
                                if m.cellules[cellule].offunits <= max_envoi :
                                    envoi = m.cellules[cellule].offunits - 1
                                else :
                                    envoi = max_envoi - 1 #par securite, a voir si necessaire 

                                # order avec comme pourcentage : envoi/cellule.offunits
                                toSend = round((envoi / m.cellules[cellule].offunits)*100)
                                order_string = "[" + str(identifiant) + "]MOV" + str(toSend) + "FROM" + str(cellule) + "TO" + str(cible_alliee)
                                order(order_string)
                rang_en_cours -= 1
                cellules_en_cours = [] 

        elif 'GAMEOVER' in msg: # on arrête d'envoyer des ordres. On observe seulement...
            order ('[{}]GAMEOVEROK'.format(identifiant))
            logging.debug('[play_pooo] Received game over: {}'.format(msg))
        elif 'ENDOFGAME' in msg: # on sort de la boucle de jeu
            logging.debug('[play_pooo] Received end of game: {}'.format(msg))
            break
        else:
            logging.error('[play_pooo] Unknown msg: {!r}'.format(msg))
    logging.info('>>> Exit play_pooo function')


    
    