import sys
import os
import autosolver as aut

counter = 1

for i in range(counter):

    orig_stdout = sys.stdout
    f = open('out'+str(i)+'.txt', 'w')
    sys.stdout = f

    aut.autosolver()

    sys.stdout = orig_stdout
    f.close()