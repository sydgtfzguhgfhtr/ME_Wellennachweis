from Klassen import *
import matplotlib.pyplot as plt

Werkstoff.aus_csv_laden()

Zwischenwelle = Welle("Zwischenwelle", 0, 313, "42CrMo4", "nein")
Zwischenwelle.set_geometrie(
    ((0,90),
    (46,90),
    (46,65),
    (163,65),
    (163,45),
    (243,45),
    (243,50),
    (290,50),
    (290,90),
    (336,90),
    (336,80),
    (378,80),
    (378,70),
    (438,70))
)

# z12
Zwischenwelle.set_Kraft(5961,"t",438,227.47,0)
Zwischenwelle.set_Kraft(-2309,"r",438,227.47,0)
Zwischenwelle.set_Kraft(-2170,"a",438,227.47,0)

#z21
Zwischenwelle.set_Kraft(26195,"t",203,50.73,0)
Zwischenwelle.set_Kraft(-9871,"r",203,50.73,0)
Zwischenwelle.set_Kraft(7019,"a",203,50.73,0)



Zwischenwelle.lagerkräfte_berechnen()
Zwischenwelle.verformung_berechnen()

Zwischenwelle.plot()

Zwischenwelle.plots_speichern()

a1 = Welle_Absatz(Zwischenwelle, 46, "Absatz", 10, 5)
a2 = Welle_Absatz(Zwischenwelle, 163, "Absatz",10,1)
z21 = Welle_Absatz(Zwischenwelle,203,"Pressverbindung",4)
a3 = Welle_Absatz(Zwischenwelle,243,"Absatz",10,1)
a4 = Welle_Absatz(Zwischenwelle,290,"Absatz",10,5)
a5 = Welle_Absatz(Zwischenwelle,336,"Absatz",10,10)
a6 = Welle_Absatz(Zwischenwelle,378,"Absatz",10,1)
z12 = Welle_Absatz(Zwischenwelle,438,"Pressverbindung",4)

Werte_in_CSV_speichern("Zwischenwelle",a1,a2,z21,a3,a4,a5,a6,z12)