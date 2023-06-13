from Klassen import Welle, Werkstoff
import math

class Welle_Absatz():
    def __init__(self,welle:Welle,z):
        self.welle = welle
        self.z = z
        
    def K1(self, D, B_oder_S):
        """Einflussfaktor K1

        Args:
            D (int): großer Durchmesser
            B_oder_S (str): S: Zugfestigkeit; B: Strekcgrenze 
            werkstoff (str): Werkstoff der Welle

        Returns:
            K_1 (float): Einflussfaktor K1
        """
        D = max(self.welle.d(z), self.welle.d(z+3))
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
        
    def Zugfestigkeit(self, D):
        """Zugfestigkeit für Durchmesser

        Args:
            D (int): großer Durchmesser der Welle
            werkstoff (str): Werkstoff der Welle
        
        Returns:
            sigma_B: Zugfestigkeit für D
        """
        werkstoff = self.welle.werkstoff
        sigma_B = int(Werkstoff.Werkstoffe[werkstoff].sigma_B)
        K_1 = self.K1(D, "B", werkstoff)
        return(sigma_B*K_1)