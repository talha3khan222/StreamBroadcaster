import os
import requests


def download_file_from_google_drive(id, destination):
    if not os.path.exists(destination):
        print("Downloading Supported Files...")
        URL = "https://drive.google.com/uc?export=download"
        session = requests.Session()
        response = session.get(URL, params={'id': id}, stream=True)
        token = get_confirm_token(response)
        if token:
            params = {'id': id, 'confirm': token}
            response = session.get(URL, params=params, stream=True)
        save_response_content(response, destination)
        print("Downloading Completed...")


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


class GoogleDriveDownloader:
    def __init__(self):
        link = "https://drive.google.com/drive/folders/1Vz-6phclxoqS1hBGBRfLjhxj16L_G8ux?usp=sharing"

    def download_file(self, local_destination, remote_file_id):
        if not os.path.exists(local_destination):
            print("Downloading File from Drive")
            download_file_from_google_drive(remote_file_id, local_destination)
            print("Downloading Completed")
