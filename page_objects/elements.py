from pathlib import Path

import pandas as pd
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from log import logger
from utils import hover_to_element, normalize_text, wait_download


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
        button_logout = self.wait_element((By.XPATH, "/html/body/nav/div/div/a"))
        hover_to_element(self.driver, button_logout).click()
        logger.info("Logout realizado com sucesso")

    def validate_login(self, username, password):
        try:
            login_message_alert = self.wait_element(
                (By.CLASS_NAME, "alert"), time=60
            ).text.lower()
            logger.info("Identificando mensagem de retorno do site")
            if "sucesso" in login_message_alert:
                logger.info(f"Mensagem do site {login_message_alert}")
                return True
            elif "incorretos" in login_message_alert:
                logger.info(f"Mensagem do site: {login_message_alert}")
                raise LoginCredentialsError(
                    f"error login with the following message: {login_message_alert}"
                )
        except TimeoutException:
            logger.info("Atualizando navegador")
            self.driver.refresh()
            self.validate_login(username, password)


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
        try:
            wait_download(download_dir, timeout=10)
        except TimeoutError:
            self.driver.back()
            self.download_file(download_dir)
        logger.info("Download realizado com sucesso")


class RegisterEmployees:
    def __init__(self, driver):
        self.driver = driver

    def change_frame(self):
        iframe = self.wait_element((By.ID, "registerIframe"))
        self.driver.switch_to.frame(iframe)

    def wait_element(self, element, time=10, condition=EC.presence_of_element_located):
        return WebDriverWait(self.driver, time).until(condition(element))

    def set_employees(self, download_dir):
        folder = Path(download_dir)
        xlsx_file = list(folder.glob("*.xlsx"))
        if not xlsx_file:
            logger.error("Download do arquivo não realizado")
            raise XlsxFileDoesNotExists("xlsx file not found")
        self.access_registration_page()
        self.change_frame()
        df = pd.read_excel(xlsx_file[0])
        print(df)
        for value in df.to_dict("records"):
            self.fill_out(value)

    def access_registration_page(self):
        logger.info("Acessando página de cadastro")
        self.wait_element(
            (By.XPATH, "/html/body/div/div/div[4]/div[2]/div/div/a")
        ).click()

    def validate_registration_page(self):
        registration_page_header = self.wait_element(
            (By.XPATH, "/html/body/div/div/div[1]/div/div/div/div/div[1]/h1")
        ).text.lower()
        if "cadastro" in registration_page_header:
            return True
        else:
            raise RegistrationPageDoesNotExists("registration page does not found")

    def fill_out(self, value):
        logger.info("Iniciando o cadastro de funcionários")
        for k, v in value.items():
            print(f"{k}:{v}")
            elements = self.wait_element(
                (By.TAG_NAME, "label"), condition=EC.presence_of_all_elements_located
            )
            element = [
                element for element in elements if normalize_text(element.text) == k
            ][0]
            id_input = element.get_attribute("for")
            input_element = self.driver.find_element(By.ID, id_input)
            input_element.clear()
            input_element.send_keys(v)
        try:
            button_submit = self.wait_element(
                (By.XPATH, "//button[@type = 'submit']"), time=4
            )
            hover_to_element(self.driver, button_submit).click()
            alert = self.wait_element((By.CLASS_NAME, "alert")).text
            if "sucesso" not in alert.lower():
                logger.error(f"não foi possível realizar o cadastro: {alert}")
                return
            btn_close = self.wait_element((By.CLASS_NAME, "btn-close"))
            hover_to_element(self.driver, btn_close).click()
            logger.info("Funcionário registrado com sucesso")
        except Exception as e:
            logger.error(f"Erro na página de cadastro: {e}")
            self.driver.refresh()
            self.change_frame()
            self.fill_out(value)
