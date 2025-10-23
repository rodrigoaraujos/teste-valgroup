from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import wait_download


class LoginCredentialsError(Exception):
    pass


class LoginExceededAttempts(Exception):
    pass


class LoginForm:
    def __init__(self, driver):
        self.driver = driver
        self.count = 0

    def wait_element(self, element, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(element)
        )

    def login(self, username, password):
        self.wait_element((By.ID, "username")).send_keys(username)
        self.wait_element((By.ID, "password")).send_keys(password)
        self.wait_element((By.ID, "loginBtn")).click()
        self.validate_login(username, password)

    def validate_login(self, username, password):
        login_message_alert = self.wait_element(
            (By.CLASS_NAME, "alert"), time=60
        ).text.lower()
        if "sucesso" in login_message_alert:
            return True
        elif "incorretos" in login_message_alert:
            raise LoginCredentialsError(
                f"error login with the following message: {login_message_alert}"
            )
        else:
            self.driver.refresh()
            if self.count == 5:
                raise LoginExceededAttempts(f"login failed after {self.count} attempts")
            self.login(username, password)
            self.count += 1


class DownloadFile:
    def __init__(self, driver):
        self.driver = driver

    def wait_element(self, element, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(element)
        )

    def download_file(self, download_dir):
        self.wait_element(
            (By.XPATH, "/html/body/div/div/div[4]/div[1]/div/div/a")
        ).click()
        wait_download(download_dir)


class RegisterEmployees:
    def __init__(self, driver):
        self.driver = driver
