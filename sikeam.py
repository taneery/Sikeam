import sys
import json
import requests
import os
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont

# Güncelleme
def check_update():
    json_url = "https://raw.githubusercontent.com/taneery/Sikeam/master/games.json"
    try:
        response = requests.get(json_url)
        with open("games.json", "wb") as f:
            f.write(response.content)
        print("Oyun listesi güncellendi.")
    except:
        print("JSON güncelleme başarısız.")

# İndirme ve birleştirme
def download_and_extract(links, game_name):
    os.makedirs("temp", exist_ok=True)
    for i, link in enumerate(links):
        response = requests.get(link, stream=True)
        part_file = f"temp/{game_name}_part_{i}.rar"
        with open(part_file, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    os.system(f"unrar x temp/{game_name}_part_0.rar games/")
    shutil.rmtree("temp")

# Ana pencere
class SikeamWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sikeam")
        self.setGeometry(100, 100, 1280, 720)

        # Stil yükleme
        with open("styles/steam.qss", "r") as f:
            self.setStyleSheet(f.read())

        # Ana layout
        main_layout = QHBoxLayout()

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(300)
        main_layout.addWidget(self.sidebar)

        # Sağ panel
        right_panel = QFrame()
        right_layout = QVBoxLayout()

        # Üst boşluk
        right_layout.addStretch(1)

        # Oyun resmi
        self.game_image = QLabel()
        self.game_image.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.game_image)

        # Oyun adı
        self.game_name = QLabel("Sikeam")
        self.game_name.setFont(QFont("Arial", 28, QFont.Bold))  # Motiva Sans yoksa Arial
        self.game_name.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.game_name)

        # Durum
        self.status_label = QLabel("Bir oyun seç")
        self.status_label.setFont(QFont("Arial", 14))
        self.status_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.status_label)

        # Buton
        self.action_btn = QPushButton("İndir")
        self.action_btn.setFixedSize(200, 50)
        self.action_btn.setFont(QFont("Arial", 16))
        right_layout.addWidget(self.action_btn, alignment=Qt.AlignCenter)

        right_layout.addStretch(2)

        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel)

        # Merkezi widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Oyunları yükle
        self.load_games()

    def load_games(self):
        check_update()
        try:
            with open("games.json", "r") as f:
                self.games = json.load(f)["games"]
            for game in self.games:
                self.sidebar.addItem(game["name"])
            self.sidebar.itemClicked.connect(self.show_game_details)
        except:
            print("Oyun listesi yüklenemedi.")

    def show_game_details(self, item):
        game = next(g for g in self.games if g["name"] == item.text())
        pixmap = QPixmap(f"assets/{game['image']}")
        self.game_image.setPixmap(pixmap.scaled(600, 280, Qt.KeepAspectRatio))
        self.game_name.setText(game["name"])
        game_path = f"games/{game['name']}"
        if os.path.exists(game_path):
            self.status_label.setText("Installed")
            self.action_btn.setText("Play")
            self.action_btn.clicked.connect(lambda: os.startfile(f"{game_path}/{game['exe']}"))
        else:
            self.status_label.setText("Not Installed")
            self.action_btn.setText("Install")
            self.action_btn.clicked.connect(lambda: self.start_download(game["links"], game["name"]))

    def start_download(self, links, game_name):
        download_and_extract(links, game_name)
        self.status_label.setText("Installed")
        self.action_btn.setText("Play")

# Çalıştır
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SikeamWindow()
    window.show()
    sys.exit(app.exec_())