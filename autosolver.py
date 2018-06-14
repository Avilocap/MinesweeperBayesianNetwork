from __future__ import print_function
from msgame import MSGame
from BayesianNetworkGenerator import gameNetworkGenerator
from msboard import bcolors
from random import randint
import pgmpy.inference as pgmi
import networkx
import numpy
import sys
import pgmpy.inference.EliminationOrder as elor
game = MSGame(5, 5, 5)
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
reverse = False



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
                # evidencias["Y" + str(i) + str(j)] = field_status

    print("")
    print("△ Evidencias descubiertas tras el click  -----------------------------")
    print("")
    print(" ◻︎ Número de evicencias : %d" % len (evidencias))
    print("")
    # print(evidencias)
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
    if(reverse is False):
        rr = reversed(casillasParaIterarSet)
        casillasParaIterarSet = list(rr)
        reverse = True
    else:
        reverse =  False
    
    # Se descartan los nodos irrelevantes
    for u in casillasParaIterarSet:
        if u in casillasMarcadas:
            casillasParaIterarSet.remove(u)
    
    print("casillas para recorrer antes de la iteración")
    print(casillasParaIterarSet)

    for p in range(len(casillasParaIterarSet)):
        print("Consultando probabilidad de la casilla: " + casillasParaIterarSet[p])
        # print(casillasParaIterarSet)
        # print(casillasParaIterarSet[p])
        modeloCopia = modelo.copy()
        nodosDescartados = []
        noBorrar =[]
        kee = casillasParaIterarSet[p][1:2]
        lee = casillasParaIterarSet[p][2:3]
        listaVecinosConsulta = game.neightbours_of_position(int(kee),int(lee))
        noBorrar.append("Y"+str(kee)+str(lee))
        noBorrar.append(casillasParaIterarSet[p])
        # for k in list(evidencias.keys()):
        #     noBorrar.append(k)
        # print(noBorrar)
        nodosDescartados=[]
        contadorEvideciasVecinos = 0




        for vesiii in listaVecinosConsulta:
            # if vesiii in list(evidencias.keys()):
            if vesiii in list(evidencias.keys()):
                contadorEvideciasVecinos = contadorEvideciasVecinos + 1
            ke = vesiii[1:2]
            le = vesiii[2:3]
            noBorrar.append("Y"+str(ke)+str(le))
            noBorrar.append(vesiii)
            # print("NB")
            # print(noBorrar)
        print()
        print("número de evidencias en esta iteración:")
        print(contadorEvideciasVecinos)
        descubierto = False
        if contadorEvideciasVecinos < 2:
            continue


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
        # print(consulta[casillasParaIterarSet[p]])
        print("[P. !BOMBA - P. BOMBA]")
        print(consulta[casillasParaIterarSet[p]].values)
        # casillasParaIterarSet.remove(casillasParaIterarSet[p])
        valores = consulta[casillasParaIterarSet[p]].values
        listaDeProbsFinales.append(valores)

        
        
        if valores[1] >= 0.790:
                game.play_move("flag",int(kee),int(lee))
                casillasMarcadas.append("X"+str(kee)+str(lee))
                print()
                print("¡¡ Encontrada bomba !!")
                print()
                game.print_board()
                if casillasParaIterarSet.count == game.num_mines:
                    sys.exit()
                continue

        if valores[0] >= 0.830:
            valorReal = 1 - valores[0]
            print("Se ha descubierto que la casilla " + casillasParaIterarSet[p] + " es la que menos posibilidades tiene de contener una mina, en concreto: " + str(valorReal))
            # print("Click en " + casillasParaIterarSet[p])
            print("Click en: "+str(kee)+","+str(lee))
            game.play_move("click",int(kee),int(lee))
            game.print_board()
            board = game.board
            print("----------------------------------------------------------------------------------------------------------------------")
            descubierto = True
        
            break

        

    # for x in range(len(casillasParaIterarSet)):
    #    # listaDeProbsFinales.append(consulta[casillasParaIterarSet[x]].values)
    if descubierto is False:
        if not listaDeProbsFinales:
            print("Pocas evidencias, reintentar")
            break
        print("casillas para recorrer despues de la iteración")
        print(casillasParaIterarSet)
        listasCeros = [item[0] for item in listaDeProbsFinales]
        con_bombas = [item[1] for item in listaDeProbsFinales]
        elementos = []
        for h in range(len(con_bombas)):
            #Aquí estamos viendo si un número enorme en coma flotante es idéntico a 1, llega un punto al final del algoritmo, en el que en las últimas iteraciones la probabilidad de bomba para 
            #para una casilla no se acerca a 1.0 y no podemos marcarla bien con flag para ganar el juego.
            if con_bombas[h] >= .800:
                elemento = casillasParaIterarSet[h]
                # elementos.append(sindescubrir[h])
                ke = elemento[1:2]
                le = elemento[2:3]
                game.play_move("flag",int(ke),int(le))
                casillasMarcadas.append("X"+str(ke)+str(le))
                print()
                print("¡¡ Encontrada bomba !!")
                print()
                game.print_board()
                print("Casillas marcadas")
                print(casillasMarcadas)
                
            
            # print(board.info_map)
        if game.game_status == 1:
            print("")
            # print(bcolors.OKGREEN + "¡¡ SE HAN MARCADO TODAS LAS MINAS Y NO HAN EXPLOTADO !!" + bcolors.ENDC)
            # print("")
            game.print_board()
            sys.exit()
        else:
            maximo = numpy.amax(listaDeProbsFinales)
            winner = listaDeProbsFinales[listasCeros.index(maximo)]
            print(winner)
            res = 1 - maximo
            #print("Se ha descubierto que la casilla " + winner + " es la que menos posibilidades tiene de contener una mina, en concreto: " + str(res))
            # print("Click en " + winner + " ?. Pulsa enter para continuar")
            # input()  
            k = winner[1:2]
            l = winner[2:3]
            print("Click en: "+str(k)+","+str(l))
            game.play_move("click",int(k),int(l))
            game.print_board()
            board = game.board
            print("----------------------------------------------------------------------------------------------------------------------")




        
