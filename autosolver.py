from __future__ import print_function
from msgame import MSGame
from BayesianNetworkGenerator import gameNetworkGenerator
from random import randint
import pgmpy.inference as pgmi
import sys


game = MSGame(10, 10, 5)
modelo = gameNetworkGenerator(game)


game.print_board()
posX = randint(0,game.board_width-1)
posY = randint(0,game.board_width-1)
try:
    input = raw_input
except NameError:
    pass


game.play_move("click",posX,posY)
print("Move: " + str(posX)+","+str(posY))
board = game.board
print(board.info_map)
print(board.mine_map)

while game.game_status == 2:
    no_bombas_enYij={} 
    no_bombas_enXij={} 
    evidencias= {}
    sindescubrir = []
    con_bombas = []
    for i in range(board.board_width):
        for j in range(board.board_height):
            field_status = board.info_map[j, i]
            if field_status in range(1,8):
                evidencias["X" + str(i) + str(j)] = 0
                evidencias["Y" + str(i) + str(j)] = field_status
            elif field_status == 0:
                evidencias["X" + str(i) + str(j)] = 0
                evidencias["Y" + str(i) + str(j)] = 0
            elif field_status == 11:
                sindescubrir.append("X" + str(i) + str(j))
    print(evidencias)
    Model_Game_ev = pgmi.VariableElimination(modelo)
    consulta = Model_Game_ev.query(sindescubrir, evidencias)
    listaDeProbsFinales = []
    for x in range(len(sindescubrir)):
        listaDeProbsFinales.append(consulta[sindescubrir[x]].values)
    listasCeros = [item[0] for item in listaDeProbsFinales]
    con_bombas = [item[1] for item in listaDeProbsFinales]
    elementos = []
    for h in range(len(con_bombas)):
        if con_bombas[h] == 1.0:
            elemento = sindescubrir[h]
            # elementos.append(sindescubrir[h])
            ke = elemento[1:2]
            le = elemento[2:3]
            game.play_move("flag",int(ke),int(le))
    
    if game.game_status == 1:
        print("SE HAN MARCADO TODAS LAS MINAS Y NO HAN EXPLOTADO")
        game.print_board()
    else:
        print(elementos)
        maximo = max(listasCeros)
        winner = sindescubrir[listasCeros.index(max(listasCeros))]
        print("Se ha descubierto que la casilla " + winner + " es la que menos posibilidades tiene de contener una mina, en concreto: " + str(maximo))
        print("Click en " + winner + "?. Pulsa enter para continuar")
        input()  
        k = winner[1:2]
        l = winner[2:3]
        print("Click on: "+str(k)+","+str(l))
        game.play_move("click",int(k),int(l))
        game.print_board()
        board = game.board
        # print(board.info_map)