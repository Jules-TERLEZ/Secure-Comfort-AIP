import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# 1. Connexion au serveur (vérifie bien l'IP de ta Pi)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(('192.168.1.87', 12345)) 
    print("Connecté au serveur.")
except Exception as e:
    print(f"Erreur de connexion : {e}")
    exit()

# 2. Réception de la clé publique de Bob
bob_public_key_data = client.recv(2048)
bob_public_key = RSA.import_key(bob_public_key_data)
print("Clé publique de Bob reçue.\n")

# Initialisation du module de chiffrement
cipher = PKCS1_OAEP.new(bob_public_key)

# 3. Saisie utilisateur et envoi
while True:
    # On demande à l'utilisateur de saisir son message
    phrase = input("Saisissez le message à chiffrer (ou 'exit' pour quitter) : ")
    
    if phrase.lower() == 'exit':
        break

    # Conversion de la chaîne en octets (UTF-8)
    message_a_chiffrer = phrase.encode('utf-8')

    try:
        # 4. Chiffrement
        encrypted_msg = cipher.encrypt(message_a_chiffrer)

        # 5. Envoi au serveur
        client.send(encrypted_msg)
        print("-> Message chiffré envoyé avec succès.\n")
    except ValueError:
        print("Erreur : Le message est trop long pour la taille de la clé RSA !")

print("Fermeture de la connexion.")
client.close()