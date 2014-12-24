import re

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
        chaine_decodee['matchid'] = decodagePartie1.group(1)
        chaine_decodee['nbPlayer'] = decodagePartie1.group(2)
        chaine_decodee['me'] = decodagePartie1.group(3)




    """
    ----------------------------------------------------------------------------
    On traite la deuxième partie de la chaine

    <speed>;
    ----------------------------------------------------------------------------
    """
    speed = parties[1]
    if speed :
        chaine_decodee['speed'] = speed



    """
    ----------------------------------------------------------------------------
    On traite la troisième partie de la chaine
    
    <#cells>CELLS:<cellid>(<x>,<y>)'<radius>'<offsize>'<defsize>'<prod>,...;
    ----------------------------------------------------------------------------
    """
    nbCELLS = re.search(r'([0-9]+)CELLS', parties[2])
    if nbCELLS :
        chaine_decodee['nbCELLS'] = nbCELLS.group(1)


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

    chaine_decodee['cellules'] = cellulesDecodees




    """
    ----------------------------------------------------------------------------
    On traite la dernière partie de la chaine

    <#lines>LINES:<cellid>@<dist>OF<cellid>,...
    ----------------------------------------------------------------------------
    """
    nbLINES = re.search(r'([0-9]+)LINES', parties[3])
    if nbLINES :
        chaine_decodee['nbLINES'] = nbLINES.group(1)


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

    chaine_decodee['aretes'] = aretesDecodees


    return chaine_decodee



def main() :
    dico = decodage()
    print(dico)


if __name__ == '__main__' :
    main()
