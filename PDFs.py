from rpy2.robjects import r, pandas2ri
import rpy2.robjects.packages as rpackages
import subprocess

pandas2ri.activate()
knitr = rpackages.importr('knitr')

with open("Absaetze.csv","r",encoding="utf8") as datei:
    daten = datei.readlines()

D = []

for line in daten:
    if line[0] != "#":
        D.append([line])

for i in D:
    if i[0] == "Absatz":
        r.assign("name", str(i[0]))
