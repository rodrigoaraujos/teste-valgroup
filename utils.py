import os
import time


def wait_download(folder, timeout=60):
    start_time = time.time()
    while True:
        files = os.listdir(folder)
        downloading = [f for f in files if f.endswith(".crdownload")]
        if not downloading and files:
            return os.path.join(folder, files[0])
        if time.time() - start_time > timeout:
            raise TimeoutError("timed out waiting for download.")
        time.sleep(1)
