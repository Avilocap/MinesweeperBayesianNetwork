from __future__ import print_function
from msgame import MSGame
from BayesianNetworkGenerator import gameNetworkGenerator
from msboard import bcolors
from random import randint
import numpy as np
import pgmpy.inference as pgmi
import sys
import pgmpy.inference.EliminationOrder as elor
import itertools
import pgmpy.estimators.BayesianEstimator as bae
from pgmpy.inference import BeliefPropagation
game = MSGame(10, 10, 5)
modelo = gameNetworkGenerator(game)

print(modelo.active_trail_nodes('X12'))
# independencies = modelo.local_independencies("X55")
# print(independencies)
# independencies2 = modelo.local_independencies("X55").reduce
# print(independencies2)
print(modelo.get_cpds("Y00"))
print(modelo.get_cpds("X00"))
phi = modelo.get_cpds("Y00").to_factor()
phi.reduce([('X11',0),('X01',0),('X10',1)])
print(phi)


# belief_propagation = BeliefPropagation(modelo)
# mq = belief_propagation.map_query(variables=['X00'],  evidence={'X11': 0, 'X01': 0})
# print(mq)
# a = np.arange(60.).reshape(3,4,5)
# b = np.arange(24.).reshape(4,3,2)
# c = np.tensordot(a,b, axes=([1,0],[0,1]))

# print(c)