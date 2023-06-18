from Klassen import Welle,Werkstoff,Welle_Absatz,Werte_in_CSV_speichern

import PySimpleGUI as sg

sg.theme("Dark Teal 9")

running = True
wellenname = "Welle 1"
material = ""
oberflächenv = "nein"
festlager_z = 0
loslager_z = 100
Rz = 20
n_punkte = 2 # Standardwert für die Punktzahl
n_kräfte = 1 # Standardwert für die Kräftezahl
lasttab = "Lager"
add_n_p = 1
add_n_k = 1
csvname = "TEST"

hsalogo = "iVBORw0KGgoAAAANSUhEUgAAAUUAAAFFCAIAAAD0FmgKAAAFFGlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS41LjAiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICAgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIgogICAgeG1sbnM6ZXhpZj0iaHR0cDovL25zLmFkb2JlLmNvbS9leGlmLzEuMC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIgogICAgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIKICAgeG1wOkNyZWF0ZURhdGU9IjIwMjItMTEtMjNUMTg6MzE6MTQrMDEwMCIKICAgeG1wOk1vZGlmeURhdGU9IjIwMjItMTEtMjNUMTg6MzI6MjkrMDE6MDAiCiAgIHhtcDpNZXRhZGF0YURhdGU9IjIwMjItMTEtMjNUMTg6MzI6MjkrMDE6MDAiCiAgIHBob3Rvc2hvcDpEYXRlQ3JlYXRlZD0iMjAyMi0xMS0yM1QxODozMToxNCswMTAwIgogICBwaG90b3Nob3A6Q29sb3JNb2RlPSIzIgogICBwaG90b3Nob3A6SUNDUHJvZmlsZT0ic1JHQiBJRUM2MTk2Ni0yLjEiCiAgIGV4aWY6UGl4ZWxYRGltZW5zaW9uPSIzMjUiCiAgIGV4aWY6UGl4ZWxZRGlt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"

welle = None
optionen_oberfl = ("nein","Nitrieren","Einsatzhärten","Karbonierhärten","Festwalzen","Kugelstrahlen","Flammhärten")
FL_Fx,FL_Fy,FL_Fz,LL_Fx,LL_Fy = 0,0,0,0,0 

punkteinput = [] # Beinhaltet die Nutzerdaten für die Punkte
punktreihe_stdwerte = {"NW":False,"Z":0,"R":0,"EXTRA":"","Rz":0,"RUNDUNGSR":0,"KERBGRUNDD":0,"NUTT":0,"NUTR":0,"NUTB":0}
for i in range(n_punkte):
    punkteinput.append(punktreihe_stdwerte)

kräfteinput = [] # Beinhaltet die Nutzerdaten für die Kräfte

def fehler(nachricht:str):
    sg.PopupError(nachricht,title="Fehlermeldung")

def punktreihe(key:str):
    i = int(key)
    key = str(key)
    arten = ["Absatz","umlaufende Rundnut","umlaufende Rechtecknut","eine Passfeder","zwei Passfedern","umlaufende Spitzkerbe","Keilwelle","Kerbzahnwelle","Zahnwelle","Pressverbindung"]
    art_ui = [sg.Text("Rundungsradius =",visible=False,key="RUNDUNGSRTEXT"+key),sg.Input(punkteinput[i]["RUNDUNGSR"],size=(5,None),visible=False,key="RUNDUNGSRIN"+key),sg.Text("Kerbgrunddurchmesser =",visible=False,key="KERBGRUNDDTEXT"+key),sg.Input(punkteinput[i]["KERBGRUNDD"],size=(5,None),visible=False,key="KERBGRUNDDIN"+key),sg.Text("Nuttiefe =",visible=False,key="NUTTTEXT"+key),sg.Input(punkteinput[i]["NUTT"],size=(5,None),visible=False,key="NUTTIN"+key),sg.Text("Nutradius =",visible=False,key="NUTRTEXT"+key),sg.Input(punkteinput[i]["NUTR"],size=(5,None),visible=False,key="NUTRIN"+key),sg.Text("Nutbreite =",visible=False,key="NUTBTEXT"+key),sg.Input(punkteinput[i]["NUTB"],size=(5,None),visible=False,key="NUTBIN"+key)]

    return [sg.Text(key,size=(3,None)),sg.Checkbox("Nachweisen",key="NW"+key,default=punkteinput[i]["NW"]),sg.Text("z [mm]="),sg.Input(punkteinput[i]["Z"],size=(5,None),key="Z"+key),sg.Text("r [mm]="),sg.Input(punkteinput[i]["R"],size=(5,None),key="R"+key),sg.Text("Rz [m^-6]="),sg.Input(punkteinput[i]["Rz"],(5,None),key="RZ"+key),sg.Combo(default_value=punkteinput[i]["EXTRA"],values=arten,key="EXTRA"+key,enable_events=True)]+art_ui

