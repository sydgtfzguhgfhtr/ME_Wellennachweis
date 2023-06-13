from Klassen import Welle, Werkstoff
import numpy as np
import math

Werkstoff.aus_csv_laden()


class Welle_Absatz():
    def __init__(self,welle:Welle,z, Art, *args):
        self.welle = welle
        self.z = z
        self.Art = Art
        if self.Art == "Absatz":
            self.D = max(self.welle.d(self.z-1), self.welle.d(self.z+1))
            self.d = min(self.welle.d(self.z-1), self.welle.d(self.z+1))
            r = args[0]
            self.r = r
            self.t = (self.D-self.d)/2
        if Art == "umlaufende Rundnut":
            d, r, b = args
            self.d = d
            self.r = r
            self.b = b
            self.D = self.welle.d(self.z)
            self.t = (self.D-self.d)/2
        if Art == "umlaufende Rechtecknut":
            t, r, b = args
            self.t = t
            self.r = r
            self.b = b

    def K1(self, B_oder_S):
        """Einflussfaktor K1

        Args:
            D (int): großer Durchmesser
            B_oder_S (str): S: Zugfestigkeit; B: Strekcgrenze 
            werkstoff (str): Werkstoff der Welle

        Returns:
            K_1 (float): Einflussfaktor K1
        """
        D = max(self.welle.d(self.z-1), self.welle.d(self.z+1))
        w = Werkstoff.Werkstoffe[self.welle.werkstoff]
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
        
    def Zugfestigkeit(self):
        """Zugfestigkeit für Durchmesser

        Args:
            D (int): großer Durchmesser der Welle
            werkstoff (str): Werkstoff der Welle
        
        Returns:
            sigma_B: Zugfestigkeit für D
        """
        sigma_B = int(Werkstoff.Werkstoffe[self.welle.werkstoff].sigma_B)
        K_1 = self.K1("B")
        return(sigma_B*K_1)
    
    def Streckgrenze(self):
        """Streckgrenze für Durchmesser

        Args:
            D (int): großer Durchmesser der Welle
            werkstoff (str): Werkstoff der Welle
        Returns:
            sigma_s: Streckgrenze für D
        """
        D = max(self.welle.d(self.z-1), self.welle.d(self.z+1))
        sigma_S = int(Werkstoff.Werkstoffe[self.welle.werkstoff].sigma_S)
        K_1 = self.K1("S")
        return(sigma_S*K_1)

    def K3_dBK_durch_K3_D(self, dBK, alpha_dBK_beta_dBK):
        """K3(dBK)/K3(d)

        Args:
            d (int): Durchmesser der Welle
            dBK (int): Bezugsdurchmesser
            alpha_dBK_beta_dBK (float): Form- oder Kerbwirkungszahl
        Returns:
            K3(dBK/K3(d))
        """
        d = self.welle.d(self.z)
        if d >= 7.5 and d < 150:
            K_3_dBK = 1-0.2*np.log10(alpha_dBK_beta_dBK)*(np.log10(dBK/7.5)/np.log10(20))
        elif d >= 150:
            K_3_dBK = 1-0.2*np.log10(alpha_dBK_beta_dBK)

        if d >= 7.5 and d < 150:
            K_3_d = 1-0.2*np.log10(alpha_dBK_beta_dBK)*(np.log10(d/7.5)/np.log10(20))
        elif d >= 150:
            K_3_d = 1-0.2*np.log10(alpha_dBK_beta_dBK)
        return(K_3_dBK/K_3_d)
    
    def Kerbwirkungszahl(self):
        """Berechnung der Kerbwirkungszahlen

        Args:
            Art (str): Art der Querschnittsschwächung
            werkstoff (str): Werkstoff der Welle
            D (int): großer Durchmesser

            wenn Art == umlaufende Rechtecknut
            argv = (kleiner Durchmesser, Radius, Breite der Nut)

            wenn Art == Absatz
            argv = (kleiner Durchmesser, Radius)

            wenn Art == umlaufende Rundnut
            argv = (kleiner Durchmesser, Radius)

        Returns:
            beta_sigma (float): Kerbwirkungszahl Biegung
            beta_tau (float): Kerbwirkungszahl Torsion
            beta_zd (float): Kerbwirkungszahl Zug/Druck
        """
        Art = self.Art
        D = max(self.welle.d(self.z-1), self.welle.d(self.z+1))
        d = self.welle.d(self.z)
        def Formzahl_Unterfunktion_Formel(A,B,C,z,d,D,r,t):
            a = 1+ 1/(np.sqrt(A*r/t+2*B*r/d*(1+2*r/d)**2+C*(r/t)**z*d/D))
            return a
        
        sigma_B_d = self.Zugfestigkeit()
        if Art == "eine Passfeder":
            beta_sigma_dBK = 3*(sigma_B_d/1000)**0.38
            beta_tau_dBK = 0.56*beta_sigma_dBK+0.1
            beta_zd = 1
            beta_sigma = beta_sigma_dBK*self.K3_dBK_durch_K3_D(40, beta_sigma_dBK)
            beta_tau = beta_tau_dBK*self.K3_dBK_durch_K3_D(40, beta_sigma_dBK)
        elif Art == "zwei Passfedern":
            beta_sigma_dBK = 3*(sigma_B_d/1000)**0.38

            beta_tau_dBK = 0.56*beta_sigma_dBK+0.1
            beta_zd = 1
            beta_sigma = beta_sigma_dBK*self.K3_dBK_durch_K3_D(40, beta_sigma_dBK)
            beta_sigma = 1.15*beta_sigma*self.K3_dBK_durch_K3_D(40, beta_sigma_dBK)
            beta_tau = beta_tau_dBK
        elif Art == "Pressverbindung":
            beta_sigma_dBK = 2.7*(sigma_B_d/1000)**0.43
            beta_tau_dBK = 0.65*beta_sigma_dBK+0.1
            beta_zd = 1
            beta_sigma = beta_sigma_dBK*self.K3_dBK_durch_K3_D(40, beta_sigma_dBK)
            beta_tau = beta_tau_dBK*self.K3_dBK_durch_K3_D(40, beta_sigma_dBK)
        elif Art == "Keilwelle":
            beta_tau_dBK_stern = math.e**(4.2*10**(-7)*sigma_B_d**2)
            beta_tau_dBK = beta_tau_dBK_stern
            beta_sigma_dBK = 1+0.45*(beta_tau_dBK_stern-1)
            beta_zd = 1
            beta_sigma = beta_sigma_dBK*self.K3_dBK_durch_K3_D(29, beta_sigma_dBK)
            beta_tau = beta_tau_dBK*self.K3_dBK_durch_K3_D(29, beta_sigma_dBK)
        elif Art == "Kerbzahnwelle":
            beta_tau_dBK_stern = math.e**(4.2*10**(-7)*sigma_B_d**2)
            beta_tau_dBK = beta_tau_dBK_stern
            beta_sigma_dBK = 1+0.65*(beta_tau_dBK_stern-1)
            beta_zd = 1
            beta_sigma = beta_sigma_dBK*self.K3_dBK_durch_K3_D(29, beta_sigma_dBK)
            beta_tau = beta_tau_dBK*self.K3_dBK_durch_K3_D(29, beta_sigma_dBK)
        elif Art == "Zahnwelle":
            beta_tau_dBK_stern = math.e**(4.2*10**(-7)*sigma_B_d**2)
            beta_tau_dBK = 1+0.75*(beta_tau_dBK_stern-1)
            beta_sigma_dBK = 1+0.49*(beta_tau_dBK_stern-1)
            beta_zd = 1
            beta_sigma = beta_sigma_dBK*self.K3_dBK_durch_K3_D(29, beta_sigma_dBK)
            beta_tau = beta_tau_dBK*self.K3_dBK_durch_K3_D(29, beta_sigma_dBK)
        elif Art == "umlaufende Spitzkerbe":
                beta_zd_dBK = 0.109*sigma_B_d
                beta_sigma_dBK = 0.0923*sigma_B_d
                beta_tau_dBK = 0.8*beta_sigma_dBK
                beta_sigma = beta_sigma_dBK*self.K3_dBK_durch_K3_D(15, beta_sigma_dBK)
                beta_tau = beta_tau_dBK*self.K3_dBK_durch_K3_D(15, beta_sigma_dBK)
                beta_zd = beta_zd_dBK*self.K3_dBK_durch_K3_D(159, beta_sigma_dBK)
        if Art == "umlaufende Rechtecknut":
            sigma_S = int(Werkstoff.Werkstoffe[self.welle.werkstoff].sigma_S)
            t = self.t

            rho_s = 10**(-(0.514+0.00152*sigma_S))
            beta_zd_stern = 0.9*(1.27+1.17*(np.sqrt(t/(self.r+2.9*rho_s))))
            beta_sigma_stern = 0.9*(1.14+1.08*(np.sqrt(t/(self.r+2.9*rho_s))))
            beta_tau_stern = 1*(1.48+0.45*(np.sqrt(t/(self.r+1*rho_s))))
            
            if self.b/t >= 1.4:
                beta_zd_dBK = beta_zd_stern
                beta_sigma_dBK = beta_sigma_stern
                beta_tau_dBK = beta_tau_stern
            else:
                beta_zd_dBK = beta_zd_stern*1.08*(self.b/t)**(-0.2)
                beta_sigma_dBK = beta_sigma_stern*1.08*(self.b/t)**(-0.2)
                beta_tau_dBK = beta_tau_stern*1.08*(self.b/t)**(-0.2)

            beta_sigma = beta_sigma_dBK*self.K3_dBK_durch_K3_D(30, beta_sigma_dBK)
            beta_zd = beta_zd_dBK*self.K3_dBK_durch_K3_D(30, beta_zd_dBK)
            beta_tau = beta_tau_dBK*self.K3_dBK_durch_K3_D(30, beta_tau_dBK)
        if Art == "Absatz" or Art == "umlaufende Rundnut":
            if Art == "Absatz":
                t = self.t
                print(self.r)
                alpha_zd = Formzahl_Unterfunktion_Formel(0.62,3.5,0,0,self.d,D,self.r,t)
                alpha_b = Formzahl_Unterfunktion_Formel(0.62,5.8,0.2,3,self.d,D,self.r,t)
                alpha_t = Formzahl_Unterfunktion_Formel(3.4,19,1,2,self.d,D,self.r,t)
            if Art == "umlaufende Rundnut":
                t = self.t
                alpha_zd = Formzahl_Unterfunktion_Formel(0.22,1.37,0,0,self.d,D,self.r,t)
                alpha_b = Formzahl_Unterfunktion_Formel(0.2,2.75,0,0,self.d,D,self.r,t)
                alpha_t = Formzahl_Unterfunktion_Formel(0.7,10.3,0,0,self.d,D,self.r,t)
                sigma_S = self.Streckgrenze()

            if ((D-self.d)/self.d <= 0.5):
                phi = 1/(np.sqrt(8*(D-self.d)/self.r)+2)
            else: 
                phi = 0

            if Art == "Absatz":
                G_s_zd = 2.3/self.r*(1+phi)
                G_s_sigma = G_s_zd
                G_s_tau = 1.15/self.r
            elif Art == "umlaufende Rundnut":
                G_s_zd = 2/self.r*(1+phi)
                G_s_sigma = G_s_zd
                G_s_tau = 1/self.r

            w = Werkstoff.Werkstoffe[self.welle.werkstoff]
            sigma_S = int(w.sigma_S)
            if w.art == "Vergütungsstahl" or w.art == "Einsatzstahl" or w.art == "Automatenstahl" or w.art == "Baustahl":
                n_zd = 1+np.sqrt(G_s_zd)*10**(-(0.33+sigma_S/712))
                n_sigma = 1+np.sqrt(G_s_sigma)*10**(-(0.33+sigma_S/712))
                n_tau = 1+np.sqrt(G_s_tau)*10**(-(0.33+sigma_S/712))
            elif w.art == "Nitrierstahl":
                n_zd = 1+np.sqrt(G_s_zd)*10**(-0.7)
                n_sigma = 1+np.sqrt(G_s_sigma)*10**(-0.7)
                n_tau = 1+np.sqrt(G_s_tau)*10**(-0.7)

            beta_zd = alpha_zd/n_zd
            beta_sigma = alpha_b/n_sigma
            beta_tau = alpha_t/n_tau
        return(beta_sigma, beta_tau, beta_zd)

    def K2(self):
        """Einflussfaktor K2

        Args:
            d (int): Durchmesser der Welle
        
        Returns:
            K2
        """
        d = self.welle.d(self.z)
        if d < 150:
            K_2 = 1-0.2*(math.log10(d/7.5))/math.log10(20)
        else:
            K_2 = 0.8
        return(K_2)

    def KF(self):
        """Einflussfaktor KF

        Args:
            Rz (float): Rz
            werkstoff (str): Werkstoff der Welle
            D (int): Durchmesser der Welle

        Returns:
            K_F_sigma (float): KF bei Biegung
            K_F_tau (float): KF bei Torsion
        """
        """
        aber in Übungspdf steht nichts weiter aber in gelösten Übungsaufgaben manchmal anders gemacht (keine Ahnung warum?)
        """
        Rz = self.welle.Rz
        werkstoff = self.welle.werkstoff
        D = self.welle.d(self.z)
        sigma_B = self.Zugfestigkeit()
        K_F_sigma = 1-0.22*math.log10(Rz)*(math.log10(sigma_B/20)-1)
        K_F_tau = 0.575*K_F_sigma+0.425

        return(K_F_sigma, K_F_tau)

    def KV(self):
        """Einflussfaktor KV

        Args:
            Oberfl (str): Art der Oberflächenverfestigung, falls nicht vorhanden: "nein"
            D (int): Durchmesser der Welle
            Art (str): Art der Querschnittsschwächung
        
        Returns:
            KV
        """
        """
        irgendwie komisch beschrieben in pdf, vielleicht ist KV auch immer 1?
        """
        Art = self.Art 
        D = self.welle.d(self.z)
        if Art == "umlaufende Rundnut" or Art == "Absatz":
            K_V = 1
        Oberflächenverfestigung = self.welle.Oberflächenverfestigung
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

    def Gesamtgrößeneinflussfaktor(self):
        """Gesamtgößeneinflussfaktor

        Args:
            D (int): großer Duchmesser
            d (int): kleiner Durchmesser
            beta_sigma (float): Kerbwirkungszahl Biegung
            beta_tau (float): Kerbwirkungszahl Torsion
            Rz (float): Rz
            werkstoff (str): Werkstoff der Welle
            Oberflächenverfestigung (str): Art der Oberflächenverfestigung, falls nicht vorhanden: "nein"
            Art (str): Art der Querschnittsschwächung

        Returns:
            K_Sigma (float): Gesamteinflussfaktor Biegung
            K_tau (float): Gesamteinflussfaktor Torsion
        """
        beta_sigma, beta_tau, _ = self.Kerbwirkungszahl()
        d = min(self.welle.d(self.z-1), self.welle.d(self.z+1))
        D = max(self.welle.d(self.z-1), self.welle.d(self.z+1))

        K_2 = self.K2()
        K_V = self.KV()
        (K_F_sigma, K_F_tau) = self.KF()
        K_sigma = ((beta_sigma/K_2)+(1/K_F_sigma)-1)*(1/K_V)
        K_tau = ((beta_tau/K_2)+(1/K_F_tau)-1)*(1/K_V)



        return(K_sigma, K_tau)

    def Bauteilwechselfestigkeiten(self):
        """Bauteilwechselfestigkeiten
        
        Args:
            D (int): großer Durchmesser der Welle
            werkstoff (str): Werkstoff der Welle
            K_sigma (float): Gesamteinflussfaktor Biegung
            K_tau (float): Gesamteinflussfaktor Torsion

        Returns:
            sigma_bWK (float): Biegewechselfestigkeit
            tau_tWK (float): Torsionswechselfestigkeit
        """
        K_sigma, K_tau = self.Gesamtgrößeneinflussfaktor()
        D = max(self.welle.d(self.z+1), self.welle.d(self.z-1))
        werkstoff = self.welle.werkstoff
        K_1 = self.K1("B")
        sigma_bW = Werkstoff.Werkstoffe[werkstoff].sigma_bW
        tau_tW = Werkstoff.Werkstoffe[werkstoff].tau_tW
        sigma_bWK = (K_1*sigma_bW)/K_sigma
        tau_tWK = (K_1*tau_tW)/K_tau

        return(sigma_bWK, tau_tWK)

    """
    2. Bauteilfließgrenzen
    """
    def K2F(self):
        """Einflussfaktor K2F

        Args:
            Belastungsart (str): Art der Belastung
        
        Returns:
            K2F
        """
        K_2Fsigma = 1.2
        K_2F_tau = 1.2
        K_2F_zd = 1
        return(K_2Fsigma, K_2F_tau)

    def Erhöhungsfaktor_der_Fließgrenze(self, Kerbzahl_sigma):
        """gamma_F

        Args:
            Kerbzahl (float): Kerbwirkungszahl
            Belastungsart (str): Art der Belastung (Biegung, Torsion oder Zug/Druck)

        Returns:
            gamma_F
        """

        if Kerbzahl_sigma <= 1.5:
            gamma_F_sigma = 1
        elif Kerbzahl_sigma <= 2:
            gamma_F_sigma = 1.05
        elif Kerbzahl_sigma <= 3:
            gamma_F_sigma = 1.1
        else:
            gamma_F_sigma = 1.15
        gamma_F_tau = 1

        return(gamma_F_sigma, gamma_F_tau)

    def Bauteilfließgrenzen(self):
        """Bauteilfließgrenzen
        
        Args:
            Kerbzahl_sigma (float): Kerbzahl Biegung
            Kerbzahl_tau (float): Kerbzahl Torsion
            D (int): Wellendurchmesser
            werkstoff (str): Werkstoff der Welle
        """
        beta_sigma, _ , _ = self.Kerbwirkungszahl()
        K_2F_sigma, K_2F_tau = self.K2F()
        gamma_sigma, gamma_tau = self.Erhöhungsfaktor_der_Fließgrenze(beta_sigma)
        K_1 = self.K1("S")
        sigma_S = int(Werkstoff.Werkstoffe[self.welle.werkstoff].sigma_S)


        sigma_bFK = K_1*K_2F_sigma*gamma_sigma*sigma_S
        tau_tFK = K_1*K_2F_tau*gamma_tau*(sigma_S/np.sqrt(3))

        return(sigma_bFK, tau_tFK)

    """
    3. Gestaltfestigkeiten
    """
    def Vergleichsmittelspannungen(self, sigma_zdm, sigma_bm, tau_tm):
        """Vergleichsmittelspannungen

        Args:
            sigma_zdm (float): mittlere Zug/Druck-Spannung
            sigma_bm (float): mittlere Biegespannung
            tau_tm (float): mittlere Torsionsspannung

        Returns:
            sigma_mv (float): Vergleichsmittelspannung Biegung
            tau_mv (float): Vergleichsmittelspannung Torsion
        """
        sigma_mv = np.sqrt((sigma_zdm+sigma_bm)**2+3*tau_tm**2)
        tau_mv = sigma_mv/np.sqrt(3)

        if tau_tm == 0:
            tau_mv = 0

        return(sigma_mv, tau_mv)

    def Mittelspannungsempfindlichkeit(self):
        """Mittelspannungsempfindlichkeit

        Args:
            D (int): Wellendurchmesser
            tau_tWK (float): Torsionswechselfestigkeit
            sigma_zd_bWK (float): Biegewechselfestigkeit
            werkstoff (str): Werkstoff der Welle

        Returns:
            Psi_zd_b_sigma (float): Mittelspannungsempfindlichkeit Biegung
            Psi_tauK (float): Mittelspannungsempfindlichkeit Torsion
        """
        sigma_zd_bWK, tau_tWK = self.Bauteilwechselfestigkeiten()
        D = max(self.welle.d(self.z-1), self.welle.d(self.z+1))
        sigma_B = int(Werkstoff.Werkstoffe[self.welle.werkstoff].sigma_B)
        K_1 = self.K1("B")
        Psi_zd_b_sigma_K = (sigma_zd_bWK)/(2*K_1*sigma_B-sigma_zd_bWK)
        Psi_tauK = (tau_tWK)/(2*K_1*sigma_B-tau_tWK)

        return(Psi_zd_b_sigma_K, Psi_tauK)

    def Gestaltfestigkeit(self,sigma_zdm, sigma_bm, tau_tm):
        """Gestaltfestigkeit

        Args:
            D (int): Wellendurchmesser
            werkstoff (str): Werkstoff der Welle
            gamma_F_sigma (float): Erhöhungsfaktor der Fließgrenze Biegung
            gamma_F_tau (float): Erhöhungsfaktor der Fließgrenze Torsion
            sigma_mv (float): Vergleichsmittelspannung Biegung
            tau_mv (float): Vergleichsmittelspannung Torsion
            sigma_bWK (float): Biegewechselfestigkeit
            Psi_b_sigma_K (float): Mittelspannungsempfindlichkeit Biegung
            tau_tWK (float): Torsionswechselfestigkeit
            Psi_tau_K (float): Mittelspannungsempfindlichkeit Torsion

        Returns:
            sigma_bADK (float): Gestaltfestigkeit Biegung
            tau_tADK (float): Gestaltfestigkeit Torsion
        """
        sigma_bWK, tau_tWK = self.Bauteilwechselfestigkeiten()
        sigma_mv, tau_mv = self.Vergleichsmittelspannungen(sigma_zdm, sigma_bm, tau_tm)
        beta_sigma, _, _ = self.Kerbwirkungszahl()
        gamma_F_sigma, gamma_F_tau = self.Erhöhungsfaktor_der_Fließgrenze(beta_sigma)
        Psi_b_sigma_K, Psi_tau_K = self.Mittelspannungsempfindlichkeit()
        D = max(self.welle.d(self.z+1), self.welle.d(self.z-1))
        werkstoff = self.welle.werkstoff
        K2F_sigma , K2F_tau = self.K2F()
        sigma_S = int(Werkstoff.Werkstoffe[self.welle.werkstoff].sigma_S)
        sigma_bFK = self.K1("S", )*K2F_sigma*gamma_F_sigma*sigma_S
        tau_tFK = self.K1("S")*K2F_tau*gamma_F_tau*(sigma_S/np.sqrt(3))

        if sigma_mv <= (sigma_bFK-sigma_bWK)/(1-Psi_b_sigma_K) and tau_mv <= (tau_tFK-tau_tWK)/(1-Psi_tau_K):
            sigma_bADK = sigma_bWK-Psi_b_sigma_K*sigma_mv
            tau_tADK = tau_tWK-Psi_tau_K*tau_mv
        else: 
            Psi_b_sigma_K = 1
            Psi_tau_K = 1
            sigma_bADK = sigma_bWK-Psi_b_sigma_K*sigma_mv
            tau_tADK = tau_tWK-Psi_tau_K*tau_mv
        
        return(sigma_bADK, tau_tADK)

    def Spannungen(self, z):
        pass

    def Sicherheiten(self, sigma_bmax, tau_tmax, sigma_bq, tau_ta, sigma_zdm, sigma_bm, tau_tm):
        """Sicherheiten

        Args:
            sigma_bmax (float): maximale Biegespannung
            sigma_bFK (float): Gestaltfestigkeit Biegung
            tau_tmax (float): maximale Torsionsspannung
            tau_tFK (float): Gestaltfestigkeit Torsion
            sigma_bq (float): Biegeausschlagspannung
            sigma_bADK (float): Dauerfestigkeit Biegung
            tau_ta (float): Torsionsausschlagspannung
            tau_tADK (float): Dauerfestigkeit Torsion
        """
        sigma_bADK, tau_tADK = self.Gestaltfestigkeit(sigma_zdm, sigma_bm, tau_tm)
        sigma_bFK, tau_tFK = self.Bauteilfließgrenzen()
        S_F = 1/(np.sqrt((sigma_bmax/sigma_bFK)**2+(tau_tmax/tau_tFK)**2))
        S_D = 1/(np.sqrt((sigma_bq/sigma_bADK)**2+(tau_ta/tau_tADK)**2))

        return(S_F, S_D)
    
test = Welle("Test", 0, 10, "34CrMo4", 5, "nein")
test.set_geometrie(
    ((0, 25),
    (10,25),
    (10,26),
    (40,26))
)
#test.plot()
Abschnitt = Welle_Absatz(test, 10, "Absatz", 3)

print(Abschnitt.Sicherheiten(146.677, 183.346, 97.785, 100, 0, 100, 200))