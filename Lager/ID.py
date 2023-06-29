import pandas as pd
import numpy as np

Daten = pd.read_csv(r"Lager\Einreihige_Zylinderrollenlager.csv")

Nummern = []

for i in range(791,1347):
    Nummern.append(i)

neu = pd.concat([Daten,{"ID":[i for i in range(791,1347)]}],axis=1)

#print(neu)

#Daten.to_csv(r"Lager\Einreihige_Zylinderrollenlager.csv", sep=',')