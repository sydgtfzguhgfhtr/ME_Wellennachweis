from klassen import *
import math

di = 40
n = 1500
Fr = math.sqrt(9**2+4**2)
Fa = 2.3
nu = 40
eta_C = 0.6


for i in range(290,302):
    R = Rillenkugellager("A",di,n,Fr,Fa,nu,eta_C)
    R.aus_CSV_laden(i)
    print(R.erweiterte_Lebensdauer_in_Stunden())

