from Klassen import *
import matplotlib.pyplot as plt

Werkstoff.aus_csv_laden()

Abtriebswelle = Welle("Abtriebswelle", 180, 575, "42CrMo4", "nein")
Abtriebswelle.set_geometrie(
    (
        (0,30),
        (155,30),
        (155,35),
        (205,35),
        (205,38),
        (402,38),
        (402,40),
        (482,40),
        (482,50),
        (529,50),
        (529,40),
        (575,40)
    )
)

Abtriebswelle.set_Kraft(24384,"t",442,213.785,0)
Abtriebswelle.set_Kraft(9188,"r",442,213.785,0)
Abtriebswelle.set_Kraft(6534,"a",442,213.785,0)

Abtriebswelle.welle_darstellen()


Abtriebswelle.lagerkräfte_berechnen()
Abtriebswelle.verformung_berechnen()

Abtriebswelle.plot()

Abtriebswelle.plots_speichern()

p1 = Welle_Absatz(Abtriebswelle,77.5,"eine Passfeder",10)
a1 = Welle_Absatz(Abtriebswelle,155,"Absatz",10,5)
r1 = Welle_Absatz(Abtriebswelle,159,"umlaufende Rechtecknut",10,3,0.1,2)
a2 = Welle_Absatz(Abtriebswelle,205,"Absatz",10,10)
a3 = Welle_Absatz(Abtriebswelle,402,"Absatz",10,5)
p1 = Welle_Absatz(Abtriebswelle,482,"Pressverbindung",2)
a4 = Welle_Absatz(Abtriebswelle,482,"Absatz",10,1)


Werte_in_CSV_speichern("Abtriebswelle",p1,a1,r1,a2,a3,p1,a4)