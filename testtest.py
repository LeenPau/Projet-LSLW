from parsage import *

if __name__ == '__main__':
	state = "STATEfe7550c5-3b31-4713-bc1f-26bb181673efIS2;16CELLS:0[-1]6'0,1[-1]6'0,2[-1]12'0,3[0]4'0,4[-1]6'0,5[-1]6'0,6[-1]6'0,7[-1]6'0,8[-1]6'0,9[-1]6'0,10[-1]6'0,11[-1]6'0,12[1]4'0,13[-1]12'0,14[-1]6'0,15[-1]6'0;0MOVES"
	res = decodage_state(state)

	print(res)