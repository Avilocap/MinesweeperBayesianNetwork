from __future__ import print_function
from msgame import MSGame
from BayesianNetworkGenerator import gameNetworkGenerator
from random import randint
import pgmpy.inference as pgmi
import sys

game = MSGame(10, 10, 9)
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

no_bombas_enYij={} 
no_bombas_enXij={} 
evidencias= {}
sindescubrir = []
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

orig_stdout0 = sys.stdout
f0 = open('nextStepOracleOut.txt', 'w')
sys.stdout = f0

Model_Game_ev = pgmi.VariableElimination(modelo)
consulta = Model_Game_ev.query(sindescubrir, evidencias)

listaDeProbsFinales = []
for x in range(len(sindescubrir)):
    print(consulta[sindescubrir[x]])
    # print(consulta[sindescubrir[x]].values)
    listaDeProbsFinales.append(consulta[sindescubrir[x]].values)
listasCeros = [item[0] for item in listaDeProbsFinales]
maximo = max(listasCeros)
print(listasCeros.index(max(listasCeros)))
f0.close()
sys.stdout = orig_stdout0
winner = sindescubrir[listasCeros.index(max(listasCeros))]
print("Casilla sugerida" + winner)



# while game.game_status == 2:
#     # play move
    
    
#     move = input("Move: ")
#     game.play_move_msg(move)
#     game.print_board()
#     board = game.board
#     print(board.info_map)
#     print(board.mine_map)