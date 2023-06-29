import pandas as pd

Daten = pd.read_csv(r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\Lager\einreihige_Rillenkugellager.csv")

Daten.to_csv(r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\Lager\einreihige_Rillenkugellager.csv", sep=',')