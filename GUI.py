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


welle = None
optionen_oberfl = ("nein","Nitrieren","Einsatzhärten","Karbonierhärten","Festwalzen","Kugelstrahlen","Flammhärten")


punkteinput = [] # Beinhaltet die Nutzerdaten für die Punkte
kräfteinput = [] # Beinhaltet die Nutzerdaten für die Kräfte

def punktreihe(key:str):
    arten = ["Absatz","umlaufende Rundnut","eine Passfeder","zwei Passfedern","umlaufende Spitzkerbe","Keilwelle","Kerbzahnwelle","Zahnwelle","Pressverbindung"]
    i = int(key)
    key = str(key)
    try:
        return [sg.Text(key),sg.Checkbox("Nachweisen",key="NW"+key,default=punkteinput[i][0]),sg.Text("z [mm]="),sg.Input(punkteinput[i][1],size=(5,None),key="Z"+key),sg.Text("r [mm]="),sg.Input(punkteinput[i][2],size=(5,None),key="R"+key),sg.OptionMenu(default_value=punkteinput[i][3],values=arten,key="EXTRA"+key),sg.Text("Rz [m^-6]="),sg.Input(punkteinput[i][4],(5,None),key="RZ"+key)]
    except IndexError:
        return [sg.Text(key),sg.Checkbox("Nachweisen",key="NW"+key),sg.Text("z [mm]="),sg.Input(size=(5,None),key="Z"+key),sg.Text("r [mm]="),sg.Input(size=(5,None),key="R"+key),sg.OptionMenu(values=arten,key="EXTRA"+key,default_value="Absatz"),sg.Text("Rz [m^-6]="),sg.Input(Rz,(5,None),key="RZ"+key)]

def kraftreihe(key):
    i = int(key)
    key = str(key)
    arten = ("Axial","Radial","Tangential")
    try:
        return [sg.Text(key),sg.Text("F [N]="),sg.Input(kräfteinput[i][0],key="F"+key,size=(7,None)),sg.Text("N     z [mm]="),sg.Input(kräfteinput[i][1],size=(7,None),key="FZ"+key),sg.Text("r [mm]="),sg.Input(kräfteinput[i][2],size=(7,None),key="FR"+key),sg.Text("phi [grad]="),sg.Input(kräfteinput[i][3],size=(7,None),key="FPHI"+key),sg.Text("Art:"),sg.OptionMenu(arten,key="FART"+key,default_value=kräfteinput[i][4],)]
    except IndexError:
        return [sg.Text(key),sg.Text("F [N]="),sg.Input(key="F"+key,size=(7,None)),sg.Text("N     z [mm]="),sg.Input("",size=(7,None),key="FZ"+key),sg.Text("r [mm]="),sg.Input("",size=(7,None),key="FR"+key),sg.Text("phi [grad]="),sg.Input("",size=(7,None),key="FPHI"+key),sg.Text("Art:"),sg.OptionMenu(arten,key="FART"+key)]

def new_window():
    return sg.Window("Wellenachweis",layout=layout)

def read_point_vals():
    global punkteinput
    punkteinput = []
    for i in range(n_punkte):
        key = str(i)
        punkteinput.append((values["NW"+key],values["Z"+key],values["R"+key],values["EXTRA"+key],values["RZ"+key]))

def read_force_vals():
    global kräfteinput
    kräfteinput = []
    for i in range(n_kräfte):
        key = str(i)
        kräfteinput.append((values["F"+key],values["FZ"+key],values["FR"+key],values["FPHI"+key],values["FART"+key]))

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

Werkstoff.aus_csv_laden()

while running:
    instance = True

    geometrie_layout = [
    [sg.Text("Geometrie definieren",font=(any,20))],
    [sg.Button("Punkt hinzufügen",key="-ADD_PUNKT-"),sg.Button("Punkt entfernen",key="-REM_PUNKT-")],
    [sg.Text("Punkte",font=(any,15))],
    ]
    for i in range(n_punkte):
        geometrie_layout.append(punktreihe(i))

    kräfte_layout = [
        [sg.Text("Belastung definieren",font=(any,20))],
        [sg.Button("Kraft hinzufügen",key="-ADD_KRAFT-"),sg.Button("Kraft entfernen",key="-REM_KRAFT-")],
    ]
    for i in range(n_kräfte):
        kräfte_layout.append(kraftreihe(i))

    layout = [
    [sg.Titlebar("Wellennachweis")],
    [sg.Text("Wellennachweis nach DIN 743",font=(any,30))],
    [sg.Text("Nadine Schulz und Quentin Huss"),sg.Push(),sg.Text("Angaben ohne Gewähr!")],
    [sg.HorizontalSeparator()],

    [sg.Text("Name der Welle",font=(any,20))],
    [sg.Input(wellenname,key="-NAME-")],

    [sg.Text("Werkstoff",font=(any,20))],
    [sg.Text('aus Datei "Werkstoffdaten.csv"'),sg.Combo(list(Werkstoff.Werkstoffe.keys()),material,key="-WERKSTOFF-")],
    [sg.Text("Oberflächenrauheit Rz ="),sg.Input(Rz,(7,any),key="-RZ-")],
    [sg.Text("Oberfläche verfestigt?"),sg.OptionMenu(optionen_oberfl,oberflächenv,key="-OBERFV-")],

    [sg.Text("Lagerpositionen",font=(any,20))],
    [sg.Text("Festlager:"),sg.Input(festlager_z,size=(7,None),key="-FLZ-"),sg.Text("mm")],
    [sg.Text("Loslager: "),sg.Input(loslager_z,size=(7,None),key="-LLZ-"),sg.Text("mm")],

    [sg.Column(geometrie_layout),sg.VSep(),sg.Column(kräfte_layout)],
    [sg.Button("Welle darstellen",key="-DRAW WELLE-"),sg.Button("Belastungen berechnen",key="-CALC LAGERKRÄFTE-")],
    ]

    window = new_window()

    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            running = False
            window.close()
            #print("FENSTER GESCHLOSSEN")
            break
        if event == "-DRAW WELLE-":
            save_all()
            welle = Welle(name=wellenname,festlager_z=festlager_z,loslager_z=loslager_z,werkstoff=material,Oberflächenverfestigung=oberflächenv)
            geometrie = [(float(punkt[1]),float(punkt[2])) for punkt in punkteinput]
            welle.set_geometrie(geometrie)
            welle.welle_darstellen()

        if event=="-CALC LAGERKRÄFTE-":
            save_all()
            welle = Welle(name=wellenname,festlager_z=festlager_z,loslager_z=loslager_z,werkstoff=material,Oberflächenverfestigung=oberflächenv)
            geometrie = [(float(punkt[1]),float(punkt[2])) for punkt in punkteinput]
            welle.set_geometrie(geometrie)
            for kraft in kräfteinput:
                welle.set_Kraft(float(kraft[0]),kraft[4],float(kraft[1]),float(kraft[2]),float(kraft[3]))
            welle.lagerkräfte_berechnen()
            welle.plot()
        if event=="-ADD_PUNKT-":
            save_all()
            n_punkte += 1
            window.close()
            break
        if event=="-REM_PUNKT-":
            save_all()
            if n_punkte>2:
                n_punkte -= 1
            window.close()
            break
        if event=="-ADD_KRAFT-":
            save_all()
            n_kräfte += 1
            window.close()
            break
        if event=="-REM_KRAFT-":
            save_all()
            if n_kräfte>1:
                n_kräfte -= 1
            window.close()
            break
