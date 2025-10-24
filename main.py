import os
import tempfile

from dotenv import load_dotenv
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from page_objects.pages import DashboardPage, MainPage
from send_email import send_email_gmail

load_dotenv(override=True)
username = os.getenv("APP_USERNAME")
password = os.getenv("APP_PASSWORD")
rementente = os.getenv("GMAIL_USERNAME")
senha = os.getenv("GMAIL_PASSWORD")

URL = "https://desafio-rpa-946177071851.us-central1.run.app"


def automate_client_registration(driver, download_dir):
    login_page = MainPage(driver=driver)
    dashboard_page = DashboardPage(driver=driver)
    login_page.login_form.login(username, password)
    dashboard_page.download_button.download_file(download_dir)
    dashboard_page.register_employees.set_employees(download_dir)
    login_page.login_form.logout()


def main():
    with tempfile.TemporaryDirectory(delete=False) as download_dir:
        options = Options()
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
            },
        )

        driver = Chrome(options=options)
        driver.maximize_window()

        driver.get(URL)

        try:
            send_email_gmail(
                rementente,
                "Inicio do processo",
                "O processo de automação de cadastro foi iniciado",
                rementente,
                senha,
            )
            automate_client_registration(driver, download_dir)
            send_email_gmail(
                rementente,
                "Fim do processo",
                "O processo de automação de cadastro foi finalizado com sucesso",
                rementente,
                senha,
            )
        except Exception as e:
            send_email_gmail(
                rementente,
                "Erro de execução",
                f"O processo de automação foi finalizado sem sucesso devido a um erro na execução: {e}",
                rementente,
                senha,
            )
        finally:
            driver.quit()


if __name__ == "__main__":
    main()
