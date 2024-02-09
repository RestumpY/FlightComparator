import datetime
from parse import parse
from concurrent.futures import ThreadPoolExecutor
import json

# # Demande à l'utilisateur la destination
# depart = str(input("Entrez le lieu de départ: "))
destination = str(input("Entrez le lieu d'arrivé: "))
nbreSemaine = int(input("Entrez le nombre de semaines à ajouter : "))
dateDepart = input("Entrez la date de départ (Format JJ/MM): ")

# Analyser les dates en objets datetime
dateDepart = datetime.datetime.strptime(dateDepart, "%d/%m")
dateArrive = dateDepart + datetime.timedelta(weeks=nbreSemaine)

datesDeparts = []
datesArrives = []
destinations = []

# Initialiser la liste de dates
for i in range(10):
    destinations.append(destination)
    datesDeparts.append(dateDepart + datetime.timedelta(days=i))
    datesArrives.append(dateArrive + datetime.timedelta(days=i))

def parse_date(destination, dateDepart, dateArrive):
    return parse(destination, dateDepart, dateArrive)

with ThreadPoolExecutor() as executor:
    results = executor.map(parse_date, destinations, datesDeparts, datesArrives)
    
# Liste pour stocker tous les items
all_items = []

for result in results:
    # Traitez le résultat de parsing ici
    all_items.extend(result)

with open('items.json', 'w', encoding='utf-8') as json_file:
    json.dump([item.__dict__ for item in all_items], json_file, ensure_ascii=False, indent=4)

print("Les données ont été enregistrées dans le fichier 'items.json'")