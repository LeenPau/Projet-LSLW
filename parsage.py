import re

def decodage_init(init_string) :
    # On commence par diviser la chaine en plusieurs parties, chacunes des parties étant séparées par un ";"
    parties = re.split(';', init_string)

    data = {}

    
    """
    ----------------------------------------------------------------------------
    On traite la première partie de la chaine

    INIT<matchid>TO<#players>[<me>];
    ----------------------------------------------------------------------------
    """
    decodagePartie1 = re.search(r'INIT(.+)TO([0-9]+)\[([0-9]+)\]', parties[0])
    if decodagePartie1 :
        data['matchid']   = str(decodagePartie1.group(1))
        data['nbPlayers'] = int(decodagePartie1.group(2))
        data['me']        = int(decodagePartie1.group(3))




    """
    ----------------------------------------------------------------------------
    On traite la deuxième partie de la chaine

    <speed>;
    ----------------------------------------------------------------------------
    """
    speed = parties[1]
    if speed :
        data['speed'] = int(speed)



    """
    ----------------------------------------------------------------------------
    On traite la troisième partie de la chaine
    
    <#cells>CELLS:<cellid>(<x>,<y>)'<radius>'<offsize>'<defsize>'<prod>,...;
    ----------------------------------------------------------------------------
    """
    nbCELLS = re.search(r'([0-9]+)CELLS', parties[2])
    if nbCELLS :
        data['nbCELLS'] = int(nbCELLS.group(1))


    # cellulesBruts = liste contenant les infos sur chacunes des cellules, mais sous un format brut
    cellulesBruts = re.findall(r'[0-9]+\([0-9]+,[0-9]+\)\'[0-9]+\'[0-9]+\'[0-9]+\'I+', init_string)

    # cellulesDecodees = cellulesBruts + traitement des données
    cellulesDecodees = []
    
    for cellule in cellulesBruts :
        # rappel : <cellid>(<x>,<y>)'<radius>'<offsize>'<defsize>'<prod>
        decodageCellules = re.search(r'([0-9]+)\(([0-9]+),([0-9]+)\)\'([0-9]+)\'([0-9]+)\'([0-9])\'(I+)', cellule)
        if decodageCellules :
            celluleEnCours = {}
            celluleEnCours['cellid']    = int(decodageCellules.group(1))
            celluleEnCours['x']         = int(decodageCellules.group(2))
            celluleEnCours['y']         = int(decodageCellules.group(3))
            celluleEnCours['radius']    = int(decodageCellules.group(4))
            celluleEnCours['offsize']   = int(decodageCellules.group(5))
            celluleEnCours['defsize']   = int(decodageCellules.group(6))
            celluleEnCours['prod']      = len(decodageCellules.group(7))
            
            cellulesDecodees.append(celluleEnCours)

    data['cellules'] = cellulesDecodees


    """
    ----------------------------------------------------------------------------
    On traite la dernière partie de la chaine

    <#lines>LINES:<cellid>@<dist>OF<cellid>,...
    ----------------------------------------------------------------------------
    """
    nbLINES = re.search(r'([0-9]+)LINES', parties[3])
    if nbLINES :
        data['nbLINES'] = nbLINES.group(1)


    # aretesBruts = liste contenant les infos sur chacunes des aretes, mais sous un format brut
    aretesBruts = re.findall(r'[0-9]+@[0-9]+OF[0-9]+', init_string)

    # aretesDecodees = aretesBruts + traitement des données
    aretesDecodees = []
    
    for arete in aretesBruts :
        # rappel : <cellid>@<dist>OF<cellid>
        decodageAretes = re.search(r'([0-9]+)@([0-9]+)OF([0-9]+)', arete)
        if decodageAretes :
            areteEnCours = {}
            areteEnCours['cellid1']     = int(decodageAretes.group(1))
            areteEnCours['distance']    = int(decodageAretes.group(2))
            areteEnCours['cellid2']     = int(decodageAretes.group(3))

            aretesDecodees.append(areteEnCours)

    data['aretes'] = aretesDecodees


    return data


def decodage_state(string) :
    #Initialisation
        data = {}
        data['cells'] = []
        data['moves'] = []

        #Parsage de la partie CELLS
        infos = re.search(r"([0-9]*CELLS)([:,]?[0-9]*\[[-]?[0-9]*\][0-9]*'[0-9]*[,]?)*", string)
        if infos is not None:
            complete = infos.group(0)
            first = complete.split(':')[1]
            second = first.split(',')

            for i in second:
                tmp = {}
                cell = re.search(r"([0-9]*)\[([-]?[0-9]*)\]([0-9]*)'([0-9]*)", i)
                
                tmp['cellid']       = int(cell.group(1))
                tmp['owner']        = int(cell.group(2))
                tmp['offunits']     = int(cell.group(3))
                tmp['defunits']     = int(cell.group(4))

                data['cells'].append(tmp)

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
                        toAdd = {}
                        meta = re.search(r"([<>])([0-9]*)\[([0-9]*)\](@[0-9]*)", i)
                        if meta is not None:
                            if(meta.group(1) == "<"):
                                toAdd['source']         = int(cellule_fin)
                                toAdd['destination']    = int(cellule_debut)
                                toAdd['nbUnits']        = int(meta.group(2))
                                toAdd['owner']          = int(meta.group(3))
                                toAdd['timestamp']      = str(meta.group(4))
                            else:
                                toAdd['source']         = int(cellule_fin)
                                toAdd['destination']  = int(cellule_debut)
                                toAdd['nbUnits']        = int(meta.group(2))
                                toAdd['owner']          = int(meta.group(3))
                                toAdd['timestamp']      = str(meta.group(4))

                            data['moves'].append(toAdd)

        return data
