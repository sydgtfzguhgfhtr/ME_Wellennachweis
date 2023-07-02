from klassen import *
import math

visk_10 = [4,76,32,10]
visk_15 = [4,91,54,10]
visk_22 = [4,105,84,10]
visk_32 = [4,115,128,10]
visk_46 = [4,124,260,10]
visk_68 = [5.1,120,300,16]
visk_100 = [6.5,120,300,22]
visk_150 = [9,120,300,29]
visk_220 = [11,120,300,35]
visk_320 = [14,120,300,41]
visk_460 = [18,120,300,47]
visk_680 = [22.5,120,300,55]
visk_1000 = [27.5,120,300,60]
visk_1500 = [35,120,300,66]

di = 40
n = 1500
Fr = math.sqrt(9**2+4**2)
Fa = 2.3
nu = 40
eta_C = 0.6


for i in range(290,302):
    R = Rillenkugellager("A",di,n,Fr,Fa,visk_1000,65,eta_C)
    R.aus_CSV_laden(i)
    print(R.Kurzzeichen)

