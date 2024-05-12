# IT-Sicherheit SoSe24, Praktikum 1, Aufgabe 4
# von Gruppe 27
#
### Grundprinzip ###
#
# Wenn 2 Nachrichten m1, m2 mit dem selben OTP-Schlüssel k verschlüsselt werden, gilt:
# m1 ^ k = e1 & m2 ^ k = e2
# und da k ^ k = 0, folgt:
# e1 ^ e2 = m1 ^ m2
#
# Wenn man jetzt den Inhalt einer der Nachrichten erraten könnte (z.B. durch einen Wörterbuch-Angriff),
# lässt sich auf den benutzten OTP-Schlüssel schließen:
#
# Gegeben seien
# e1, e2, mit t = e1 ^ e2
# und ein erratener byte-string b = m1
# dann gilt:
# 
# t ^ b = m2
# und da e2 ^ k = m2, gilt umgekehrt
# e2 ^ m2 = k
#
### Das Programm ###
#
# Mit diesem Programm lässt sich aus einer vordefinierten Wortliste ein byte-String zusammensetzen,
# um den Klartext einer der beiden Chiffren e1, e2 zu erraten.
# 
# Dazu wird (e1^e2) mit einem Wort aus dem Wörterbuch geXORt (= mögl. Klartext der einen Nachricht)
# und dann mit dem Ergebnis nach einem weiteren Wort aus dem Wörterbuch gesucht (mögl. Klartext der anderen Nachricht).
# Sehen die Resultate sinnvoll aus, kann man eins der Worte speichern und nach dem nächsten suchen.
# Ist der so zusammengesetzte String schließlich lang genug, kann man den möglichen OTP-Schlüssel errechnen.
#
# Annahmen:
# - die Klartexte bestehen aus Wörtern in der Wortliste
# - die erste Nachricht beginnt mit einem dieser Worte
# - zwischen den Wörtern sind Leerzeichen
#
# (Spoiler: Programm starten, drei Mal ENTER drücken und 'key1' eingeben.)
#

import re   
    
# Gibt a ^ b zurück
# (b lässt sich über einen positiven offset nach rechts verschieben)
def xorBytes(a, b, bOffset = 0):
    b = (b'\x00' * bOffset) + b
    sz = min(len(a), len(b))
    return (bytes([(a[i] ^ b[i]) for i in range(sz)]))[bOffset:]

# Überprüft, ob string s in einem Wort der Wortliste vorkommt
# und gibt entweder den Treffer oder einen leeren String zurück    
def isInWordList(s, wordList):
    if(s):
        for w in wordList:
            if(s in w):
                return w
    return ""
    
