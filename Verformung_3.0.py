import numpy as np
import scipy.integrate as spt
import matplotlib.pyplot as plt

class Welle:
    def __init__(self,name:str,lagerabstand) -> None:
        self.name = str(name)
        self.lagerabstand = lagerabstand
        self.länge = 0
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
        lges = self.lagerabstand
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
    def plot(self,kräfte=True,biegemomente=True):
        """Stellt die Welle dar."""
        _,z_kräfte,_,_,_,_,_=zip(*test.belastungen)
        max_z_k = max(z_kräfte)
        max_z = max(self.z_daten)

        zrange = np.linspace(0,max_z,1000)
        z_range_k = np.linspace(0,max_z_k,1000)
        rrange = np.array(tuple(map(self.radius,zrange)))

        fig,ax = plt.subplots(2,2,constrained_layout=True,sharex="col",sharey="row",num=self.name+" Belastungsplot")
        fig.set_size_inches(15,10)
        fig.suptitle(f'Welle "{self.name}"',fontsize=18)
        ax[0,0].plot(zrange,rrange,"k")
        ax[0,0].plot(zrange,rrange*-1,"k")
        ax[0,0].hlines(0,-5,self.z_daten[-1]+5,linestyles="dashdot",colors="black")
        for i,z in enumerate(self.z_daten):
            ax[0,0].vlines(z,self.radius(z)*-1,self.radius(z),colors="black")

        # maximale Kraft ermitteln, zum skalieren der Vektoren
        l_max = 50
        max_f = max((self.belastungen[i][0] for i in range(len(self.belastungen))))

        for kraft in self.belastungen:
            _,z,r,phi,fx,fy,fz = kraft
            if round(abs(fy),5)>0: # Y Kräfte zeichnen
                ax[0,0].arrow(z,r*np.cos(phi),0,l_max*-fy/max_f,head_width=2,width=1,color="green",zorder=100)
            if round(abs(fz),5)>0: # Z Kräfte zeichnen
                ax[0,0].arrow(z,r*np.cos(phi),l_max*fz/max_f,0,head_width=2,width=1,color="blue",zorder=100)

        ax[0,0].grid()
        ax[0,0].set_title("YZ-Ebene")
        ax[0,0].set_xlabel("$z\\,[mm]$")
        ax[0,0].set_ylabel("$r\\,[mm]$")

        ax[0,1].plot(zrange,rrange,"k")
        ax[0,1].plot(zrange,rrange*-1,"k")
        ax[0,1].hlines(0,-5,self.z_daten[-1]+5,linestyles="dashdot",colors="black")
        for i,z in enumerate(self.z_daten):
            ax[0,1].vlines(z,self.radius(z)*-1,self.radius(z),colors="black")

        for kraft in self.belastungen:
            _,z,r,phi,fx,fy,fz = kraft
            if round(abs(fx),5)>0: # X Kräfte zeichnen
                ax[0,1].arrow(z,r*np.sin(phi),0,l_max*-fx/max_f,head_width=2,width=1,color="red",zorder=100)
            if round(abs(fz),5)>0: # Z Kräfte zeichnen
                ax[0,1].arrow(z,r*np.sin(phi),l_max*fz/max_f,0,head_width=2,width=1,color="blue",zorder=100)

        ax[0,1].grid()
        ax[0,1].set_title("XZ-Ebene")
        ax[0,1].set_xlabel("$z\\,[mm]$")
        ax[0,1].set_ylabel("$r\\,[mm]$")

        # Mbx Biegemomentenverlauf
        mbx_daten = tuple(map(self.Mbx,z_range_k))
        ax[1,0].plot(z_range_k,mbx_daten)
        ax[1,0].fill_between(z_range_k,0,mbx_daten,alpha=0.3)
        ax[1,0].set_xlabel("$z\\,[mm]$")
        ax[1,0].set_ylabel("$Mb_x\\,[Nmm]$")
        ax[1,0].set_title("Biegemoment um X")
        ax[1,0].grid()

        # Mby Biegemomentenverlauf
        mby_daten = tuple(map(self.Mby,z_range_k))
        ax[1,1].plot(z_range_k,mby_daten)
        ax[1,1].fill_between(z_range_k,0,mby_daten,alpha=0.3)
        ax[1,1].set_xlabel("$z\\,[mm]$")
        ax[1,1].set_ylabel("$Mb_y\\,[Nmm]$")
        ax[1,1].set_title("Biegemoment um Y")
        ax[1,1].grid()

        ax[1,1].invert_yaxis() # Achse invertieren

        plt.show()

    def Mbx(self,z):
        """Berechnet numerisch den Biegemomentenverlauf um die globale X-Achse in `N*mm`"""
        result = 0
        for kraft in self.belastungen:
            _,z_kraft,r,phi,fx,fy,fz = kraft
            if z_kraft<z:
                result += -1*fy*(z-z_kraft)
                result += fz*r*np.cos(phi)
        return round(result,10)
    
    def Mby(self,z):
        """Berechnet numerisch den Biegemomentenverlauf um die globale Y-Achse in `N*mm`"""
        result = 0
        for kraft in self.belastungen:
            _,z_kraft,r,phi,fx,fy,fz = kraft
            if z_kraft<z:
                result += -1*fx*(z-z_kraft)
                result += fz*r*np.sin(phi)
        return round(result,10)
    
    def Wb(self,z):
        """Gibt das Widerstandsmoment gegen Biegung an der Stelle z in `mm^3` aus."""
        return np.pi/32 * self.d(z)**3
    
    def sigma_x(self, z):
        return(self.Mbx(z)/self.Wb(z))
    
    def sigma_y(self, z):
        return(self.Mby(z)/self.Wb(z))

    def Verformung(self, z, NUM):
        E = 210000
        q_x = []
        q_y = []
        q_x_F_int = []
        q_y_F_int = []

        mm = np.linspace(0, self.länge, num = NUM*self.länge)

        for i in mm:
            q_x.append((64*self.Mbx(i))/(np.pi*self.d(i)**4))
            q_y.append((64*self.Mby(i))/(np.pi*self.d(i)**4))
            q_x_F_int.append((64*self.Mbx(i))/(np.pi*self.d(i)**4)*(self.länge-i))
            q_y_F_int.append((64*self.Mby(i))/(np.pi*self.d(i)**4)*(self.länge-i))

        F_ers_x = 1/self.länge * spt.simps(q_x_F_int, mm)
        F_ers_y = 1/self.länge * spt.simps(q_y_F_int, mm)

        nn = np.linspace(0, z, num = (NUM*z))

        Integral_x = spt.simps(q_x, nn)
        Integral_y = spt.simps(q_y, nn)

        print(Integral_x)

        phi_x = 1/E * (F_ers_x-Integral_x)


lab2 = 290
lz21 = 95
lz22 = 115
düb = 75
z_ritzel = 20
r_ritzel = 10
z_rad = 135
r_rad = 27.5

test = Welle("Zwischenwelle",195)
test.set_geometrie([
    (0,10),
    (40,10),
    (40,20),
    (80,20),
    (80,27.5),
    (160,15),
    (195,15)
])

test.set_Kraft(0,"a",z_rad,r_rad,0)
test.set_Kraft(3500,"r",z_rad,r_rad,0) # Rad z12
test.set_Kraft(0,"t",z_rad,r_rad,0)

test.set_Kraft(0,"a",z_ritzel,r_ritzel,0)
test.set_Kraft(-4500,"r",z_ritzel,r_ritzel,0) # Ritzel z21
test.set_Kraft(0,"t",z_ritzel,r_ritzel,0)

test.lagerkräfte_berechnen()


test.Verformung(0, 2)
