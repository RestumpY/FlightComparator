import datetime
from parse import parse
# # Demande à l'utilisateur la destination
destination = str(input("Entrez la destination: "))
# # Demande à l'utilisateur le nombre de semaines à ajouter
nbreSemaine = int(input("Entrez le nombre de semaines à ajouter : "))

parse(destination,nbreSemaine)