def kraftreihe(key):
    i = int(key)
    key = str(key)
    arten = ("Axial","Radial","Tangential")
    try:
        return [sg.Text(key,size=(3,None)),sg.Text("F [N]="),sg.Input(kräfteinput[i]["F"],key="F"+key,size=(7,None)),sg.Text("N     z [mm]="),sg.Input(kräfteinput[i]["Z"],size=(7,None),key="FZ"+key),sg.Text("r [mm]="),sg.Input(kräfteinput[i]["R"],size=(7,None),key="FR"+key),sg.Text("phi [grad]="),sg.Input(kräfteinput[i]["PHI"],size=(7,None),key="FPHI"+key),sg.Text("Art:"),sg.OptionMenu(arten,key="FART"+key,default_value=kräfteinput[i]["ART"])]
    except IndexError:
        return [sg.Text(key,size=(3,None)),sg.Text("F [N]="),sg.Input(key="F"+key,size=(7,None)),sg.Text("N     z [mm]="),sg.Input("",size=(7,None),key="FZ"+key),sg.Text("r [mm]="),sg.Input("",size=(7,None),key="FR"+key),sg.Text("phi [grad]="),sg.Input("",size=(7,None),key="FPHI"+key),sg.Text("Art:"),sg.OptionMenu(arten,key="FART"+key)]

def new_window():
    return sg.Window("Wellenachweis",layout=layout,finalize=True)

def read_point_vals():
    global punkteinput
    punkteinput = []
    for i in range(n_punkte):
        key = str(i)
        punkteinput.append({"NW":values["NW"+key],"Z":values["Z"+key],"R":values["R"+key],"EXTRA":values["EXTRA"+key],"Rz":values["RZ"+key],"RUNDUNGSR":values["RUNDUNGSRIN"+key],"KERBGRUNDD":values["KERBGRUNDDIN"+key],"NUTT":values["NUTTIN"+key],"NUTR":values["NUTRIN"+key],"NUTB":values["NUTBIN"+key]})

def read_force_vals():
    global kräfteinput
    kräfteinput = []
    for i in range(n_kräfte):
        key = str(i)
        kräfteinput.append({"F":values["F"+key],"Z":values["FZ"+key],"R":values["FR"+key],"PHI":values["FPHI"+key],"ART":values["FART"+key]})

def read_misc_vals():
    global wellenname,material,festlager_z,loslager_z,oberflächenv
    wellenname = values["-NAME-"]
    material = values["-WERKSTOFF-"]
    festlager_z = float(values["-FLZ-"])
    loslager_z = float(values["-LLZ-"])
    oberflächenv = values["-OBERFV-"]

def save_all():
    read_point_vals()
    read_force_vals()
    read_misc_vals()

