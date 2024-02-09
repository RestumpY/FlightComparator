from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

driver.get('https://www.google.com/travel/flights?hl=fr')


consent = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Tout accepter"]')))
consent.click()

arrival = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i21"]/div[4]/div/div/div[1]/div/div/input')))
arrival.send_keys('Berlin')
# arrival.send_keys(Keys.ENTER)

first_result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.DFGgtd li:first-child')))
first_result.click()

time.sleep(60)