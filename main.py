import datetime
from parse import parse
# # Demande à l'utilisateur la destination
# depart = str(input("Entrez le lieu de départ: "))
destination = str(input("Entrez le lieu d'arrivé: "))
nbreSemaine = int(input("Entrez le nombre de semaines à ajouter : "))
dateDepart = input("Entrez la date de départ (Format JJ/MM): ")

# Analyser les dates en objets datetime
dateDepart = datetime.datetime.strptime(dateDepart, "%d/%m")
dateArrive = dateDepart + datetime.timedelta(weeks=nbreSemaine)

# Convertir les dates en format de chaîne de caractères
dateDepart = dateDepart.strftime("%d/%m")
dateArrive = dateArrive.strftime("%d/%m")

parse(destination,dateDepart,dateArrive)