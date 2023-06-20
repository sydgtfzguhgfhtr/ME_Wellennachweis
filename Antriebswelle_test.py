from Klassen import *
import matplotlib.pyplot as plt

Werkstoff.aus_csv_laden()

Antriebswelle = Welle("Antriebswelle", 342, 81, "42CrMo4", "nein")
Antriebswelle.set_geometrie(
    ((0, 22.5),
     (60, 22.5),
     (60, 25),
     (102, 25),
     (102, 28),
     (148, 28),
     (148, 30),
     (317, 30),
     (317, 20),
     (367, 20),
     (367, 16),
     (387, 16),
     (387, 15),
     (463, 15))
)

Antriebswelle.set_Kraft(6145, "t", 0, 38.31, 0)
Antriebswelle.set_Kraft(2380, "r", 0, 38.31, 0)
Antriebswelle.set_Kraft(-2237, "a", 0, 38.31, 0)

Antriebswelle.welle_darstellen()
Antriebswelle.lagerkräfte_berechnen()
Antriebswelle.verformung_berechnen()

#Antriebswelle.plot()



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


L = [z11, a1, a2, a3, a4, Rechtecknut, a5, a6, p1]

Werte_in_CSV_speichern("Antriebswelle",z11, a1, a2, a3, a4, Rechtecknut, a5, a6, p1)
