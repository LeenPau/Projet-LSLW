# -*- coding: utf-8 -*-

from match import Match
import parsage

def main() :
    init_string = "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"
    data_init = parsage.decodage_init(init_string)
    
    m = Match(data_init)

    print(m)
    print(m)
    for cell in m.cellules.values() :
        print(cell.neighbours)
        
if __name__ == '__main__' :
    main()