def update_artparameter():
    global values
    for i in range(n_punkte):
        art = values["EXTRA"+str(i)]
        if art == "Absatz":
            # RUNDUNGSRADIUS
            window["RUNDUNGSRTEXT"+str(i)].update(visible=True)
            window["RUNDUNGSRIN"+str(i)].update(visible=True)
            # KERBGRUNDDURCHMESSER
            window["KERBGRUNDDTEXT"+str(i)].update(visible=False)
            window["KERBGRUNDDIN"+str(i)].update(visible=False)
            # NUTTIEFE
            window["NUTTTEXT"+str(i)].update(visible=False)
            window["NUTTIN"+str(i)].update(visible=False)
            # NUTRADIUS
            window["NUTRTEXT"+str(i)].update(visible=False)
            window["NUTRIN"+str(i)].update(visible=False)
            # NUTBREITE
            window["NUTBTEXT"+str(i)].update(visible=False)
            window["NUTBIN"+str(i)].update(visible=False)
        elif art == "umlaufende Rundnut":
            # RUNDUNGSRADIUS
            window["RUNDUNGSRTEXT"+str(i)].update(visible=False)
            window["RUNDUNGSRIN"+str(i)].update(visible=False)
            # KERBGRUNDDURCHMESSER
            window["KERBGRUNDDTEXT"+str(i)].update(visible=True)
            window["KERBGRUNDDIN"+str(i)].update(visible=True)
            # NUTTIEFE
            window["NUTTTEXT"+str(i)].update(visible=False)
            window["NUTTIN"+str(i)].update(visible=False)
            # NUTRADIUS
            window["NUTRTEXT"+str(i)].update(visible=True)
            window["NUTRIN"+str(i)].update(visible=True)
            # NUTBREITE
            window["NUTBTEXT"+str(i)].update(visible=True)
            window["NUTBIN"+str(i)].update(visible=True)
        elif art == "umlaufende Rechtecknut":
            # RUNDUNGSRADIUS
            window["RUNDUNGSRTEXT"+str(i)].update(visible=False)
            window["RUNDUNGSRIN"+str(i)].update(visible=False)
            # KERBGRUNDDURCHMESSER
            window["KERBGRUNDDTEXT"+str(i)].update(visible=False)
            window["KERBGRUNDDIN"+str(i)].update(visible=False)
            # NUTTIEFE
            window["NUTTTEXT"+str(i)].update(visible=True)
            window["NUTTIN"+str(i)].update(visible=True)
            # NUTRADIUS
            window["NUTRTEXT"+str(i)].update(visible=True)
            window["NUTRIN"+str(i)].update(visible=True)
            # NUTBREITE
            window["NUTBTEXT"+str(i)].update(visible=True)
            window["NUTBIN"+str(i)].update(visible=True)
        else:
            # RUNDUNGSRADIUS
            window["RUNDUNGSRTEXT"+str(i)].update(visible=False)
            window["RUNDUNGSRIN"+str(i)].update(visible=False)
            # KERBGRUNDDURCHMESSER
            window["KERBGRUNDDTEXT"+str(i)].update(visible=False)
            window["KERBGRUNDDIN"+str(i)].update(visible=False)
            # NUTTIEFE
            window["NUTTTEXT"+str(i)].update(visible=False)
            window["NUTTIN"+str(i)].update(visible=False)
            # NUTRADIUS
            window["NUTRTEXT"+str(i)].update(visible=False)
            window["NUTRIN"+str(i)].update(visible=False)
            # NUTBREITE
            window["NUTBTEXT"+str(i)].update(visible=False)
            window["NUTBIN"+str(i)].update(visible=False)

Werkstoff.aus_csv_laden()

