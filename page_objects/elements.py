from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

from utils import wait_download, normalize_text
from log import logger
from pathlib import Path

import pandas as pd


class LoginCredentialsError(Exception):
    pass


class LoginExceededAttempts(Exception):
    pass

class XlsxFileDoesNotExists(Exception):
    pass

class RegistrationPageDoesNotExists(Exception):
    pass


class MainForm:
    def __init__(self, driver):
        self.driver = driver
        self.count = 0

    def wait_element(self, element, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(element)
        )

    def login(self, username, password):
        logger.info("Realizando login")
        self.wait_element((By.ID, "username")).send_keys(username)
        self.wait_element((By.ID, "password")).send_keys(password)
        self.wait_element((By.ID, "loginBtn")).click()
        self.validate_login(username, password)
        logger.info("Login realizado com sucesso")

    def logout(self):
        logger.info("Realizando logout")
        self.driver.switch_to.default_content()
        button_logout = self.wait_element((By.XPATH, '/html/body/nav/div/div/a'))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button_logout)
        actions = ActionChains(self.driver)
        actions.move_to_element(button_logout).perform()
        button_logout.click()
        logger.info("Logout realizado com sucesso")

    def validate_login(self, username, password):
        try:
            login_message_alert = self.wait_element(
                (By.CLASS_NAME, "alert"), time=60
            ).text.lower()
        except TimeoutException:
            self.driver.refresh()
            if self.count == 5:
                raise LoginExceededAttempts(f"login failed after {self.count} attempts")
            self.login(username, password)
            self.count += 1
        if "sucesso" in login_message_alert:
            return True
        elif "incorretos" in login_message_alert:
            raise LoginCredentialsError(
                f"error login with the following message: {login_message_alert}"
            )            


class DownloadFile:
    def __init__(self, driver):
        self.driver = driver

    def wait_element(self, element, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(element)
        )

    def download_file(self, download_dir):
        logger.info("Realizando download do arquivo")
        self.wait_element(
            (By.XPATH, "/html/body/div/div/div[4]/div[1]/div/div/a")
        ).click()
        wait_download(download_dir)
        logger.info("Download realizado com sucesso")



class RegisterEmployees:
    def __init__(self, driver):
        self.driver = driver

    def change_frame(self):
        iframe = self.wait_element((By.ID, 'registerIframe'))
        self.driver.switch_to.frame(iframe)

    def wait_element(self, element, time=10, condition=EC.presence_of_element_located):
        return WebDriverWait(self.driver, time).until(
            condition(element)
        )
    
    def set_employees(self, download_dir):
        folder = Path(download_dir)
        xlsx_file = list(folder.glob('*.xlsx'))
        if not xlsx_file:
            logger.error("Download do arquivo não realizado")
            raise XlsxFileDoesNotExists("xlsx file not found")
        self.access_registration_page()
        self.change_frame()
        df = pd.read_excel(xlsx_file[0])
        for value in df.to_dict("records"):
            self.fill_out(value)
    
    def access_registration_page(self):
        logger.info("Acessando página de cadastro")
        self.wait_element(
            (By.XPATH, "/html/body/div/div/div[4]/div[2]/div/div/a")
        ).click()

    def validate_registration_page(self):
        registration_page_header = self.wait_element((By.XPATH, "/html/body/div/div/div[1]/div/div/div/div/div[1]/h1")).text.lower()
        if "cadastro" in registration_page_header:
            return True
        else:
            raise RegistrationPageDoesNotExists(
                f"registration page does not found"
            )

    def fill_out(self, value):
        logger.info("Iniciando o cadastro de funcionários")
        for k, v in value.items():
            print(f'{k}:{v}')
            elements = self.wait_element((By.TAG_NAME,'label'), condition=EC.presence_of_all_elements_located)
            element = [element for element in elements if normalize_text(element.text) == k][0]
            id_input = element.get_attribute('for')
            input_element = self.driver.find_element(By.ID, id_input)
            input_element.clear()
            input_element.send_keys(v)
        try:
            button_submit = self.wait_element((By.XPATH, "//button[@type = 'submit']"), time=4)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button_submit)
            actions = ActionChains(self.driver)
            actions.move_to_element(button_submit).perform()
            button_submit.click()
            self.wait_element((By.CLASS_NAME, "alert"))
            logger.info("Funcionário registrado com sucesso")
        except:
            logger.error("Erro na página de cadastro")
            self.driver.refresh()
            self.change_frame()
            self.fill_out(value)
