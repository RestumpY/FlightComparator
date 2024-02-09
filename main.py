import datetime
from parse import parse
from concurrent.futures import ThreadPoolExecutor

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

# Initialiser la liste de dates
for i in range(10):
    datesDeparts.append(dateDepart + datetime.timedelta(days=i))
    datesArrives.append(dateArrive + datetime.timedelta(days=i))

def parse_date(destination, dateDepart, dateArrive):
    return parse(destination, dateDepart, dateArrive)

with ThreadPoolExecutor() as executor:
    results = executor.map(parse_date, [destination]*10, datesDeparts, datesArrives)

for result in results:
    # Traitez le résultat de parsing ici
    print(result)
