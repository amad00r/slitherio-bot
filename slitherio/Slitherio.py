from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


class Slitherio:
    def __init__(self, maximize=False, headless=False):
        if headless:
            options = Options()
            options.add_argument('--headless')
        else:
            options = None

        self.driver = webdriver.Firefox(options=options, service=Service(Path('slitherio/driver/geckodriver.exe').resolve()))

        if maximize:
            self.driver.maximize_window()

        self.driver.get('http://slither.io/')

        self.score = 10

    def new_game(self, username):
        self.score = 10
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'nick')))
        self.driver.find_element(By.ID, 'nick').clear()
        self.driver.find_element(By.ID, 'nick').send_keys(username)
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div/div/div[3]').click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[15]/canvas')))
        sleep(1)

    def running(self):
        return self.driver.find_element(By.XPATH, '/html/body/div[15]/canvas').is_displayed()

    def update(self):
        try:
            self.score = int(self.driver.find_element(By.XPATH, '/html/body/div[13]/span[1]/span[2]').text)
        except:
            pass

    def close(self):
        self.driver.quit()