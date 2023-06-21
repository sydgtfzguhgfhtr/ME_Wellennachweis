import pandas as pd
from datetime import datetime

Datum = datetime.now().strftime("%d.%m.%Y")

D = pd.read_csv(r"PDFs\Abtriebswelle.csv", delimiter='\t')
print(D)

plot1 = D.loc[0,"Welle"]+"WELLE.png"
plot2 = D.loc[0,"Welle"]+"plot.png"

Ausgabe = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[german]{babel}
\usepackage[T1]{fontenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{pstricks}
\usepackage{float}
\usepackage{tikz}
\usepackage{pgfplots}
\usepackage{asymptote}
\usepackage{mathptmx}
\usepackage{caption}
\usepackage[left=2cm, right=2cm, top=2cm,bottom=2cm]{geometry}
\usepackage[colorlinks=true, urlcolor=blue, linkcolor=blue]{hyperref}
"""+r"\title{Wellennachweis - "+f"{D.loc[0,'Welle']}"+r"}"+r"""
\author{Quentin Huss, Nadine Schulz}
"""+r"\date{"+f"{Datum}"+r"}"+r"""
\begin{document}
\maketitle

\section{Darstellung der Welle}
\begin{figure}[!h]
\centering
\includegraphics[scale=0.5]{"""+f"{D.loc[0,'Welle']+'WELLE.png'}"+r"}"+r"""
\end{figure}

\pagebreak

\begin{figure}[!ht]
\section{Plots}
\centering
\includegraphics[scale=0.5]{"""+f"{D.loc[0,'Welle']+'plot.png'}"+r"}"+r"""
\end{figure}



\section{Verformung und Neigung}

\begin{center}
\begin{tabular}{|lll|}
maximale Verformung in x: & """+f"{D.loc[0,'verfx']}" + r"""& $\mu m$ \\
Verformungsgradient in x: & """ + f"{D.loc[0,'verfxPM']}" + r"""& $\dfrac{mm}{m}$ \\
maximale Verformung in y: & """ + f"{D.loc[0,'verfy']}" + r"""& $\mu m$ \\
Verformungsgradient in y: &""" + f"{D.loc[0,'verfyPM']}" + r"""& $\dfrac{mm}{m}$ \\
maximale Verformung addiert: & """+ f"{D.loc[0,'verfges']}" + r"""& $\mu m$ \\
Verformungsgradient addiert: &""" + f"{D.loc[0,'verfgesPM']}" + r"""& $\dfrac{mm}{m}$ \\
\hline 
Neigung im Festlager x: &""" + f"{D.loc[0,'Neigung_FLX']}" + r"""& rad \\
Neigung im Festlager y: &""" + f"{D.loc[0,'Neigung_FLY']}" + r"""& rad \\
Neigung im Loslager x: &""" + f"{D.loc[0,'Neigung_LLX']}" + r"""& rad \\
Neigung im Loslager y: &""" + f"{D.loc[0,'Neigung_LLY']}" + r"""& rad \\
\end{tabular}
\end{center}

"""

Arten = []
Geometrien = []
Beanspruchungen = []
Nachweis = []

for i in range(len(D)):
    Art = r"""
\section*{"""+f"{D.loc[i,'Name']} an Stelle {D.loc[i,'z_Wert']} mm"+"}\n"
    Arten.append(Art)

    Geometrie = r"""
\subsection*{Geometrie}
"""
    if D.loc[i,"Name"] == "Absatz":
        Geometrie_Angaben = r"""
\begin{center}
\begin{tabular}{|ll|}
großer Durchmesser & $D ="""+f"{D.loc[i,'anderes'].split(';')[0]}"+r"""\ mm$ \\
kleiner Durchmesser & $d ="""+f"{D.loc[i,'anderes'].split(';')[1]}"+r"""\ mm$ \\
Radius & $r ="""+f"{D.loc[i,'anderes'].split(';')[2]}"+r"""\ mm$ \\
Absatzsprung & $t ="""+f"{D.loc[i,'anderes'].split(';')[3]}"+r"""\ mm$
\end{tabular}
\end{center}
"""
    Geometrien.append(Geometrie+Geometrie_Angaben)


for i in range(len(D)):
    print("APPEND")
    Ausgabe += Arten[i]
    Ausgabe += Geometrien[i]
    Ausgabe += Beanspruchungen[i]
    Ausgabe += Nachweis[i]
    Ausgabe += "\pagebreak"

Ausgabe += r"\end{document}"

def string_in_txt(string, dateipfad):
    with open(dateipfad, 'w', encoding='utf-8') as datei:
        datei.write(string)
    print("String erfolgreich in die Datei gespeichert.")


string_in_txt(Ausgabe,r"Test Ergebnisse als LaTex Datei ausgeben\Test.tex")