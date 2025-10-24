import time
from pathlib import Path

from selenium.webdriver.common.action_chains import ActionChains


def wait_download(folder, timeout=60):
    start_time = time.time()
    while time.time() - start_time <= timeout:
        current_files_list = list(Path(folder).resolve().iterdir())
        if current_files_list:
            file_path = current_files_list[0]
            if (
                file_path.suffix not in (".tmp", ".crdownload")
                and ".com.google.Chrome." not in file_path.name
            ):
                return file_path
        time.sleep(1)
    raise TimeoutError("timed out waiting for download.")


def normalize_text(text):
    return text.replace("*", "").strip()


def hover_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    return element
