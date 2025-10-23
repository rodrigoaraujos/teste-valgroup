from .elements import DownloadFile, LoginForm


class LoginPage:
    def __init__(self, driver):
        self.login_form = LoginForm(driver)


class DashboardPage:
    def __init__(self, driver):
        self.download_button = DownloadFile(driver)
