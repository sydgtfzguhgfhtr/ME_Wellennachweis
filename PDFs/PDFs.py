import subprocess
import os
from rpy2.robjects import r 
from rpy2.robjects import pandas2ri, packages
import rpy2.robjects.packages as rpackages
import PyPDF4
import numpy as np
import pandas as pd
from datetime import datetime


aktuelles_datum = datetime.now()


formatiertes_datum = aktuelles_datum.strftime("%d.%m.%Y")



pandas2ri.activate()
knitr = rpackages.importr('knitr')



D = pd.read_csv(r"PDFs\Abtriebswelle.csv")


plot1 = "C:\\Users\\Nadine\\Documents\\Studium\\Studium\\1234567890\\ME_Wellen\\ME_Wellennachweis\\"+D.loc[0,"Welle"]+"WELLE.png"
plot2 = D.loc[0,"Welle"]+"plot.png"

erste_Seite_PDF = f"""
---
title: Wellennachweis - {D.loc[0,"Welle"]}
author: "Quentin Huss, Nadine Schulz"
date: "{formatiertes_datum}"
---
\pagebreak
![]({plot1})  

![]({plot2})


"""

with open('erste_Seite.Rmd','w') as file:
    file.write(erste_Seite_PDF)

knitr.knit(r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\erste_Seite.Rmd")
subprocess.run(["pandoc","-s","C:\\Users\\Nadine\\Documents\\Studium\\Studium\\1234567890\\ME_Wellen\\ME_Wellennachweis\\erste_Seite.md","-o","erste_Seite.pdf"])

files = ["erste_Seite.pdf"]
name_values = D["Name"].tolist()

for i in range(len(D)):
    filename ="C:\\Users\\Nadine\\Documents\\Studium\\Studium\\1234567890\\ME_Wellen\\ME_Wellennachweis\\"+ str(D.loc[i,"Welle"])+"_"+str(D.loc[i,"Name"])+"_"+str(i)+".pdf"
    files.append(filename)
    output_file = "Wellennachweis"+str(D.loc[i,"Welle"])+".pdf"
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
    if D.loc[i,"Name"] == "Absatz":             # fertig
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
    if D.loc[i,"Name"] == "umlaufende Rundnut":     # fertig
        l = anderes.split(";")
        d = l[0]
        R = l[1]
        b = l[2]
        dw = l[3]
        r.assign("dw",dw)
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
        dw = l[3]
        r.assign("dw",dw)
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
    r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\Wellen_Absaetze_Zahnwelle.md",
    r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\erste_Seite.md",
    r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\erste_Seite.Rmd"
    ]

def merge_pdfs(input_files, output_file):
    merger = PyPDF4.PdfFileMerger()

    # Füge jede PDF-Datei der Merger-Instanz hinzu
    for file in input_files:
        with open(file, 'rb') as pdf_file:
            merger.append(pdf_file)

    # Speichere die zusammengeführte PDF-Datei
    with open(output_file, 'wb') as output:
        merger.write(output)

    print("Die PDF-Dateien wurden erfolgreich zusammengeführt!")

merge_pdfs(files, output_file)

for line in Dateien_md:
    if os.path.exists(line):
        os.remove(line)

for line in files:
    os.remove(line)

os.remove(plot1)
os.remove(plot2)