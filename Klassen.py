"""
Klassendefinitionen
Code geschrieben von: Nadine Schulz, Quentin Huss
"""

import numpy as np
import matplotlib.pyplot as plt
from numba import njit,jit,jit_module

class Werkstoff():
    Werkstoffe = {} # Dictionary mit allen erzeugten Werkstoffen

    def __init__(self, name, sigma_zdW, sigma_bW, tau_tW,art, Cr_Ni_Einsatzstahl, sigma_B, sigma_S):
        self.name = name
        self.sigma_zdW = float(sigma_zdW)
        self.sigma_bW = float(sigma_bW)
        self.tau_tW = float(tau_tW)
        self.art = art
        self.Cr_Ni_Einsatzstahl = int(Cr_Ni_Einsatzstahl)
        self.sigma_B = sigma_B
        self.sigma_S = sigma_S
        Werkstoff.Werkstoffe[name] = self
    def __repr__(self) -> str:
        return self.name
    def data_sheet(self):
        print(
            f"""
---------------------------------------------------
Name:                           {self.name}
Art:                            {self.art}
Zug-Druck-Wechselfestigkeit:    {self.sigma_zdW}
Biegewechselfestigkeit:         {self.sigma_bW}
Torsionswechselfestigkeit:      {self.tau_tW}
---------------------------------------------------
            """
        )
    def aus_csv_laden():
        """
        Lädt die Werkstoffdaten aus `'\\Werkstoffdaten.csv'` in `Werkstoff.Werkstoffe`.
        Bei Dopplung werden alte Einträge mit neuen Überschrieben.
        """
        with open("Werkstoffdaten.csv","r",encoding="utf8") as datei:
            rohdaten = datei.readlines()

        for line in rohdaten:
            if line[0] != "#":
                args = line.strip().split(",")
                Werkstoff(*args)
        return 1

