"""
Funktionssammlung zur Durchführung eines Wellennachweis.
"""

# Importe:
import numpy as np
import math
from Klassen import Werkstoff

Werkstoff.aus_csv_laden() # Werkstoffdaten laden

# Benötigte gegebene Größen:
Durchmesser = 50
Art_der_Schwächung = "Absatz"



"""
Spannungsverläufe:
"""
def Spannungsverlaeufe():
    pass
        

"""
1. Bauteilwechselfestigkeiten
"""
# Zugfestigkeit und Streckgrenze in Abhängigkeit des technologische Größeneinflussfaktors
def K1(D, B_oder_S, werkstoff):
    """
    !fertig!
    """
    w = Werkstoff.Werkstoffe[werkstoff]
    if B_oder_S == "B":
        if w.art == "Nitrierstahl" or w.art == "Baustahl":
            if D <= 100:
                K_1 = 1
            elif D <= 300:
                K_1 = 1-0.23*math.log10(D/100)
            elif D >= 500:
                K_1 = 0.89
            else:
                raise ValueError("Welle nicht über 500mm bei K1\nsigma_B und Nitrierstahl oder Baustahl")
        elif w.art == "Vergütungsstahl" or (w.art == "Einsatzstahl" and w.Cr_Ni_Einsatzstahl == 1):
            if D <= 16:
                K_1 = 1
            elif D <= 300:
                K_1 = 1-0.26*math.log10(D/16)
            elif D >= 500:
                K_1 = 0.67
            else:
                raise ValueError("Welle nicht über 500mm bei K1\nsigma_B und Vergütungsstahl und Cr-Ni-Einsatzstahl")
        elif w.art == "Einsatzstahl" and w.Cr_Ni_Einsatzstahl == 0:
            if D <= 16:
                K_1 = 1
            elif D <= 150:
                K_1 = 1-0.41*math.log10(D/16)
            elif D >= 500:
                K_1 = 0.6
            else:
                raise ValueError("Welle nicht über 500mm bei K1\nsigma_B und Einsatzstahl ohne Cr-Ni-Einsatzstahl")
    elif B_oder_S == "S":
        if w.art == "Nitrierstahl":
            if D <= 100:
                K_1 = 1
            elif D <= 300:
                K_1 = 1-0.23*math.log10(D/100)
            elif D >= 500:
                K_1 = 0.89
            else:
                raise ValueError("Welle nicht über 500mm bei K1\nsigma_S und Nitrierstahl")
        elif w.art == "Baustahl":
            if D <= 32:
                K_1 = 1
            elif D <= 300:
                K_1 = 1-0.26*math.log10(D/100)
            elif D >= 500:
                K_1 = 0.75
            else:
                raise ValueError("Welle nicht über 500mm bei K1\nsigma_S und Baustahl")
        elif w.art == "Einstazstahl" and w.Cr_Ni_Einsatzstahl == 1:
            if D <= 16:
                K_1 = 1
            elif D <= 300:
                K_1 = 1-0.26*math.log10(D/16)
            elif D >= 500:
                K_1 = 0.67
            else:
                raise ValueError("Welle nicht über 500mm bei K1\nsigma_S und Cr-Ni-Einsatzstahl")
        elif w.art == "Vergütungsstahl":
            if D <= 16:
                K_1 = 1
            elif D <= 300:
                K_1 = 1-0.34*math.log10(D/16)
            elif D >= 500:
                K_1 = 0.57
            else:
                raise ValueError("Welle nicht über 500mm bei K1\nsigma_S und Vergütungsstahl")
        elif w.art == "Einsatzstahl" and w.Cr_Ni_Einsatzstahl == 0:
            if D <= 16:
                K_1 = 1
            elif D <= 150:
                K_1 = 1-0.41*math.log10(D/16)
            elif D >= 500:
                K_1 = 0.6
            else:
                raise ValueError("Welle nicht über 500mm bei K1\nsigma_S und Einsatzstahl ohne Cr-Ni-Einsatzstahl")
    else:
        raise ValueError("bei K1 Werkstoff wurde nicht zugeordnet")
    return K_1

def Zugfestigkeit(D, werkstoff, sigma_B):
    """
    !fertig!
    """
    K_1 = K1(D, "B", werkstoff)
    return(sigma_B*K_1)

def Streckgrenze(D, werkstoff, sigma_S):
    """
    !fertig!
    """
    K_1 = K1(D, "S", werkstoff)
    return(sigma_S*K_1)

