"""
Klassendefinitionen
"""

import numpy as np
import matplotlib.pyplot as plt

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
    def __init__(self,name:str,festlager_z,loslager_z, werkstoff, Rz, Oberflächenverfestigung) -> None:
        self.name = str(name)
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
        self.dz = 0.1 # Schrittweite in Z in mm

        # Zwischenspeicher
        self.__F_ers = None

    
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
        self.länge = abs(max(self.z_daten)-min(self.z_daten))

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
        rrange = np.array(tuple(map(self.radius,zrange)))

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
        mbx_daten = tuple(map(self.Mbx,z_range_k))
        ax[1,0].plot(z_range_k,mbx_daten)
        ax[1,0].fill_between(z_range_k,0,mbx_daten,alpha=0.3)
        ax[1,0].set_xlabel("$z\\,[mm]$")
        ax[1,0].set_ylabel("$Mb_x\\,[Nm]$")
        ax[1,0].set_title("Biegemoment um X")
        ax[1,0].grid()

        # Mby Biegemomentenverlauf
        mby_daten = tuple(map(self.Mby,z_range_k))
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
        return round(result/1000,10)
    
    def Mby(self,z):
        """Berechnet numerisch den Biegemomentenverlauf um die globale Y-Achse in `N*m`"""
        result = 0
        for kraft in self.belastungen:
            _,z_kraft,r,phi,fx,fy,fz = kraft
            if z_kraft<z:
                result += -1*fx*(z-z_kraft)
                result += fz*r*np.sin(phi)
        return round(result/1000,10)
    
    def Mt(self,z):
        """Berechnet numerisch den Torsionsmomentenverlauf um die Globale Z-Achse in `N*m`"""
        result = 0
        for kraft in self.belastungen:
            _,z_kraft,r,phi,fx,fy,fz = kraft
            if z_kraft<=z:
                result += -1*fx*r*np.cos(phi)
                result += -1*fy*r*np.sin(phi)
        return round(result/1000,10)
    
    def Wb(self,z):
        """Gibt das Widerstandsmoment gegen Biegung an der Stelle z in `mm^3` aus."""
        return np.pi/32 * self.d(z)**3
    
    def Verformung_x(self,z,*schrittweite):
        """Berechnet die Verformungs- und Neigungsvektoren. Es kann optional die Schrittweite der Integration angegeben werden."""
        E = 210e3 # N/mm^2
        if len(schrittweite)==0:
            dz = self.dz
        else:
            dz = schrittweite[0]
        minL = min(self.z_daten)
        maxL = max(self.z_daten)
        z_range = np.arange(minL,maxL,dz)

        def q_ers(z):
            return (64*self.Mbx(z))/(np.pi*self.d(z)**4)
        
        def F_ers():
            integral = 0
            for z in z_range:
                integral+=q_ers(z)*(maxL-z)
            F_ers = 1/maxL * integral*dz
            return (F_ers)*1000 # N/mm^2
        
        if self.__F_ers is None:
            self.__F_ers = F_ers()
        F_e = self.__F_ers

        # Biegung
        def Biegung(z):
            integral = 0
            for s in z_range[z_range<=z]:
                integral += q_ers(s)*(z-s)*dz
            return 1/E*(F_e*z-integral*1000)
        plt.plot(z_range,tuple(map(Biegung,z_range)))
        plt.gca().invert_yaxis()
        plt.grid()
        plt.show()
        return Biegung(z)
    
    
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

if __name__ == "__main__":
    Werkstoff.aus_csv_laden()
    test = Welle("Test", 0, 195,Werkstoff.Werkstoffe["S275N"])

    test.set_geometrie(
        ((0,10),
        (40,10),
        (40,20),
        (80,20),
        (80,27.5),
        (160,27.5),
        (160,15),
        (195,15))
    )
    test.set_Kraft(3500, "r", 20, -test.d(20)/2)
    test.set_Kraft(-4500, "r", 135, -test.d(135)/2, 0)

    test.lagerkräfte_berechnen()
    #test.plot()
    print(test.Verformung_x(190,1))


    
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