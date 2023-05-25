"""
Dient zum testen der Klassen außerhalb der eigenen Datei.
"""

from Klassen import Werkstoff

Werkstoff.aus_csv_laden()

testws: Werkstoff
testws = Werkstoff.Werkstoffe["S235JR"]
print(testws.name,testws.sigma_zdW,testws.sigma_bW,testws.tau_tW,testws.art)