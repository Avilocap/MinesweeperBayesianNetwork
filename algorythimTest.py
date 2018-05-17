import networkx  # Permite trabajar con grafos
import pgmpy as pgm
import pgmpy.models as pgmm
import pgmpy.factors.discrete as pgmf  # Tablas de probabilidades condicionales y
import pgmpy.inference as pgm
from msgame import MSGame

game = MSGame(20, 20, 40)

graph = []
nodes = game.name_nodes()
width = game.board.board_width
height = game.board.board_height

for i in range(width):
    for j in range(height):
       vecinos = game.neightbours_of_position(i,j)
       for x in range(0,len(vecinos)):
           graph.append(("Y" + str(i) + str(j),vecinos[x]))
    
Modelo_msgame = pgmm.BayesianModel(graph)
print(Modelo_msgame.nodes())
print("EDGEEEEEESSS")
print(Modelo_msgame.edges())