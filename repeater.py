import sys
import os
import autosolver as aut
import time
import datetime
from functools import wraps
pruebas = ([5,5,5],[5,5,6],[5,5,7],[8,8,13],[8,8,14],[8,8,15],[10,10,23],[10,10,24],[10,10,25])


for i in range(0,len(pruebas)-1):
    success = False
    while not success:
        orig_stdout = sys.stdout
        print('Resolviendo tablero: '+str(pruebas[i][0])+'x'+str(pruebas[i][1])+'_con_'+str(pruebas[i][2])+'minas')
        f = open('Prueba_'+str(pruebas[i][0])+'x'+str(pruebas[i][1])+'_'+str(pruebas[i][2])+'_minas'+'.txt', 'w')
        sys.stdout = f
        start_time = time.time()
        status = aut.autosolver(pruebas[i][0],pruebas[i][1],pruebas[i][2])
        elapsed_time = time.time() - start_time
        print("Tiempo transcurrido")
        print(str(datetime.timedelta(seconds=elapsed_time)))
        sys.stdout = orig_stdout
        f.close()
        print(str(datetime.timedelta(seconds=elapsed_time)))
        if status == 0:
            success = False
        else:
            success = True
    