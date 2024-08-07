import datetime
from parse import parse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
# Inputs user
depart = str(input("Entrez le lieu de départ: "))
destination = str(input("Entrez le lieu d'arrivée: "))
classe_input = str(input("Entrez la classe de vol (True pour la classe affaire, False pour la classe économique): "))
nbreSemaine = int(input("Entrez le nombre de semaines à ajouter : "))
dateDepart = input("Entrez la date de départ (Format JJ/MM): ")

# Convertir l'entrée de classe en booléen
classe = classe_input.lower() == 'true'

# Analyser les dates en objets datetime
dateDepart = datetime.datetime.strptime(dateDepart, "%d/%m")
dateArrive = dateDepart + datetime.timedelta(weeks=nbreSemaine)

datesDeparts = []
datesArrives = []
departs = []
classes = []
destinations = []

# Récupérer la valeur de la variable d'environnement
nbre_iterations = int(os.getenv("NBRE_ITERATIONS"))
maxWorkers = int(os.getenv("MAX_WORKERS"))

# Initialiser la liste de dates
for i in range(nbre_iterations):
    departs.append(depart)
    destinations.append(destination)
    classes.append(classe)
    datesDeparts.append(dateDepart + datetime.timedelta(days=i))
    datesArrives.append(dateArrive + datetime.timedelta(days=i))

def parse_date(depart, destination, classe, dateDepart, dateArrive):
    return parse(depart, destination, classe, dateDepart, dateArrive)

with ThreadPoolExecutor(max_workers=maxWorkers) as executor:
    results = executor.map(parse_date, departs, destinations, classes, datesDeparts, datesArrives)
    
# Liste pour stocker tous les items
all_items = []

for result in results:
    # Traitez le résultat de parsing ici
    all_items.extend(result)

with open('items.json', 'w', encoding='utf-8') as json_file:
    json.dump([item.__dict__ for item in all_items], json_file, ensure_ascii=False, indent=4)

print("Les données ont été enregistrées dans le fichier 'items.json'")
