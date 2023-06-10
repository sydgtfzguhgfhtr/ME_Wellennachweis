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
            kraft = (betrag,z,r,phi,betrag*np.sin(phi),betrag*np.cos(phi),0)
        elif typ[0].casefold()=="t":
            kraft = (betrag,z,r,phi,betrag*np.cos(phi),betrag*np.sin(phi),0)
        elif typ[0].casefold()=="a":
            kraft = (betrag,z,r,phi,0,0,betrag)
        else:
            raise ValueError("Krafttyp wurde nicht erkannt. Erlaubt sind 'radial','tangential' und 'axial'.")
        self.belastungen.append(kraft)
        # Lagerkräfte berechnen und in Belastungen aufnehmen
        # Lagerkraft Loslager
        lges = self.z_daten[-1]
        summe_krafthebely = 0
        summe_kräftey,summe_kräftez = 0,0
        for _,zk,rk,_,fx,fy,fz in self.belastungen:
            summe_krafthebely += -fy*zk
        self.belastungen[4] = (summe_krafthebely/lges,lges,0,0,0,summe_krafthebely/lges,0) # Lagerkraft Loslager Y
        for _,zk,rk,_,fx,fy,fz in self.belastungen:
            summe_kräftey += -fy
            summe_kräftez += -fz
        self.belastungen[1] = (summe_kräftey,0,0,0,0,summe_kräftey,0) # Lagerkraft Festlager Y
        self.belastungen[2] = (summe_kräftez,0,0,0,0,0,summe_kräftez) # Lagerkraft Festlager Z



    def set_geometrie(self,punkte:list):
        """
        Definiert die Wellengeometrie als Liste aus Punkten in der Form [[z1,r1],[z2,r2],...]
        """
        self.geometrie = punkte
        self.z_daten,self.r_daten = zip(*self.geometrie)

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
    def plot(self,biegemomente=False):
        """Stellt die Welle dar."""
        zrange = np.arange(0,max(self.z_daten),0.1)
        rrange = np.array(tuple(map(self.radius,zrange)))

        plt.plot(zrange,rrange,"k")
        plt.plot(zrange,rrange*-1,"k")
        plt.hlines(0,-5,self.z_daten[-1]+5,linestyles="dashdot",colors="black")
        for i,z in enumerate(self.z_daten):
            plt.vlines(z,self.radius(z)*-1,self.radius(z),colors="black")
        plt.grid()
        plt.title(f'Welle "{self.name}"')
        plt.xlabel("$z\\,[mm]$")
        plt.ylabel("$r\\,[mm]$")
        plt.axis("equal")
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
    test.set_Kraft(1,"r",100,test.radius(100),0)
    #test.plot()
    print(test.belastungen)