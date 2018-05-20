import networkx  # Permite trabajar con grafos
import pgmpy as pgm
import pgmpy.models as pgmm
import pgmpy.factors.discrete as pgmf  # Tablas de probabilidades condicionales y
import pgmpy.inference as pgmi
from msgame import MSGame
from itertools import count, islice, product, repeat, combinations, permutations, combinations_with_replacement

game = MSGame(4, 4, 5)

graph = []
nodes = game.name_nodes()
width = game.board.board_width
height = game.board.board_height

for i in range(width):
    for j in range(height):
       vecinos = game.neightbours_of_position(i,j)
       for x in range(0,len(vecinos)):
           graph.append((vecinos[x],"Y" + str(i) + str(j)))
    
Modelo_msgame = pgmm.BayesianModel(graph)
# print(graph)
# print(Modelo_msgame.nodes())
# print("EDGEEEEEESSS")
# print(Modelo_msgame.edges())

probabilidadBomba = game.board.num_mines/(game.board.board_height*game.board_width)
probabilidadNoBomba = 1 - probabilidadBomba

modelnodes = Modelo_msgame.nodes()
modelnodesY = Modelo_msgame.nodes()
res  = [s for s in modelnodes if 'X' in s] 

for e in range(0,len(res)):
    cpd_msgameX =  "cpd_msgame"+(res[e])
    cpd_msgameX = pgmf.TabularCPD(res[e],2,[[probabilidadNoBomba,probabilidadBomba]])
    Modelo_msgame.add_cpds(cpd_msgameX)
    # print(cpd_msgameX)



# lista = [probabilidadNoBomba,probabilidadBomba]
# listaNo =[1- probabilidadNoBomba, 1 - probabilidadBomba] 
# res1 = list(product(lista,repeat = 3))
# res2 = (x[0]*x[1]*x[2] for x in res1)
# print(list(res2))
# #list res2, valores para Y(si)
# #list res 4, valores para Y(no)

# res3 = list(product(listaNo,repeat = 3))
# res4 = (1-(x[0]*x[1]*x[2]) for x in res1)
# print(list(res4))


resY  = [s for s in modelnodesY if 'Y' in s] 
for l in range(0,len(resY)):
    i = resY[l][1:2]
    j = resY[l][2:3]
    # print(i,j)
    vecinos = game.neightbours_of_position(int(i),int(j))
    # print(vecinos)
    lista = [probabilidadNoBomba,probabilidadBomba]
    listaNo =[1- probabilidadNoBomba, 1 - probabilidadBomba]
    res1 = list(product(lista,repeat = len(vecinos)))
    res2 = (x[0]*x[1]*x[2] for x in res1)
    res3 = list(product(listaNo,repeat = len(vecinos)))
    res4 = (1-(x[0]*x[1]*x[2]) for x in res1)
    totallist = [list(res2),list(res4)]
    # print(totallist)
    cpd_letrasY =  "cpd_letras"+(resY[l])
    cpd_letrasY = pgmf.TabularCPD(resY[l],2,totallist,vecinos,[2]*len(vecinos))
    Modelo_msgame.add_cpds(cpd_letrasY)

    # for x in range(0,len(vecinos)): 
    #     lista = [probabilidadNoBomba,probabilidadBomba]
    #     cpd_msgameY = "cpd_msgame"+(resY[x])
    #     cpd_msgameY = pgmf.TabularCPD(resY[x],2*len(vecinos),res2,res4)
    #     print(cpd_msgameY)
    # 
Modelo_msgame.check_model()



Modelo_msgame_ev = pgmi.VariableElimination(Modelo_msgame)
cosulta = Modelo_msgame_ev.query(["Y11"])

print(cosulta)


# noditos = list(Modelo_msgame.nodes())
# for p in range(len(noditos)):
#     phiY =  "phi"+(noditos[p])
#     cpd = Modelo_msgame.get_cpds(noditos[p])
#     phiY =  cpd.to_factor()
#     print(phiY)    


# phi_Y00 = Modelo_msgame.get_cpds('Y00')
# print(phi_Y00.scope())  
# print(phi_Y00)



# print(res)
# print(probabilidadBomba)
# print(probabilidadNoBomba)

# print(Modelo_msgame.active_trail_nodes('Y00'))
# print(Modelo_msgame.is_active_trail('Y00','X10'))
# print(Modelo_msgame.is_active_trail('Y00','X22'))
# print(Modelo_msgame.is_active_trail('X10','X11'))
# print(Modelo_msgame.is_active_trail('X10','Y00'))

# Modelo_msgame_ev = pgmi.VariableElimination(Modelo_msgame)
# consulta = Modelo_msgame_ev.query(['X00'])