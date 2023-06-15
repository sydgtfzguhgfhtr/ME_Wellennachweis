from Klassen import Welle,Werkstoff,Welle_Absatz

import PySimpleGUI as sg

sg.theme("DarkBlue14")

running = True
n_punkte = 2 # Standardwert für die Punktzahl

welle = None

punkteinput = []
for zeile in range(n_punkte):
    punkteinput.append([0])


def punktreihe(key:str):
    arten = ["Absatz","umlaufende Rundnut","eine Passfeder","zwei Passfedern","umlaufende Spitzkerbe","Keilwelle","Kerbzahnwelle","Zahnwelle","Pressverbindung"]
    i = int(key)
    key = str(key)
    try:
        return [sg.Text(key),sg.Checkbox("Nachweisen",key="NW"+key,default=punkteinput[i][0]),sg.Text("z="),sg.Input(punkteinput[i][1],size=(5,None),key="Z"+key),sg.Text("r="),sg.Input(punkteinput[i][2],size=(5,None),key="R"+key),sg.OptionMenu(default_value=punkteinput[i][3],values=arten,key="EXTRA"+key)]
    except IndexError:
        return [sg.Text(key),sg.Checkbox("Nachweisen",key="NW"+key),sg.Text("z="),sg.Input(size=(5,None),key="Z"+key),sg.Text("r="),sg.Input(size=(5,None),key="R"+key),sg.OptionMenu(values=arten,key="EXTRA"+key,default_value="Absatz")]

def new_window():
    return sg.Window("Wellenachweis",layout=layout)

def read_point_vals():
    global punkteinput
    punkteinput = []
    for i in range(n_punkte):
        key = str(i)
        punkteinput.append([values["NW"+key],values["Z"+key],values["R"+key],values["EXTRA"+key]])

Werkstoff.aus_csv_laden()

while running:
    instance = True

    layout = [
    [sg.Titlebar("Wellennachweis")],
    [sg.Text("Wellennachweis nach DIN 743",font=(any,30))],
    [sg.Text("Nadine Schulz und Quentin Huss"),sg.Push(),sg.Text("Alle Angaben in mm!")],
    [sg.HorizontalSeparator()],

    [sg.Text("Name der Welle",font=(any,20))],
    [sg.Input("Welle 1",key="-NAME-")],

    [sg.Text("Werkstoff",font=(any,20))],
    [sg.Text('aus Datei "Werkstoffdaten.csv"'),sg.Combo(list(Werkstoff.Werkstoffe.keys()))],

    [sg.Text("Geometrie definieren",font=(any,20))],
    [sg.Button("hinzufügen",key="-ADD_PUNKT-"),sg.Button("entfernen",key="-REM_PUNKT-")],
    [sg.Text("Punkte (z,r,phi)",font=(any,20))],
    [punktreihe(str(i)) for i in range(n_punkte)],
    [sg.Button("Lagerkräfte berechnen",key="-CALC LAGERKRÄFTE-")]
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
            welle = Welle(name=values["-NAME-"],festlager_z=0,loslager_z=100)
        if event=="-ADD_PUNKT-":
            read_point_vals()
            n_punkte += 1
            window.close()
            break
        if event=="-REM_PUNKT-":
            read_point_vals()
            if n_punkte>2:
                n_punkte -= 1
            window.close()
            break
