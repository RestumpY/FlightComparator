from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import datetime

driver = webdriver.Chrome()
driver.get('https://www.google.com/travel/flights?hl=fr')

# Demande à l'utilisateur la destination
destination = str(input("Entrez la destination: "))

# Demande à l'utilisateur le nombre de semaines à ajouter
nombre_semaines = int(input("Entrez le nombre de semaines à ajouter : "))

# Ajoute le nombre de semaines à la date actuelle
date1 = datetime.datetime.now()
date2 = date1 + datetime.timedelta(weeks=nombre_semaines)
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

# button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc nCP5yc AjY5Oe LQeN7 TUT4y zlyfOd"]'))) 
# button.click()


# element = driver.find_element(By.CSS_SELECTOR, '#yDmH0d > c-wiz.zQTmif.SSPGKf > div > div:nth-child(2) > c-wiz > div.cKvRXe > c-wiz > div.vg4Z0e > div:nth-child(1) > div.SS6Dqf.POQx1c > div.AJxgH > div > div.rIZzse > div.bgJkKe.K0Tsu > div > div > div.cQnuXe.k0gFV > div > div > div:nth-child(1) > div > div.oSuIZ.YICvqf.kStSsc.ieVaIb > div > div.Z4JKhb.CKPWLe.HDVC8.Xbfhhd > button > span.VfPpkd-kBDsod > svg') 
# print(dateweek.date_flight)
# for i in range(10):
#     element.click()

time.sleep(60)