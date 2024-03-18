import json

import requests

titolo = input("Inserisci il titolo del libro: ")
codice_autore = input("Inserisci il codice dell'autore: ")
data = {"titolo": titolo, "codice_autore": int(codice_autore)}
url = "http://localhost:5000/inserisci_libro"
headers = {'Content-Type': 'application/json'}
response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.text)
