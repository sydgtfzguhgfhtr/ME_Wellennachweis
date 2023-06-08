import PySimpleGUI as sg

sg.theme("DarkBlue14")

running = True
n_lager = 2 # Standardwert für die Lageranzahl

lagertable = []
for zeile in range(n_lager):
    lagertable.append([f"Lager {zeile+1}",0])

while running:
    layout = [
    [sg.Titlebar("Wellennachweis")],
    [sg.Text("Wellennachweis nach DIN 743",font=(any,30))],
    [sg.Text("erstellt von Nadine Schulz und Quentin Huss")],
    [sg.HorizontalSeparator()],
    [sg.Text("Lager definieren",font=(any,20))],
    [sg.Button("hinzufügen",key="-ADD_LAGER-"),sg.Button("entfernen",key="-REM_LAGER-")],
    [sg.Table(lagertable,["Name","z"],auto_size_columns=False,enable_events=True,key="-LAGERTABLE-")],
    ]

    window = sg.Window("Wellenachweis",layout=layout)

    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            running = False
            break
        if event=="-LAGERTABLE-":
            # Es wurde eine Zeile in der Lagertabelle angeklickt
            if len(values["-LAGERTABLE-"])>0:
                rowselect = values["-LAGERTABLE-"][0]
            else:
                rowselect = len(lagertable)
            print(rowselect)
        if event=="-ADD_LAGER-":
            lagertable.append([f"Lager {len(lagertable)+1}",0])
            window["-LAGERTABLE-"].update(values=lagertable)
        if event=="-REM_LAGER-":
            lagertable = lagertable[:-1]
            window["-LAGERTABLE-"].update(values=lagertable)