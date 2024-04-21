import sys
from PyQt5.QtWidgets import QApplication
import ctypes
import subprocess
import re
import os 
import psutil

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

class Notify:
    @staticmethod
    def Send(summary, text):
        os.system("notify-send -i '{}' '{}'".format(summary, text))

class Session:
    @staticmethod
    def lockOS():
        os.system("swaylock")

    @staticmethod
    def unlockOS():
        os.system("pkill --signal SIGUSR1 swaylock")
    
    @staticmethod
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
    
    @staticmethod
    def getSessionTime():
        pid = os.getpid()  # Получаем PID текущего процесса
        stat_path = f"/proc/{pid}/stat"

        with open(stat_path, 'r') as stat_file:
            stat_info = stat_file.read().split()

        # Время активности процесса в тактах ядра
        utime = int(stat_info[13])  # utime - user mode time

        # Количество тактов в секунде
        ticks_per_second = os.sysconf(os.sysconf_names['SC_CLK_TCK'])

        # Переводим время активности процесса из тактов в секунды
        session_time_seconds = utime / ticks_per_second

        return session_time_seconds
    
    @staticmethod
    def getSystemUptime():
        try:
            uptime_seconds = psutil.boot_time()
            uptime_formatted = timedelta(seconds=uptime_seconds)
            return str(uptime_formatted)
        except Exception as e:
            print(f"Error getting system uptime: {e}")
            return None
