import os

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

    def aus_datenbank_laden(self=None) -> None:
        for line in werkstoffdaten.splitlines():
            if line[0] != "#":
                args = line.strip().split(",")
                Werkstoff.Werkstoffe[args[0]] = Werkstoff(*args)
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


werkstoffdaten = """# Name,sigma_zdW (Zug-Druck-Wechselfestigkeit),sigma_bW (Biegewechselfestigkeit),tau_tW (Torsionswechselfestigkeit),Art,Cr-Ni-Einsatzstahl (0=nein;1=ja), sigma_B, sigma_S
S235JR,140,180,105,Baustahl,0,360,235
S275J0,170,215,125,Baustahl,0,410,275
E295,195,245,145,Baustahl,0,470,295
S355J0,205,255,150,Baustahl,0,470,355
E335,235,290,180,Baustahl,0,570,335
E360,275,345,205,Baustahl,0,670,360
S275N,150,185,110,Baustahl,0,370,275
S355N,190,235,140,Baustahl,0,470,355
S420N,210,260,155,Baustahl,0,520,420
S460,220,275,165,Baustahl,0,550,460
C10E,200,250,150,Einsatzstahl,0,500,310
17Cr3,320,400,240,Einsatzstahl,0,800,545
16MnCr5,400,500,300,Einsatzstahl,0,1000,695
20MnCr5,480,600,360,Einsatzstahl,0,1200,850
18MnCrS4,440,550,330,Einsatzstahl,0,1100,775
18CrNiMo7-6,480,600,360,Einsatzstahl,1,1200,850
31CrMo12,400,500,300,Nitrierstahl,0,1000,800
31CrMoV9,400,500,300,Nitrierstahl,0,1000,800
15CrMoV59,360,450,270,Nitrierstahl,0,900,750
34CrAlMo5,320,400,240,Nitrierstahl,0,800,600
34CrAlNi7,340,425,255,Nitrierstahl,0,850,650
1 C22,200,250,150,Vergütungsstahl,0,500,340
2 C22,200,250,150,Vergütungsstahl,0,500,340
1 C25,220,275,165,Vergütungsstahl,0,550,370
1 C30,240,300,180,Vergütungsstahl,0,600,400
1 C35,250,315,190,Vergütungsstahl,0,630,430
1 C40,260,325,200,Vergütungsstahl,0,650,460
1 C45,280,350,210,Vergütungsstahl,0,700,490
2 C45,280,350,210,Vergütungsstahl,0,700,490
1 C50,300,375,220,Vergütungsstahl,0,750,520
1 C60,340,425,250,Vergütungsstahl,0,850,580
46Cr2,360,450,270,Vergütungsstahl,0,900,650
41Cr4,400,500,300,Vergütungsstahl,0,1000,800
34CrMo4,400,500,300,Vergütungsstahl,0,1000,800
42CrMo4,440,550,330,Vergütungsstahl,0,1100,900
50CrMo4,440,550,330,Vergütungsstahl,0,1100,900
36CrNiMo4,440,550,330,Vergütungsstahl,0,1100,900
30CrNiMo8,500,625,375,Vergütungsstahl,0,1250,1050
34CrNiMo6,480,600,360,Vergütungsstahl,0,1200,1000
"""