class Welle:
    def __init__(self,name:str,festlager_z:int,loslager_z:int, werkstoff:Werkstoff, Rz, Oberflächenverfestigung,dz=0.1) -> None:
        self.name = str(name)
        self.Emod = 210e3 # N/mm^2
        self.festlager_z = festlager_z
        self.loslager_z = loslager_z
        self.lagerabstand = abs(festlager_z-loslager_z)
        self.länge = 0
        self.geometrie = []
        self.z_daten = []
        self.r_daten = []
        self.werkstoff = werkstoff
        self.Rz = Rz
        self.Oberflächenverfestigung = Oberflächenverfestigung
        self.belastungen = [(0,0,0,0,0,0,0),(0,0,0,0,0,0,0),(0,0,0,0,0,0,0),(0,0,0,0,0,0,0),(0,0,0,0,0,0,0)]
        self.dz = dz # Schrittweite in Z in mm
        self.minL = None
        self.maxL = None
        self.z_range = None
        self.len_z_range = None
        self.biegung_x = None
        self.biegung_y = None
        self.neigung_x = None
        self.neigung_y = None

    
    def set_Kraft(self,betrag,typ:str,z=0,r=0,phi=0):
        """Legt eine Krafteinleitung an der Welle fest.
        Der Typ kann "radial","tangential" oder "axial" sein.
        Radialkräfte nach innen sind positiv.
        z: Z-Position (längs) wo die Kraft angreift
        r: Entfernung der Kraft von der Drehachse der Welle.
        phi: Winkel der Krafteinleitung in Grad. Kräfte von oben haben phi=0
        """
        phi = np.deg2rad(phi)
        if typ[0].casefold()=="r":
            kraft = (betrag,z,r,phi,betrag*np.sin(phi),betrag*np.cos(phi),0) # Radial
        elif typ[0].casefold()=="t":
            kraft = (betrag,z,r,phi,betrag*np.cos(phi),betrag*np.sin(phi),0) # Tangential
        elif typ[0].casefold()=="a":
            kraft = (betrag,z,r,phi,0,0,betrag) # Axial
        else:
            raise ValueError("Krafttyp wurde nicht erkannt. Erlaubt sind 'radial' ('r'),'tangential' ('t') und 'axial' ('a').")
        self.belastungen.append(kraft)

    def lagerkräfte_berechnen(self):
        # Lagerkräfte berechnen und in Belastungen aufnehmen
        # Lagerkraft Loslager
        lges = self.lagerabstand
        summe_krafthebelx,summe_krafthebely = 0,0
        summe_kräftex,summe_kräftey,summe_kräftez = 0,0,0
        for _,zk,rk,phi,fx,fy,fz in self.belastungen:
            if self.festlager_z<self.loslager_z:
                summe_krafthebely += -fy*(zk-self.festlager_z)-fz*rk*np.cos(phi)
                summe_krafthebelx += -fx*(zk-self.festlager_z)
            else:
                summe_krafthebely += fy*(zk-self.festlager_z)+fz*rk*np.cos(phi)
                summe_krafthebelx += fx*(zk-self.festlager_z)
        self.belastungen[3] = (abs(summe_krafthebelx/lges),self.loslager_z,0,0,summe_krafthebelx/lges,0,0) # Lagerkraft Loslager X
        self.belastungen[4] = (abs(summe_krafthebely/lges),self.loslager_z,0,0,0,summe_krafthebely/lges,0) # Lagerkraft Loslager Y

        for _,zk,rk,_,fx,fy,fz in self.belastungen:
            summe_kräftex += -fx
            summe_kräftey += -fy
            summe_kräftez += -fz
        self.belastungen[0] = (abs(summe_kräftex),self.festlager_z,0,0,summe_kräftex,0,0) # Lagerkraft Festlager X
        self.belastungen[1] = (abs(summe_kräftey),self.festlager_z,0,0,0,summe_kräftey,0) # Lagerkraft Festlager Y
        self.belastungen[2] = (abs(summe_kräftez),self.festlager_z,0,0,0,0,summe_kräftez) # Lagerkraft Festlager Z

    def set_geometrie(self,punkte:list):
        """
        Definiert die Wellengeometrie als Liste aus Punkten in der Form [[z1,r1],[z2,r2],...]
        """
        self.geometrie = punkte
        self.z_daten,self.r_daten = zip(*self.geometrie) # Entpackt die Geometriedaten in Vektoren
        self.minL = min(self.z_daten)
        self.maxL = max(self.z_daten)
        self.länge = abs(self.maxL-self.minL)
        self.z_range = np.arange(self.minL,self.maxL,self.dz)
        self.len_z_range = len(self.z_range)


    def radius(self,z):
        """Gibt Radius der Welle an Stelle z aus. Alle Längen werden in `mm` angegeben"""
        for i,zr in enumerate(self.geometrie):
            z1,z2 = self.geometrie[i-1][0],self.geometrie[i][0]
            r1,r2 = self.geometrie[i-1][1],self.geometrie[i][1]
            
            if z<=z2:
                m = (z - z1) / (z2 - z1)
                return r1 + m * (r2 - r1)
        else:
            return 0

    def r(self,z):
        """Gibt Radius der Welle an Stelle z aus. Alle Längen werden in `mm` angegeben"""
        return self.radius(z)
    def d(self,z):
        """Gibt Durchmesser der Welle an Stelle z aus. Alle Längen werden in `mm` angegeben"""
        return 2*self.radius(z)
    def durchmesser(self,z):
        """Gibt Durchmesser der Welle an Stelle z aus. Alle Längen werden in `mm` angegeben"""
        return self.d(z)
    def plot(self,kräfte=True):
        """Stellt die Welle dar."""
        _,z_kräfte,_,_,_,_,_=zip(*self.belastungen)
        max_z_k = max(z_kräfte)
        max_z = max(self.z_daten)
        min_z = min(self.z_daten)
        min_z_k = min(z_kräfte)

        zrange = np.linspace(min_z,max_z,1000)
        z_range_k = np.linspace(min_z_k,max_z_k,1000)
        rrange = np.fromiter(map(self.radius,zrange),float,len(zrange))

        fig,ax = plt.subplots(2,2,constrained_layout=True,sharex="col",sharey="row",num=self.name+" Belastungsplot")
        fig.set_size_inches(15,10)
        fig.suptitle(f'Welle "{self.name}"',fontsize=18)
        ax[0,0].plot(zrange,rrange,"k")
        ax[0,0].plot(zrange,rrange*-1,"k")
        ax[0,0].hlines(0,min_z-self.länge*0.05,self.z_daten[-1]+self.länge*0.05,linestyles="dashdot",colors="black")
        for i,z in enumerate(self.z_daten):
            ax[0,0].vlines(z,self.radius(z)*-1,self.radius(z),colors="black")

        # maximale Kraft ermitteln, zum skalieren der Vektoren
        l_max = self.länge/3
        max_f = max((self.belastungen[i][0] for i in range(len(self.belastungen))))

        for kraft in self.belastungen:
            _,z,r,phi,fx,fy,fz = kraft
            if round(abs(fy),5)>0: # Y Kräfte zeichnen
                ax[0,0].arrow(z,r*np.cos(phi),0,l_max*-fy/max_f,color="green",zorder=100,width=l_max/20)

            if round(abs(fz),5)>0: # Z Kräfte zeichnen
                ax[0,0].arrow(z,r*np.cos(phi),l_max*fz/max_f,0,color="blue",zorder=100,width=l_max/20)

        ax[0,0].grid()
        ax[0,0].set_title("YZ-Ebene")
        ax[0,0].set_xlabel("$z\\,[mm]$")
        ax[0,0].set_ylabel("$r\\,[mm]$")
        #ax[0,0].set_ylim(ax[0,0].get_xlim())

        ax[0,1].plot(zrange,rrange,"k")
        ax[0,1].plot(zrange,rrange*-1,"k")
        ax[0,1].hlines(0,min_z-self.länge*0.05,self.z_daten[-1]+self.länge*0.05,linestyles="dashdot",colors="black")
        for i,z in enumerate(self.z_daten):
            ax[0,1].vlines(z,self.radius(z)*-1,self.radius(z),colors="black")

        for kraft in self.belastungen:
            _,z,r,phi,fx,fy,fz = kraft
            if round(abs(fx),5)>0: # X Kräfte zeichnen
                ax[0,1].arrow(z,r*np.sin(phi),0,l_max*-fx/max_f,color="red",zorder=100,width=l_max/20)
            if round(abs(fz),5)>0: # Z Kräfte zeichnen
                ax[0,1].arrow(z,r*np.sin(phi),l_max*fz/max_f,0,color="blue",zorder=100,width=l_max/20)

        ax[0,1].grid()
        ax[0,1].set_title("XZ-Ebene")
        ax[0,1].set_xlabel("$z\\,[mm]$")
        ax[0,1].set_ylabel("$r\\,[mm]$")

        # Mbx Biegemomentenverlauf
        mbx_daten = np.fromiter(map(self.Mbx,z_range_k),float,len(z_range_k))
        ax[1,0].plot(z_range_k,mbx_daten)
        ax[1,0].fill_between(z_range_k,0,mbx_daten,alpha=0.3)
        ax[1,0].set_xlabel("$z\\,[mm]$")
        ax[1,0].set_ylabel("$Mb_x\\,[Nm]$")
        ax[1,0].set_title("Biegemoment um X")
        ax[1,0].grid()

        # Mby Biegemomentenverlauf
        mby_daten = np.fromiter(map(self.Mby,z_range_k),float,len(z_range_k))
        ax[1,1].plot(z_range_k,mby_daten)
        ax[1,1].fill_between(z_range_k,0,mby_daten,alpha=0.3)
        ax[1,1].set_xlabel("$z\\,[mm]$")
        ax[1,1].set_ylabel("$Mb_y\\,[Nm]$")
        ax[1,1].set_title("Biegemoment um Y")
        ax[1,1].grid()

        ax[0,0].invert_yaxis() # Achse invertieren

        plt.show()

    def plot_torsion(self):
        """Stellt die Welle dar."""
        _,z_kräfte,_,_,_,_,_=zip(*self.belastungen)
        max_z_k = max(z_kräfte)
        max_z = max(self.z_daten)
        min_z = min(self.z_daten)
        min_z_k = min(z_kräfte)

        zrange = np.linspace(min_z,max_z,1000)
        z_range_k = np.linspace(min_z_k,max_z_k,1000)
        rrange = np.array(tuple(map(self.radius,zrange)))

        fig,ax = plt.subplots(2,1,constrained_layout=True,sharex="col",sharey="row",num=self.name+" Belastungsplot")
        fig.set_size_inches(15,10)
        fig.suptitle(f'Welle "{self.name}"',fontsize=18)
        ax[0].plot(zrange,rrange,"k")
        ax[0].plot(zrange,rrange*-1,"k")
        ax[0].hlines(0,min_z-self.länge*0.05,self.z_daten[-1]+self.länge*0.05,linestyles="dashdot",colors="black")
        for i,z in enumerate(self.z_daten):
            ax[0].vlines(z,self.radius(z)*-1,self.radius(z),colors="black")
        ax[0].set_title("Darstellung")
        
        mt = tuple(map(self.Mt,z_range_k))

        ax[1].plot(z_range_k,mt)
        ax[1].set_xlabel("$z\\,[mm]$")
        ax[1].set_ylabel("$M_t\\,[Nm]$")
        ax[1].set_title("Torsionsmoment")
        ax[0].grid()
        ax[1].grid()

        plt.show()

    def Mbx(self,z):
        """Berechnet numerisch den Biegemomentenverlauf um die globale X-Achse in `N*m`"""
        result = 0
        for kraft in self.belastungen:
            _,z_kraft,r,phi,fx,fy,fz = kraft
            if z_kraft<z:
                result += -1*fy*(z-z_kraft)
                result += fz*r*np.cos(phi)
        return result/1000

    
    def Mby(self,z):
        """Berechnet numerisch den Biegemomentenverlauf um die globale Y-Achse in `N*m`"""
        result = 0
        for kraft in self.belastungen:
            _,z_kraft,r,phi,fx,fy,fz = kraft
            if z_kraft<z:
                result += -1*fx*(z-z_kraft)
                result += fz*r*np.sin(phi)
        return result/1000
    
    def Mt(self,z):
        """Berechnet numerisch den Torsionsmomentenverlauf um die Globale Z-Achse in `N*m`"""
        result = 0
        for kraft in self.belastungen:
            _,z_kraft,r,phi,fx,fy,fz = kraft
            if z_kraft<=z:
                result += -1*fx*r*np.cos(phi)
                result += -1*fy*r*np.sin(phi)
        return result
    
    def Wb(self,z):
        """Gibt das Widerstandsmoment gegen Biegung an der Stelle z in `mm^3` aus."""
        return np.pi/32 * self.d(z)**3
    
    def verformung_berechnen(self):
        """Berechnet die Verformungs- und Neigungsvektoren. Es kann optional die Schrittweite der Integration angegeben werden."""
        E = self.Emod
        dz = self.dz
        z_range = self.z_range
        minL = self.minL
        maxL = self.maxL

        def q_ers_x(z):
            return (64*self.Mbx(z))/(np.pi*self.d(z)**4)
        def q_ers_y(z):
            return (64*self.Mby(z))/(np.pi*self.d(z)**4)

        def F_ers_x():
            integral = 0
            for z in z_range:
                integral+=q_ers_x(z)*(maxL-z)
            F_ers = 1/maxL * integral*dz
            return (F_ers)*1000 # N/mm^2
        def F_ers_y():
            integral = 0
            for z in z_range:
                integral+=q_ers_y(z)*(maxL-z)
            F_ers = 1/maxL * integral*dz
            return (F_ers)*1000 # N/mm^2
        
        # Ersatzlagerkräfte
        F_ex = F_ers_x()
        F_ey = F_ers_y()

        # Biegung
        def Biegung_x(z):
            integral = 0
            for s in z_range[z_range<=z]:
                integral += q_ers_x(s)*(z-s)*dz
            return 1/E*(F_ex*z-integral*1000)

        def Biegung_y(z):
            integral = 0
            for s in z_range[z_range<=z]:
                integral += q_ers_y(s)*(z-s)*dz
            return 1/E*(F_ey*z-integral*1000)
        
        def Neigung_x(z):
            integral = 0
            for s in z_range[z_range<z]:
                integral += q_ers_x(s)*dz
            return 1/E * (F_ex-integral*1000)
        def Neigung_y(z):
            integral = 0
            for s in z_range[z_range<z]:
                integral += q_ers_y(s)*dz
            return 1/E * (F_ey-integral*1000)

        self.biegung_x = np.fromiter(map(Biegung_x,z_range),float,self.len_z_range)
        self.biegung_y = np.fromiter(map(Biegung_y,z_range),float,self.len_z_range)
        self.neigung_x = np.fromiter(map(Neigung_x,z_range),float,self.len_z_range)
        self.neigung_y = np.fromiter(map(Neigung_y,z_range),float,self.len_z_range)

        # Schlusslinie in X
        m = (Biegung_x(self.festlager_z) - Biegung_x(self.loslager_z))/ (self.festlager_z - self.loslager_z)    # Gerade zwischen Lagern
        n = Biegung_x(self.loslager_z) - m * self.loslager_z                     
        y_range = m * z_range + n
        self.biegung_x = self.biegung_x - y_range

        # Schlusslinie in y
        m = (Biegung_y(self.festlager_z) - Biegung_y(self.loslager_z))/ (self.festlager_z - self.loslager_z)    # Gerade zwischen Lagern
        n = Biegung_y(self.loslager_z) - m * self.loslager_z
        y_range = m * z_range + n
        self.biegung_y = self.biegung_x - y_range


    def Spannungen(self, z):
        """Spannungen
        Gibt Biegepannung in x, y und Torsionsspannung an z aus 
        """
        wbz = self.Wb(z)
        sigma_x = self.Mbx(z)*1000/wbz
        sigma_y = self.Mby(z)*1000/wbz
        tau = self.Mt(z)*1000/(np.pi/16 * self.d(z)**4)
        return(sigma_x, sigma_y, tau)
    
    def print_Lagerkräfte(self):
        print("\n")
        print(f"Lagerkraefte der Welle \"{self.name}\"\n")
        print("-"*48)
        print("|"," "*3,"Fx".center(10),"|","Fy".center(10),"|","Fz".center(10),"|","z".center(10),"|",sep="")
        print("-"*48)
        for i in range(5):
            betrag,z,r,phi,fx,fy,fz = self.belastungen[i]
            print("|",i,": ",str(round(fx,3)).center(10),"|",str(round(fy,3)).center(10),"|",str(round(fz,3)).center(10),"|",str(round(z,3)).center(10),"|",sep="")
            print("-"*48)