# Kerbwirkungszahlen
def Formzahl(Absatzart, Belastung, grosser_Durchmesser, kleiner_Durchmesser, Radius):
    """
    !fertig!
    """
    def Formzahl_Unterfunktion_Formel(A,B,C,z,d,D,r,t):
        a = 1+ 1/(np.sqrt(A*r/t+2*B*r/d*(1+2*r/d)**2+C*(r/t)**z*d/D))
        return a
    t = (grosser_Durchmesser-kleiner_Durchmesser)/2
    if Absatzart == "umlaufende Rundnut":
        match Belastung:
            case "Zug/Druck":
                alpha = Formzahl_Unterfunktion_Formel(0.22,1.37,0,0,kleiner_Durchmesser,grosser_Durchmesser,Radius,t)
            case "Biegung":
                alpha = Formzahl_Unterfunktion_Formel(0.2,2.75,0,0,kleiner_Durchmesser,grosser_Durchmesser,Radius,t)
            case "Torsion":
                alpha = Formzahl_Unterfunktion_Formel(0.7,10.3,0,0,kleiner_Durchmesser,grosser_Durchmesser,Radius,t)
    elif Absatzart == "Absatz":
        match Belastung:
            case "Zug/Druck":
                alpha = Formzahl_Unterfunktion_Formel(0.62,3.5,0,0,kleiner_Durchmesser,grosser_Durchmesser,Radius,t)
            case "Biegung":
                alpha = Formzahl_Unterfunktion_Formel(0.62,5.8,0.2,3,kleiner_Durchmesser,grosser_Durchmesser,Radius,t)
            case "Torsion":
                alpha = Formzahl_Unterfunktion_Formel(3.4,19,1,2,kleiner_Durchmesser,grosser_Durchmesser,Radius,t)
    return alpha

def Kerbwirkungszahl_ohne_Formzahl(Art, sigma_B, D, werkstoff):
    sigma_B_d = Zugfestigkeit(D, werkstoff, sigma_B)
    match Art:
        case "eine Passfeder":
            beta_sigma_dBK = 3*(sigma_B_d/1000)**0.38
            print(beta_sigma_dBK)
            beta_tau_dBK = 0.56*beta_sigma_dBK+0.1
            beta_zd = 1
            beta_sigma = beta_sigma_dBK*K3_dBK_durch_K3_D(D, 40, beta_sigma_dBK)
            beta_tau = beta_tau_dBK*K3_dBK_durch_K3_D(D, 40, beta_sigma_dBK)
        case "zwei Passfedern":
            beta_sigma_dBK = 3*(sigma_B_d/1000)**0.38
            print(beta_sigma_dBK)
            beta_tau_dBK = 0.56*beta_sigma_dBK+0.1
            beta_zd = 1
            beta_sigma = beta_sigma_dBK*K3_dBK_durch_K3_D(D, 40, beta_sigma_dBK)
            beta_sigma = 1.15*beta_sigma*K3_dBK_durch_K3_D(D, 40, beta_sigma_dBK)
            beta_tau = beta_tau_dBK
        case "Pressverbindung":
            beta_sigma_dBK = 2.7*(sigma_B_d/1000)**0.43
            print(beta_sigma_dBK)
            beta_tau_dBK = 0.65*beta_sigma_dBK+0.1
            beta_zd = 1
            beta_sigma = beta_sigma_dBK*K3_dBK_durch_K3_D(D, 40, beta_sigma_dBK)
            beta_tau = beta_tau_dBK*K3_dBK_durch_K3_D(D, 40, beta_sigma_dBK)
        case "Keilwelle":
            beta_tau_dBK_stern = math.e**(4.2*10**(-7)*sigma_B_d**2)
            beta_tau_dBK = beta_tau_dBK_stern
            beta_sigma_dBK = 1+0.45*(beta_tau_dBK_stern-1)
            beta_zd = 1
            beta_sigma = beta_sigma_dBK*K3_dBK_durch_K3_D(D, 29, beta_sigma_dBK)
            beta_tau = beta_tau_dBK*K3_dBK_durch_K3_D(D, 29, beta_sigma_dBK)
        case "Kerbzahnwelle":
            beta_tau_dBK_stern = math.e**(4.2*10**(-7)*sigma_B_d**2)
            beta_tau_dBK = beta_tau_dBK_stern
            beta_sigma_dBK = 1+0.65*(beta_tau_dBK_stern-1)
            beta_zd = 1
            beta_sigma = beta_sigma_dBK*K3_dBK_durch_K3_D(D, 29, beta_sigma_dBK)
            beta_tau = beta_tau_dBK*K3_dBK_durch_K3_D(D, 29, beta_sigma_dBK)
        case "Zahnwelle":
            beta_tau_dBK_stern = math.e**(4.2*10**(-7)*sigma_B_d**2)
            beta_tau_dBK = 1+0.75*(beta_tau_dBK_stern-1)
            beta_sigma_dBK = 1+0.49*(beta_tau_dBK_stern-1)
            beta_zd = 1
            beta_sigma = beta_sigma_dBK*K3_dBK_durch_K3_D(D, 29, beta_sigma_dBK)
            beta_tau = beta_tau_dBK*K3_dBK_durch_K3_D(D, 29, beta_sigma_dBK)
        case "Spitzkerbe":
            beta_zd_dBK = 0.109*sigma_B_d
            beta_sigma_dBK = 0.0923*sigma_B_d
            beta_tau_dBK = 0.8*beta_sigma_dBK
            beta_sigma = beta_sigma_dBK*K3_dBK_durch_K3_D(D, 15, beta_sigma_dBK)
            beta_tau = beta_tau_dBK*K3_dBK_durch_K3_D(D, 15, beta_sigma_dBK)
            beta_zd = beta_zd_dBK*K3_dBK_durch_K3_D(D, 159, beta_sigma_dBK)

    return(beta_sigma, beta_tau, beta_zd)

