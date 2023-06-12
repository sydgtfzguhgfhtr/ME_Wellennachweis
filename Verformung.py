import numpy as np
import matplotlib.pyplot as plt
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

test.set_Kraft(2191,"a",z_rad,r_rad,0)
test.set_Kraft(2332,"r",z_rad,r_rad,0) # Rad z12
test.set_Kraft(-6021,"t",z_rad,r_rad,0)

test.set_Kraft(-7162,"a",z_ritzel,r_ritzel,0)
test.set_Kraft(10071,"r",z_ritzel,r_ritzel,0) # Ritzel z21
test.set_Kraft(-26727,"t",z_ritzel,r_ritzel,0)

test.lagerkräfte_berechnen()

NUM = 1000

L = [0, max(test.z_daten)]


def Spannungsverlauf_x(x):
    Wb = np.pi/32 * test.d(x)**3
    sigma = test.Mbx(x)/Wb
    return(sigma)

def Spannungsverlauf_y(x):
    Wb = np.pi/32 * test.d(x)**3
    sigma = test.Mby(x)/Wb
    return(sigma)

def Verformung(L, E_Modul):


    def Ersatzstreckenlast_x(x):
        q_x = (64*test.Mbx(x))/(np.pi*test.d(x)**4)
        return(q_x)

    def Ersatzstreckenlast_y(x):
        q_y = (64*test.Mby(x))/(np.pi*test.d(x)**4)
        return(q_y)

    def Ersatzlagerkraft_x(x):
        def Ersatzstreckenlast_mal_irgendwas(x):
            return Ersatzstreckenlast_x(x) * (max(L) - x)

        x = np.linspace(0, max(L), num=NUM)

        Integral = np.trapz(np.vectorize(Ersatzstreckenlast_mal_irgendwas)(x), x)       #np.trapz() -> Integrate along the given axis using the composite trapezoidal rule.
        F_value = 1 / max(L) * Integral                                  #np.vectorize() -> geht sonst nicht mit x als Vektor
        return(F_value)
    
    def Ersatzlagerkraft_y(x):
        def Ersatzstreckenlast_mal_irgendwas(x):
            return Ersatzstreckenlast_y(x) * (max(L) - x)

        x = np.linspace(0, max(L), num=NUM)

        Integral = np.trapz(np.vectorize(Ersatzstreckenlast_mal_irgendwas)(x), x)       #np.trapz() -> Integrate along the given axis using the composite trapezoidal rule.
        F_value = 1 / max(L) * Integral                                  #np.vectorize() -> geht sonst nicht mit x als Vektor
        return(F_value)

    def Neigung_x(x):
        s = np.linspace(0, x, num = NUM)
        Integral = np.trapz(np.vectorize(Ersatzstreckenlast_x)(s), s)
        phi = (1/E_Modul*(Ersatzlagerkraft_x(0)-Integral))*1000
        return(phi)
    
    def Neigung_y(x):
        s = np.linspace(0, x, num = NUM)
        Integral = np.trapz(np.vectorize(Ersatzstreckenlast_y)(s), s)
        phi = (1/E_Modul*(Ersatzlagerkraft_y(0)-Integral))*1000
        return(phi)

    def Biegung_x(x):
        def UNTER_BIEGUNG_FUNKTION(s):
            return(Ersatzstreckenlast_x(s)*(x-s))
        s = np.linspace(0, x, num = NUM)
        Integral = np.trapz(np.vectorize(UNTER_BIEGUNG_FUNKTION)(s), s)   
        f = (1/E_Modul*(Ersatzlagerkraft_x(0)*x-Integral))*1000000
        return(f)
    
    def Biegung_y(x):
        def UNTER_BIEGUNG_FUNKTION(s):
            return(Ersatzstreckenlast_y(s)*(x-s))
        s = np.linspace(0, x, num = NUM)
        Integral = np.trapz(np.vectorize(UNTER_BIEGUNG_FUNKTION)(s), s)   
        f = (1/E_Modul*(Ersatzlagerkraft_y(0)*x-Integral))*1000000
        return(f)
    


    Mb_x = np.fromfunction(np.vectorize(Biegung_x), (max(L), ))
    phi_x = np.fromfunction(np.vectorize(Neigung_x), (max(L), ))

    Mb_y = np.fromfunction(np.vectorize(Biegung_y), (max(L), ))
    phi_y = np.fromfunction(np.vectorize(Neigung_y), (max(L), ))    

    print(Biegung_x(200))
    return(Mb_x, phi_x, Biegung_x(200), Mb_y, phi_y, Biegung_y(200))


def Diagramme(Mb_x, phi_x, f_Lager_x, Lager1_x, Lager2_x, Mb_y, phi_y, f_Lager_y):

    
    print("NICHT VERSCHOBEN")
    Mb_verschoben_x = Mb_x
    Mb_verschoben_y = Mb_y


    plt.subplot(2, 2, 1)
    plt.plot(Mb_verschoben_x, label = "Mb_x")
    plt.plot(Mb_verschoben_y, label = "Mb_y")
    plt.grid(True)
    plt.legend()
    plt.title("Biegung")

    plt.subplot(2, 2, 2)
    plt.plot(phi_x, label = "phi_x")
    plt.plot(phi_y, label = "phi_y")
    plt.grid(True)
    plt.legend()
    plt.title("Neigung")

    sigma_x = np.fromfunction(np.vectorize(Spannungsverlauf_x), (max(L), ))
    sigma_y = np.fromfunction(np.vectorize(Spannungsverlauf_y), (max(L), ))

    plt.subplot(2, 2, 3)
    plt.plot(sigma_x, label = "sigma_x")
    plt.plot(sigma_y, label = "sigma_y")
    plt.grid(True)
    plt.legend()
    plt.title("Spannung")

    plt.subplots_adjust(hspace=0.4)

    plt.show()

Mb_x, phi_x, f_Lager_x, Mb_y, phi_y, f_Lager_y = Verformung(L, 210000)

Diagramme(Mb_x, phi_x, f_Lager_x, 0, 480, Mb_y, phi_y, f_Lager_y)