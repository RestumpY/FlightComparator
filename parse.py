import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from item import Item
import time

def parse(destination, nbreSemaine):
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/travel/flights?hl=fr")

    # # Ajoute le nombre de semaines à la date actuelle
    date1 = datetime.datetime.now()
    date2 = date1 + datetime.timedelta(weeks=nbreSemaine)
    date_depart = date1.strftime("%d/%m")
    date_arrivee = date2.strftime("%d/%m")

    consent = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Tout accepter"]')))
    consent.click()

    arrival = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i21"]/div[4]/div/div/div[1]/div/div/input')))
    arrival.send_keys(destination)
    first_result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.DFGgtd li:first-child')))
    first_result.click()

    time.sleep(2)

    select_date_depart = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[jscontroller="OKD1oe"] > input[aria-label="Départ"]')))
    select_date_depart.send_keys(date_depart)

    select_date_arrivee = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[jscontroller="OKD1oe"] > input[aria-label="Retour"]')))
    select_date_arrivee.send_keys(date_arrivee)
    select_date_arrivee.send_keys(Keys.ENTER)

    time.sleep(2)
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
        dateDepart= driver.find_element(By.CSS_SELECTOR, 'div.cQnuXe.k0gFV > div > div > div:nth-child(1) > div > div.oSuIZ.YICvqf.kStSsc.ieVaIb input').get_attribute('value') 
        dateArrive = driver.find_element(By.CSS_SELECTOR, 'div.cQnuXe.k0gFV > div > div > div:nth-child(1) > div > div.oSuIZ.YICvqf.lJODHb.qXDC9e input').get_attribute('value') 

        horaires = price.find_elements(By.CSS_SELECTOR, 'span[jscontroller="cNtv4b"] > span')
        heureAller = horaires[0].text
        heureArrive = horaires[1].text
        duree = price.find_element(By.CSS_SELECTOR, 'div.OgQvJf.nKlB3b > div.Ak5kof > div').text
        compagnie = price.find_element(By.CSS_SELECTOR,'div.OgQvJf.nKlB3b > div.Ir0Voe > div.sSHqwe.tPgKwe.ogfYpf > span:nth-child(1)').text
        prix = price.find_element(By.CSS_SELECTOR,'div.U3gSDe span').text
        
        item = Item(villeDepart=villeDepart, villeArrive=villeArrive, prix=prix, duree=duree, departDate=dateDepart, retourDate=dateArrive, heureDepart=heureAller, heureArrive=heureArrive, compagnie=compagnie)
        items.append(item)

    for item in items:
        print("Ville de départ:", item.villeDepart)
        print("Heure de départ:", item.heureDepart)
        print("Date de départ:", item.departDate)
        print("Ville d'arrivée:", item.villeArrive)
        print("Heure d'arrivé:", item.heureArrive)
        print("Prix:", item.prix)
        print("Durée:", item.duree)
        print("Compagnie:", item.compagnie)
        print("Date de retour:", item.retourDate)

        print('--'*6)
    return items
