import time
import psutil
import os

import socket
from CryptoSym import cesar_dechiffre, vigenere_dechiffre, substitution_dechiffre

#HOST = '192.168.1.178'
HOST = '192.168.1.123'
PORT = 50007

def demander_parametres(method):
    if method == 'cesar':
        decalage = int(input("Décalage César : "))
        return {'decalage': decalage}
    elif method == 'vigenere':
        cle = input("Clé Vigenère : ")
        return {'cle': cle}
    elif method == 'substitution':
        alphabet_subst = input("Alphabet de substitution (26 lettres) : ")
        return {'alphabet_subst': alphabet_subst}
    else:
        return {}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Serveur en attente de connexion...")
    conn, addr = s.accept()
    with conn:
        print('Connecté par', addr)
        data = conn.recv(4096)
        if not data:
            print("Aucune donnée reçue.")
            exit()
        # Le client envoie : method|param|message_chiffre
        recu = data.decode().split('|', 2)
        if len(recu) != 3:
            print("Format de message incorrect.")
            exit()
        method, param, message_chiffre = recu
        print(f"Méthode : {method}")
        print(f"Message chiffré reçu : {message_chiffre}")

        # --- Vérification limite du message ---
        if len(message_chiffre) > 50000:
            print("⚠ Message trop long pour être déchiffré.")
            exit()

        # Demander le paramètre de déchiffrement
        params = demander_parametres(method)
        if method == 'cesar':
            message_dechiffre = cesar_dechiffre(message_chiffre, params['decalage'])
        elif method == 'vigenere':
            message_dechiffre = vigenere_dechiffre(message_chiffre, params['cle'])
        elif method == 'substitution':
            message_dechiffre = substitution_dechiffre(message_chiffre, params['alphabet_subst'])
        else:
            message_dechiffre = "Méthode inconnue."
        print("\n" + "="*120)
        print("Message déchiffré :", message_dechiffre)
        print("="*120)

        # --- Début mesure du temps (après saisie utilisateur) ---
        start_time = time.time()
        cpu_start = time.process_time()

        # --- Fin mesure du temps ---
        end_time = time.time()
        temps_dechiffrement = end_time - start_time
        cpu_end = time.process_time()
        cpu_time = cpu_end - cpu_start

        if temps_dechiffrement > 0:
            cpu_load = (cpu_time / temps_dechiffrement) * 100
        else:
            cpu_load = 0

        print(f"\nTemps de déchiffrement : {temps_dechiffrement:.6f} secondes")

         # --- Consommation ressources ---
        process = psutil.Process(os.getpid())
        mem = process.memory_info().rss / (1024*1024)

        print(f"Temps CPU consommé : {cpu_time:.9f} secondes | Charge CPU du programme : {cpu_load:.2f} %")

        def to_mo(octets):
            return octets / (1024 * 1024)

        mem_sys = psutil.virtual_memory()

        mem_totale = mem_sys.total
        mem_dispo = mem_sys.available

        process = psutil.Process(os.getpid())
        mem_proc = process.memory_info().rss
        part_disponible = ((mem_dispo - mem_proc) / mem_dispo) * 100

        impact_dispo = (mem_proc / mem_dispo) * 100
        impact_total = (mem_proc / mem_totale) * 100
        reste_dispo = 100 - impact_dispo

        print(f"Impact sur mémoire disponible : {impact_dispo:.6f} % | Impact sur mémoire totale : {impact_total:.6f} % | Mémoire dispo restante : {reste_dispo:.6f} %\n")
