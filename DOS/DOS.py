import requests
import threading

URL = "http://localhost:5000/"
NUM_THREADS = 500  # Nombre de requêtes simultanées
i=0

def send_request():
    global i
    try:
        response = requests.get(URL)
        i+=1
        print(str(i)+f" Réponse: {response.status_code}")
    except Exception as e:
        i+=1
        print(str(i)+" Erreur")

threads = []

for _ in range(NUM_THREADS):
    thread = threading.Thread(target=send_request)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
