from Werkstoffdaten_alternativ import Werkstoff

Werkstoff.aus_csv_laden()

Werkstoff("Wasser",0,0,0)

testws: Werkstoff
testws = Werkstoff.Werkstoffe["S235JR"]
print(testws.name,testws.sigma_zdW,testws.sigma_bW,testws.tau_tW,testws.art)