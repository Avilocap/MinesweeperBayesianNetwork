import sys
import os


counter = 1

for i in range(counter):

    orig_stdout = sys.stdout
    f = open('out'+str(i)+'.txt', 'w')
    sys.stdout = f

    os.system("autosolver.py 1")

    sys.stdout = orig_stdout
    f.close()