#Protocole de communication avec le serveur

##Sommaire :
1. Présentation du protocole de communication
2. Fonction order(msg)
3. Fonction state()
4. Fonction state_on_update()
5. Fonction etime()

##Présentation du protocole
Le serveur dispose de 4 fonctions qui peuvent être appelées de la manière suivante. Ces fonctions sont implémentées par le module poooc et ne font donc pas partie des différentes fonctions que nous devons implémenter nous mêmes. Nous nous contentons de les appeler en leur fournissant le bon "message" à envoyer.

## Fonction order : 
Fonction permettant de signifier un déplacement d'unités

Le paramètre d'entrée (une string) se découpe de la manière suivante :

    [<userid>] : Identifiant du robot qui demande le déplacement 
			 ex : [0947e717-02a1-4d83-9470-a941b6e8ed07]

    MOV<% of units> : Pourcentage d'unités de la case qu'il faut déplacer
				  ex : MOV33

    FROM<cell id> : Identifiant de la cellule de départ
				ex : FROM1

    TO<cell id> : Identifiant de la cellule d'arrivée
			  ex : TO4

Ce qui donne au final :[0947e717-02a1-4d83-9470-a941b6e8ed07]MOV33FROM1TO4

Le pourcentage des unités offensives utilise la divion entière. Par exemple : 25% de 50 égal à 50*25/100=12. Un ordre dont l'effectif d'unités off est nul (par ex., 33% de 2 unités) est ignoré, tout comme des ordres incorrects (cellule non occupée, cellules non adjacentes, etc.)

##Fonction state
Fonction de demande de l'état courant du jeu.

    Retourne STATE<matchid>IS<#players>;<#cells>CELLS:<cellid>[<owner>]<offunits>'<defunits>,...'<#moves>MOVES:<cellid><direction><#units>[<owner>]@<timestamp>'...<cellid>,...

    Type de retour :  chaîne de caractères (utf-8 string)
    
    Example "STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]33'6;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3"
    
    "<timestamp>" en millisecondes, donnée à vitesse x1 : top départ des unités de la cellule source. 
    "<direction>" désigne le caractère '>' ou '<' et indique le sens des unités en mouvement en suivant la pointe de flèche.
* "STATE" : nom de la commande
* "20ac18ab-6d18-450e-94af-bee53fdc8fca" : Identifiant du match
* "IS2" : nb joueurs
* "3CELLS" : 3 Cellules modifiées
    * 1[2]12' : Cellule 1, du joueur 2, 12 unités offensives
    * 4,2[2]15' : Cellules 4 et 2, du joueur 2, 15 unités offensives
    * 2,3[1]33'6; : Cellules 2 et 3, du joueur 1, 33 unités offensives, 6 unités défensives
    
* "4MOVES": 4 mouvements  "1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3" 
    * Déplacement de la cellule 2 vers la cellule 1:
        * 5 unités du joueur 2 au temps 232
    * Déplacement de la cellule 1 vers la cellule 2:
        * 6 unités du joueur 2 au temps 488
        * 3 unités du joueur 1 au temps 4330
    * Déplacement de la cellule 3 vers la cellule 1
        * 10 unités du joueur 1 au temps 2241
        
##Fonction state_on_update()
Demande l'état du jeu modifié

    Retourne uniquement les éléments modifiés par rapport à la dernière MAJ demandée de l'état du plateau

La valeur de retour est identique à celle de la fonction state()
La principale différence provient du fait que le processus est mis en attente d'une mise à jour de l'état du jeu

L'appel de state_on_update() est bloquant, ce qui signifie que le jeu ne progresse pas tant que cette fonction 
ne s'est pas executée en entier

## Fonction etime()
Retourne le temps écoulé (elapsed time) depuis le début du match

    Retour :  temps écoulé (elapsed time) en millisecondes
    Type de retour :  entier

/!\ le temps indiqué n'est qu'une approximation (la plus précise possible)

