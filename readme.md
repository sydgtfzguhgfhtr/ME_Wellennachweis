# Belegarbeit Maschinenelemente 2 - Wellen- und Lagernachweis

Nadine Schulz, Quentin Huss

## Übersicht

Dieses Projekt ist eine Python-Implementierung zur Durchführung von Wellen- und Lagernachweisen im Rahmen der Belegarbeit für die Lehrveranstaltung Maschinenelemente 2. Es bietet Funktionalitäten zur Modellierung von Wellen, Wellenabsätzen, Werkstoffen und Lagern, sowie zur Berechnung relevanter Kenngrößen für die Nachweise.

## Funktionen

### Wellen

- Modellierung von Wellen mit unterschiedlichen Durchmessern entlang der Längsachse
- Berechnung von Durchmesser und Radius an beliebigen Stellen der Welle
- Hinzufügen von Wellenabsätzen (Absatz, umlaufende Rundnut, Passfeder, Spitzkerbe, Keilwelle, Kerbzahnwelle, Zahnwelle, Pressverbindung)

### Werkstoffe

- Verwaltung von Werkstoffdaten (Name, Festigkeitskennwerte, Werkstoffart)
- Laden von Werkstoffdaten aus einer integrierten Datenbank
- Ausgabe von Werkstoffdatenblättern

### Lager

- Modellierung von Wälzlagern (Rillenkugellager, Tonnenlager, Pendelrollenlager, Zylinderrollenlager)
- Berechnung der äquivalenten statischen und dynamischen Belastung
- Berechnung der Lebensdauererwartung nach SKF-Richtlinien

## Installation

1. Stellen Sie sicher, dass Python (Version 3.6 oder höher) auf Ihrem System installiert ist.
2. Klonen Sie dieses Repository oder laden Sie den Quellcode herunter.
3. Navigieren Sie im Terminal zum Projektverzeichnis.
4. Installieren Sie die erforderlichen Abhängigkeiten mit dem Befehl:

```bash
pip install -r requirements.txt
```

## Verwendung

1. Importieren Sie die benötigten Module in Ihr Python-Skript.
2. Erstellen Sie Instanzen der Klassen `Welle`, `Werkstoff` und `Lager` entsprechend Ihrer Anforderungen.
3. Rufen Sie die gewünschten Methoden auf, um Berechnungen durchzuführen oder Daten auszugeben.


