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
game = MSGame(5, 5, 10)
graph = []
width = game.board.board_width
height = game.board.board_height
numb = game.board.num_mines
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


res  = [s for s in modelnodes if 'X' in s] 

#"A partir de aqui se obtienen las CPDS de las Xij"
for e in range(0,len(res)):
    cpd_msgameX =  "cpd_msgame"+(res[e])
    cpd_msgameX = pgmf.TabularCPD(res[e],2,[[probabilidadNoBomba,probabilidadBomba]])
    Modelo_msgame.add_cpds(cpd_msgameX)


orig_stdout0 = sys.stdout
f0 = open('CPDSFinal.txt', 'w')
sys.stdout = f0
print("\n")
print("Sacamos ahora los vecinos de cada Yij y calculamos sus CPDS")
resY  = [s for s in modelnodesY if 'Y' in s] 
for l in range(0,len(resY)):
    i = resY[l][1:2]
    j = resY[l][2:3]
    vecinos = game.neightbours_of_position(int(i),int(j))
    listOpt = [0,1]
    #Se realizan las combinaciones
    resA = list(product(listOpt,repeat = len(vecinos)))
    #Se suman los unos de cada una de las combinaciones, es decir, se suman el número de bombas
    def counterPermutations(lsa):
        count = 0
        for f in range(len(lsa)):
            if lsa[f] is 1:
                count = count + 1
        return count
    #Generamos tantas listas como Y necesitamos + 1 (incluyendo la inexistencia de bomba)
    probabilidades_unidas = []
    for v in range(len(vecinos)+1):
        probabilidades_calculadas = []
        for a in range(len(resA)):
            lsta = resA[a]
            counter = counterPermutations(lsta)
            if counter is v:
                probabilidades_calculadas.append(1)
            else:
                probabilidades_calculadas.append(0)
        probabilidades_unidas.append(probabilidades_calculadas)
    #Generamos la CPD
    cpd_letrasY =  "cpd_letras"+(resY[l])
    cpd_letrasY = pgmf.TabularCPD(resY[l],len(vecinos)+1,probabilidades_unidas,vecinos,[2]*len(vecinos))
    Modelo_msgame.add_cpds(cpd_letrasY)
    print(cpd_letrasY)
f0.close()
sys.stdout = orig_stdout0
Modelo_msgame.check_model()

orig_stdout3 = sys.stdout
f3 = open('2. testCPDSFinal.txt', 'w')
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

f3.close()
sys.stdout = orig_stdout3