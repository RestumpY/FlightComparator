from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from item import Item
import time
import json
from datetime import datetime

# Fonction pour convertir la durée en heures décimales
def convert_duration_to_hours(duration_str):
    parts = duration_str.split()
    hours = 0
    minutes = 0
    for i, part in enumerate(parts):
        if 'h' in part:
            # Gestion des espaces autour de 'h'
            hours_str = part.replace('h', '').strip()
            if hours_str:
                hours = int(hours_str)
            else:
                # Gestion des cas où 'h' est séparé du nombre par un espace
                hours = int(parts[i - 1])
        if 'min' in part:
            # Gestion des espaces autour de 'min'
            minutes_str = part.replace('min', '').strip()
            if minutes_str:
                minutes = int(minutes_str)
            else:
                # Gestion des cas où 'min' est séparé du nombre par un espace
                minutes = int(parts[i - 1])
    return hours + minutes / 60

# Fonction pour parser les données
def parse(depart, destination, classe, dateDepart, dateArrive):
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.google.com/travel/flights?hl=fr")
        
        # Convertir les dates en format de chaîne de caractères
        dateDepart = dateDepart.strftime("%d/%m")
        dateArrive = dateArrive.strftime("%d/%m")
        consent = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Tout accepter"]')))
        consent.click()

        # Gestion de la classe de vol
        classe_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[3]')))
        classe_element.click()
        print(classe)
        if classe == 1:
            classeName = "Affaires"
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[3]/div/div/div/div[2]/ul/li[3]'))).click()
        else:
            classeName = "Economique"

        departure = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input')))
        departure.clear()
        departure.send_keys(depart)
        first_result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.DFGgtd li:first-child')))
        first_result.click()
        time.sleep(1)

        arrival = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[4]/div/div/div[1]/div/div/input')))
        arrival.send_keys(destination)
        first_result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.DFGgtd li:first-child')))
        first_result.click()
        time.sleep(1)

        select_date_depart = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[jscontroller="OKD1oe"] > input[aria-label="Départ"]')))
        select_date_depart.send_keys(dateDepart)
        select_date_arrivee = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[jscontroller="OKD1oe"] > input[aria-label="Retour"]')))
        select_date_arrivee.send_keys(dateArrive)
        select_date_arrivee.send_keys(Keys.ENTER)
        time.sleep(1)

        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc.nCP5yc.AjY5Oe.LQeN7.TUT4y.zlyfOd'))) 
        button.click()

        bestPrice = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.Rk10dc')))
        bestPrice = WebDriverWait(bestPrice[0], 5).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'li')))

        items = []

        for price in bestPrice:
            villeDepart = driver.find_element(By.CSS_SELECTOR, 'div.e5F5td.BGeFcf div.cQnuXe.k0gFV > div > div > input').get_attribute('value')
            villeArrive = driver.find_element(By.CSS_SELECTOR, 'div.e5F5td.vxNK6d div.cQnuXe.k0gFV > div > div > input').get_attribute('value')
            dateDepart= driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input').get_attribute('value') 
            dateArrive = driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[2]/div/input').get_attribute('value') 
            heureAller_element = price.find_element(By.CSS_SELECTOR, 'span[aria-label^="Heure de départ"] span[role="text"]')
            heureAller = heureAller_element.text if heureAller_element else None
            heureArrive_element = price.find_element(By.CSS_SELECTOR, 'span[aria-label^="Heure d\'arrivée"] span[role="text"]')
            heureArrive = heureArrive_element.text if heureArrive_element else None
            duree_str = price.find_element(By.CSS_SELECTOR, '.gvkrdb').text
            duree = convert_duration_to_hours(duree_str)  # Utilisation de la fonction de conversion
            compagnie = price.find_element(By.CSS_SELECTOR, 'div.sSHqwe.tPgKwe.ogfYpf > span').text
            prix = price.find_element(By.CSS_SELECTOR, 'div.U3gSDe').text.split('\n')[0]

            item = Item(villeDepart=villeDepart, villeArrive=villeArrive, classe=classeName, prix=prix, duree=duree, departDate=dateDepart, retourDate=dateArrive, heureDepart=heureAller, heureArrive=heureArrive, compagnie=compagnie)
            items.append(item)
       
        return items

    finally:
        driver.quit()
