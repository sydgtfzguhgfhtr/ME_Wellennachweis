import PySimpleGUI as sg

sg.theme("DarkBlue14")

running = True
n_lager = 2 # Standardwert für die Lageranzahl

def constr_lagertable(n):
    table = []
    for zeile in range(n):
        table.append([f"Lager {zeile+1}",0])
    return table


while running:
    lagertable = constr_lagertable(n_lager)
    layout = [
    [sg.Titlebar("Wellennachweis")],
    [sg.Text("Wellennachweis nach DIN 743",font=(any,30))],
    [sg.Text("erstellt von Nadine Schulz und Quentin Huss")],
    [sg.HorizontalSeparator()],
    [sg.Text("Anzahl der Lager: "),sg.Input(str(n_lager),key="-N_LAGER-"),sg.Button("Bestätige",key="-CONFIRM_LAGER-")],
    [sg.Table(lagertable,["Name","z"],auto_size_columns=False,enable_events=True,key="-TABLE-")],
    ]

    window = sg.Window("Wellenachweis",layout=layout)

    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            running = False
            break
        if event=="-TABLE-":
            print(values)
        if "-CONFIRM_LAGER-" == event:
            n_lager = int(values["-N_LAGER-"])
            if n_lager>0 and n_lager<=30:
                window.close()
                break
            