class Welle_Absatz():
    """einzelne nachzuweisende Wellenabsätze
    """
    def __init__(self,welle:Welle,z, Art, *args):
        """Wellenabsatz

        Args:
            welle (Welle): Welle für die Absatz nachgewiesen werden soll
            z (float): z-Koordinate des Absatzes auf der Welle
            Art (str): Art der Querschnittsschwächung

        Möglichkeiten für Art:
            Absatz,
            umlaufende Rundnut,
            eine Passfeder,
            zwei Passfedern,
            umlaufende Rundnut,
            umlaufende Spitzkerbe,
            Keilwelle,
            Kerbzahnwelle,
            Zahnwelle,
            Pressverbindung

        zusätzliche Argumente für bestimmte Arten (*args):
        Absatz: Radius;
        umlaufende Rundnut: Kerbgrunddurchmesser, Radius, Breite der Nut;
        umlaufende Rechtecknut: Tiefe der Nut, Radius, Breite der Nut
        """
        self.welle = welle
        self.z = z
        self.Art = Art
        self.Werte = []
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
                    K_1 = 1-0.23*np.log10(D/100)
                elif D >= 500:
                    K_1 = 0.89
                else:
                    raise ValueError("Welle nicht über 500mm bei K1\nsigma_B und Nitrierstahl oder Baustahl")
            elif w.art == "Vergütungsstahl" or (w.art == "Einsatzstahl" and w.Cr_Ni_Einsatzstahl == 1):
                if D <= 16:
                    K_1 = 1
                elif D <= 300:
                    K_1 = 1-0.26*np.log10(D/16)
                elif D >= 500:
                    K_1 = 0.67
                else:
                    raise ValueError("Welle nicht über 500mm bei K1\nsigma_B und Vergütungsstahl und Cr-Ni-Einsatzstahl")
            elif w.art == "Einsatzstahl" and w.Cr_Ni_Einsatzstahl == 0:
                if D <= 16:
                    K_1 = 1
                elif D <= 150:
                    K_1 = 1-0.41*np.log10(D/16)
                elif D >= 500:
                    K_1 = 0.6
                else:
                    raise ValueError("Welle nicht über 500mm bei K1\nsigma_B und Einsatzstahl ohne Cr-Ni-Einsatzstahl")
        elif B_oder_S == "S":
            if w.art == "Nitrierstahl":
                if D <= 100:
                    K_1 = 1
                elif D <= 300:
                    K_1 = 1-0.23*np.log10(D/100)
                elif D >= 500:
                    K_1 = 0.89
                else:
                    raise ValueError("Welle nicht über 500mm bei K1\nsigma_S und Nitrierstahl")
            elif w.art == "Baustahl":
                if D <= 32:
                    K_1 = 1
                elif D <= 300:
                    K_1 = 1-0.26*np.log10(D/100)
                elif D >= 500:
                    K_1 = 0.75
                else:
                    raise ValueError("Welle nicht über 500mm bei K1\nsigma_S und Baustahl")
            elif w.art == "Einstazstahl" and w.Cr_Ni_Einsatzstahl == 1:
                if D <= 16:
                    K_1 = 1
                elif D <= 300:
                    K_1 = 1-0.26*np.log10(D/16)
                elif D >= 500:
                    K_1 = 0.67
                else:
                    raise ValueError("Welle nicht über 500mm bei K1\nsigma_S und Cr-Ni-Einsatzstahl")
            elif w.art == "Vergütungsstahl":
                if D <= 16:
                    K_1 = 1
                elif D <= 300:
                    K_1 = 1-0.34*np.log10(D/16)
                elif D >= 500:
                    K_1 = 0.57
                else:
                    raise ValueError("Welle nicht über 500mm bei K1\nsigma_S und Vergütungsstahl")
            elif w.art == "Einsatzstahl" and w.Cr_Ni_Einsatzstahl == 0:
                if D <= 16:
                    K_1 = 1
                elif D <= 150:
                    K_1 = 1-0.41*np.log10(D/16)
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
            beta_tau_dBK_stern = np.e**(4.2*10**(-7)*sigma_B_d**2)
            beta_tau_dBK = beta_tau_dBK_stern
            beta_sigma_dBK = 1+0.45*(beta_tau_dBK_stern-1)
            beta_zd = 1
            beta_sigma = beta_sigma_dBK*self.K3_dBK_durch_K3_D(29, beta_sigma_dBK)
            beta_tau = beta_tau_dBK*self.K3_dBK_durch_K3_D(29, beta_sigma_dBK)
        elif Art == "Kerbzahnwelle":
            beta_tau_dBK_stern = np.e**(4.2*10**(-7)*sigma_B_d**2)
            beta_tau_dBK = beta_tau_dBK_stern
            beta_sigma_dBK = 1+0.65*(beta_tau_dBK_stern-1)
            beta_zd = 1
            beta_sigma = beta_sigma_dBK*self.K3_dBK_durch_K3_D(29, beta_sigma_dBK)
            beta_tau = beta_tau_dBK*self.K3_dBK_durch_K3_D(29, beta_sigma_dBK)
        elif Art == "Zahnwelle":
            beta_tau_dBK_stern = np.e**(4.2*10**(-7)*sigma_B_d**2)
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
            K_2 = 1-0.2*(np.log10(d/7.5))/np.log10(20)
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
        K_F_sigma = 1-0.22*np.log10(Rz)*(np.log10(sigma_B/20)-1)
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

    def Werte_speichern(self):
        self.Werte = []
        # Geometrie
        self.Werte.append(str(self.Art))
        self.Werte.append(str(self.welle.werkstoff))
        self.Werte.append(str(self.z))
        self.Werte.append(str(self.welle.name))

        # Kerbwirkungszahlen
        beta_sigma, beta_tau, _ = self.Kerbwirkungszahl()
        self.Werte.append(str(beta_sigma))
        self.Werte.append(str(beta_tau))

        # Gesamtgrößeneinflussfaktor
        K_ges_sigma, K_ges_tau = self.Gesamtgrößeneinflussfaktor()
        self.Werte.append(str(K_ges_sigma))
        self.Werte.append(str(K_ges_tau))

        # Bauteilwechselfestigkeiten
        sigma_bWK, tau_tWK = self.Bauteilwechselfestigkeiten()
        self.Werte.append(str(sigma_bWK))
        self.Werte.append(str(tau_tWK))

        # Bauteilfließgrenzen
        sigma_bFK, tau_tFK = self.Bauteilfließgrenzen()
        self.Werte.append(str(sigma_bFK))
        self.Werte.append(str(tau_tFK))

        # Gestaltfestigkeiten
        sigma_bADK, tau_tADK = self.Gestaltfestigkeit(100, 100, 100)
        self.Werte.append(str(sigma_bADK))
        self.Werte.append(str(tau_tADK))

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
        self.Werte_speichern()
        sigma_bADK, tau_tADK = self.Gestaltfestigkeit(sigma_zdm, sigma_bm, tau_tm)
        sigma_bFK, tau_tFK = self.Bauteilfließgrenzen()
        S_F = 1/(np.sqrt((sigma_bmax/sigma_bFK)**2+(tau_tmax/tau_tFK)**2))
        S_D = 1/(np.sqrt((sigma_bq/sigma_bADK)**2+(tau_ta/tau_tADK)**2))

        # Werte für csv
        self.Werte.append(str(S_F))
        self.Werte.append(str(S_D))
        if self.Art == "Absatz":
            self.Werte.append(str(self.D)+";"+str(self.d)+";"+str(self.r)+";"+str((self.D-self.d)/2))
        elif self.Art == "umlaufende Rundnut":
            self.Werte.append(str(self.d)+";"+str(self.r)+";"+str(self.b))
        elif self.Art == "umlaufende Rechtecknut":
            self.Werte.append(str(self.t)+";"+str(self.r)+";"+str(self.b))
        else:
            self.Werte.append("-")

        return(S_F, S_D, self.Werte)

