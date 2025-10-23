import os
import tempfile

from dotenv import load_dotenv
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from page_objects.pages import DashboardPage, LoginPage

load_dotenv(override=True)
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

URL = "https://desafio-rpa-946177071851.us-central1.run.app"


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

        driver.get(URL)

        login_page = LoginPage(driver=driver)
        dashboard_page = DashboardPage(driver=driver)
        login_page.login_form.login(username, password)
        dashboard_page.download_button.download_file(download_dir)


if __name__ == "__main__":
    main()
