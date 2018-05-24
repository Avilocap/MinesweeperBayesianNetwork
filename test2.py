import networkx  # Permite trabajar con grafos
import pgmpy as pgm
import pgmpy.models as pgmm
import pgmpy.factors.discrete as pgmf  # Tablas de probabilidades condicionales y
import pgmpy.inference as pgmi
from msgame import MSGame
from itertools import count, islice, product, repeat, combinations, permutations, combinations_with_replacement


#Definimos el tablero
game = MSGame(5, 5, 5)
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
# print("Creamos la red bayesiana que quedaria de esta forma")
# print("\n")
# print("NODOS ------------------------------")
# print(Modelo_msgame.nodes())
# print("\n")
# print("ARISTAS -------------------------------")
# print(Modelo_msgame.edges())

moral = Modelo_msgame.to_markov_model()
print(moral.edges())