# Setzt aus den Elementen w der wordList einen String (wPrefix + w) zusammen und rechnet ihn XOR target.
# Besteht die Nachricht aus mehreren Wörtern, kann man diese in wPrefix speichern,
# um dann über einen rekursiven Aufruf das nächste w zu suchen.
def wordListAttack(wordList, target, wPrefix = b""):
    if(wPrefix):
        print("Using prefix:", wPrefix, "\n")
        
    for w in wordList:
        testStringA = wPrefix + w
        xorCheckA = xorBytes(target, testStringA)       # = target ^ (wPrefix + w)
        matchCandidate = xorCheckA.split(b' ')[-1]      # letztes Wort im xorCheck-string (zum Finden in der wordList)
        match = isInWordList(matchCandidate, wordList)  # nach match in der wordList suchen
        
        if(match):
            print("target ^ ", testStringA, "  ->  ", xorCheckA, " (", matchCandidate, " found in word ", match, ")", sep="")
            
            u = match[match.find(matchCandidate):]      # match ebenfalls testen (& vorher ggf. slicen)
            testStringB = wPrefix + u
            xorCheckB = xorBytes(target, testStringB)
            
            print("target ^", testStringB, " -> ", xorCheckB, "\n")
            
            if(len(testStringA) >= len(target) or len(testStringB) >= len(target)):
                print("(One of the strings reached target length - Consider checking for a key.)\n")
            
            print("- press ENTER to continue search", \
                "\n- type 'save1' to save word(s)", testStringB, \
                "\n- type 'save2' to save word(s)", testStringA, \
                "\n- type 'key1' to calculate keys with string", testStringB, \
                "\n- type 'key2' to calculate keys with string", testStringA, \
                "\n- type 'exit' to abort the search")
            inp = input(">>> ").strip()
            
            if(len(inp)):
                if(reMatch := re.match("save([1-2]{1})", inp)):
                
                    newPrefix = wPrefix + u.split(b" ")[0]  # für 'save1' -> erstes vollständiges Wort in u
                    if(reMatch.group(1) == "2"):
                        newPrefix = wPrefix + w             # für 'save2'
                        
                    newPrefix += b" "                       # Leerzeichen zwischen den Worten
                    wordListAttack(wordList, target, newPrefix) # Rekursion mit neuem prefix string
                        
                elif(reMatch := re.match("key([1-2]{1})", inp)):
                
                    key_base = wPrefix + u                  # für 'key1'
                    if(reMatch.group(1) == "2"):
                        key_base = wPrefix + w              # für 'key2'
                        
                    k1 = xorBytes(e1, key_base)
                    k2 = xorBytes(e2, key_base)
                    k1_test1 = xorBytes(e1, k1)
                    k1_test2 = xorBytes(e2, k1)
                    k2_test1 = xorBytes(e1, k2)
                    k2_test2 = xorBytes(e2, k2)
                    print("\nPossible key k1: ", k1, \
                        "\nPossible key k2: ", k2, \
                        "\nk1 ^ e1 =" , k1_test1, \
                        "\nk1 ^ e2 =" , k1_test2, \
                        "\nk2 ^ e1 =" , k2_test1, \
                        "\nk2 ^ e2 =" , k2_test2)
                        
                    inp = input("Type 'exit' to abort or anything else to continue search: ").strip()

                if(inp == "exit"):
                    print("Exiting ...")
                    exit()
                        
            print("Continuing word list search ... \n")
            
    print("\nNO MATCHES FOUND", end="")
    if(wPrefix):
        print(" with prefix", wPrefix)


def main():
    # get cipher hex strings e1, e2
    global e1
    global e2
    try:
        with open("Aufgabe4_1.txt", "r") as f:
            e1 = f.read()
        with open("Aufgabe4_2.txt", "r") as f:
            e2 = f.read()
    except FileNotFoundError: #failsafe
        e1 = "012625062E2D22212C36212022"
        e2 = "153B2114312921382C36212022"  
    print("Reading cipher strings e1 & e2 ...", \
        "\nHex e1: " + e1,
        "\nHex e2: " + e2)
        
    # convert hex strings to bytes
    e1 = bytes.fromhex(e1)
    e2 = bytes.fromhex(e2)
    print("\nHex -> Bytes e1:", e1, \
        "\nHex -> Bytes e2:", e2)
    
    # get e1 ^ e2 = m1 ^ m2
    eX = xorBytes(e1, e2)
    print("\ntarget string (e1^e2): "+ str(eX))
    
    wordList = []
    print("\nReading word list from file ... ", end="")
    try:
        with open("aufg4_wordlist.txt", "rb") as f:
            wordList = f.read().split(b' ')
        print("Done")
    except FileNotFoundError: #failsafe
        wordList = [b"ZU", b"SO", b"PROGRAMM", b"DOKUMENTIEREN", b"BUCHSTABENH\xc3\x84UFIGKEIT", b"KRYPTOGRAPHIE"]
        print("Failed. Using failsafe word list")
    
    input("Press ENTER to start word list attack on the target string:\n")
    wordListAttack(wordList, eX)    
        
if __name__ == '__main__':
    main()