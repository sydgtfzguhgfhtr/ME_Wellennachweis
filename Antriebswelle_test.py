from Klassen import *
import matplotlib.pyplot as plt

Werkstoff.aus_csv_laden()

Antriebswelle = Welle("Antriebswelle", 342, 81, "42CrMo4", "nein")
Antriebswelle.set_geometrie(
    ((0, 30),
     (60, 30),
     (60, 50),
     (102, 50),
     (102, 90),
     (148, 90),
     (148, 100),
     (317, 100),
     (317, 90),
     (367, 90),
     (367, 50),
     (387, 50),
     (387, 40),
     (463, 40))
)

Antriebswelle.set_Kraft(6145, "t", 0, 38.31, 0)
Antriebswelle.set_Kraft(2380, "r", 0, 38.31, 0)
Antriebswelle.set_Kraft(2237, "a", 0, 38.31, 0)

# Antriebswelle.welle_darstellen()

Antriebswelle.lagerkräfte_berechnen()
Antriebswelle.verformung_berechnen()

# plt.plot(Antriebswelle.z_range,Antriebswelle.neigung_x,label="X")
# plt.plot(Antriebswelle.z_range,Antriebswelle.neigung_y,label="Y")
# plt.grid()
# plt.legend()
# plt.gca().invert_yaxis()
# plt.show()

z11 = Welle_Absatz(Antriebswelle, 0, "Pressverbindung", 10)
a1 = Welle_Absatz(Antriebswelle, 60, "Absatz", 10, 5)
a2 = Welle_Absatz(Antriebswelle, 102, "Absatz", 10, 3)
a3 = Welle_Absatz(Antriebswelle, 148, "Absatz", 10, 1)
a4 = Welle_Absatz(Antriebswelle, 317,"Absatz",10, 1)
Rechtecknut = Welle_Absatz(Antriebswelle, 363, "umlaufende Rechtecknut", 10, 7, 0.2, 2)
a5 = Welle_Absatz(Antriebswelle, 367, "Absatz", 10, 5)
a6 = Welle_Absatz(Antriebswelle, 387, "Absatz", 10, 5)
p1 = Welle_Absatz(Antriebswelle, 450, "eine Passfeder", 10)

Antriebswelle.plots_speichern()
# Antriebswelle.plot()



sigma_x = []
sigma_y = []
tau = []

for i in range(Antriebswelle.länge):
    sigma_x.append(Antriebswelle.Spannungen(i)[0])
    sigma_y.append(Antriebswelle.Spannungen(i)[1])
    tau.append(Antriebswelle.Spannungen(i)[2])

# plt.plot(sigma_x)
# plt.plot(sigma_y)
# plt.plot(tau)
# plt.show()

L = [z11, a1, a2, a3, a4, Rechtecknut, a5, a6, p1]

Werte_in_CSV_speichern(z11, a1, a2, a3, a4, Rechtecknut, a5, a6, p1)

# Warnung beim Ausführen:
# PS C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis> & "C:/Program Files/Python310/python.exe" c:/Users/Nadine/Documents/Studium/Studium/1234567890/ME_Wellen/ME_Wellennachweis/Antriebswelle_test.py
# c:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\Klassen.py:390: IntegrationWarning: The integral is probably divergent, or slowly convergent.
#   integral,_ = quad(q_ers_x,minl,z,epsabs=1e-4)
# PS C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis> 