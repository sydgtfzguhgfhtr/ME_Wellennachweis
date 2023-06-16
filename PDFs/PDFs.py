import subprocess
import os
import shutil
from rpy2.robjects import r 
from rpy2.robjects import pandas2ri, packages
import rpy2.robjects.packages as rpackages
import numpy as np
import pandas as pd

pandas2ri.activate()
knitr = rpackages.importr('knitr')

D = pd.read_csv(r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\PDFs\Absaetze.csv")
files = []
name_values = D["Name"].tolist()

for i in range(len(D)):
    filename = str(D.loc[i,"Welle"])+"_"+str(D.loc[i,"Name"])+"_"+str(i)+".pdf"
    files.append(filename)
    r.assign("z_Koordinate",D.loc[i,"z_Wert"])
    r.assign("sigma_max",D.loc[i,"Biegespannung"])
    r.assign("tau_max",D.loc[i,"Torsionsspannung"])
    r.assign("Name",str(D.loc[i,"Name"]))
    r.assign("werkstoff",str(D.loc[i,"Werkstoff"]))
    r.assign("z_Wert",float(D.loc[i,"z_Wert"]))
    r.assign("Welle",str(D.loc[i,"Welle"]))
    r.assign("beta_sigma",D.loc[i,"beta_sigma"])
    r.assign("beta_tau",D.loc[i,"beta_tau"])
    r.assign("K_ges_sigma",D.loc[i,"K_ges_sigma"])
    r.assign("K_ges_tau",D.loc[i,"K_ges_tau"])
    r.assign("sigma_bWK",D.loc[i,"sigma_bWK"])
    r.assign("tau_bWK",D.loc[i,"tau_bWK"])
    r.assign("sigma_bFK",D.loc[i,"sigma_bFK"])
    r.assign("tau_tFK",D.loc[i,"tau_tFK"])
    r.assign("sigma_bADK",D.loc[i,"sigma_bADK"])
    r.assign("tau_tADK",D.loc[i,"tau_tADK"])
    r.assign("S_F",D.loc[i,"S_F"])
    r.assign("S_D",D.loc[i,"S_D"])
    anderes = D.loc[i,"anderes"]
    if D.loc[i,"Name"] == "Absatz":
        l = anderes.split(";")
        Durch = l[0]
        print(D)
        d = l[1]
        R = l[2]
        b = l[3]
        r.assign("D",Durch)
        r.assign("d",d)
        r.assign("r",R)
        r.assign("t",b)
        knitr.knit(r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\PDFs\Wellen_Absaetze_Absatz.Rmd")
        subprocess.run(["pandoc","-s","Wellen_Absaetze_Absatz.md","-o",filename])
    if D.loc[i,"Name"] == "umlaufende Rundnut":
        l = anderes.split(";")
        d = l[0]
        R = l[1]
        b = l[2]
        r.assign("d",d)
        r.assign("r",R)
        r.assign("b",b)
        knitr.knit(r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\PDFs\Wellen_Absaetze_Rundnut.Rmd")
        subprocess.run(["pandoc","-s","Wellen_Absaetze_Rundnut.md","-o",filename])
    if D.loc[i,"Name"] == "umlaufende Rechtecknut":
        l = anderes.split(";")
        t = l[0]
        R = l[1]
        b = l[2]
        r.assign("t",t)
        r.assign("r",R)
        r.assign("b",b)
        knitr.knit(r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\PDFs\Wellen_Absaetze_Rechtecknut.Rmd")
        subprocess.run(["pandoc","-s","Wellen_Absaetze_Rechtecknut.md","-o",filename])
    if D.loc[i,"Name"] == "eine Passfeder" or D.loc[i,"Name"] == "zwei Passfedern":
        dw = anderes
        r.assign("dw",dw)
        knitr.knit(r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\PDFs\Wellen_Absaetze_Passfeder.Rmd")
        subprocess.run(["pandoc","-s","Wellen_Absaetze_Passfeder.md","-o",filename])
    if D.loc[i,"Name"] == "umlaufende Spitzkerbe":
        dw = anderes
        r.assign("dw",dw)
        knitr.knit(r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\PDFs\Wellen_Absaetze_Spitzkerbe.Rmd")
        subprocess.run(["pandoc","-s","Wellen_Absaetze_Spitzkerbe.md","-o",filename])
    if D.loc[i,"Name"] == "Keilwelle":
        dw = anderes
        r.assign("dw",dw)
        knitr.knit(r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\PDFs\Wellen_Absaetze_Keilwelle.Rmd")
        subprocess.run(["pandoc","-s","Wellen_Absaetze_Keilwelle.md","-o",filename])
    if D.loc[i,"Name"] == "Kerbzahnwelle":
        dw = anderes
        r.assign("dw",dw)
        knitr.knit(r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\PDFs\Wellen_Absaetze_Kerbzahnwelle.Rmd")
        subprocess.run(["pandoc","-s","Wellen_Absaetze_Kerbzahnwelle.md","-o",filename])
    if D.loc[i,"Name"] == "Zahnwelle":
        dw = anderes
        r.assign("dw",dw)
        knitr.knit(r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\PDFs\Wellen_Absaetze_Zahnwelle.Rmd")
        subprocess.run(["pandoc","-s","Wellen_Absaetze_Zahnwelle.md","-o",filename])
    if D.loc[i,"Name"] == "Pressverbindung":
        dw = anderes
        r.assign("dw",dw)
        knitr.knit(r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\PDFs\Wellen_Absaetze_Pressverbindung.Rmd")
        subprocess.run(["pandoc","-s","Wellen_Absaetze_Pressverbindung.md","-o",filename])

Dateien_md = [
    r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\Wellen_Absaetze_Absatz.md",
    r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\Wellen_Absaetze_Keilwelle.md",
    r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\Wellen_Absaetze_Kerbzahnwelle.md",
    r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\Wellen_Absaetze_Passfeder.md",
    r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\Wellen_Absaetze_Pressverbindung.md",
    r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\Wellen_Absaetze_Rechtecknut.md",
    r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\Wellen_Absaetze_Rundnut.md",
    r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\Wellen_Absaetze_Spitzkerbe.md",
    r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\Wellen_Absaetze_Zahnwelle.md"
    ]


for line in Dateien_md:
    if os.path.exists(line):
        os.remove(line)

for file in files:
    shutil.move(file, r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\PDFs\Ergebnisse")