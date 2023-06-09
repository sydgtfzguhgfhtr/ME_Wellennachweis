import numpy as np
import matplotlib.pyplot as plt

NUM = 1000

f = [110]
D = [200, 200]
L = [110, 480]

def Biegemoment_x(x):
    if x < f[0]:
        return((-10298*x)/1000)
    elif x <= max(L):
        return((306822.5+90819.46+398.04-829.25*x)/1000)
    
def Biegemoment_y(x):
    if x < f[0]:
        return((-19372*x)/1000)
    elif x <= max(L):
        return((5759.2*x-2764.4-630747.6-2111548)/1000)

print(Biegemoment_x(140))

def Wellendurchmesser(x):
    i = 0
    while x > L[i]:
        i += 1
        if i == len(L):
            break
    return(D[i])


def Spannungsverlauf_x(x):
    Wb = np.pi/32 * Wellendurchmesser(x)**3
    sigma = Biegemoment_x(x)/Wb
    return(sigma)

def Spannungsverlauf_y(x):
    Wb = np.pi/32 * Wellendurchmesser(x)**3
    sigma = Biegemoment_y(x)/Wb
    return(sigma)

def Verformung(f, D, L, E_Modul):


    def Ersatzstreckenlast_x(x):
        q_x = (64*Biegemoment_x(x))/(np.pi*Wellendurchmesser(x)**4)
        return(q_x)

    def Ersatzstreckenlast_y(x):
        q_y = (64*Biegemoment_y(x))/(np.pi*Wellendurchmesser(x)**4)
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

    return(Mb_x, phi_x, Biegung_x(200), Mb_y, phi_y, Biegung_y(200))


def Diagramme(Mb_x, phi_x, f_Lager_x, Lager1_x, Lager2_x, Mb_y, phi_y, f_Lager_y):

    
    print("NICHT VERSCHOBEN")
    Mb_verschoben_x = Mb_x
    Mb_verschoben_y = Mb_y


    plt.subplot(2, 2, 1)
    plt.plot(Mb_verschoben_x, label = "$Mb_x$")
    plt.plot(Mb_verschoben_y, label = "$Mb_y$")
    plt.grid(True)
    plt.legend()
    plt.title("Biegung")

    plt.subplot(2, 2, 2)
    plt.plot(phi_x, label = r"$\varphi_x$")
    plt.plot(phi_y, label = r"$\varphi_y$")
    plt.grid(True)
    plt.legend()
    plt.title("Neigung")

    sigma_x = np.fromfunction(np.vectorize(Spannungsverlauf_x), (max(L), ))
    sigma_y = np.fromfunction(np.vectorize(Spannungsverlauf_y), (max(L), ))

    plt.subplot(2, 2, 3)
    plt.plot(sigma_x, label = r"$\sigma_x$")
    plt.plot(sigma_y, label = r"$\sigma_y$")
    plt.grid(True)
    plt.legend()
    plt.title("Spannung")

    plt.subplots_adjust(hspace=0.4)

    plt.show()

Mb_x, phi_x, f_Lager_x, Mb_y, phi_y, f_Lager_y = Verformung(f, D, L, 210000)

Diagramme(Mb_x, phi_x, f_Lager_x, 0, 480, Mb_y, phi_y, f_Lager_y)