def Kerbwirkungszahl_für_Rechtecknut(sigma_S ,grosser_Durchmesser, kleiner_Durchmesser, Radius, Breite_der_Nut):
    """
    !fertig!
    """
    D = grosser_Durchmesser
    d = kleiner_Durchmesser
    m = Breite_der_Nut
    t = (D-d)/2
    r = Radius

    rho_s = 10**(-(0.514+0.00152*sigma_S))
    beta_zd_stern = 0.9*(1.27+1.17*(np.sqrt(t/(r+2.9*rho_s))))
    beta_sigma_stern = 0.9*(1.14+1.08*(np.sqrt(t/(r+2.9*rho_s))))
    beta_tau_stern = 1*(1.48+0.45*(np.sqrt(t/(r+1*rho_s))))
    
    if m/t >= 1.4:
        beta_zd_dBK = beta_zd_stern
        beta_sigma_dBK = beta_sigma_stern
        beta_tau_dBK = beta_tau_stern
    else:
        beta_zd_dBK = beta_zd_stern*1.08*(m/t)**(-0.2)
        beta_sigma_dBK = beta_sigma_stern*1.08*(m/t)**(-0.2)
        beta_tau_dBK = beta_tau_stern*1.08*(m/t)**(-0.2)

    beta_sigma = beta_sigma_dBK*K3_dBK_durch_K3_D(d, 30, beta_sigma_dBK)
    beta_zd = beta_zd_dBK*K3_dBK_durch_K3_D(d, 30, beta_zd_dBK)
    beta_tau = beta_tau_dBK*K3_dBK_durch_K3_D(d, 30, beta_tau_dBK)

    return(beta_sigma, beta_tau, beta_zd)

def Kerbwirkungszahl_mit_Fromzahl(werkstoff, sigma_S, alpha_zd, alpha_sigma, alpha_tau, Art, D, d, r):
    """
    !fertig!
    """
    sigma_S = Streckgrenze(D, werkstoff, sigma_S)
    if ((D-d)/d <= 0.5):
        phi = 1/(np.sqrt(8*(D-d)/r)+2)
    else: 
        phi = 0

    if Art == "Absatz":
        G_s_zd = 2.3/r*(1+phi)
        G_s_sigma = G_s_zd
        G_s_tau = 1.15/r
    elif Art == "umlaufende Rundnut":
        G_s_zd = 2/r*(1+phi)
        G_s_sigam = G_s_zd
        G_s_tau = 1/r

    w = Werkstoff.Werkstoffe[werkstoff]
    if w.art == "Vergütungsstahl" or w.art == "Einsatzstahl" or w.art == "Automatenstahl" or w.art == "Baustahl":
        n_zd = 1+np.sqrt(G_s_zd)*10**(-(0.33+sigma_S/712))
        n_sigma = 1+np.sqrt(G_s_sigma)*10**(-(0.33+sigma_S/712))
        n_tau = 1+np.sqrt(G_s_tau)*10**(-(0.33+sigma_S/712))
    elif w.art == "Nitrierstahl":
        n_zd = 1+np.sqrt(G_s_zd)*10**(-0.7)
        n_sigma = 1+np.sqrt(G_s_sigma)*10**(-0.7)
        n_tau = 1+np.sqrt(G_s_tau)*10**(-0.7)

    beta_zd = alpha_zd/n_zd
    beta_sigma = alpha_sigma/n_sigma
    beta_tau = alpha_tau/n_tau

    return(beta_zd, beta_sigma, beta_tau)

