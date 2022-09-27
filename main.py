from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import time

load_dotenv('.env')
mobile = os.environ.get("mobile")
password = os.environ.get("Password")

class Walcart():

    def setUp(self):
        ###old chromedriver path
        #self.driver = webdriver.Chrome("U:\chromedriver.exe")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        ### for a specific window size
        #self.driver.set_window_position(0, 0)
        #self.driver.set_window_size(1920, 1080)
        self.driver.get("https://www.walcart.com/")

    def test_login(self):
        self.driver.find_element(By.CLASS_NAME, "authorization-link").click()
        self.driver.find_element(By.ID, "mobile").send_keys(mobile)
        self.driver.find_element(By.CLASS_NAME, "actions-toolbar").click()
        self.driver.implicitly_wait(2)
        self.driver.find_element(By.ID, "pass").send_keys(password)
        self.driver.find_element(By.CLASS_NAME, "mobile-login-code-button").click()
        welcomeText = self.driver.find_element(By.CLASS_NAME, "acc-btn").text
        ### Verify if the log in was successful
        assert "Hi," == welcomeText

    def test_order(self):
        time.sleep(5)
        self.driver.find_element(By.CLASS_NAME, "input-text").send_keys('Nescafe - 3 in 1')
        self.driver.implicitly_wait(8)
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Nescafe - 3 in 1").click()
        self.driver.find_element(By.CLASS_NAME, "increase").click()
        self.driver.find_element(By.CLASS_NAME, "tocart").click()
        self.driver.find_element(By.CLASS_NAME, "checkout").click()
        element = self.driver.find_element(By.CLASS_NAME, "continue")
        self.driver.execute_script("arguments[0].click();", element)
        element2 = self.driver.find_element(By.XPATH, ".//input[@type='radio' and @value='cashondelivery']")
        self.driver.execute_script("arguments[0].click();", element2)
        ### verify if the checkout button is clickable
        assert self.driver.find_element(By.CLASS_NAME, "checkout").is_displayed()

    def test_logout(self):
        self.driver.find_element(By.CLASS_NAME, "acc-btn").click()
        self.driver.find_element(By.CLASS_NAME, "mbi-exit").click()
        self.driver.implicitly_wait(4)
        loginText = self.driver.find_element(By.CLASS_NAME, "phoneview-user").text
        ### Verify if the log out was successful
        assert "Log In" == loginText

    def shutdown(self):
        self.driver.close()


x = Walcart()
x.setUp()
x.test_login()
x.test_logout()
x.test_order()
x.shutdown()
