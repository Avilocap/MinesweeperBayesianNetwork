from __future__ import print_function
from msgame import MSGame
from BayesianNetworkGenerator import gameNetworkGenerator
from random import randint
import pgmpy.inference as pgmi
import sys
import pgmpy.inference.EliminationOrder as elor




game = MSGame(5, 5, 6)
modelo = gameNetworkGenerator(game)

print("")
print("△ Tablero ------------------------------------------------------")
print("")
game.print_board()
posX = randint(0,game.board_width-1)
posY = randint(0,game.board_width-1)
try:
    input = raw_input
except NameError:
    pass

game.play_move("click",posX,posY)
print("△ Move --> click: " + str(posX)+","+str(posY)+"  ---------------------------------------")
print("")
board = game.board
# print(board.info_map)
print("△ CHEAT: Mapa de minas ------------------------------------------------------")
print("")
print(board.mine_map)
print("")
no_bombas_enYij={} 
no_bombas_enXij={} 
evidencias= {}
sindescubrir = []
listaEvidencias = []
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
            listaEvidencias.append("Y" + str(i) + str(j))
            sindescubrir.append("X" + str(i) + str(j))
print("")
print("△ Evidencias descubiertas tras el click  -----------------------------")
print("")
print(evidencias)
print("")
print("-------  △  --  CALCULANDO SIGUIENTE MOVIMIENTO --  △   ---------------------------------")
print("------------------    Por favor, espera    ------------------------------------------")
print("")
orig_stdout0 = sys.stdout
f0 = open('nextStepOracleOut.txt', 'w')
sys.stdout = f0

Model_Game_ev = pgmi.VariableElimination(modelo)
Model_el = elor.BaseEliminationOrder(modelo)
#consulta = Model_Game_ev.query(sindescubrir, evidencias,Model_el.get_elimination_order(listaEvidencias))
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
print("Casilla sugerida: " + winner+ " es la que menor probabilidad tiene de contener una mina, en concreto: " + str(maximo))


# while game.game_status == 2:
#     # play move
    
    
#     move = input("Move: ")
#     game.play_move_msg(move)
#     game.print_board()
#     board = game.board
#     print(board.info_map)
#     print(board.mine_map)