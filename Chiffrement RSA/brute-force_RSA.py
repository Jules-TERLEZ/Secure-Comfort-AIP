import time
import math
import psutil
import os

# Méthode naïve pour factoriser n
def naive_factorization(n):
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return i, n // i
    return None, None

# Choix de grands nombres premiers p et q
p = 100000007
q = 100000037
n = p * q

print("\n--- Lancement de l'attaque par Force Brute (RSA - Factorisation) ---")
print(f"Valeur de n à factoriser : {n}")

# --- DÉBUT DES MESURES ---
start_time = time.time()
cpu_start = time.process_time()

found_p, found_q = naive_factorization(n)

# --- FIN DES MESURES ---
end_time = time.time()
cpu_end = time.process_time()

temps_total = end_time - start_time
cpu_time = cpu_end - cpu_start

# --- CALCUL DES MÉTRIQUES ---

# Charge CPU
if temps_total > 0:
    cpu_load = (cpu_time / temps_total) * 100
else:
    cpu_load = 0

# Métriques Mémoire Système
mem_sys = psutil.virtual_memory()
mem_totale = mem_sys.total
mem_dispo = mem_sys.available

# Métriques Processus
process = psutil.Process(os.getpid())
mem_proc = process.memory_info().rss 

# Calcul des impacts mémoire
impact_dispo = (mem_proc / mem_dispo) * 100
impact_total = (mem_proc / mem_totale) * 100
reste_dispo = 100 - impact_dispo

# --- AFFICHAGE DES RÉSULTATS (Format identique à César) ---
print("\n" + "="*60)
print(f"ANALYSE DES PERFORMANCES DU BRUTE-FORCE RSA")
print("="*60)
print(f"Facteurs retrouvés        : p = {found_p}, q = {found_q}")
print(f"Temps total d'exécution   : {temps_total:.6f} secondes")
print(f"Temps CPU consommé        : {cpu_time:.9f} secondes")
print(f"Charge CPU du programme   : {cpu_load:.2f} %")
print("-" * 40)
print(f"Impact sur mémoire dispo  : {impact_dispo:.6f} %")
print(f"Impact sur mémoire totale : {impact_total:.6f} %")
print(f"Mémoire dispo restante    : {reste_dispo:.6f} %")
print("="*60 + "\n")