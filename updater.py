import requests
import os
import shutil

def update_sikeam():
    base_url = "https://raw.githubusercontent.com/taneery/Sikeam/master/"
    files = ["sikeam.py", "games.json", "styles/steam.qss"]
    for file in files:
        try:
            response = requests.get(f"{base_url}{file}")
            if "styles" in file:
                os.makedirs("styles", exist_ok=True)
            with open(file, "wb") as f:
                f.write(response.content)
            print(f"{file} güncellendi.")
        except:
            print(f"{file} güncellenemedi.")

if __name__ == "__main__":
    update_sikeam()
    os.system("sikeam.exe")