def K3_dBK_durch_K3_D(d, dBK, alpha_dBK_beta_dBK):
    """
    Größenfaktor K_3
    d in mm
    !fertig!
    """
    if d >= 7.5 and d < 150:
        K_3_dBK = 1-0.2*np.log10(alpha_dBK_beta_dBK)*(np.log10(dBK/7.5)/np.log10(20))
    elif d >= 150:
        K_3_dBK = 1-0.2*np.log10(alpha_dBK_beta_dBK)

    if d >= 7.5 and d < 150:
        K_3_d = 1-0.2*np.log10(alpha_dBK_beta_dBK)*(np.log10(d/7.5)/np.log10(20))
    elif d >= 150:
        K_3_d = 1-0.2*np.log10(alpha_dBK_beta_dBK)
    return(K_3_dBK/K_3_d)

def K2(d):
    """
    !fertig!
    """
    if d < 150:
        K_2 = 1-0.2*(math.log10(d/7.5))/math.log10(20)
    else:
        K_2 = 0.8
    return(K_2)

def KF(Rz, sigma_B, werkstoff, D):
    """
    !fertig! 
    aber in Übungspdf steht nichts weiter aber in gelösten Übungsaufgaben manchmal anders gemacht (keine Ahnung warum?)
    """
    sigma_B = Zugfestigkeit(D, werkstoff, sigma_B)
    K_F_sigma = 1-0.22*math.log10(Rz)*(math.log10(sigma_B/20)-1)
    K_F_tau = 0.575*K_F_sigma+0.425

    return(K_F_sigma, K_F_tau)

def KV(Oberflächenverfestigung, D, Art):
    """
    !fertig!: 
    irgendwie komisch beschrieben in pdf, vielleicht ist KV auch immer 1?
    """
    if Art == "umlaufende Rundnut" or Art == "Absatz":
        K_V = 1
    match Oberflächenverfestigung:
        case "nein":
            K_V = 1
        case "Nitrieren":
            if D < 25:
                K_V = 1.5
            elif D < 40:
                K_V = 1.2
            else:
                K_V = 1
        case "Einsatzhärten":
            if D < 25:
                K_V = 1.5
            elif D < 40:
                K_V = 1.2
            else:
                K_V = 1
        case "Karbonierhärten":
            if D < 25:
                K_V = 1.4
            elif D <40:
                K_V = 1.1
            else:
                K_V = 1
        case "Festwalzen":
            if D < 25:
                K_V = 1.5
            elif D < 40:
                K_V = 1.3
            else:
                K_V = 1
        case "Kugelstrahlen":
            if D < 25:
                K_V = 1.4
            elif D < 40:
                K_V = 1.1
            else:
                K_V = 1
        case "Flammhärten":
            if D < 25:
                K_V = 1.4
            elif D < 40:
                K_V = 1.2
            elif D < 250:
                K_V = 1.1
            else:
                K_V = 1
    return(K_V)

def Gesamtgrößeneinflussfaktor(D, d, sigma_B, beta_sigma, beta_tau, Rz, werkstoff, Oberflächenverfetigung, Art):
    """
    !fertig!
    """
    sigma_B = Zugfestigkeit(D, werkstoff, sigma_B)
    K_2 = K2(d)
    K_V = KV(Oberflächenverfetigung, D, Art)
    (K_F_sigma, K_F_tau) = KF(Rz, sigma_B, werkstoff, D)
    K_sigma = ((beta_sigma/K_2)+(1/K_F_sigma)-1)*(1/K_V)
    K_tau = ((beta_tau/K_2)+(1/K_F_tau)-1)*(1/K_V)

    return(K_sigma, K_tau)

def Bauteilwechselfestigkeiten(D, werkstoff, K_sigma, K_tau, sigma_bW, tau_tW):
    K_1 = K1(D, "B", werkstoff)

    sigma_bWK = (K_1*sigma_bW)/K_sigma
    tau_tWK = (K_1*tau_tW)/K_tau

    return(sigma_bWK, tau_tWK)


print(Bauteilwechselfestigkeiten(50, "34CrMo4", 1.801, 1.473, 500, 300))