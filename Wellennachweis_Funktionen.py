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

def Kerbwirkungszahl_nach_Bezugsdurchmesser(Art, sigma_B, *argv):
    """
    bei umlaufender Rechtecknut : argv = (D, d, r, Breite_der_Nut, sigma_S)
    Kerbwirkungszahl für Passfedern, Keilwellen, Kerbzahnwellen und Zahnwellen
    returns: (Kerbwirkungszahl für Zug/Druck, Kerbwirkungszahl für Biegung, Kerbwirkungszahl für Torsion)
    """
    if Art == "eine Passfeder":
        beta_sigma = 3*(sigma_B/1000)**0.38
        beta_tau = 0.56*beta_sigma+0.1
        beta_zd = 1
    elif Art == "zwei Passfedern":
        beta_sigma = (3*(sigma_B/1000)**0.38)*1.15
        beta_tau = 0.56*beta_sigma+0.1
        beta_zd = 1
    elif Art == "Pressverband":
        beta_sigma = 2.7*(sigma_B/1000)**0.43
        beta_tau = 0.65*beta_sigma
        beta_zd = 1
    elif Art == "Keilwelle" or Art == "Kerbzahnwelle" or Art == "Zahnwelle":
        beta_tau_stern = math.e**(4.2*10**(-7)*(sigma_B)**2)
        beta_zd = 1
        match Art:
            case "Keilwelle":
                beta_sigma = 1+0.45*(beta_tau_stern-1)
                beta_tau = beta_tau_stern
            case "Kerbzahnwelle":
                beta_sigma = 1+0.65*(beta_tau_stern-1)
                beta_tau = beta_tau_stern
            case "Zahnwelle":
                beta_sigma = 1+0.49*(beta_tau_stern-1)
                beta_tau = 1+0.75*(beta_tau_stern-1)
    elif Art == "Spitzkerbe":
        beta_zd = 0.109*sigma_B
        beta_sigma = 0.0923 * sigma_B
        beta_tau = 0.8*beta_sigma
    elif Art == "umlaufende Rechtecknut":
        (D,d,r,m,sigma_S) = argv
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
            beta_zd = beta_zd_stern
            beta_sigma = beta_sigma_stern
            beta_tau = beta_tau_stern
        else:
            beta_zd = beta_zd_stern*1.08*(m_t)**(-0.2)
            beta_sigma = beta_sigma_stern*1.08*(m_t)**(-0.2)
            beta_tau = beta_tau_stern*1.08*(m_t)**(-0.2)    
    Ergebnis = (beta_zd, beta_sigma, beta_tau)
    return Ergebnis

