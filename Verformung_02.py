import numpy as np
import matplotlib as plt
from Klassen import Welle

lab2 = 290
lz21 = 95
lz22 = 115
düb = 75
z_ritzel = lab2-lz22
r_ritzel = 101.46/2
z_rad = lab2+lz21
r_rad = 454.94/2

test = Welle("Zwischenwelle",lab2)
test.set_geometrie([
    [0,düb*0.8],
    [30,düb*0.8],
    [30,düb],
    [lab2-30,düb],
    [lab2-30,düb*0.8],
    [lab2+lz21-15,düb*0.8],
    [lab2+lz21-15,düb*0.6],
    [lab2+lz21+15,düb*0.6]
])

test.set_Kraft(0,"a",z_rad,r_rad,0)
test.set_Kraft(3500,"r",z_rad,r_rad,0) # Rad z12
test.set_Kraft(0,"t",z_rad,r_rad,0)

test.set_Kraft(0,"a",z_ritzel,r_ritzel,0)
test.set_Kraft(4500,"r",z_ritzel,r_ritzel,0) # Ritzel z21
test.set_Kraft(0,"t",z_ritzel,r_ritzel,0)

test.lagerkräfte_berechnen()

def Verformung(x, W: Welle):
    E_Modul = 210000 #Nmm^-2
    L = max(W.z_daten) # muss noch allgemein aus Klasse Welle kommen
    NUM = 10*L
    z = np.linspace(0, L, num = NUM)

    q_x = []
    q_y = []
    q_x_F_ers = []
    q_y_F_ers = []
    q_x_Biegung = []
    q_y_Biegung = []

    # Ersatzstreckenlasten
    for i in z:
        q_x.append((64*W.Mbx(i))/(np.pi*W.d(i)))
        q_y.append((64*W.Mbx(i))/(np.pi*W.d(i)))
        q_x_F_ers.append((64*W.Mbx(i))/(np.pi*W.d(i))*(L-i))
        q_y_F_ers.append((64*W.Mbx(i))/(np.pi*W.d(i))*(L-i))

    # Ersatzlagerkraft
    F_ers_x = 1 / L * np.trapz(q_x_F_ers, z)
    F_ers_y = 1 / L + np.trapz(q_y_F_ers, z)

    s = np.linspace(0, x, num = NUM)
    # Neigung
    phi_Integral_x = np.trapz(q_x, s)
    phi_x = (1/E_Modul*(F_ers_x-phi_Integral_x))

    phi_Integral_y = np.trapz(q_y, s)
    phi_y = (1/E_Modul*(F_ers_y-phi_Integral_y))

    # Biegefervormung
    for i in s:
        q_x_Biegung.append((64*W.Mbx(i))/(np.pi*W.d(i))*(x-s))
        q_y_Biegung.append((64*W.Mby(i))/(np.pi*W.d(i))*(x-s))

    f_Integral_x = np.trapz(q_x_Biegung, s)[-1]
    f_x = (1/E_Modul*(F_ers_x*x-f_Integral_x))

    f_Integral_y = np.trapz(q_y_Biegung, s)[-1]
    f_y = (1/E_Modul*(F_ers_y*x-f_Integral_y))

    print(f_x)


print(Verformung(2, test))