# speichert Werte in CSV um daraus pdf zu erzeugen als Berechnung
def Werte_in_CSV_speichern(*args:Welle_Absatz):
    W = []
    W.append(["Name", "Werkstoff", "z_Wert", "Welle", "beta_sigma", "beta_tau", "K_ges_sigma", "K_ges_tau", "sigma_bWK", "tau_bWK", "sigma_bFK", "tau_tFK", "sigma_bADK", "tau_tADK", "S_F", "S_D", "anderes"])
    for Absatz in args:
        W.append(Absatz.Sicherheiten(100, 100, 100, 20, 20, 30 , 30)[2])

    print(W)
    np.savetxt("Absaetze.csv", np.array(W), fmt='%s', delimiter=',')


if __name__ == "__main__":
    Werkstoff.aus_csv_laden()
    test = Welle("Test", 0, 200, "42CrMo4" , 2, "nein",dz=1)

    test.set_geometrie(
        ((0,25),
        (40,25),
        (40,21),
        (80,21),
        (80,27.5),
        (160,27.5),
        (160,15),
        (300,15))
    )
    test.set_Kraft(3500, "r", 20, 0, 0)
    test.set_Kraft(-4500, "r", 280, 0, 0)

    test.lagerkräfte_berechnen()
    test.verformung_berechnen()


    # test.plot()
    # plt.plot(test.z_range,test.biegung_x)
    # plt.plot(test.z_range,test.biegung_y)
    # plt.plot(test.z_range,test.biegung_x)
    # plt.plot(test.z_range,test.biegung_x)
    # plt.grid()
    # plt.gca().invert_yaxis()
    # plt.show()

    Abschnitt1 = Welle_Absatz(test, 40, "Absatz", 5)
    Abschnitt2 = Welle_Absatz(test, 40, "Absatz", 2)
    Abschnitt3 = Welle_Absatz(test, 40, "Absatz", 0.1)
    Abschnitt4 = Welle_Absatz(test, 40, "Absatz", 0.1)
    Abschnitt5 = Welle_Absatz(test, 40, "Absatz", 0.1)
    Abschnitt6 = Welle_Absatz(test, 40, "Absatz", 0.1)
    Abschnitt7 = Welle_Absatz(test, 40, "Absatz", 0.1)
    Abschnitt8 = Welle_Absatz(test, 40, "Absatz", 0.1)
    Werte_in_CSV_speichern(Abschnitt1, Abschnitt2, Abschnitt3, Abschnitt4, Abschnitt5, Abschnitt6, Abschnitt7, Abschnitt8)


    # welle = Welle("Online Rechner",1,5)
    # welle.set_geometrie(((0,1),(5,1)))

    # welle.set_Kraft(1,"r",0,0,0)
    # welle.set_Kraft(1,"r",3,0,0)
    # welle.set_Kraft(1,"a",3,0,0)
    # welle.set_Kraft(1,"a",3,1,0) # Moment

    # welle.lagerkräfte_berechnen()
    # welle.print_Lagerkräfte()
    # welle.plot()

    # lab2 = 290
    # lz21 = 95
    # lz22 = 115
    # düb = 75
    # z_ritzel = lab2-lz22
    # r_ritzel = 101.46/2
    # z_rad = lab2+lz21
    # r_rad = 454.94/2

    # test = Welle("Zwischenwelle",0,lab2)
    # test.set_geometrie([
    #     [-30,düb*0.8],
    #     [30,düb*0.8],
    #     [30,düb],
    #     [lab2-30,düb],
    #     [lab2-30,düb*0.8],
    #     [lab2+lz21-15,düb*0.8],
    #     [lab2+lz21-15,düb*0.6],
    #     [lab2+lz21+15,düb*0.6]
    # ])

    # test.set_Kraft(2191,"axial",z_rad,r_rad,0)
    # test.set_Kraft(2332,"r",z_rad,r_rad,0) # Rad z12
    # test.set_Kraft(-6021,"t",z_rad,r_rad,0)

    # test.set_Kraft(-7162,"a",z_ritzel,r_ritzel,0)
    # test.set_Kraft(10071,"r",z_ritzel,r_ritzel,0) # Ritzel z21
    # test.set_Kraft(26727,"t",z_ritzel,r_ritzel,0)

    # test.lagerkräfte_berechnen()