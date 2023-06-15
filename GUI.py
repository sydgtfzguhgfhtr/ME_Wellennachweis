from Klassen import Welle,Werkstoff,Welle_Absatz

import PySimpleGUI as sg

sg.theme("Dark Teal 9")

running = True
wellenname = "Welle 1"
material = ""
festlager_z = 0
loslager_z = 100
Rz = 20
n_punkte = 2 # Standardwert für die Punktzahl
n_kräfte = 1 # Standardwert für die Kräftezahl


welle = None

punkteinput = [] # Beinhaltet die Nutzerdaten für die Punkte
kräfteinput = [] # Beinhaltet die Nutzerdaten für die Kräfte

def punktreihe(key:str):
    arten = ["Absatz","umlaufende Rundnut","eine Passfeder","zwei Passfedern","umlaufende Spitzkerbe","Keilwelle","Kerbzahnwelle","Zahnwelle","Pressverbindung"]
    i = int(key)
    key = str(key)
    try:
        return [sg.Text(key),sg.Checkbox("Nachweisen",key="NW"+key,default=punkteinput[i][0]),sg.Text("z [mm]="),sg.Input(punkteinput[i][1],size=(5,None),key="Z"+key),sg.Text("r [mm]="),sg.Input(punkteinput[i][2],size=(5,None),key="R"+key),sg.OptionMenu(default_value=punkteinput[i][3],values=arten,key="EXTRA"+key)]
    except IndexError:
        return [sg.Text(key),sg.Checkbox("Nachweisen",key="NW"+key),sg.Text("z [mm]="),sg.Input(size=(5,None),key="Z"+key),sg.Text("r [mm]="),sg.Input(size=(5,None),key="R"+key),sg.OptionMenu(values=arten,key="EXTRA"+key,default_value="Absatz")]

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
        punkteinput.append((values["NW"+key],values["Z"+key],values["R"+key],values["EXTRA"+key]))

def read_force_vals():
    global kräfteinput
    kräfteinput = []
    for i in range(n_kräfte):
        key = str(i)
        kräfteinput.append((values["F"+key],values["FZ"+key],values["FR"+key],values["FPHI"+key],values["FART"+key]))
    print(values)
    print(kräfteinput)

def read_misc_vals():
    global wellenname,material,festlager_z,loslager_z
    wellenname = values["-NAME-"]
    material = values["-WERKSTOFF-"]
    festlager_z = values["-FLZ-"]
    loslager_z = values["-LLZ-"]

def save_for_refresh():
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
    [sg.Text("Oberflächenrauheit Rz ="),sg.Input(Rz,(7,any))],

    [sg.Text("Lagerpositionen",font=(any,20))],
    [sg.Text("Festlager:"),sg.Input(festlager_z,size=(7,None),key="-FLZ-")],
    [sg.Text("Loslager: "),sg.Input(loslager_z,size=(7,None),key="-LLZ-")],

    [sg.Column(geometrie_layout),sg.VSep(),sg.Column(kräfte_layout)],
    [sg.Button("Lagerkräfte berechnen",key="-CALC LAGERKRÄFTE-")],
    ]

    window = new_window()

    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            running = False
            window.close()
            #print("FENSTER GESCHLOSSEN")
            break
        if event=="-CALC LAGERKRÄFTE-":
            #welle = Welle(name=wellenname,festlager_z=festlager_z,loslager_z=loslager_z,werkstoff=material)
            pass
        if event=="-ADD_PUNKT-":
            save_for_refresh()
            n_punkte += 1
            window.close()
            break
        if event=="-REM_PUNKT-":
            save_for_refresh()
            if n_punkte>2:
                n_punkte -= 1
            window.close()
            break
        if event=="-ADD_KRAFT-":
            save_for_refresh()
            n_kräfte += 1
            window.close()
            break
        if event=="-REM_KRAFT-":
            save_for_refresh()
            if n_kräfte>1:
                n_kräfte -= 1
            window.close()
            break
