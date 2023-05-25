"""
Klassendefinition für Werkstoffe
"""

class Werkstoff():
    Werkstoffe = {} # Dictionary mit allen erzeugten Werkstoffen

    def __init__(self, name, sigma_zdW, sigma_bW, tau_tW):
        self.name = name
        self.sigma_zdW = sigma_zdW
        self.sigma_bW = sigma_bW
        self.tau_tW = tau_tW
        Werkstoff.Werkstoffe[name] = self
    def __repr__(self) -> str:
        return self.name
    def aus_csv_laden():
        with open("Werkstoffdaten.csv","r",encoding="utf8") as datei:
            rohdaten = datei.readlines()

        for line in rohdaten:
            if line[0] != "#":
                name,zdw,bwf,twf = line.strip().split(",")
                Werkstoff(name,float(zdw),float(bwf),float(twf))
        return 1