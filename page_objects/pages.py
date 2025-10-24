from .elements import DownloadFile, MainForm, RegisterEmployees


class MainPage:
    def __init__(self, driver):
        self.login_form = MainForm(driver)


class DashboardPage:
    def __init__(self, driver):
        self.download_button = DownloadFile(driver)
        self.register_employees = RegisterEmployees(driver)
