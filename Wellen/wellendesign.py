from Klassen import *

Festlager = 95
Loslager  = Festlager+215
Fr = -3280
Ft = 6145
Fa = -2237

geometrie = (
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

Antriebswelle = Welle("Antriebswelle",Festlager,Loslager,"42CrMo4","nein")
Antriebswelle.set_geometrie(geometrie)
# Kräfte aus z11
Antriebswelle.set_Kraft(Fr,"r",0,-38.31, 0)
Antriebswelle.set_Kraft(Ft,"t",0,-38.31, 0)
Antriebswelle.set_Kraft(Fa,"a",0,-38.31, 0)
Antriebswelle.lagerkräfte_berechnen()
Antriebswelle.welle_darstellen()