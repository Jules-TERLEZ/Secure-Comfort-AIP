import socket
import time
import psutil
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# 1. Génération des clés de Bob
print("Génération des clés RSA en cours...")
key = RSA.generate(2048)
private_key = key
public_key = key.publickey().export_key()
cipher = PKCS1_OAEP.new(private_key)

# 2. Configuration du réseau
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 12345)) 
server.listen(1)

print("Serveur prêt. En attente de connexion...")

try:
    conn, addr = server.accept()
    print(f"Connecté par {addr}")

    # 3. Envoi de la clé publique
    conn.send(public_key)
    print("Clé publique envoyée au client.")

    # 4. Boucle de réception des messages
    while True:
        try:
            encrypted_msg = conn.recv(256) 
            
            if not encrypted_msg:
                print("\nLe client a fermé la connexion.")
                break

            # --- DÉBUT MESURE DU TEMPS ET CPU ---
            start_time = time.time()
            cpu_start = time.process_time()

            # 5. Déchiffrement RSA
            message = cipher.decrypt(encrypted_msg)
            message_final = message.decode('utf-8')

            # --- FIN MESURE DU TEMPS ET CPU ---
            end_time = time.time()
            cpu_end = time.process_time()
            
            temps_dechiffrement = end_time - start_time
            cpu_time = cpu_end - cpu_start

            # Affichage du message avec le visuel demandé
            print("\n" + "="*120)
            print("Message déchiffré :", message_final)
            print("="*120)

            # --- CALCULS ET AFFICHAGE RESSOURCES ---
            if temps_dechiffrement > 0:
                cpu_load = (cpu_time / temps_dechiffrement) * 100
            else:
                cpu_load = 0

            print(f"\nTemps de déchiffrement : {temps_dechiffrement:.6f} secondes")
            
            process = psutil.Process(os.getpid())
            mem_proc = process.memory_info().rss
            
            mem_sys = psutil.virtual_memory()
            mem_totale = mem_sys.total
            mem_dispo = mem_sys.available

            impact_dispo = (mem_proc / mem_dispo) * 100
            impact_total = (mem_proc / mem_totale) * 100
            reste_dispo = 100 - impact_dispo

            print(f"Temps CPU consommé : {cpu_time:.9f} secondes | Charge CPU du programme : {cpu_load:.2f} %")
            print(f"Impact sur mémoire disponible : {impact_dispo:.6f} % | Impact sur mémoire totale : {impact_total:.6f} % | Mémoire dispo restante : {reste_dispo:.6f} %\n")
            
        except Exception as e:
            print(f"Erreur lors du traitement : {e}")
            break

finally:
    print("Fermeture du serveur.")
    conn.close()
    server.close()