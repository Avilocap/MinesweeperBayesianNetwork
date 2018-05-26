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

Model_Game_ev = pgmi.VariableElimination(modelo)
consulta = Model_Game_ev.query(sindescubrir, evidencias)

listaDeProbsFinales = []
for x in range(len(sindescubrir)):
    # print(consulta[sindescubrir[x]])
    # print(consulta[sindescubrir[x]].values)
    listaDeProbsFinales.append(consulta[sindescubrir[x]].values)
listasCeros = [item[0] for item in listaDeProbsFinales]
maximo = max(listasCeros)
# print(listasCeros.index(max(listasCeros)))
winner = sindescubrir[listasCeros.index(max(listasCeros))]
print("Click en " + winner)

if game.game_status == 0:
    print("YOU LOOSE!")
elif game.game_status == 1:
    print("YOU WON!")

while game.game_status == 2:
    # play move
    
    
    # move = input("Move: ")
    i = winner[1:2]
    j = winner[2:3]
    print("Click on: "+str(i)+","+str(j))
    game.play_move("click",i,j)
    game.print_board()
    board = game.board
    print(board.info_map)
    # print(board.mine_map)
    if game.game_status == 0:
        print("YOU LOOSE!")
    elif game.game_status == 1:
        print("YOU WON!")