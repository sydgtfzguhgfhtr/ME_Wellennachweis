from Klassen import Welle,Werkstoff,Welle_Absatz

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
    global wellenname,material,festlager_z,loslager_z,Rz,oberflächenv
    wellenname = values["-NAME-"]
    material = values["-WERKSTOFF-"]
    festlager_z = float(values["-FLZ-"])
    loslager_z = float(values["-LLZ-"])
    Rz = float(values["-RZ-"])
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
    [sg.Column(punkte_reihe,scrollable=True,vertical_scroll_only=True,expand_y=5)],
    ]

    kräfte_reihe = []
    for i in range(n_kräfte):
        kräfte_reihe.append(kraftreihe(i))
    kräfte_layout = [
        [sg.Text("Belastung definieren",font=(any,20))],
        [sg.Input(1,(5,None),key="ADD_N_K"),sg.Button("hinzufügen",key="-ADD_KRAFT-"),sg.Button("entfernen",key="-REM_KRAFT-")],
        [sg.Text("Kräfte",font=(any,15))],
        [sg.Column(kräfte_reihe,scrollable=True,vertical_scroll_only=True,expand_y=5)],
    ]

    tab_werkstoff = sg.Tab("Werkstoff",[
        [sg.Text("Werkstoff",font=(any,20))],
        [sg.Text('aus Datei "Werkstoffdaten.csv"'),sg.Combo(list(Werkstoff.Werkstoffe.keys()),material,key="-WERKSTOFF-")],
        [sg.Text("Oberflächenrauheit Rz ="),sg.Input(Rz,(7,any),key="-RZ-")],
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
        [sg.Button("Plot Verformung",key="-PLOT VERFORMUNG-",size=(30,None))],
        [sg.Button("Plot Neigung",key="-PLOT NEIGUNG-",size=(30,None))],
        [sg.Button("Plot Kräfte/Biegung",key="-PLOT KRÄFTE BIEGUNG-",size=(30,None))],
        [sg.Button("Plot Torsion",key="-PLOT TORSION-",size=(30,None))],
        ])
    tab_lagerkräfte = sg.Tab("Lagerkräfte",[
        [sg.Text("Lagerkräfte",font=(any,17))],
        [sg.Table((("Festlager",1e10,1e10,1e10),("Loslager",1e10,1e10,1e10)),("","Fx [N]","Fy [N]","Fz [N]"),key="LAGERKRÄFTE TABLE")],
    ])
    tab_verformung = sg.Tab("Verformung",[
        [sg.Text("Lagerkräfte",font=(any,17))],
        [sg.Text("Maximale Verformung in X: ",size=(30,None)),sg.Text("",key="MAXVERFX"),sg.Text("[m^-6]")],
        [sg.Text("Maximaler Verformungsgradient in X: ",size=(30,None)),sg.Text("",key="MAXVERFXGRAD"),sg.Text("[mm/m]")],
        [sg.Text("Maximale Verformung in Y: ",size=(30,None)),sg.Text("",key="MAXVERFY"),sg.Text("[m^-6]")],
        [sg.Text("Maximaler Verformungsgradient in Y: ",size=(30,None)),sg.Text("",key="MAXVERFYGRAD"),sg.Text("[mm/m]")],
    ])
    tab_absätze = sg.Tab("Absätze",[
        [sg.Text("Absätze",font=(any,17))],
        [sg.Table([],("Name der Welle","Werkstoff","z_Wert","Welle","beta_sigma","beta_tau","K_ges_sigma","K_ges_tau","sigma_bWK","tau_bWK","sigma_bFK","tau_tFK","sigma_bADK","tau_tADK","S_F","S_D","Biegespannung","Torsionsspannung"),key="ABSATZTABLE",def_col_width=5)],
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
    [sg.Button("Welle darstellen",key="-DRAW WELLE-"),sg.Button("vollständige Auswertung",key="-CALC ALL-"),sg.Text("RECHNE...",key="-RECHNE-",visible=False)],
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

                    window["MAXVERFX"].update(str(round(welle.maxVerf_x*1000,3)))
                    window["MAXVERFXGRAD"].update(str(round(welle.maxVerf_x_PM,3)))
                    window["MAXVERFY"].update(str(round(welle.maxVerf_y*1000,3)))
                    window["MAXVERFYGRAD"].update(str(round(welle.maxVerf_y_PM,3)))

                except ValueError:
                    fehler("Unvollständige Eingaben. (ValueError)")
                except ZeroDivisionError:
                    fehler("Fehler bei der Berechnung. Eingaben überprüfen. (ZeroDivisionError)")
                window["-RECHNE-"].update(visible=False)
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