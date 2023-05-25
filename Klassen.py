"""
Klassendefinitionen
"""

class Werkstoff():
    Werkstoffe = {} # Dictionary mit allen erzeugten Werkstoffen

    def __init__(self, name, sigma_zdW, sigma_bW, tau_tW,art="NA"):
        self.name = name
        self.sigma_zdW = float(sigma_zdW)
        self.sigma_bW = float(sigma_bW)
        self.tau_tW = float(tau_tW)
        self.art = art
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