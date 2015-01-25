from parsage import *

if __name__ == '__main__':
	state = "STATE48b1d7d3-58bb-4138-8e6e-577f1bf057d7IS2;7CELLS:0[0]20'8,1[1]8'2,2[-1]6'0,3[-1]12'0,4[1]1'7,5[-1]9'0,6[1]1'8;10MOVES:1<2[1]@10776911'<1[1]@10777486'<1[1]@10777488'<1[1]@10777872'4,4>1[1]@10778870'5,4<1[1]@10776306'<1[1]@10776307'<1[1]@10776372'<1[1]@10777369'<1[1]@10778373'6"
	res = decodage_state(state)

	print(res)

	moves = res['moves']

	for move in moves:
		print(move)
		print(move['destination'])