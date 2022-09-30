from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import time

load_dotenv('.env')
mobile = os.environ.get("mobile")
password = os.environ.get("Password")

class Walcart():

    def setUp(self):
        ### old chromedriver path
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

        ### Verify if the login is ok
        welcomeText = self.driver.find_element(By.CLASS_NAME, "acc-btn").text
        assert "Hi," == welcomeText

    def category_selection(self):
        self.driver.find_element(By.CLASS_NAME, "d-md-block").click()
        self.driver.find_element(By.CLASS_NAME, "level0 nav-5 level-top mega_left parent").click()

        element = self.driver.find_element(By.CLASS_NAME, "magebig-nav")
        self.driver.execute_script("arguments[0].click();", element)

    def test_order(self):
        time.sleep(5)
        self.driver.find_element(By.CLASS_NAME, "input-text").send_keys('Nescafe - 3 in 1')
        self.driver.implicitly_wait(5)
        try:
            self.driver.find_element(By.PARTIAL_LINK_TEXT, "Nescafe - 3 in 1").click()
        except NoSuchElementException:
            print("Product not found")

        ### increase quantity
        self.driver.find_element(By.CLASS_NAME, "increase").click()
        self.driver.find_element(By.ID, "qty").clear()
        self.driver.find_element(By.ID, "qty").send_keys("5")
        self.driver.find_element(By.CLASS_NAME, "tocart").click()

        ### verify if the quantity is allowed, if not then reset the quantity to 1
        errMsg = self.driver.find_element(By.ID, "qty-error").text
        if errMsg == "The maximum you may purchase is 2.":
            self.driver.find_element(By.ID, "qty").clear()
            self.driver.find_element(By.ID, "qty").send_keys("1")
            self.driver.find_element(By.CLASS_NAME, "tocart").click()
        else:
            self.driver.find_element(By.CLASS_NAME, "checkout").click()

        self.driver.find_element(By.CLASS_NAME, "checkout").click()
        ### check if the user is logged in
        element = self.driver.find_element(By.CLASS_NAME, "continue")
        self.driver.execute_script("arguments[0].click();", element)
        element2 = self.driver.find_element(By.XPATH, ".//input[@type='radio' and @value='cashondelivery']")
        self.driver.execute_script("arguments[0].click();", element2)

        ### If the button is clickable then it assumed that the order can be placed
        assert self.driver.find_element(By.CLASS_NAME, "checkout").is_displayed()

        ### or just click the button for actual order, replace the above line with this
        #self.driver.find_element(By.CLASS_NAME, "checkout").click()

    def test_logout(self):
        self.driver.find_element(By.CLASS_NAME, "acc-btn").click()
        self.driver.find_element(By.CLASS_NAME, "mbi-exit").click()
        self.driver.implicitly_wait(4)
        loginText = self.driver.find_element(By.CLASS_NAME, "phoneview-user").text

        ### Verify if logout is successful
        assert "Log In" == loginText

    def shutdown(self):
        self.driver.close()


x = Walcart()
x.setUp()
x.test_login()
#x.category_selection()
x.test_order()
x.test_logout()
x.shutdown()
