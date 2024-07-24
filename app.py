from flask import Flask, request, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from datetime import datetime
from helper import Item, convert_duration_to_hours, parse_time, get_time_slot, convert_escale,clean_price

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrap', methods=['POST'])
def scrap():
    depart = request.form['ville_depart']
    destination = request.form['ville_arrive']
    dateDepart = request.form['date_depart']
    dateDepart = datetime.strptime(dateDepart, '%Y-%m-%d').strftime("%d/%m")
    dateArrive = request.form['date_arrive']
    dateArrive = datetime.strptime(dateArrive, '%Y-%m-%d').strftime("%d/%m")

    classe = request.form['classe']

    # Appel de la fonction de scrapping
    items = scrap_price(depart, destination, classe, dateDepart, dateArrive)

    # Convertir les objets Item en dictionnaires
    items_list = [item.to_dict() for item in items]

    # Retourner les données JSON
    return jsonify(items_list)

def scrap_price(depart, destination, classe, dateDepart, dateArrive):
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.google.com/travel/flights?hl=fr")
        consent = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Tout accepter"]')))
        consent.click()

        classe_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[3]')))
        classe_element.click()
        if classe == '1':
            classeName = "Business"
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[3]/div/div/div/div[2]/ul/li[3]'))).click()
        else:
            classeName = "Economy"

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
            dateDepart = driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input').get_attribute('value') 
            dateArrive = driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[2]/div/input').get_attribute('value') 
            heureAller_element = price.find_element(By.CSS_SELECTOR, 'span[aria-label^="Heure de départ"] span[role="text"]')
            heureAller = heureAller_element.text if heureAller_element else None
            heureArrive_element = price.find_element(By.CSS_SELECTOR, 'span[aria-label^="Heure d\'arrivée"] span[role="text"]')
            heureArrive = heureArrive_element.text if heureArrive_element else None
            heureAller_decimal = parse_time(heureAller)
            heureArrive_decimal = parse_time(heureArrive)
            heureAller_slot = get_time_slot(heureAller_decimal)
            heureArrive_slot = get_time_slot(heureArrive_decimal)
            duree_str = price.find_element(By.CSS_SELECTOR, '.gvkrdb').text
            duree = convert_duration_to_hours(duree_str)
            escale = price.find_element(By.CSS_SELECTOR, 'div.BbR8Ec > div.EfT7Ae > span.ogfYpf').text
            escale = convert_escale(escale)
            compagnie = price.find_element(By.CSS_SELECTOR, 'div.sSHqwe.tPgKwe.ogfYpf > span').text
            prix = price.find_element(By.CSS_SELECTOR, 'div.U3gSDe').text.split('\n')[0]
            prix = clean_price(prix)
            item = Item(villeDepart=villeDepart, villeArrive=villeArrive, classe=classeName, nbreEscale=escale, prix=prix, duree=duree, departDate=dateDepart, retourDate=dateArrive, heureDepart=heureAller, heureDepartName=heureAller_slot, heureArrive=heureArrive, heureArriveName=heureArrive_slot, compagnie=compagnie)
            items.append(item)

        return items

    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
