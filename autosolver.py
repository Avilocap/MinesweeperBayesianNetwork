from __future__ import print_function
from msgame import MSGame
from BayesianNetworkGenerator import gameNetworkGenerator
from msboard import bcolors
from random import randint
import pgmpy.inference as pgmi
import networkx
import sys
import pgmpy.inference.EliminationOrder as elor
game = MSGame(8, 8, 13)
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
game.print_board()
board = game.board
# print(board.info_map)
# print("")
# print(board.mine_map)

while game.game_status == 2:
    no_bombas_enYij={} 
    no_bombas_enXij={} 
    evidencias= {}
    sindescubrir = []
    con_bombas = []
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
    print(" ◻︎ Número de evicencias : %d" % len (evidencias))
    print("")
    print(evidencias)
    print("")
    print("-------  △  -- "+bcolors.OKBLUE+" CALCULANDO SIGUIENTE MOVIMIENTO"+bcolors.ENDC+"  --  △   ---------------------------------")
    print("---------------------  "+bcolors.OKBLUE+"  Por favor, espera "+bcolors.ENDC+"   ------------------------------------------")
    print("")


    # print("nodos antes")
    # print(modelo.nodes())

    # Se descartan los nodos irrelevantes
    todas = sindescubrir + list(evidencias.keys())
    nodosDescartados = []
    padres = []
    modeloCopia = modelo.copy()
    for x in todas:
        padres = modeloCopia.subgraph(networkx.ancestors(modeloCopia, x)).nodes() 
    for y in modeloCopia.nodes():
        if y not in todas and y not in padres:
            nodosDescartados.append(y)
    
    modeloCopia.remove_nodes_from(nodosDescartados)

    # print("Descartados")
    # print(nodosDescartados)
    # print("Padres")
    # print(padres)
    # print()
    # print("nodos despues")
    # print(modelo.nodes())

    Model_Game_ev = pgmi.VariableElimination(modeloCopia)
    consulta = Model_Game_ev.query(sindescubrir, evidencias)

    

    listaDeProbsFinales = []
    for x in range(len(sindescubrir)):
        listaDeProbsFinales.append(consulta[sindescubrir[x]].values)
    listasCeros = [item[0] for item in listaDeProbsFinales]
    con_bombas = [item[1] for item in listaDeProbsFinales]
    elementos = []
    
    for h in range(len(con_bombas)):
        #Aquí estamos viendo si un número enorme en coma flotante es idéntico a 1, llega un punto al final del algoritmo, en el que en las últimas iteraciones la probabilidad de bomba para 
        #para una casilla no se acerca a 1.0 y no podemos marcarla bien con flag para ganar el juego.
        if con_bombas[h] >= .98:
            elemento = sindescubrir[h]
            # elementos.append(sindescubrir[h])
            ke = elemento[1:2]
            le = elemento[2:3]
            game.play_move("flag",int(ke),int(le))
    
    if game.game_status == 1:
        print("")
        # print(bcolors.OKGREEN + "¡¡ SE HAN MARCADO TODAS LAS MINAS Y NO HAN EXPLOTADO !!" + bcolors.ENDC)
        # print("")
        game.print_board()
    else:
        # print(elementos)
        # print(sindescubrir)
        # print(listaDeProbsFinales)
        maximo = max(listasCeros)
        winner = sindescubrir[listasCeros.index(max(listasCeros))]
        print("Se ha descubierto que la casilla " + winner + " es la que menos posibilidades tiene de contener una mina, en concreto: " + str(maximo))
        print("Click en " + winner + " ?. Pulsa enter para continuar")
        # input()  
        k = winner[1:2]
        l = winner[2:3]
        print("Click on: "+str(k)+","+str(l))
        game.play_move("click",int(k),int(l))
        game.print_board()
        board = game.board
        print("----------------------------------------------------------------------------------------------------------------------")
        # print(board.info_map)
