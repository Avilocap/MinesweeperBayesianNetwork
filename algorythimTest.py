import networkx  # Permite trabajar con grafos
import pgmpy as pgm
import pgmpy.models as pgmm
import pgmpy.factors.discrete as pgmf  # Tablas de probabilidades condicionales y
import pgmpy.inference as pgm
from msgame import MSGame

Modelo_msgame = pgmm.BayesianModel()
game = MSGame(5, 5, 5)



""" Modelo_msgame.add_nodes_from(game.get_board.nodes)

Modelo_alarma.add_edges_from([('Robo', 'Alarma'),
                              ('Terremoto', 'Alarma'),
                              ('Alarma', 'Llamada'),
                              ('Terremoto', 'Noticia')])
Modelo_alarma = pgmm.BayesianModel([('Robo', 'Alarma'),
                                    ('Terremoto', 'Alarma'),
                                    ('Alarma', 'Llamada'),
                                    ('Terremoto', 'Noticia')])
print(Modelo_alarma.nodes()) """