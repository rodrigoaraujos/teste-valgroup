import os
import time

from pathlib import Path


def wait_download(folder, timeout=60):
    start_time = time.time()
    while time.time() >= start_time:
        current_files_list = list(
            Path(folder).resolve().iterdir())
        if current_files_list:
            file_path = current_files_list[0]
            if file_path.suffix not in ('.tmp', '.crdownload') and '.com.google.Chrome.' not in file_path.name:
                return file_path
        time.sleep(1)
    raise TimeoutError("timed out waiting for download.")


def normalize_text(text):
        return text.replace('*','').strip()