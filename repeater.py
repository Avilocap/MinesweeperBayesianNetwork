import sys
import os
import autosolver as aut
import time
import datetime
from functools import wraps
from itertools import cycle
from msboard import bcolors



pruebas = ([5,5,5],[5,5,6],[5,5,7],[8,8,13],[8,8,14],[8,8,15],[10,10,23],[10,10,24],[10,10,25])

"""
Recorre el array de pruebas dado [tam,tam,numBombas], crea el juego y la red bayesiana para resolverlo automáticamente,
hasta que el estado del juego no es 0 (se ha ganado), no se pasa a el siguiente caso de prueba.

Parámetros
----------
pruebas: list, array-like
    casos de prueba a realizar
"""
pruebas = ([5,5,5],[5,5,6],[5,5,7],[8,8,13],[8,8,14],[8,8,15],[10,10,23],[10,10,24],[10,10,25])
for i in range(0,len(pruebas)-1):
    success = False
    while not success:
        print()
        print(bcolors.WARNING+"Test " + str(i+1) + " de " + str(len(pruebas))+"."+bcolors.ENDC)
        print()
        orig_stdout = sys.stdout
        print(bcolors.OKBLUE+'Generando tablero: '+bcolors.ENDC+str(pruebas[i][0])+' x '+str(pruebas[i][1])+' con '+str(pruebas[i][2])+' minas')
        print('...')
        print(bcolors.OKBLUE+'Resolviendo tablero: '+bcolors.ENDC+str(pruebas[i][0])+' x '+str(pruebas[i][1])+' con '+str(pruebas[i][2])+' minas')
        f = open('Prueba_'+str(pruebas[i][0])+'x'+str(pruebas[i][1])+'_'+str(pruebas[i][2])+'_minas'+'.txt', 'w')
        sys.stdout = f
        start_time = time.time()
        status = aut.autosolver(pruebas[i][0],pruebas[i][1],pruebas[i][2])
        elapsed_time = time.time() - start_time
        print(bcolors.OKBLUE+" Tiempo transcurrido: "+bcolors.ENDC)
        print(str(datetime.timedelta(seconds=elapsed_time)))
        sys.stdout = orig_stdout
        f.close()
        
        if status == 0:
            success = False
            print()
            print(bcolors.FAIL+" Partida perdida, reintentando... "+bcolors.ENDC)
            print()
            print(bcolors.OKBLUE+" Tiempo empleado: "+bcolors.ENDC)
            print(str(datetime.timedelta(seconds=elapsed_time)))
            print("-----------------------------------------------------------------------------------------------------")
        else:
            success = True
            print()
            print(bcolors.OKGREEN+" ! Partida ganada ! "+bcolors.ENDC)
            print()
            print(bcolors.OKBLUE+" Tiempo empleado: "+bcolors.ENDC)
            print(str(datetime.timedelta(seconds=elapsed_time)))
            print("-----------------------------------------------------------------------------------------------------")