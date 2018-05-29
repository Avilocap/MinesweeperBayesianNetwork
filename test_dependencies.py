from __future__ import print_function
from msgame import MSGame
from BayesianNetworkGenerator import gameNetworkGenerator
from msboard import bcolors
from random import randint
import pgmpy.inference as pgmi
import sys
import pgmpy.inference.EliminationOrder as elor

game = MSGame(10, 10, 5)
modelo = gameNetworkGenerator(game)

# print(modelo.active_trail_nodes('X12'))
# independencies = modelo.local_independencies("X55")
# print(independencies)
# independencies2 = modelo.local_independencies("X55").reduce
# print(independencies2)
print(modelo.get_cpds("Y00"))
phi = modelo.get_cpds("Y00").to_factor()
phi2= modelo.get_cpds("Y00").to_factor()
phi.reduce([('X11',0),('X01',0)])
print(phi.marginalize(['Y00']))


