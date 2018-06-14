import sys
import os
import autosolver as aut

counter = 1

pruebas = ([5,5,5],[5,5,6],[5,5,7],[8,8,13],[8,8,14],[8,8,15],[10,10,23],[10,10,24],[10,10,25])


for i in range(len(pruebas)):

    orig_stdout = sys.stdout
    f = open('Prueba_'+str(pruebas[i][0])+'x'+str(pruebas[i][1])+'_'+str(pruebas[i][2])+'minas'+'.txt', 'w')
    sys.stdout = f

    aut.autosolver(pruebas[i][0],pruebas[i][1],pruebas[i][2])

    sys.stdout = orig_stdout
    f.close()