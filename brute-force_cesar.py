import time
import psutil
import os

def cesar_brute_force(message_chiffre):
    print("\n--- Lancement de l'attaque par Force Brute (César) ---")
    
    # --- DÉBUT DES MESURES ---
    start_time = time.time()
    cpu_start = time.process_time()
    
    # On teste les 26 décalages possibles
    for decalage_test in range(1, 27):
        tentative = ""
        for char in message_chiffre:
            if char.isalpha():
                decalage_base = ord('A') if char.isupper() else ord('a')
                # Algorithme de décalage inverse
                tentative += chr((ord(char) - decalage_base - decalage_test) % 26 + decalage_base)
            else:
                tentative += char
        
        # Affichage des essais pour simuler l'activité de l'attaque
        #print(f"Clé {decalage_test:02d} : {tentative[:60]}...") 

    # --- FIN DES MESURES ---
    end_time = time.time()
    cpu_end = time.process_time()
    
    temps_total = end_time - start_time
    cpu_time = cpu_end - cpu_start
    
    return temps_total, cpu_time

# --- Saisie utilisateur ---
msg_utilisateur = input("Entrez la chaîne de caractères à briser : ")

if not msg_utilisateur:
    print("Erreur : Message vide.")
else:
    # Exécution de la fonction
    temps_total, cpu_time = cesar_brute_force(msg_utilisateur)

    # --- Calcul de la Charge CPU ---
    if temps_total > 0:
        cpu_load = (cpu_time / temps_total) * 100
    else:
        cpu_load = 0

    # --- Métriques Mémoire Système ---
    mem_sys = psutil.virtual_memory()
    mem_totale = mem_sys.total
    mem_dispo = mem_sys.available

    # --- Métriques Processus (ce script) ---
    process = psutil.Process(os.getpid())
    mem_proc = process.memory_info().rss  # Mémoire utilisée par le processus
    
    # Calcul des impacts mémoire
    impact_dispo = (mem_proc / mem_dispo) * 100
    impact_total = (mem_proc / mem_totale) * 100
    reste_dispo = 100 - impact_dispo

    # --- AFFICHAGE DES RÉSULTATS ---
    print("\n" + "="*80)
    print(f"ANALYSE DES PERFORMANCES DU BRUTE-FORCE CÉSAR")
    print("="*80)
    print(f"Temps total d'exécution   : {temps_total:.6f} secondes")
    print(f"Temps CPU consommé         : {cpu_time:.9f} secondes")
    print(f"Charge CPU du programme    : {cpu_load:.2f} %")
    print("-" * 40)
    print(f"Impact sur mémoire dispo   : {impact_dispo:.6f} %")
    print(f"Impact sur mémoire totale  : {impact_total:.6f} %")
    print(f"Mémoire dispo restante     : {reste_dispo:.6f} %")
    print("="*80 + "\n")