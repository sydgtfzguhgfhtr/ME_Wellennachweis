import numpy as np

"""
CSV mit Werkstoffdaten:
0...Name
1..sigma_zdW (Zug-Druck-Wechselfestigkeit)
2...sigma_bW (Biegewechselfestigkeit) / manchmal sigma_bm (in Übungen in MathCad)
3...tau_tW (Torsionswechselfestigkeit)

Festigkeitswerte (alle in N/mm^-2):
for i in Werkstoffliste:
    if i == "Name":
        Zug_Druck_Wechselfestigkeit = i.sigma_zdW
        Biegewechselfestigkeit = i.sigma_bW
        Torsionswechselfestigkeit = i.tau_tW
"""
Daten = np.loadtxt("Werkstoffdaten.csv",delimiter=",",dtype=np.ndarray)

class Werkstoff():
    def __init__(self, name, sigma_zdW, sigma_bW, tau_tW):
        self.name = name
        self.sigma_zdW = sigma_zdW
        self.sigma_bW = sigma_bW
        self.tau_tW = tau_tW

Namen = []; Sigma_B = []; Sigma_S = []; Sigma_zdW = []; Sigma_bW = []; Tau_tW = []

for i in range(55):
    Namen.append(Daten[i][0])
    Sigma_zdW.append(Daten[i][1])
    Sigma_bW.append(Daten[i][2])
    Tau_tW.append(Daten[i][3])

Werkstoff_liste = []

for i in range(len(Namen)):
    Werkstoff_liste.append(Werkstoff(Namen[i], int(Sigma_zdW[i]), int(Sigma_bW[i]), int(Tau_tW[i])))

#Beispiel:
# for Werkstoff in Werkstoff_liste:
#    if Werkstoff.name == "S235JR":
#        print(Werkstoff.sigma_bW)

# Werkstoffarten:
Baustähle = ["S235JR","S275JR","E295","S355J0","E335","E360","S275N","S355N","S420N","S460N"]
Einsatzstähle = ["C10E", "17Cr3", "16MnCr5", "20MnCr5", "18MoCrS4", "18CrNiMo7-6"]
Nitrierstähle = ["31CrMo12", "31CrMoV9", "15CrMoV59", "34CrAlMo5", "34CrAlNi7"]
Vergütungsstähle = ["1 C22", "2 C22", "1 C25", "1 C30", "1 C35", "1 C35", "1 C40", "1 C45", "2 C45", "1 C50", "1 C60", "46Cr2", "41Cr4", "34CrMo4", "42CrMo4", "50CrMo4", "36CrNiMo4", "30CrNiMo8", "34CrNiMo6"]