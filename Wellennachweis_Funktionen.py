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


# Formzahl für Absätze, und Ringnuten:
def Formzahl(Absatzart, Belastung, grosser_Durchmesser, kleiner_Durchmesser, Radius):
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

def K3(d, alpha_dBK_beta_dBK):
    """
    Größenfaktor K_3
    d in mm
    """
    if d >= 7.5 and d < 150:
        K_3 = 1-0.2*np.log10(alpha_dBK_beta_dBK)*(np.log10(d/7.5)/np.log10(20))
    elif d >= 150:
        K_3 = 1-0.2*np.log10(alpha_dBK_beta_dBK)


def Kerbwirkungszahl_ohne_Formzahl(Art, d, sigma_B, *argv):
    """
    d = kleiner Durchmesser oder Kerbgrunddurchmesser
    bei umlaufender Rechtecknut : argv = (D, r, Breite_der_Nut, sigma_S)
    Kerbwirkungszahl für Passfedern, Keilwellen, Kerbzahnwellen und Zahnwellen
    returns: (Kerbwirkungszahl für Zug/Druck, Kerbwirkungszahl für Biegung, Kerbwirkungszahl für Torsion)
    """
    if Art == "eine Passfeder":
        # Werte auf d_BK bezogen
        beta_sigma_dBK = 3*(sigma_B/1000)**0.38
        beta_tau_dBK = 0.56*beta_sigma_dBK+0.1
        d_BK = 15
        # Werte auf Bauteildurchmesser bezogen:
        beta_sigma = beta_sigma_dBK*K3(d_BK)/K3(d)
        beta_tau = beta_tau_dBK*K3(d_BK)/K3(d)
        beta_zd = 1
    elif Art == "zwei Passfedern":
        # Werte auf d_BK bezogen
        beta_sigma_dBK = (3*(sigma_B/1000)**0.38)*1.15
        beta_tau_dBK = 0.56*beta_sigma_dBK+0.1
        d_BK = 15
        # Werte auf Bauteildurchmesser bezogen
        beta_sigma = beta_sigma_dBK*K3(d_BK)/K3(d)
        beta_tau = beta_tau_dBK*K3(d_BK)/K3(d)
        beta_zd = 1
    elif Art == "Pressverband":
        # Werte auf d_BK bezogen
        beta_sigma_dBK = 2.7*(sigma_B/1000)**0.43
        beta_tau_dBK = 0.65*beta_sigma_dBK
        d_BK = 40
        # Werte auf Bauteildurchmesser bezogen
        beta_sigma = beta_sigma_dBK*K3(d_BK)/K3(d)
        beta_tau = beta_tau_dBK*K3(d_BK)/K3(d)
        beta_zd = 1
    elif Art == "Keilwelle" or Art == "Kerbzahnwelle" or Art == "Zahnwelle":
        # Werte auf d_BK bezogen:
        beta_tau_stern = math.e**(4.2*10**(-7)*(sigma_B)**2)
        d_BK = 29
        match Art:
            case "Keilwelle":
                beta_sigma_dBK = 1+0.45*(beta_tau_stern-1)
                beta_tau_dBK = beta_tau_stern
            case "Kerbzahnwelle":
                beta_sigma_dBK = 1+0.65*(beta_tau_stern-1)
                beta_tau_dBK = beta_tau_stern
            case "Zahnwelle":
                beta_sigma_dBK = 1+0.49*(beta_tau_stern-1)
                beta_tau_dBK = 1+0.75*(beta_tau_stern-1)
        # Werte auf Bauteildurchmesser bezogen
        beta_sigma = beta_sigma_dBK*K3(d_BK)/K3(d)
        beta_tau = beta_tau_dBK*K3(d_BK)/K3(d)
        beta_zd = 1
    elif Art == "Spitzkerbe":
        # Werte auf d_BK bezogen
        beta_zd_dBK = 0.109*sigma_B
        beta_sigma_dBK = 0.0923 * sigma_B
        beta_tau_dBK = 0.8*beta_sigma_dBK
        d_BK = 15
        # Werte auf Bauteildurchmesser bezogen
        beta_sigma = beta_sigma_dBK*K3(d_BK)/K3(d)
        beta_tau = beta_tau_dBK*K3(d_BK)/K3(d)
        beta_zd = beta_zd_dBK*K3(d_BK)/K3(d)
    elif Art == "umlaufende Rechtecknut":
        # Werte aud d_BK bezogen
        d_BK = 30
        (D,r,m,sigma_S) = argv
        t = (D-d)/2
        Zug_Druck = (0.9, 1.27, 1.17, 2.9)
        Biegung = (0.9, 1.14, 1.08, 2.9)
        Torsion = (1, 1.48, 0.45, 1)
        rho = 0.306196*(0.996506)**sigma_S
        beta_zd_stern = Zug_Druck[0]*(Zug_Druck[1]+Zug_Druck[2]*np.sqrt(t/(r+Zug_Druck[3]*rho)))
        beta_sigma_stern = Biegung[0]*(Biegung[1]+Biegung[2]*np.sqrt(t/(r+Biegung[3]*rho)))
        beta_tau_stern = Torsion[0]*(Torsion[1]+Torsion[2]*np.sqrt(t/(r+Torsion[3]*rho)))
        m_t = m/t
        if m_t >= 1.4:
            beta_zd_dBK = beta_zd_stern
            beta_sigma_dBK = beta_sigma_stern
            beta_tau_dBK = beta_tau_stern
        else:
            beta_zd_dBK = beta_zd_stern*1.08*(m_t)**(-0.2)
            beta_sigma_dBK = beta_sigma_stern*1.08*(m_t)**(-0.2)
            beta_tau_dBK = beta_tau_stern*1.08*(m_t)**(-0.2)    
        # Werte auf Bauteildurchmesser bezogen
        beta_sigma = beta_sigma_dBK*K3(d_BK)/K3(d)
        beta_tau = beta_tau_dBK*K3(d_BK)/K3(d)
        beta_zd = beta_zd_dBK*K3(d_BK)/K3(d)
    Ergebnis = (beta_zd, beta_sigma, beta_tau)
    return Ergebnis

def Kerbwirkungszahl_mit_formzahl(alpha_sigma, alpha_tau, Werkstoff, Art, r, D, d, sigma_S):
    """
    returns = [
    beta_sigma,
    beta_tau
    ]
    """
    def n(G_s, W):
        """
        Stützzahl berechnen
        """
        Material: Werkstoff
        Material = Werkstoff.Werkstoffe[W]
        if Material.art in ("Vergütungsstahl", "Einatzstahl"):
            n = 1 + np.sqrt(G_s)*10**(-(0.33+(sigma_S)/712))
        elif Material.art == "Nitrierstahl":
            n = 1 + np.sqrt(G_s)*10**(-0.7)
        else:
            n = 1

    if (D-d)/d <= 0.5:
        phi = 1/(np.sqrt(8*(D-d)/r)+2)
    else:
        phi = 0

    if Art == "Absatz":
        G_s_sigma = 2.3/r*(1/phi)
        G_s_tau = 1.15/r
    elif Art == "umlaufende Rundnut":
        G_s_sigma = 2/r*(1+phi)
        G_s_tau = 1/r

    beta_sigma = alpha_sigma/n(G_s_sigma, Werkstoff)
    beta_tau = alpha_tau/n(G_s_tau,Werkstoff)
    return (beta_sigma, beta_tau)