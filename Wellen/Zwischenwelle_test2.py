#%%
from Klassen import *

Festlager = 95
Loslager  = 310
B_fl = 21
B_ll = 20
Fr = -3280
Ft = 6145
Fa = -2237

geometrie = (
    (-30, 22),
     (30, 22),
     (60, 35),
     #Festlager
     (Festlager+B_fl/2,35),
     (Festlager+B_fl/2,36),
     (Festlager+B_fl/2+3, 36),
     (Loslager-B_ll/2,25),
     (Loslager-B_ll/2, 24),
     #Loslager
     (367, 24),
     (387, 16),
     (387, 15),
     (463, 15)
)

Antriebswelle = Welle("Antriebswelle",Festlager,Loslager,"42CrMo4","nein")
Antriebswelle.set_geometrie(geometrie)
# Kräfte aus z11
Antriebswelle.set_Kraft(Fr,"r",0,-38.31, 0)
Antriebswelle.set_Kraft(Ft,"t",0,-38.31, 0)
Antriebswelle.set_Kraft(Fa,"a",0,-38.31, 0)
Antriebswelle.lagerkräfte_berechnen()
#%%
Antriebswelle.plot()
Antriebswelle.plot_spannungen()
#Antriebswelle.welle_darstellen()

#%%
Antriebswelle.verformung_berechnen()
#%%
Antriebswelle.plot_biegung()
Antriebswelle.plot_neigung()
#%%
print("maxVerf_ges = ",Antriebswelle.maxVerfPM_ges)