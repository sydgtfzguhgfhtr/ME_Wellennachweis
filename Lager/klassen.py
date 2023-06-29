# Klassendefinitionen für Lagernachweis
# Code von Nadine Schulz, Quentin Huss

import numpy as np

class Lager:
    def __init__(self,name,Innendurchmesser,Drehzahl,Radialkraft,Axialkraft,Ölviskosität,Verunreinigung,Pa=0.1) -> None:
        self.name = str(name)
        self.n = Drehzahl # Drehzahl in 1/min
        self.d = Innendurchmesser # Innendurchmesser in mm
        self.Fr = Radialkraft #Radialkraft in kN
        self.Fa = Axialkraft # Axialkraft in kN
        self.a1 = (np.log(1/(1-Pa)/np.log(1/0.9)))**1/1.5 # Lebensdauerbeiwert
        self.nu = Ölviskosität # Ölviskosität
        self.eta = Verunreinigung # Grad der Verunreinigung
        self.p = None # Lebensdauerexponent

    def __repr__(self) -> str:
        return "Lager: "+self.name
    
    def a_SKF(self):
        raise NotImplemented()
    
    def Betriebsviskosität(self):
        # siehe Übung Folie 36
        raise NotImplemented()
    
    def Bezugsviskosität(self):
        raise NotImplemented()
    
    def aus_CSV_laden(self,ID):
        """
        Lädt per ID die Daten aus der CSV und importiert die Attribute.
        """
        raise NotImplemented()
    
    def kappa(self):
        kappa = self.nu/self.Betriebsviskosität()
        return(kappa)
    
    def aequivalente_dynamische_Belastung(self):
        # X und Y für Rillenkugellager Übung Folie 17
        # X und Y bei Zylinderrollenlager WLK seite 511
        """äquivalente statische Lagerbelastung 
          [kN]
          Y Axiallastfaktor des Lagers
          = 0,6 für Lager der Reihen 10, 18, 19, 2, 3, 4
          = 0,4 für Lager der Reihen 12, 20, 22, 23, 28, 29, 30, 39
            """
        raise NotImplemented()
    
    def aequivalente_statische_Bealstung(self):
        P0 = self.X0*self.Fr+self.Y0*self.Fa
        return P0

    def fs(self):
        raise NotImplemented()

class Zylinderrollenlager(Lager):
    # ID ab 791
    def __init__(self, name, di, Drehzahl, Radialkraft, Axialkraft, Ölviskosität, Verunreinigung, Pa=0.1) -> None:
        super().__init__(name, di, Drehzahl, Radialkraft, Axialkraft, Ölviskosität, Verunreinigung, Pa)
        self.X0 = 1 # für statische Belastung
        self.Y0 = 0 # für statische Belastung
        self.p = 10/3 # Lebensdauerexponent

class Rillenkugellager(Lager):
    # ID bis einschließlich 790
    def __init__(self, name, di, Drehzahl, Radialkraft, Axialkraft, Ölviskosität, Verunreinigung, Pa=0.1) -> None:
        super().__init__(name, di, Drehzahl, Radialkraft, Axialkraft, Ölviskosität, Verunreinigung, Pa)
        self.X0 = 0.6   # für statische Belastung
        self.Y0 = 0.5   # für statische Belastung
        self.p = 3 # Lebensdauerexponent