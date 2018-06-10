from __future__ import print_function
from msgame import MSGame
from BayesianNetworkGenerator import gameNetworkGenerator
from msboard import bcolors
from random import randint
import pgmpy.inference as pgmi
import networkx
import sys
import pgmpy.inference.EliminationOrder as elor
game = MSGame(10, 10, 6)
modelo = gameNetworkGenerator(game)



print("")
print("△ Tablero ------------------------------------------------------")
print("")
game.print_board()
board = game.board
print(board.mine_map)
posX = randint(0,game.board_width-1)
posY = randint(0,game.board_width-1)
try:
    input = raw_input
except NameError:
    pass

# game.mover_minas_alrededor(posX,posY)
game.mover_minas_alrededor(posX,posY)
game.play_move("click",posX,posY)
print("△ Move --> click: " + str(posX)+","+str(posY)+"  ---------------------------------------")
print("")
game.print_board()
print(board.mine_map)
casillasMarcadas = []
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
            elif field_status == 9:
                evidencias["X" + str(i) + str(j)] = 1
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
    listaDeProbsFinales = []
    #Reducion de evidencias:
    casillasParaIterar = []
    for e in range(len(list(evidencias.keys()))):
        #Sacara los vecinos de cada una de las evidedncias.
        ke = list(evidencias.keys())[e][1:2]
        le = list(evidencias.keys())[e][2:3]
        listaVecinosEvidencia = game.neightbours_of_position(int(ke),int(le))
        for vesii in listaVecinosEvidencia:
            if vesii not in list(evidencias.keys()):
                casillasParaIterar.append(vesii)
    
    casillasParaIterarSet = list(set(casillasParaIterar))

    
    # Se descartan los nodos irrelevantes
    for u in casillasParaIterarSet:
        if u in casillasMarcadas:
            casillasParaIterarSet.remove(u)
        
    print("casillas para interar antes de la iteración")
    print(casillasParaIterarSet)

    for p in range(len(casillasParaIterarSet)):
        print("Consultando probabilidad de la casilla: " + casillasParaIterarSet[p])
        print(casillasParaIterarSet)
        print(casillasParaIterarSet[p])
        modeloCopia = modelo.copy()
        nodosDescartados = []
        noBorrar =[]
        ke = casillasParaIterarSet[p][1:2]
        le = casillasParaIterarSet[p][2:3]
        listaVecinosConsulta = game.neightbours_of_position(int(ke),int(le))
        noBorrar.append("Y"+str(ke)+str(le))
        noBorrar.append(casillasParaIterarSet[p])
        nodosDescartados=[]
        for vesiii in listaVecinosConsulta:
            # if vesiii in list(evidencias.keys()):
            ke = vesiii[1:2]
            le = vesiii[2:3]
            noBorrar.append("Y"+str(ke)+str(le))
            noBorrar.append(vesiii)
            # print("NB")
            # print(noBorrar)
        for y in modeloCopia.nodes():
            if y not in noBorrar and y not in evidencias.keys():
                nodosDescartados.append(y)
        # evidenciasIteracion = {}
        # for h in noBorrar:
        #     if h in evidencias.keys():
        #         valorEnEvidencias = evidencias.get(h)
        #         evidenciasIteracion[h] = valorEnEvidencias

        modeloCopia.remove_nodes_from(nodosDescartados)
        """
        Ahora mismo coge las Ys evidencias y todas las X vecinos.

        """
        Model_Game_ev = pgmi.VariableElimination(modeloCopia)
        consulta = Model_Game_ev.query([casillasParaIterarSet[p]], evidencias)
        print(consulta[casillasParaIterarSet[p]])
        print(consulta[casillasParaIterarSet[p]].values)
        # casillasParaIterarSet.remove(casillasParaIterarSet[p])
        listaDeProbsFinales.append(consulta[casillasParaIterarSet[p]].values)
        
        






    # todas = sindescubrir + list(evidencias.keys())
    
    # padres = []
    # modeloCopia = modelo.copy()
    # for x in todas:
    #     padres = modeloCopia.subgraph(networkx.ancestors(modeloCopia, x)).nodes() 
    # for y in modeloCopia.nodes():
    #     if y not in todas and y not in padres:
    #         nodosDescartados.append(y)
    
    # modeloCopia.remove_nodes_from(nodosDescartados)

    # print("Descartados")
    # print(nodosDescartados)
    # print("Padres")
    # print(padres)
    # print()
    # print("nodos despues")
    # print(modelo.nodes())

    # Model_Game_ev = pgmi.VariableElimination(modeloCopia)
    # consulta = Model_Game_ev.query(sindescubrir, evidencias)

    

    # for x in range(len(casillasParaIterarSet)):
    #    # listaDeProbsFinales.append(consulta[casillasParaIterarSet[x]].values)
    print("casillas para interar despues de la iteración")
    print(casillasParaIterarSet)
    listasCeros = [item[0] for item in listaDeProbsFinales]
    con_bombas = [item[1] for item in listaDeProbsFinales]
    elementos = []
    
    for h in range(len(con_bombas)):
        #Aquí estamos viendo si un número enorme en coma flotante es idéntico a 1, llega un punto al final del algoritmo, en el que en las últimas iteraciones la probabilidad de bomba para 
        #para una casilla no se acerca a 1.0 y no podemos marcarla bien con flag para ganar el juego.
        if con_bombas[h] >= .998:
            elemento = casillasParaIterarSet[h]
            # elementos.append(sindescubrir[h])
            ke = elemento[1:2]
            le = elemento[2:3]
            game.play_move("flag",int(ke),int(le))
            casillasMarcadas.append("X"+str(ke)+str(le))
            print("Casillas marcadas")
            print(casillasMarcadas)
            
        
        # print(board.info_map)
    if game.game_status == 1:
        print("")
        # print(bcolors.OKGREEN + "¡¡ SE HAN MARCADO TODAS LAS MINAS Y NO HAN EXPLOTADO !!" + bcolors.ENDC)
        # print("")
        game.print_board()
    else:
        maximo = max(listasCeros)
        winner = casillasParaIterarSet[listasCeros.index(maximo)]
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
        # print(elementos)
        # print(sindescubrir)
        # print(listaDeProbsFinales)
        # listaSorteo = sindescubrir
        # if listasCeros.count(listasCeros[0]) == len(listasCeros):
        #     for p in sindescubrir:
        #         if p in casillasParaIterarSet:
        #             listaSorteo.remove(p)
        #     indiceCazilla = randint(0,len(listaSorteo)-1)
        #     cazilla = listaSorteo[indiceCazilla]
        #     m = cazilla[1:2]
        #     n = cazilla[2:3]
        #     game.play_move("click",int(m),int(n))
        #     print("△ Move --> click: " + str(posX)+","+str(posY)+"  ---------------------------------------")
        #     game.print_board()


        # else:


        
