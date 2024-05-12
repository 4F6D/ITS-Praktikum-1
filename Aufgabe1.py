# Author: René Reifen


# Für die Aufgabe wurde der Wikipedia-Artikel zur Buchstabenhäufigkeit der 
# deutschen Sprache benutzt.

# Der meistgenutzte Buchstabe der deutschen Sprache ist 'E'. In der Textdatei
# ist wiederum, der Buchstabe 'W' am häufigsten vertreten. Deshalb können wir
# Mit hoher wahrscheinlichkeit folgern, dass 'W' = 'E' ist.
# Daraus können wir dann schließen, dass 'V' = 'D' ist, da die meisten Wörter mit 
# Drei buchstaben, die einen Satz beginnen, Artikel sind wie 'Der', 'Die', 'Das'.
# Wenn wir aber davon ausgehen, dass 'W' = 'E' ist, dann bleibt nur 'Der' übrig, was
# wiederum bedeutet, 'VwJ' = 'Der' -> 'J' = 'R'.

# Aus all diesen Schlussfolgerungen, können wir nun die Vermutung Caesar: k = 18 ziehen
# Was bedeutet, dass alle Buchstaben der Verschlüsselten Nachricht um 18 nach links
# im Alphabet verschoben werden müssen um die Nachricht zu entschlüsseln.


# MATPLOTLIB WURDE ZUR GRAFISCHEN DARSTELLUNG GENUTZT, DIESE MÜSSEN VORHANDEN SEIN DAMIT DAS PROGRAMM FUNKTIONIERT
# macOS, Windows, Linux Installation:
# python -m pip install -U pip
# python -m pip install -U matplotlib

# Import von Matplotlib zur grafischen Darstellung 
import matplotlib.pyplot as plt

# Öffnen und einlesen der Textdatei
datei = open('Aufgabe1.txt', 'r')

# Prüfen ob der Inhalt anständig ausgelesen wurde
# print(datei.read())

# Inhalt der Textdatei in einen String zwischenspeichern
text = datei.read()

# Funktion um die Buchstaben zu zählen
def buchstabenhäufigkeit(text):
	# Text in kleinbuchstaben konvertieren
	text.lower()

	# Leeres Wörterbuch(liste), um die Häufigkeit der Buchstaben zu speichern
	häufigkeit = {}

	for buchstabe in text:
		# Ignoriere Leer- & Sonderzeichen
		if buchstabe.isalpha():

			# Falls der Buchstabe im Wörterbuch bereits existiert, inkrementieren
			if buchstabe in häufigkeit:
				häufigkeit[buchstabe] += 1
			# Falls der Buchstabe nicht existiert, füge ihn hinzu
			else:
				häufigkeit[buchstabe] = 1

	return häufigkeit

# Funktion zur Entschlüsselung des Textes
def caesar_decryption(text, k):
	# Deutsches Alphabet ohne ä,ö,ü,ß definieren
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	ergebnis = []

	# Wir gehen jeden Buchstaben im Text durch und machen ihn zum Kleinbuchstaben
	for buchstabe in text.lower():
		# Prüfen ob der Buchstabe sich im deutschen Alphabet befindet
		if buchstabe in alphabet:
			# Den Index(position) des Buchstaben im Alphabet abfragen
			index = alphabet.index(buchstabe)

			# Den Index um k negativ verschieben
			new_index = index - k

			# Den decodierten Buchstaben, nach jedem Durchlauf in das Ergebnis fügen n
			ergebnis.append(alphabet[new_index])

			# Nicht alphabetische Zeichen wie Leerzeichen unverändert hinzufügen
		else:
			ergebnis.append(buchstabe)

		# Den fertigen decodierten String vollständig zurückgeben
	return "".join(ergebnis)

x_labels = []

# Buchstabenhäufigkeit ausgeben
ergebnis = buchstabenhäufigkeit(text)
for buchstabe, häufigkeit in ergebnis.items():
	print(f"{buchstabe}: {häufigkeit}")
	x_labels.append(buchstabe)

# Einfach nur eine Trennlinie ausgeben
print("--------------------------")
print("")

# Entschlüsselung und Ausgabe der Nachricht
ausgabe = caesar_decryption(text, 18)
print("Entschlüsselte Ausgabe:\n\n", ausgabe)

# Sortieren der Buchstaben nach ihrer Häufigkeit
sortierte_buchstaben = sorted(ergebnis.items(), key=lambda x: x[1], reverse=True)

# Ergebnisse grafisch darstellen
x_labels, ergebnis = zip(*sortierte_buchstaben)
plt.bar(x_labels, ergebnis)
plt.show()

