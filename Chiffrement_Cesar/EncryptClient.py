import time
import psutil
import os
import socket
import random

from CryptoSym import cesar_chiffre, vigenere_chiffre, substitution_chiffre


def demander_parametres(method):
    if method == 'cesar':
        decalage = int(input("Décalage César : "))
        return {'decalage': decalage, 'param_str': str(decalage)}
    elif method == 'vigenere':
        cle = input("Clé Vigenère : ")
        return {'cle': cle, 'param_str': cle}
    elif method == 'substitution':
        alphabet_subst = input("Alphabet de substitution (26 lettres) : ")
        return {'alphabet_subst': alphabet_subst, 'param_str': alphabet_subst}
    else:
        return {'param_str': ''}


def random_case(s):
    """Applique une casse aléatoire à chaque caractère alphabétique"""
    return ''.join(
        c.upper() if c.isalpha() and random.random() < 0.5 else c.lower()
        if c.isalpha() else c
        for c in s
    )


HOST = '192.168.1.178'
PORT = 50007

print("Méthodes disponibles : cesar, vigenere, substitution")
method = input("Choisissez la méthode de chiffrement : ").strip().lower()
message = input("Saisissez le message à chiffrer : ")
params = demander_parametres(method)

# --- Mesure du temps et vérification de taille ---
if len(message) > 50000:
    print("⚠ Erreur : message trop long pour être chiffré.")
    exit()

start_time = time.time()

if method == 'cesar':
    message_chiffre = cesar_chiffre(message, params['decalage'])
elif method == 'vigenere':
    message_chiffre = vigenere_chiffre(message, params['cle'])
elif method == 'substitution':
    message_chiffre = substitution_chiffre(message, params['alphabet_subst'])
else:
    print("Méthode inconnue.")
    exit()

end_time = time.time()
temps_chiffrement = end_time - start_time
print(f"Temps de chiffrement : {temps_chiffrement:.6f} secondes")

# --- Envoi réseau ---
message_a_envoyer = f"{method}|{params['param_str']}|{message_chiffre}"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(message_a_envoyer.encode())
    print("Message chiffré envoyé au serveur.")
