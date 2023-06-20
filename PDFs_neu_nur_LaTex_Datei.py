import pandas as pd
from datetime import datetime


aktuelles_datum = datetime.now()


formatiertes_datum = aktuelles_datum.strftime("%d.%m.%Y")

D = pd.read_csv(r"PDFs\Abtriebswelle.csv", delimiter='\t')
print(D)

plot1 = "C:\\Users\\Nadine\\Documents\\Studium\\Studium\\1234567890\\ME_Wellen\\ME_Wellennachweis\\"+D.loc[0,"Welle"]+"WELLE.png"
plot2 = D.loc[0,"Welle"]+"plot.png"

erste_Seite_Welle = f"""
---
title: Wellennachweis - {D.loc[0,"Welle"]}
author: "Quentin Huss, Nadine Schulz"
date: "{formatiertes_datum}"
---

![]({plot1})  

![]({plot2})

# Verformung / Neigung  
  
"""+r"""
\begin{center}
\begin{tabular}{|lll|}
"""+f"""
\\hline
maximale Verformung in x: & {round(D.loc[0,"verfx"],3)} & $\\mu m$ \\\\
maximaler Verformungsgradient in x: & {round(D.loc[0,"verfxPM"],3)} & $mm/m$ \\\\
maximale Verformung in y: & {round(D.loc[0,"verfy"],3)} & $\\mu m$ \\\\
maximaler Verformungsgradient in y: & {round(D.loc[0,"verfyPM"],3)} & $mm/m$ \\\\
maximale Verformung Betrag: & {round(D.loc[0,"verfges"])} & $\\mu m$ \\\\
maximaler Verformungsgradient Betrag: & {round(D.loc[0,"verfgesPM"])} & $mm/m$ \\\\
\\hline
Neigung im Festlager x: & {round(D.loc[0,"Neigung_FLX"],7)} & rad \\\\
Neigung im Festlager y: & {round(D.loc[0,"Neigung_FLY"],7)} & rad \\\\
Neigung im Loslager x: & {round(D.loc[0,"Neigung_LLX"],7)} & rad \\\\
Neigung im Loslager y: & {round(D.loc[0,"Neigung_LLY"],7)} & rad \\\\
\\hline
"""+r"""
\end{tabular}
\end{center}
"""

for i in range(len(D)):
    pass