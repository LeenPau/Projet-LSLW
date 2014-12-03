#Projet-LSLW
===========

##Présentation des règles du jeu
--------------------------------

###Little Stars for Little Wars 2
---------------------------------

1. Le terrain est généré par le système, avec une position de
départ (une cellule unique) attribuée à chaque joueur/robot
engagé ;

2. Chaque cellule neutre possède au départ un nombre d’unités
défini par le système et ne produit aucune nouvelle unité ;

3. Une proportion quelconque de l’effectif offensif d’une cellule
peut se déplacer vers une cellule adjacente, à une vitesse
définie par le système ;

4. Si l’effectif d’une cellule (off+def) est inférieur strictement à
l’effectif entrant, la cellule est conquise ;

5. Dans tous les cas, l’effectif de la cellule diminue de l’effectif
courant (off+def) moins l’effectif arrivant (min=0) ;

6. Les unités consommées en priorité sont les unités offensives ;

7. En transfert, les conflits entre unités ennemies qui se croisent
sont résolus immédiatemment.

Nombre de joueurs possibles : Illimité en théorie (3v3, 5v5, 10v10 …) en pratique en 1v1

###Lexique 
----------

Terrain : graphe géométrique planaire dont les nœuds sont les cellules du jeu ;
Cellule : nœud du graphe, avec ses propriétés
capacités offensive et défensive
effectifs offensif et défensif
cadence de production
Cellule occupée : cellule appartenant à un joueur
Cellule neutre : cellule libre de toute occupation
Conquête : prise d’une cellule par un joueur
Unité offensive : unité mobile, pour la conquête
Unité défensive : unité fixe, propre à une cellule et utilisée en cas de prise
Capacité : nombre max. d’unités que peut accueillir une cellule
Cadence de production : vitesse à laquelle sont créées les unités dans une cellule

###Objectifs du projet
----------------------

Le projet consiste à créer un programme en python qui va modéliser le fonctionnement “métier” du jeu Little Stars for Little Wars 2 (LSLW2), sans affichage d’interface graphique.
Le programme se devra d’être multijoueur et va donc nécessiter une communication client/serveur.
Enfin, les joueurs seront des bots. Il sera donc nécessaire de réaliser différentes Intelligences Artificielles (IA) correspondant à plusieurs niveaux de difficultés différents.
