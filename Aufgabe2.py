# IT-Sicherheit SoSe24, Praktikum 1, Aufgabe 2
# von Gruppe 27


import os
from hashlib import sha256


def readFile(filename):
    try:
        reader = open(filename, "rb") 
        data = reader.read()
        reader.close()
        return data
    except Exception as e:
        return e


def writeFile(data,filename):
    writer = open(filename, 'wb')
    writer.write(data)
    writer.close()

 
def xor(Byte1,Byte2):
    # 
    # Führt bitweise die XOR-Operation zwischen zwei Bytestrings aus.
    # 
    # Args:
    # Byte1 (bytes): Der erste Bytestring.
    # Byte2 (bytes): Der zweite Bytestring.
    # 
    # Returns:
    # bytes: Das Ergebnis der XOR-Operation zwischen Byte1 und Byte2
    return bytes([bit1 ^ bit2 for bit1,bit2 in zip(Byte1,Byte2)])


def blocks2Text(textBlocks):
    # 
    # Konkateniert eine Listen von Textblöcken zu einem String zusammen
    # 
    # Args:
    # textBlocks (list): Eine Liste von Textblöcken, jedes Element ist ein String.
    # 
    # 
    # Returns:
    # text (String): Ein einziger String bestehend aus allen Textblöcken.
    text = textBlocks[0] 
    
    for i in range(1,len(textBlocks)):
        text = text + textBlocks[i]
    
    return text


def padding(plaintext, block_size):
    #
    # Auffuellen des Klartexts um sicherzustellen das seine laenge ein vielfaches der Blockgoeße ist.
    #
    # Args:
    # plaintext (bytes): Der aufzufuellende Klartext
    # block_size (int): Die Groeße eines jeden Blocks in Bytes.
    #
    # Return:
    # padded_plaintext (String) : Der aufgefüllte Klartext 
    #
    padding_length = block_size -(len(plaintext) % block_size)
    padded_plaintext = plaintext + bytes([0] * padding_length)
    return padded_plaintext

def derive_key_from_passphrase(passphrase, block_size):
    #
    # Das Ableiten eines kryptographischen Schlüssels von einer Passphrase unter Verwendung der SHA-256 Hashfunktion.
    #
    # Args:
    # passprhase (bytes): Die Passphrase die als Basis für den Schlüssel dient. 
    # block_size (int): Die Größe eines jeden Blocks in Bytes.
    #
    # Return:
    # bytes : kryptographischen Schlüssel
    #

    # Die Passphrase wird mittels der SHA-256 Hashfunktion in utf-8 Darstellung gehasht
    hash_object = sha256()
    hash_object.update(passphrase.encode('utf-8'))
    hash_digest = hash_object.hexdigest()
    
    # Erweitern der Hashsumme auf die spezifische Blockgröße
    expanded_Key = hash_digest.ljust(block_size,'\x00')[:block_size]

    return bytes( expanded_Key , 'utf-8')


def encrypt(plaintext,IV,passphrase):
    # 
    # Verschlüsselt einen Klartext mit der AES-CBC Verschlüsselung bei einem gegeben Initialisierungsvektor und einer Passphrase.
    # 
    # Args:
    # plaintext (Bytes): Der Klartext der zu verschlüsseln ist.
    # IV (bytes): Der Initialisierungs Vektor für die Verschlüsselung.
    # passphrase (Bytes): Die Passphrase ist die Grundlage um den Schlüssel 
    #
    # Returns:
    # cipherText (Bytes): Der aus der Verschlüsslung resultierende Chiffriertetext.
    cipherTextBlocks =[] # Liste für das Speichern der bereits chiffrierter  Textblöcke
    block_size = 16 # Verschlüsselung in einer Blockgröße von 16 Byte
    key = derive_key_from_passphrase(passphrase , block_size)

    padded_plaintext = padding(plaintext,block_size) if len(plaintext) % block_size != 0 else plaintext
    
    # Aufteilen des Klartextes in Blöcke mit je 128-Bit länge
    plainTextBlocks = [padded_plaintext[i:i+block_size] for i in range(0, len(plaintext), block_size)]
   

    # Verschlüsselung des ersten Klartextblocks
    cipherTextBlocks.append(xor( xor(plainTextBlocks[0],IV) , key))

    for i in range(1,(len(plainTextBlocks))):
        cipherTextBlocks.append(xor(xor(plainTextBlocks[i],cipherTextBlocks[i-1]),key))

    
    # Umwandeln der Chiffreblöcke in einen String
    cipherText = blocks2Text(cipherTextBlocks)
   
    return cipherText



def main():
    key = 'ITS-Prakt2024'   # Vorgebener Schlüssel
    IV = os.urandom(128)    # Erstellen des Initialisierungs Vektors mit einer Länge von 128 Bit
    filePlainText = 'Aufgabe2.bin'
    fileCiphre ='Aufgabe2_Loesung.bin'
    plaintext = readFile(filePlainText)  # einlesen des Klartextes

    # Aufrufen der Verschlüsselungsfunktion
    if type(plaintext).__name__ == "bytes":
        print("Der Klartext wurde aus der Datei gelesen, beginne mit dem Verschlüsseln...")
        ciphertext = encrypt(plaintext,IV,key)

        # das Schreiben der Chiffre in eine Datei
        writeFile(ciphertext,fileCiphre)
        print(f"Die Chiffre wurde erfolgreich in in die Datei \'{fileCiphre}\' geschrieben." )

    
    print("Das Programm wird beendet")


if __name__ =='__main__':
    main()