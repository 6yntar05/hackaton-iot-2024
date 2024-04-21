import sys
from PyQt5.QtWidgets import QApplication
import ctypes
import subprocess
import re
import os 

class Media:
    @staticmethod
    def changeVolume(volume_level):
        # Изменение уровня громкости с помощью amixer
        os.system(f"amixer set Master {volume_level}%")

    @staticmethod
    def toggleMusic():
        # Переключение состояния музыки с помощью playerctl
        os.system("playerctl play-pause")

    @staticmethod
    def nextMusic():
        # Воспроизведение следующего трека с помощью playerctl
        os.system("playerctl next")

    @staticmethod
    def prevMusic():
        # Воспроизведение предыдущего трека с помощью playerctl
        os.system("playerctl previous")
    
    @staticmethod
    def getTrack():
        try:
            # Выполнение команды "playerctl metadata" и получение вывода
            result = subprocess.run(["playerctl", "metadata", "--format", "'{{status}} {{title}} by {{artist}}'"], capture_output=True, text=True, shell=True)
            output = result.stdout

            # Парсинг вывода с помощью регулярных выражений
            match = re.match(r"'(.*?) (.*?) by (.*?)'", output)
            if match:
                status = match.group(1)
                title = match.group(2)
                artist = match.group(3)

                return status, title, artist
            else:
                return None
        except Exception as e:
            print(f"Error getting track: {e}")
            return None

class Session:
    def lockOS():
        os.system("swaylock")

    def unlockOS():
        os.system("pkill --signal SIGUSR1 swaylock")
    
    def suspend():
        os.system("systemctl suspend")
    
    @staticmethod
    def setAutostart():
        # Создание файла .desktop для автозапуска программы
        autostart_dir = os.path.expanduser("~/.config/autostart")
        if not os.path.exists(autostart_dir):
            os.makedirs(autostart_dir)
        
        desktop_file_path = os.path.join(autostart_dir, "WorkSE.desktop")
        with open(desktop_file_path, "w") as desktop_file:
            desktop_file.write("[Desktop Entry]\n")
            desktop_file.write("Name=Aarch64: WorkSE App\n")
            desktop_file.write("Exec=WorkSE\n")
            desktop_file.write("Type=Application\n")
            desktop_file.write("X-GNOME-Autostart-enabled=true\n")
        
        print("Autostart enabled")

    @staticmethod
    def unsetAutostart():
        # Удаление файла .desktop для отключения автозапуска программы
        autostart_dir = os.path.expanduser("~/.config/autostart")
        desktop_file_path = os.path.join(autostart_dir, "WorkSE.desktop")
        if os.path.exists(desktop_file_path):
            os.remove(desktop_file_path)
            print("Autostart disabled")
        else:
            print("Autostart was not set")
