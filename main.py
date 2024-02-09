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



# #driver.get('nouvelleurl')
# bestPrice = WebDriverWait(driver, 5).until(
#     EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.Rk10dc')))

# bestPrice = WebDriverWait(bestPrice[0], 5).until(
#     EC.presence_of_all_elements_located((By.TAG_NAME, 'li')))
# for price in bestPrice:
#     print('-'*6)
#     horaires = bestPrice.find_elements(By.CSS_SELECTOR, 'span[jscontroller="cNtv4b"] > span')
#     heureAller = horaires[0].text
#     heureRetour = horaires[1].text
#     duree = bestPrice.find_element(By.CSS_SELECTOR, "div > div.yR1fYc > div > div.OgQvJf.nKlB3b > div.Ak5kof > div").text
#     compagnie = bestPrice.find_element(By.CSS_SELECTOR,'div > div.yR1fYc > div > div.OgQvJf.nKlB3b > div.Ir0Voe > div.sSHqwe.tPgKwe.ogfYpf > span:nth-child(1)")').text
#     prix = bestPrice.find(By.CSS_SELECTOR,'div > div.yR1fYc > div > div.OgQvJf.nKlB3b > div.U3gSDe > div.BVAVmf.I11szd.POX3ye > div.YMlIz.FpEdX.jLMuyc > span")').text

time.sleep(60)