while running:
    instance = True
    for i in range(add_n_p):
        punkteinput.append(punktreihe_stdwerte)

    punkte_reihe = []
    for i in range(n_punkte):
        punkte_reihe.append(punktreihe(i))

    geometrie_layout = [
    [sg.Text("Geometrie definieren",font=(any,20))],
    [sg.Input(1,(5,None),key="ADD_N_P"),sg.Button("hinzufügen",key="-ADD_PUNKT-"),sg.Button("entfernen",key="-REM_PUNKT-")],
    [sg.Text("Punkte",font=(any,15))],
    [sg.Column(punkte_reihe,scrollable=True,vertical_scroll_only=True,expand_x=True,expand_y=5)],
    ]

    kräfte_reihe = []
    for i in range(n_kräfte):
        kräfte_reihe.append(kraftreihe(i))
    kräfte_layout = [
        [sg.Text("Belastung definieren",font=(any,20))],
        [sg.Input(1,(5,None),key="ADD_N_K"),sg.Button("hinzufügen",key="-ADD_KRAFT-"),sg.Button("entfernen",key="-REM_KRAFT-")],
        [sg.Text("Kräfte",font=(any,15))],
        [sg.Column(kräfte_reihe,scrollable=True,vertical_scroll_only=True,expand_x=True,expand_y=True)],
    ]

    tab_werkstoff = sg.Tab("Werkstoff",[
        [sg.Text("Werkstoff",font=(any,20))],
        [sg.Text('aus Datei "Werkstoffdaten.csv"'),sg.Combo(list(Werkstoff.Werkstoffe.keys()),material,key="-WERKSTOFF-")],
        [sg.Text("Oberfläche verfestigt?"),sg.OptionMenu(optionen_oberfl,oberflächenv,key="-OBERFV-")],
        ])
    tab_Lagerpositionen = sg.Tab("Lager",[
        [sg.Text("Lagerpositionen",font=(any,20))],
        [sg.Text("Festlager:"),sg.Input(festlager_z,size=(7,None),key="-FLZ-"),sg.Text("mm")],
        [sg.Text("Loslager: "),sg.Input(loslager_z,size=(7,None),key="-LLZ-"),sg.Text("mm")],
        [sg.Text("Hinweis: Zur Berechnung der Verformung müssen sich die Lager innerhalb der Wellengeometrie befinden.")]
        ])
    tab_geometrie = sg.Tab("Geometrie",geometrie_layout)
    tab_kräfte = sg.Tab("Belastungen",kräfte_layout)

    # Auswertetabs
    tab_plots = sg.Tab("Plots",[
        [sg.Text("Plots",font=(any,17))],
        [sg.Button("Plot Kräfte/Biegung",key="-PLOT KRÄFTE BIEGUNG-",size=(30,None))],
        [sg.Button("Plot Torsion",key="-PLOT TORSION-",size=(30,None))],
        [sg.Button("Plot Spannungen",key="-PLOT SPANNUNG-",size=(30,None))],
        [sg.Button("Plot Verformung",key="-PLOT VERFORMUNG-",size=(30,None))],
        [sg.Button("Plot Neigung",key="-PLOT NEIGUNG-",size=(30,None))],
        ])
    tab_lagerkräfte = sg.Tab("Lagerkräfte",[
        [sg.Text("Lagerkräfte",font=(any,17))],
        [sg.Table((("Festlager",1e10,1e10,1e10),("Loslager",1e10,1e10,1e10)),("","Fx [N]","Fy [N]","Fz [N]"),key="LAGERKRÄFTE TABLE")],
    ])
    tab_verformung = sg.Tab("Verformung",[
        [sg.Text("Lagerkräfte",font=(any,17))],
        [sg.Text("Maximale Verformung in X: ",size=(30,None)),sg.Text("",key="MAXVERFX",size=(7,None)),sg.Text("[m^-6]")],
        [sg.Text("Maximaler Verformungsgradient in X: ",size=(30,None)),sg.Text("",key="MAXVERFXGRAD",size=(7,None)),sg.Text("[mm/m]")],
        [sg.Text("Maximale Verformung in Y: ",size=(30,None)),sg.Text("",key="MAXVERFY",size=(7,None)),sg.Text("[m^-6]")],
        [sg.Text("Maximaler Verformungsgradient in Y: ",size=(30,None)),sg.Text("",key="MAXVERFYGRAD",size=(7,None)),sg.Text("[mm/m]")],
        [sg.HorizontalSeparator()],
        [sg.Text("Neigung im Festlager in X:",size=(30,None)),sg.Text("",key="NEIGUNGFLX",size=(7,None)),sg.Text("[rad]")],
        [sg.Text("Neigung im Festlager in Y:",size=(30,None)),sg.Text("",key="NEIGUNGFLY",size=(7,None)),sg.Text("[rad]")],
        [sg.Text("Neigung im Loslager in X:",size=(30,None)),sg.Text("",key="NEIGUNGLLX",size=(7,None)),sg.Text("[rad]")],
        [sg.Text("Neigung im Loslager in Y:",size=(30,None)),sg.Text("",key="NEIGUNGLLY",size=(7,None)),sg.Text("[rad]")],
    ])
    tab_absätze = sg.Tab("Absätze",[
        [sg.Text("Absätze",font=(any,17))],
        [sg.Table([],("Name der Welle","Werkstoff","z_Wert","Welle","beta_sigma","beta_tau","K_ges_sigma","K_ges_tau","sigma_bWK","tau_bWK","sigma_bFK","tau_tFK","sigma_bADK","tau_tADK","S_F","S_D","Biegespannung","Torsionsspannung"),key="ABSATZTABLE",def_col_width=5)],
        [sg.Button("als CSV speichern",key="SAVETOCSV"),sg.Text(csvname,visible=False,key="SAVED")],
    ])
    tab_auswertung = sg.Tab("Auswertung",layout=[
        [sg.Text("Auswertung",font=(any,20))],
        [sg.TabGroup([[tab_lagerkräfte,tab_verformung,tab_plots,tab_absätze]])]
    ],visible=False,key="TAB AUSWERTUNG")

    layout = [
    [sg.Titlebar("Wellennachweis")],
    [sg.Text("Wellennachweis nach DIN 743",font=(any,30))],
    [sg.Text("Nadine Schulz und Quentin Huss"),sg.Push(),sg.Text("Angaben ohne Gewähr!")],
    [sg.HorizontalSeparator()],

    [sg.Text("Name der Welle",font=(any,20))],
    [sg.Input(wellenname,key="-NAME-")],

    [sg.TabGroup([[tab_werkstoff,tab_Lagerpositionen,tab_geometrie,tab_kräfte,tab_auswertung]])],
    [sg.Button("Welle darstellen",key="-DRAW WELLE-"),sg.Button("vollständige Auswertung",key="-CALC ALL-"),sg.Text("RECHNE...",visible=False,key="-RECHNE-")],
    ]

    window = new_window()
    window.maximize()

    while True:
        event,values = window.read()
        try:
            add_n_k = abs(int(values["ADD_N_K"]))
            add_n_p = abs(int(values["ADD_N_P"]))
            update_artparameter()
        except TypeError:
            pass
        if event == sg.WIN_CLOSED or event == 'Cancel':
            running = False
            window.close()
            #print("FENSTER GESCHLOSSEN")
            break
        # Was passiert wenn die Absatzart geändert wurde?
        if event == "-DRAW WELLE-":
            save_all()
            try:
                welle = Welle(name=wellenname,festlager_z=festlager_z,loslager_z=loslager_z,werkstoff=material,Oberflächenverfestigung=oberflächenv)
                geometrie = [(float(punkt["Z"]),float(punkt["R"])) for punkt in punkteinput]
                welle.set_geometrie(geometrie)
                welle.welle_darstellen()
            except:
                sg.PopupError("Es ist ein Fehler aufgetreten.\nBitte die Eingaben auf Vollständigkeit überprüfen!",title="Fehlermeldung")

        if event=="-CALC ALL-":
            save_all()
            if material=="":
                fehler("Es wurde kein Werkstoff festgelegt.")
            else:
                window["-RECHNE-"].update(visible=True)
                window.refresh()

                try:
                    welle = Welle(name=wellenname,festlager_z=festlager_z,loslager_z=loslager_z,werkstoff=material,Oberflächenverfestigung=oberflächenv)
                    geometrie = [(float(punkt["Z"]),float(punkt["R"])) for punkt in punkteinput]
                    welle.set_geometrie(geometrie)
                    for kraft in kräfteinput:
                        welle.set_Kraft(float(kraft["F"]),kraft["ART"],float(kraft["Z"]),float(kraft["R"]),float(kraft["PHI"]))
                    welle.lagerkräfte_berechnen()
                    welle.verformung_berechnen()
                    FL_Fx,FL_Fy,FL_Fz,LL_Fx,LL_Fy = welle.FL_Fx,welle.FL_Fy,welle.FL_Fz,welle.LL_Fx,welle.LL_Fy
                    window["LAGERKRÄFTE TABLE"].update(values=(("Festlager",round(FL_Fx,3),round(FL_Fy,3),round(FL_Fz,3)),("Loslager",round(LL_Fx,3),round(LL_Fy,3),0)))
                    window["TAB AUSWERTUNG"].update(visible=True)

                    absätze = []
                    for punkt in punkteinput:
                        nw = punkt["NW"]
                        if nw:
                            z = float(punkt["Z"])
                            rz = float(punkt["Rz"])
                            art = punkt["EXTRA"]
                            if art=="Absatz":
                                args = [float(punkt["RUNDUNGSR"])]
                                print("Absatz",args)
                            elif art=="umlaufende Rundnut":
                                args = [float(punkt["KERBGRUNDD"]),float(punkt["NUTR"]),float(punkt["NUTB"])]
                                print("uml. Rundnut",args)
                            elif art=="umlaufende Rechtecknut":
                                args = [float(punkt["NUTT"]),float(punkt["NUTR"]),float(punkt["NUTB"])]
                                print("uml. Rechtecknut",args)
                            else:
                                args = []
                            absätze.append(Welle_Absatz(welle,z,art,rz,*args))
                    
                    absatzerg = []
                    for absatz in absätze:
                        infos = []
                        for wert in absatz.Sicherheiten()[2][:-1]:
                            try:
                                infos.append(round(float(wert),3))
                            except:
                                infos.append(wert)
                        absatzerg.append(infos)
                    window["ABSATZTABLE"].update(values=absatzerg)

                    window["MAXVERFX"].update(str(round(welle.maxVerf_x*1000,5)))
                    window["MAXVERFXGRAD"].update(str(round(welle.maxVerf_x_PM,5)))
                    window["MAXVERFY"].update(str(round(welle.maxVerf_y*1000,5)))
                    window["MAXVERFYGRAD"].update(str(round(welle.maxVerf_y_PM,5)))
                    window["NEIGUNGFLX"].update(str(round(welle.NeigungFLx,5)))
                    window["NEIGUNGFLY"].update(str(round(welle.NeigungFLy,5)))
                    window["NEIGUNGLLX"].update(str(round(welle.NeigungLLx,5)))
                    window["NEIGUNGLLY"].update(str(round(welle.NeigungLLy,5)))

                except ValueError:
                    fehler("Unvollständige Eingaben. (ValueError)")
                except ZeroDivisionError:
                    fehler("Fehler bei der Berechnung. Eingaben überprüfen. (ZeroDivisionError)")
                window["-RECHNE-"].update(visible=False)
                window["SAVED"].update(visible=False)
        
        if event=="SAVETOCSV":
            csvname = "PDFs\\"+wellenname+".csv"
            window["SAVED"].update(f"unter '{csvname}' gespeichert...",visible=True)
            Werte_in_CSV_speichern(wellenname,*absätze)

        if event=="-PLOT SPANNUNG-":
            welle.plot_spannungen()
        if event=="-PLOT VERFORMUNG-":
            welle.plot_biegung()
        if event=="-PLOT NEIGUNG-":
            welle.plot_neigung()
        if event=="-PLOT KRÄFTE BIEGUNG-":
            welle.plot()
        if event=="-PLOT TORSION-":
            welle.plot_torsion()
        if event=="-ADD_PUNKT-":
            save_all()
            n_punkte += add_n_p
            window.close()
            break
        if event=="-REM_PUNKT-":
            save_all()
            if n_punkte<2+add_n_p:
                n_punkte = 2
            else:
                n_punkte -= add_n_p
            window.close()
            break
        if event=="-ADD_KRAFT-":
            save_all()
            n_kräfte += add_n_k
            window.close()
            break
        if event=="-REM_KRAFT-":
            save_all()
            if n_kräfte<1+add_n_k:
                n_kräfte = 1
            else:
                n_kräfte -= add_n_k
            window.close()
            break