import pandas as pd
from datetime import datetime

Datum = datetime.now().strftime("%d.%m.%Y")

D = pd.read_csv(r"PDFs\Abtriebswelle.csv", delimiter='\t')
print(D)

plot1 = "C:\\Users\\Nadine\\Documents\\Studium\\Studium\\1234567890\\ME_Wellen\\ME_Wellennachweis\\"+D.loc[0,"Welle"]+"WELLE.png"
plot2 = D.loc[0,"Welle"]+"plot.png"

Pakete = r"""
\documentclass[11pt,a4paper]{report}
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

\begin{figure}[!h]
\centering
\includegraphics[scale=0.5]{"""+f"{D.loc[0,'Welle']+'WELLE.png'}"+r"}"+r"""
\end{figure}


\begin{figure}[!h]
\centering
\includegraphics[scale=0.5]{"""+f"{D.loc[0,'Welle']+'plot.png'}"+r"}"+r"""
\end{figure}

\pagebreak

\end{document}
"""

Arten = []
Geometrien = []
Beanspruchungen = []
Nachweis = []

for i in range(len(D)):
    Art = r"""
    \section{"""+f"{D.loc[i,'Art']}"+"}\n"
    Arten.append()

    Geometrie = r"""
    \subsection{Geometrie}
    """

def string_in_txt(string, dateipfad):
    with open(dateipfad, 'w', encoding='utf-8') as datei:
        datei.write(string)
    print("String erfolgreich in die Datei gespeichert.")


# string_in_txt(Pakete,"Test.tex")