import numpy as np
import math
import matplotlib.pyplot as plt


Durchmesser = [0.130, 0.150, 0.130, 0.045]
Längen = [0.065, 0.215, 0.280, 0.341]

def d(x):
    i = 0
    while x > Längen[i]:
        i += 1
        if i == len(Längen):
            break
    return(Durchmesser[i])

def Mb(x):
    if x <= 0.215:
        Mb = 1464.8*x
    elif x <= 0.341:
        Mb = 831.78-2404*x
    return(Mb)

n = np.linspace(start=0, stop=0.341, num=1000)

MB_vec = []

for i in n:
    MB_vec.append(Mb(i))
