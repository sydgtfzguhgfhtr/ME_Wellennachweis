import numpy as np
import matplotlib.pyplot as plt

NUM = 1000

f = [140, 200]
D = [70, 90, 75, 70, 75]
L = [40, 100, 180, 220, 300]

def Verformung(f, D, L, E_Modul):
    def Biegemoment(x):
        if x < f[0]:
            return(-2.332*(x-498.39))
        elif x < f[1]:
            return(7.307*(x-1.414))
        elif x <= max(L):
            return(1.199-2.764*x)
    
    def Wellendurchmesser(x):
        i = 0
        while x > L[i]:
            i += 1
            if i == len(L):
                break
        return(D[i])

    def Ersatzstreckenlast(x):
        q = (64*Biegemoment(x))/(np.pi*Wellendurchmesser(x)**4)
        return(q)

    def Ersatzlagerkraft(x):
        def Ersatzstreckenlast_mal_irgendwas(x):
            return Ersatzstreckenlast(x) * (max(L) - x)

        x = np.linspace(0, max(L), num=NUM)

        Integral = np.trapz(np.vectorize(Ersatzstreckenlast_mal_irgendwas)(x), x)       #np.trapz() -> Integrate along the given axis using the composite trapezoidal rule.
        F_value = 1 / max(L) * Integral                                  #np.vectorize() -> geht sonst nicht mit x als Vektor
        return(F_value)

    def Neigung(x):
        s = np.linspace(0, x, num = NUM)
        Integral = np.trapz(np.vectorize(Ersatzstreckenlast)(s), s)
        phi = (1/E_Modul*(Ersatzlagerkraft(0)-Integral))*1000
        return(phi)

    def Biegung(x):
        def UNTER_BIEGUNG_FUNKTION(s):
            return(Ersatzstreckenlast(s)*(x-s))

        s = np.linspace(0, x, num = NUM)
        Integral = np.trapz(np.vectorize(UNTER_BIEGUNG_FUNKTION)(s), s)   
        f = (1/E_Modul*(Ersatzlagerkraft(0)*x-Integral))*1000000

        return(f)
    


    Mb = np.fromfunction(np.vectorize(Biegung), (max(L), ))
    phi = np.fromfunction(np.vectorize(Neigung), (max(L), ))

    Mb_max = max(max(Mb),abs(min(Mb)))
    phi_max = max(max(phi),abs(min(phi)))

    print(Biegung(200))
    return(Mb, phi)

def Diagramme(Mb, phi):
    plt.subplot(2, 1, 1)
    plt.plot(Mb)
    plt.plot([0, 200],[0, 0],"black")
    plt.title("Biegung")

    plt.subplot(2, 1, 2)
    plt.plot(phi)
    plt.title("Neigung")

    plt.subplots_adjust(hspace=0.4)

    plt.show()

Mb, phi = Verformung(f, D, L, 210000)

Diagramme(Mb, phi)