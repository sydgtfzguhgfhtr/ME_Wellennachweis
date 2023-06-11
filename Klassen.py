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
    def __init__(self,name:str) -> None:
        self.name = str(name)
        self.geometrie = []
        self.z_daten = []
        self.r_daten = []
        self.belastungen = [(0,0,0,0,0,0,0),(0,0,0,0,0,0,0),(0,0,0,0,0,0,0),(0,0,0,0,0,0,0),(0,0,0,0,0,0,0)]
    
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
        lges = self.z_daten[-1]
        summe_krafthebelx,summe_krafthebely = 0,0
        summe_kräftex,summe_kräftey,summe_kräftez = 0,0,0
        for _,zk,rk,_,fx,fy,fz in self.belastungen:
            summe_krafthebely += -fy*zk
            summe_krafthebelx += -fx*zk
        self.belastungen[3] = (abs(summe_krafthebelx/lges),lges,0,0,summe_krafthebelx/lges,0,0) # Lagerkraft Loslager X
        self.belastungen[4] = (abs(summe_krafthebely/lges),lges,0,0,0,summe_krafthebely/lges,0) # Lagerkraft Loslager Y

        for _,zk,rk,_,fx,fy,fz in self.belastungen:
            summe_kräftex += -fx
            summe_kräftey += -fy
            summe_kräftez += -fz
        self.belastungen[0] = (abs(summe_kräftex),0,0,0,summe_kräftex,0,0) # Lagerkraft Festlager X
        self.belastungen[1] = (abs(summe_kräftey),0,0,0,0,summe_kräftey,0) # Lagerkraft Festlager Y
        self.belastungen[2] = (abs(summe_kräftez),0,0,0,0,0,summe_kräftez) # Lagerkraft Festlager Z
        print("-"*20)
        print("Festlager X",test.belastungen[0])
        print("Festlager Y",test.belastungen[1])
        print("Festlager Z",test.belastungen[2])
        print("Loslager X",test.belastungen[3])
        print("Loslager Y",test.belastungen[4])

    def set_geometrie(self,punkte:list):
        """
        Definiert die Wellengeometrie als Liste aus Punkten in der Form [[z1,r1],[z2,r2],...]
        """
        self.geometrie = punkte
        self.z_daten,self.r_daten = zip(*self.geometrie) # Entpackt die Geometriedaten in Vektoren

    def radius(self,z):
        """Gibt Radius der Welle an Stelle z aus. Alle Längen werden in `mm` angegeben"""
        for i,zr in enumerate(self.geometrie):
            z1,z2 = self.geometrie[i-1][0],self.geometrie[i][0]
            r1,r2 = self.geometrie[i-1][1],self.geometrie[i][1]
            
            if z<=z2:
                m = (z - z1) / (z2 - z1)
                return r1 + m * (r2 - r1)
    def r(self,z):
        """Gibt Radius der Welle an Stelle z aus. Alle Längen werden in `mm` angegeben"""
        return self.radius(z)
    def d(self,z):
        """Gibt Durchmesser der Welle an Stelle z aus. Alle Längen werden in `mm` angegeben"""
        return 2*self.radius(z)
    def durchmesser(self,z):
        """Gibt Durchmesser der Welle an Stelle z aus. Alle Längen werden in `mm` angegeben"""
        return self.d(z)
    def plot(self,kräfte=True,biegemomente=False):
        """Stellt die Welle dar."""
        zrange = np.arange(0,max(self.z_daten),0.1)
        rrange = np.array(tuple(map(self.radius,zrange)))

        fig,ax = plt.subplots(1,2)
        fig.align_labels(ax)
        fig.suptitle(f'Welle "{self.name}"')
        ax[0].plot(zrange,rrange,"k")
        ax[0].plot(zrange,rrange*-1,"k")
        ax[0].hlines(0,-5,self.z_daten[-1]+5,linestyles="dashdot",colors="black")
        for i,z in enumerate(self.z_daten):
            ax[0].vlines(z,self.radius(z)*-1,self.radius(z),colors="black")

        if kräfte:
            # maximale Kraft ermitteln, zum skalieren der Vektoren
            l_max = 50
            max_f = max((self.belastungen[i][0] for i in range(len(self.belastungen))))

            for kraft in self.belastungen:
                _,z,r,phi,fx,fy,fz = kraft
                if round(abs(fy),5)>0: # Y Kräfte zeichnen
                    ax[0].arrow(z,r*np.cos(phi),0,l_max*-fy/max_f,head_width=2,width=1,color="green")
                if round(abs(fz),5)>0: # Z Kräfte zeichnen
                    ax[0].arrow(z,r*np.cos(phi),l_max*fz/max_f,0,head_width=2,width=1,color="blue")

        ax[0].grid()
        #ax[0].set_title(f'Welle "{self.name}" in YZ')
        ax[0].set_xlabel("$z\\,[mm]$")
        ax[0].set_ylabel("$y\\,[mm]$")
        ax[0].axis("equal")

        ax[1].plot(zrange,rrange,"k")
        ax[1].plot(zrange,rrange*-1,"k")
        ax[1].hlines(0,-5,self.z_daten[-1]+5,linestyles="dashdot",colors="black")
        for i,z in enumerate(self.z_daten):
            ax[1].vlines(z,self.radius(z)*-1,self.radius(z),colors="black")

        if kräfte:
            # maximale Kraft ermitteln, zum skalieren der Vektoren
            l_max = 50
            max_f = max((self.belastungen[i][0] for i in range(len(self.belastungen))))

            for kraft in self.belastungen:
                _,z,r,phi,fx,fy,fz = kraft
                if round(abs(fx),5)>0: # X Kräfte zeichnen
                    ax[1].arrow(z,r*np.sin(phi),0,l_max*-fx/max_f,head_width=2,width=1,color="red")
                if round(abs(fz),5)>0: # Z Kräfte zeichnen
                    ax[1].arrow(z,r*np.sin(phi),l_max*fz/max_f,0,head_width=2,width=1,color="blue")

        ax[1].grid()
        #ax[1].set_title(f'in XZ')
        ax[1].set_xlabel("$z\\,[mm]$")
        ax[1].set_ylabel("$x\\,[mm]$")
        ax[1].axis("equal")
        plt.show()

if __name__ == "__main__":
    test = Welle("Testwelle")
    test.set_geometrie([
        [0,30],
        [50,30],
        [60,35],
        [100,35],
        [100,40],
        [130,40],
        [130,25],
        [200,25],
    ])
    
    test.set_Kraft(10,"r",150,70,90)
    #test.set_Kraft(20,"a",150,70,90)
    test.lagerkräfte_berechnen()
    test.plot()

# VORZEICHENFEHLER IM X