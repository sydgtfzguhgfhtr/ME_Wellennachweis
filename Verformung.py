import numpy as np
import matplotlib.pyplot as plt
from Klassen import Welle

lab2 = 290
lz21 = 95
lz22 = 115
düb = 75
z_ritzel = 20
r_ritzel = 10
z_rad = 135
r_rad = 27.5

test = Welle("Zwischenwelle",lab2)
test.set_geometrie([
    (0,10),
    (40,10),
    (40,20),
    (80,20),
    (80,27.5),
    (160,15),
    (195,15)
])

test.set_Kraft(0,"a",z_rad,r_rad,0)
test.set_Kraft(3500,"r",z_rad,r_rad,0) # Rad z12
test.set_Kraft(0,"t",z_rad,r_rad,0)

test.set_Kraft(0,"a",z_ritzel,r_ritzel,0)
test.set_Kraft(-4500,"r",z_ritzel,r_ritzel,0) # Ritzel z21
test.set_Kraft(0,"t",z_ritzel,r_ritzel,0)

test.lagerkräfte_berechnen()

E = 210000000

NUM = 1000

def Spannungsverlauf_x(x):
    Wb = np.pi/32 * test.d(x)**3
    sigma = test.Mbx(x)/Wb
    return(sigma)

def Spannungsverlauf_y(x):
    Wb = np.pi/32 * test.d(x)**3
    sigma = test.Mby(x)/Wb
    return(sigma)

def Verformung(W: Welle):

    E_Modul = 210000

    L = W.länge

    def Ersatzstreckenlast_x(x):
        q_x = (64*W.Mbx(x))/(np.pi*W.d(x)**4)
        return(q_x)

    def Ersatzstreckenlast_y(x):
        q_y = (64*W.Mby(x))/(np.pi*W.d(x)**4)
        return(q_y)

    def Ersatzlagerkraft_x(x):
        def Ersatzstreckenlast_mal_irgendwas(x):
            return Ersatzstreckenlast_x(x) * (L - x)

        x = np.linspace(0, L, num=NUM)

        Integral = np.trapz(np.vectorize(Ersatzstreckenlast_mal_irgendwas)(x), x)       #np.trapz() -> Integrate along the given axis using the composite trapezoidal rule.
        F_value = 1 / L * Integral                                  #np.vectorize() -> geht sonst nicht mit x als Vektor
        return(F_value)
    
    def Ersatzlagerkraft_y(x):
        def Ersatzstreckenlast_mal_irgendwas(x):
            return Ersatzstreckenlast_y(x) * (L - x)

        x = np.linspace(0, L, num=NUM)

        Integral = np.trapz(np.vectorize(Ersatzstreckenlast_mal_irgendwas)(x), x)       #np.trapz() -> Integrate along the given axis using the composite trapezoidal rule.
        F_value = 1 / L * Integral                                  #np.vectorize() -> geht sonst nicht mit x als Vektor
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
    


    Mb_x = np.fromfunction(np.vectorize(Biegung_x), (L, ))
    phi_x = np.fromfunction(np.vectorize(Neigung_x), (L, ))

    Mb_y = np.fromfunction(np.vectorize(Biegung_y), (L, ))
    phi_y = np.fromfunction(np.vectorize(Neigung_y), (L, ))    



    print(Biegung_x(200))
    return(Mb_x, phi_x, Biegung_x(200), Mb_y, phi_y, Biegung_y(200))


def Diagramme(W: Welle, Mb_x, phi_x, f_Lager_x, Lager1_x, Lager2_x, Mb_y, phi_y, f_Lager_y):

    L = W.länge

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

    sigma_x = np.fromfunction(np.vectorize(Spannungsverlauf_x), (L, ))
    sigma_y = np.fromfunction(np.vectorize(Spannungsverlauf_y), (L, ))

    plt.subplot(2, 2, 3)
    plt.plot(sigma_x, label = "sigma_x")
    plt.plot(sigma_y, label = "sigma_y")
    plt.grid(True)
    plt.legend()
    plt.title("Spannung")

    plt.subplots_adjust(hspace=0.4)

    plt.show()

Mb_x, phi_x, f_Lager_x, Mb_y, phi_y, f_Lager_y = Verformung(test)

Diagramme(test, Mb_x, phi_x, f_Lager_x, 0, test.länge, Mb_y, phi_y, f_Lager_y)