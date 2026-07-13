import string

def cesar_chiffre(message, decalage):
    resultat = ""
    for char in message:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            resultat += chr((ord(char) - base + decalage) % 26 + base)
        else:
            resultat += char
    return resultat

def cesar_dechiffre(message, decalage):
    return cesar_chiffre(message, -decalage)

def vigenere_chiffre(message, cle):
    resultat = ""
    cle = cle.lower()
    i = 0
    for char in message:
        if char.isalpha():
            decalage = ord(cle[i % len(cle)]) - ord('a')
            base = ord('A') if char.isupper() else ord('a')
            resultat += chr((ord(char) - base + decalage) % 26 + base)
            i += 1
        else:
            resultat += char
    return resultat

def vigenere_dechiffre(message, cle):
    resultat = ""
    cle = cle.lower()
    i = 0
    for char in message:
        if char.isalpha():
            decalage = ord(cle[i % len(cle)]) - ord('a')
            base = ord('A') if char.isupper() else ord('a')
            resultat += chr((ord(char) - base - decalage) % 26 + base)
            i += 1
        else:
            resultat += char
    return resultat

def substitution_chiffre(message, alphabet_subst):
    alphabet = string.ascii_lowercase
    table = str.maketrans(alphabet, alphabet_subst)
    return message.lower().translate(table)

def substitution_dechiffre(message, alphabet_subst):
    alphabet = string.ascii_lowercase
    table = str.maketrans(alphabet_subst, alphabet)
    return message.lower().translate(table)
