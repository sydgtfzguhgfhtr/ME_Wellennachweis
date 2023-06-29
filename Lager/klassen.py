# Klassendefinitionen für Lagernachweis
# Code von Nadine Schulz, Quentin Huss

import numpy as np
import pandas as pd

class Lager:
    def __init__(self,name,Innendurchmesser,Drehzahl,Radialkraft,Axialkraft,Ölviskosität,Betriebstemp,Verunreinigung,Pa=0.1):
        self.name = str(name)
        self.n = Drehzahl # Drehzahl in 1/min
        self.d = Innendurchmesser # Innendurchmesser in mm
        self.Fr = Radialkraft #Radialkraft in kN
        self.Fa = Axialkraft # Axialkraft in kN
        self.a1 = (np.log(1/(1-Pa)/np.log(1/0.9)))**1/1.5 # Lebensdauerbeiwert
        self.nu = Ölviskosität # Ölviskosität
        self.T_bet = Betriebstemp # Betriebstemperatur
        self.eta = Verunreinigung # Grad der Verunreinigung
        self.p = None # Lebensdauerexponent

    def __repr__(self) -> str:
        return "Lager: "+self.name
    
    def a_SKF(self):
        # darf nicht größer 50 werden
        kappa = self.kappa()
        if kappa > 4: kappa = 4
        if self.ID <= 790:
            A = 2.56705; D = 0.83; E = 1/3; F = 9.3; G = 1
            if kappa <0.4:
                B = 2.26492
                C = 0.0543806
            elif kappa < 1:
                B = 1.99866
                C = 0.19087
            elif kappa <=4:
                B = 1.99866
                C = 0.0717391
        else:
            A = 1.58592; D = 1; E = 0.4; F = 9.185; G = 1
            if kappa < 0.4:
                B = 1.39926
                C = 0.0543806
            elif kappa < 1:
                B = 1.23477
                C = 0.19087
            elif kappa >= 4:
                B = 1.23477
                C = 0.0717391

        a = (1/10)*1/(1-((A-(B/(kappa**C)))**D)*(((self.eta*self.Pu)/(G*self.aequivalente_statische_Bealstung()))**E))**F
        return a

    def Betriebsviskosität(self,t,t1,nu1,t2,nu2):
        """Interpoliert die Betriebsviskosität in `mm^2/s` aus den 2 bekannten Viskositäten `nu1` und `nu2` und den dazugehörigen Temperaturen `t1` und `t2`."""
        b = -(np.log(t2/t1))/(np.log(nu1/nu2))
        a = nu1**-b*t1
        return np.e**((np.log(t)-np.log(a))/b)
    
    def Bezugsviskosität(self):
        dm = 0.5*(self.d+self.D)
        if self.n < 1000:
            nu_1 = 45000*self.n**(-0.83)*dm**(-0.5)
        else:
            nu_1 = 4500*self.n**(-0.5)*dm**(-0.5)
        return nu_1

    def aus_CSV_laden(self,ID):
        """
        Lädt per ID die Daten aus der CSV und importiert die Attribute.
        """
        self.ID = ID
        if ID <= 790:
            Lager = pd.read_csv(r"Lager\einreihige_Rillenkugellager.csv",delimiter=",")
            Lager = Lager[Lager["ID"]==ID]
            # hat sich irgendwie alles eins nach links verschoben funktioniert jetzt aber so
            self.d = int(Lager["Nr"])
            self.D = int(Lager["d"])
            self.B = float(Lager["D"])
            self.C = float(Lager["B"])
            self.C0 = float(Lager["C"])
            self.Pu = float(Lager["C0"])
            try:
                self.n_ref = float(Lager["Pu"])
            except ValueError:
                self.n_ref = None
            self.n_grenz = float(Lager["Referenzdrehzahl"])
            self.f0 = float(Lager["kr"])
        else:
            Lager = pd.read_csv(r"Lager\Einreihige_Zylinderrollenlager.csv",delimiter=",")
            Lager = Lager[Lager["Nr"]==ID]
            self.d = int(Lager["d"])
            self.D = int(Lager["D"])
            self.B = float(Lager["B"])
            self.C = float(Lager["C"])
            self.C0 = float(Lager["C0"])
            self.Pu = float(Lager["Pu"])   
            self.n_ref = float(Lager["Referenzdrehzahl"])
            self.n_grenz = float(Lager["Grenzdrehzahl"]) 
    
    def kappa(self):
        kappa = self.nu/self.Betriebsviskosität()
        return(kappa)
    
    def aequivalente_dynamische_Belastung(self):
        P = self.X*self.Fr+self.Y*self.Fa
        return P
    
    def aequivalente_statische_Bealstung(self):
        P0 = self.X0*self.Fr+self.Y0*self.Fa
        return P0

    def fs(self):
        fs = self.C0/self.aequivalente_statische_Bealstung()
        return fs

    def erweiterte_Lebensdauer_in_Stunden(self):
        Lmnh = (10**6/(60*self.n))*self.a1*self.a_SKF()*(self.C/self.aequivalente_statische_Bealstung())**self.p
        return(Lmnh)

class Zylinderrollenlager(Lager):
    # ID ab 791
    # NUR ALS LOSLAGER VERWENDEN (sonst stimmt äquivalente dynamische Lagerbelastung nicht)
    # nur als Loslager logisch (Reibung?)
    # sonst ist X und Y von Maßreihe abhängig (keine Ahnung wie die funktioniert)
    def __init__(self, name, di, Drehzahl, Radialkraft, Axialkraft, Ölviskosität, Verunreinigung, Pa=0.1) -> None:
        super().__init__(name, di, Drehzahl, Radialkraft, Axialkraft, Ölviskosität, Verunreinigung, Pa)
        self.X = 1
        self.Y = 0
        self.X0 = 1 # für statische Belastung
        self.Y0 = 0 # für statische Belastung
        self.p = 10/3 # Lebensdauerexponent

class Rillenkugellager(Lager):
    # ID bis einschließlich 790
    def __init__(self, name, di, Drehzahl, Radialkraft, Axialkraft, Ölviskosität, Verunreinigung, Pa=0.1) -> None:
        super().__init__(name, di, Drehzahl, Radialkraft, Axialkraft, Ölviskosität, Verunreinigung, Pa)
        self.X0 = 0.6   # für statische Belastung
        self.X = 0.56   #Folie 18
        self.Y0 = 0.5   # für statische Belastung
        self.p = 3 # Lebensdauerexponent
    def Y_Rillenkugellager(self): # Folie 18
        m,n = np.polyfit([0.172,0.345,0.689,1.03,1.38,2.07,3.45,5.17,6.89],[2.3,1.99,1.71,1.55,1.45,1.31,1.15,1.04,1],deg=1)
        Y = m*((self.f0*self.Fa)/self.C0)+n
        self.Y = Y
        return Y