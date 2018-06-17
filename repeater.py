import sys
import os
import autosolver as aut
import time
import datetime
from functools import wraps
from itertools import cycle
pruebas = ([5,5,5],[5,5,6],[5,5,7],[8,8,13],[8,8,14],[8,8,15],[10,10,23],[10,10,24],[10,10,25])
#pruebas = ([10,10,25],[5,5,2])

"""
Recorre el array de pruebas dado [tam,tam,numBombas], crea el juego y la red bayesiana para resolverlo automáticamente,
hasta que el estado del juego no es 0 (se ha ganado), no se pasa a el siguiente caso de prueba.

Parámetros
----------
pruebas: list, array-like
    casos de prueba a realizar
"""

done = 'false'
#here is the animation
def animate():
    while done == 'false':
        sys.stdout.write('\rCalculando |')
        time.sleep(0.1)
        sys.stdout.write('\rCalculando /')
        time.sleep(0.1)
        sys.stdout.write('\rCalculando -')
        time.sleep(0.1)
        sys.stdout.write('\rCalculando \\')
        time.sleep(0.1)
    sys.stdout.write('\r!Hecho!     ')


for i in range(0,len(pruebas)-1):
    success = False
    
    

    while not success:
        orig_stdout = sys.stdout
        print('Generando tablero: '+str(pruebas[i][0])+' x '+str(pruebas[i][1])+' con '+str(pruebas[i][2])+' minas')
        print('...')
        print('Resolviendo tablero: '+str(pruebas[i][0])+' x '+str(pruebas[i][1])+' con '+str(pruebas[i][2])+' minas')
        animate()
        f = open('Prueba_'+str(pruebas[i][0])+'x'+str(pruebas[i][1])+'_'+str(pruebas[i][2])+'_minas'+'.txt', 'w')
        sys.stdout = f
        start_time = time.time()
        status = aut.autosolver(pruebas[i][0],pruebas[i][1],pruebas[i][2])
        elapsed_time = time.time() - start_time
        print("Tiempo transcurrido:")
        print(str(datetime.timedelta(seconds=elapsed_time)))
        sys.stdout = orig_stdout
        f.close()
        if status == 0:
            success = False
            done = False
            print("Juego perdido, reintentando.")
            print("Tiempo invertido:")
            print(str(datetime.timedelta(seconds=elapsed_time)))
        else:
            success = True
            done = True
            print("¡Juego resuelto!")
            print("Tiempo transcurrido:")
            print(str(datetime.timedelta(seconds=elapsed_time)))
    