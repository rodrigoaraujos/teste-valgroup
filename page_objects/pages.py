from .elements import DownloadFile, RegisterEmployees, MainForm


class MainPage:
    def __init__(self, driver):
        self.login_form = MainForm(driver)


class DashboardPage:
    def __init__(self, driver):
        self.download_button = DownloadFile(driver)
        self.register_employees = RegisterEmployees(driver)

# class EmployeeFormPage:
#     def __init__(self, driver):
#         self.form_field = 

# https://desafio-rpa-946177071851.us-central1.run.app/auth/authenticate