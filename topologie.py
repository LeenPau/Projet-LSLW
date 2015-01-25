# -*- coding: utf-8 -*-

def dijkstra(src, dest, dico_voisins) :
    # Initilisation
    covered = []
    dist = {}
    pred = {}
    for cellule in dico_voisins.keys() :
        if cellule == src :
            dist[cellule] = 0
        else :
            dist[cellule] = -1    
    pivot = src

    
    # Etape fondamentale
    while pivot != dest :
        covered.append(pivot)
        for voisin, distance in dico_voisins[pivot].items() :
            if voisin not in covered :
                if ( (dist[pivot] + distance) < dist[voisin] ) or ( dist[voisin] == -1) :
                    dist[voisin] = (dist[pivot] + distance)
                    pred[voisin] = pivot

        # déterminer le nouveau pivot (le sommet le plus proche du pivot)
        plus_proche = (None, -1)
        for cellule, distance in dist.items() :
            if cellule not in covered :
                if (distance != -1) :
                    if (plus_proche[1] > distance ) or (plus_proche[1] == -1) :
                        plus_proche = (cellule, distance)
        pivot = plus_proche[0]
    return pred
                    
def set_rang(src, dst, dico_voisins):
    pred = dijkstra(src, dst, dico_voisins)
    rang = 1
    current = pred[dst]
    while (current != src) :
        current = pred[current]
        rang += 1
    return rang