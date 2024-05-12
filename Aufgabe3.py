# Überprüft, ob eine Zahl eine Primzahl ist.
def is_prime(number):
    # Eine Primzahl ist eine natürliche Zahl, die größer als 1 ist und nur durch 1 und sich selbst teilbar ist.
    if number <= 1:
        # Wenn die Zahl kleiner oder gleich 1 ist, ist sie keine Primzahl.
        return False
    # Iteriere über alle Zahlen von 2 bis zur Wurzel der Zahl, um zu überprüfen, ob die Zahl eine Primzahl ist.
    for i in range(2, int(number ** 0.5) + 1):
        # Wenn die Zahl durch eine andere Zahl als 1 und sich selbst teilbar ist, ist sie keine Primzahl.
        if number % i == 0:
            # Die Zahl ist keine Primzahl.
            return False
    # Die Zahl ist eine Primzahl.
    return True


# Berechnet den öffentlichen Schlüssel mit Basis, privatem Schlüssel und Primzahl.
def calculate_public_key(base, private_key, prime):
    # Berechnet (base^private_key) % prime
    return (base ** private_key) % prime


# Diffie-Hellman-Schlüsselaustausch
def diffie_hellman():
    # Eingabe der Primzahl, des Generators und der privaten Schlüssel
    p = int(input("Primzahl p: "))

    # Überprüfen, ob die eingegebene Zahl eine Primzahl ist
    if not is_prime(p):
        # Wenn die Zahl keine Primzahl ist, wird eine Fehlermeldung ausgegeben und das Programm beendet.
        print("Die eingegebene Zahl ist keine Primzahl.")
        exit(1)

    # Eingabe des Generators und der privaten Schlüssel
    g = int(input("Generator g: "))

    # Überprüfen, ob der Generator kleiner als die Primzahl ist
    if g >= p:
        # Wenn der Generator größer oder gleich der Primzahl ist, wird eine Fehlermeldung
        # ausgegeben und das Programm beendet.
        print("Der Generator muss kleiner als die Primzahl sein.")
        exit(1)

    # Eingabe der privaten Schlüssel
    a = int(input("Privater Schlüssel A (eine zufällige Zahl): "))
    b = int(input("Privater Schlüssel B (eine andere zufällige Zahl): "))

    # Berechnung der öffentlichen Schlüssel
    public_key_a = calculate_public_key(g, a, p)
    public_key_b = calculate_public_key(g, b, p)

    # Ausgabe der öffentlichen Schlüssel
    print(f"Öffentlicher Schlüssel A: {public_key_a}")
    print(f"Öffentlicher Schlüssel B: {public_key_b}")

    # Berechnung des gemeinsamen Schlüssels
    shared_key_a = calculate_public_key(public_key_b, a, p)
    shared_key_b = calculate_public_key(public_key_a, b, p)

    # Ausgabe des gemeinsamen Schlüssels
    print(f"Gemeinsamer Schlüssel A: {shared_key_a}")
    print(f"Gemeinsamer Schlüssel B: {shared_key_b}")

    # Überprüfen, ob beide Parteien den gleichen geheimen Schlüssel haben
    assert shared_key_a == shared_key_b
    print("Beide Parteien haben den gleichen geheimen Schlüssel.")


diffie_hellman()
