import networkx  # Permite trabajar con grafos
import pgmpy as pgm
import pgmpy.models as pgmm
import pgmpy.factors.discrete as pgmf  # Tablas de probabilidades condicionales y
import pgmpy.inference as pgmi
from msgame import MSGame
from itertools import count, islice, product, repeat, combinations, permutations, combinations_with_replacement
import math
import sys


#Definimos el tablero
game = MSGame(5, 5, 5)
graph = []
width = game.board.board_width
height = game.board.board_height
numb = game.board.num_mines
orig_stdout0 = sys.stdout
f0 = open('0. nodos&aristas.txt', 'w')
sys.stdout = f0
print("\n")
print("Se crea el tablero con tamaño " + str(width) + " x " +str(height) + ", con " + str(numb) + " minas")
print("\n")

#Averiguamos los vecinos de cada Y y creamos un conjunto con todos los nodos y las aristas relacionadas.
for i in range(width):
    for j in range(height):
       vecinos = game.neightbours_of_position(i,j)
       for x in range(0,len(vecinos)):
           graph.append((vecinos[x],"Y" + str(i) + str(j)))
    
#Añadimos a la modelo bayesiano la información obtenida anteriormente
Modelo_msgame = pgmm.BayesianModel(graph)
print("Creamos la red bayesiana que quedaria de esta forma")
print("\n")
print("NODOS ------------------------------")
print(Modelo_msgame.nodes())
print("\n")
print("ARISTAS -------------------------------")
print(Modelo_msgame.edges())

probabilidadBomba = game.board.num_mines/(game.board.board_height*game.board_width)
probabilidadNoBomba = 1 - probabilidadBomba
print("\n")
print("Se calcula la probabilidad inicial de que haya bomba en el tablero: num_minas/(width*height) = "+str(probabilidadBomba))
print("\n")
modelnodes = Modelo_msgame.nodes()
modelnodesY = Modelo_msgame.nodes()

sys.stdout = orig_stdout0
f0.close()

res  = [s for s in modelnodes if 'X' in s] 

#"A partir de aqui se obtienen las CPDS de las Xij"
for e in range(0,len(res)):
    cpd_msgameX =  "cpd_msgame"+(res[e])
    cpd_msgameX = pgmf.TabularCPD(res[e],2,[[probabilidadNoBomba,probabilidadBomba]])
    Modelo_msgame.add_cpds(cpd_msgameX)

orig_stdout2 = sys.stdout
f2 = open('1. CPDS.txt', 'w')
sys.stdout = f2
print("\n")
print("Sacamos ahora los vecinos de cada Yij y calculamos sus CPDS")
resY  = [s for s in modelnodesY if 'Y' in s] 
for l in range(0,len(resY)):
    i = resY[l][1:2]
    j = resY[l][2:3]
    # print(i,j)
    vecinos = game.neightbours_of_position(int(i),int(j))
    # print(vecinos)
    listOpt = [0,1]
    resA = list(product(listOpt,repeat = len(vecinos)))
    probNo = []
    probSi = []
    print(resA)
    a = int(0)
    b = int(0)
    suma = int(0)
    
    for a in range(0,len(resA)):
        tup = [(resA[a])]
        for num in tup:
            suma = math.fsum(num)
        probNo.append(suma/len(vecinos))
        print(tup)
        
    print(probNo)
    for b in range(0,len(probNo)):
        prob = 1-probNo[b]
        probSi.append(prob)
    print(probSi) 
    todos = [probSi,probNo]
    cpd_letrasY =  "cpd_letras"+(resY[l])
    cpd_letrasY = pgmf.TabularCPD(resY[l],2,todos,vecinos,[2]*len(vecinos))
    Modelo_msgame.add_cpds(cpd_letrasY)
    print(cpd_letrasY)

sys.stdout = orig_stdout2
f2.close()
Modelo_msgame.check_model()
orig_stdout3 = sys.stdout
f3 = open('2. testCPDS.txt', 'w')
sys.stdout = f3
# print("\n")
# print("Tras chekear el modelo creado con el método chek_model(), obtenemos como ejemplo obtenemos la CPD de una esquina para su comprobación")
print("\n")
print(" -- CPD Y44 --")
print(Modelo_msgame.get_cpds('Y44'))
print("\n")
print(" -- CPD Y00 --")
print(Modelo_msgame.get_cpds('Y00'))
print("\n")
print(" -- CPD Y23 --")
print(Modelo_msgame.get_cpds('Y23'))

sys.stdout = orig_stdout3
f3.close()
# print("\n")
# print(" -- CPD Y02 --")
# print(Modelo_msgame.get_cpds('Y02'))
 





# print(cosulta)
orig_stdout = sys.stdout
f = open('3. testOuts.txt', 'w')
sys.stdout = f
noditos = list(Modelo_msgame.nodes())
for p in range(len(noditos)):
    phiY =  "phi"+(noditos[p])
    cpd = Modelo_msgame.get_cpds(noditos[p])
    phiY =  cpd.to_factor()
    print(phiY)    
# phi_Y00 = Modelo_msgame.get_cpds('Y00')
# print(phi_Y00.scope())  
# print(phi_Y00)
print(" -- Active trail nodes: all the nodes reachable from that respective variable as values.--")
print(Modelo_msgame.active_trail_nodes('Y00'))
print(" -- Active trail nodes  Y00 --")
print(Modelo_msgame.active_trail_nodes('Y01'))
print(" -- Active trail nodes  Y01 --")
print(Modelo_msgame.active_trail_nodes('Y13'))
print(" -- Active trail nodes  Y13 --")
print(Modelo_msgame.active_trail_nodes('Y23'))
print(" -- Active trail nodes  Y23 --")
print(Modelo_msgame.active_trail_nodes('Y23'))
print(" -- Active trail nodes  Y11--")
print(Modelo_msgame.active_trail_nodes('X11'))
print(" -- Active is trail Y00-X10 --")
print(Modelo_msgame.is_active_trail('Y00','X10'))
print(" -- Active is trail Y00-Y10 --")
print(Modelo_msgame.is_active_trail('Y00','Y10'))
print(" -- Active is trail Y00-Y01 --")
print(Modelo_msgame.is_active_trail('Y00','Y01'))
print(" -- Active is trail Y00-X22 --")
print(Modelo_msgame.is_active_trail('Y00','X22'))
print(" -- Active is trail X10-X11 --")
print(Modelo_msgame.is_active_trail('X10','X11'))
print(" -- Active is trail X10-Y00 --")
print(Modelo_msgame.is_active_trail('X10','Y00'))

# Modelo_msgame_ev = pgmi.VariableElimination(Modelo_msgame)'
# consulta = Modelo_msgame_ev.query(['X00'])

sys.stdout = orig_stdout
f.close()

# print(phiY.reduce([('X33',1),('X34',0)]))
# print(phiY.scope())
# print(phiY)

Modelo_msgame_ev = pgmi.VariableElimination(Modelo_msgame)
#  {'X11', 'Y10', 'Y22', 'Y02', 'Y01', 'Y20', 'Y12', 'Y00', 'Y21'}}
# cosulta = Modelo_msgame_ev.query(['X00'],{'Y10':0,'Y11':1,'Y01':0})
# print(cosulta['X00'])
