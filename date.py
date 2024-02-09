from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import datetime

class DateWeeks:   
    def date_flight(self):
        # Demande à l'utilisateur le nombre de semaines à ajouter
        nombre_semaines = int(input("Entrez le nombre de semaines à ajouter : "))

        # Ajoute le nombre de semaines à la date actuelle
        date_actuelle = datetime.datetime.now()
        date_future = date_actuelle + datetime.timedelta(weeks=nombre_semaines)

        print("Date actuelle :", date_actuelle.strftime("%d/%m"))
        print("Date future :", date_future.strftime("%d/%m"))
        date_future.strftime("%d/%m")
        


dateweek= DateWeeks()
dateweek.date_flight()
