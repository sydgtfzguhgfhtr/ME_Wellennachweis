from Klassen import Welle
import numpy as np
from scipy.integrate import simps
import matplotlib.pyplot as plt

lab2 = 290
lz21 = 95
lz22 = 115
düb = 75
z_ritzel = lab2-lz22
r_ritzel = 101.46/2
z_rad = lab2+lz21
r_rad = 454.94/2

test = Welle("Zwischenwelle",0,195)
test.set_geometrie([
    [-30,düb*0.8],
    [30,düb*0.8],
    [30,düb],
    [lab2-30,düb],
    [lab2-30,düb*0.8],
    [lab2+lz21-15,düb*0.8],
    [lab2+lz21-15,düb*0.6],
    [lab2+lz21+15,düb*0.6]
])

test.set_Kraft(2191,"a",z_rad,r_rad,0)
test.set_Kraft(2332,"r",z_rad,r_rad,0) # Rad z12
test.set_Kraft(-6021,"t",z_rad,r_rad,0)

test.set_Kraft(-7162,"a",z_ritzel,r_ritzel,0)
test.set_Kraft(10071,"r",z_ritzel,r_ritzel,0) # Ritzel z21
test.set_Kraft(-26727,"t",z_ritzel,r_ritzel,0)

test.lagerkräfte_berechnen()

class Verformung(Welle):
    def __init__(self, name: str, festlager_z, loslager_z) -> None:
        super().__init__(name, festlager_z, loslager_z)

    def Ersatzstreckenlast_x(self, z):
        q = (64*Welle.Mbx(z))/(np.pi*Welle.d(z)**4)
        return(q)
    
    def Ersatzstreckenlast_y(self, z):
        q = (64*Welle.Mby(z))/(np.pi*Welle.d(z)**4)
        return(q)
    
    def Ersatzlagerkraft(self):
        Integral = 0
        1/Welle.Welle.länge * Integral


V = Verformung(test)

q = []

for i in range(test.länge):
    q.append(V.Ersatzstreckenlast_x(i))


plt.plot(q)