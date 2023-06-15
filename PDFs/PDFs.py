import subprocess
from rpy2.robjects import r 
from rpy2.robjects import pandas2ri, packages
import rpy2.robjects.packages as rpackages
import numpy as np
import pandas as pd

pandas2ri.activate()
knitr = rpackages.importr('knitr')

D = pd.read_csv(r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\Absaetze.csv")

name_values = D["Name"].tolist()

for i in range(len(D)):
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
        D = l[0]
        print(D)
        d = l[1]
        R = l[2]
        b = l[3]
        r.assign("D",D)
        r.assign("d",d)
        r.assign("r",R)
        r.assign("t",b)
        knitr.knit(r"C:\Users\Nadine\Documents\Studium\Studium\1234567890\ME_Wellen\ME_Wellennachweis\PDFs\Wellen_Absaetze_Absatz.Rmd")
        subprocess.run(["pandoc","-s","Wellen_Absaetze_Absatz.md","-o","AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.pdf"])


# r.assign("dw",float(dw_eingabe.text()))
# r.assign("MT",float(mt_eingabe.text()))
# r.assign("w_welle",w_welle.curentText())
# r.assign("w_nabe",w_nabe.curentText())
# r.assign("w_passfeder",w_passfeder.curentText())
# r.assign("s_f",float(sf_eingabe.text()))
# r.assign("anzahl_passfeder",2)
# knitr.knit("Passfeder.rmd")
# subprocess.run(["pandoc","-s","Passfeder.md","-o","Passfeder_2.pdf"])