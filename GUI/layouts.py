import time
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPlainTextEdit 
import datetime
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo


serial = QSerialPort()
serial.setBaudRate(115200)

class EnvironmentWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.lbl_time = QLabel()
        layout.addWidget(self.lbl_time)
        
        self.lbl_level = QLabel()
        layout.addWidget(self.lbl_level)

        self.lbl_color_temp = QLabel()
        layout.addWidget(self.lbl_color_temp)

        self.lbl_lamp = QLabel()
        layout.addWidget(self.lbl_lamp)
        
        self.time_and_temp()

        self.setLayout(layout)
        
    def time_and_temp(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        level = "Уровень света: 5%"
        color_temperature = "5000K"  #TODO: добавить логику для получения реальной цветовой температуры
        lamp_procent = "40%"
        

        time_text = f"<div align='center' style='font-size: 20px;'>Текущее время: {current_time}</div>"
        level_text = f"<div align='center' style='font-size: 20px;'>{level}</div>"
        temp_text = f"<div align='center' style='font-size: 20px;'>Цветовая температура: {color_temperature}</div>"
        lamp_text = f"<div align='center' style='font-size: 20px;'>Процент горения лампы: {lamp_procent}</div>"

        self.lbl_time.setText(time_text)
        self.lbl_level.setText(level_text)
        self.lbl_color_temp.setText(temp_text)
        self.lbl_lamp.setText(lamp_text)
    


class SecurityWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.secrity_indef = QLabel()
        layout.addWidget(self.secrity_indef)
        
        self.secrity_session = QLabel()
        layout.addWidget(self.secrity_session)
        
        #TODO Подумать как делать вывод логов
        self.secrity_log = QPlainTextEdit()
        self.secrity_log_text = QLabel()
        layout.addWidget(self.secrity_log_text)
        layout.addWidget(self.secrity_log)
        
        self.secrity()

        self.setLayout(layout)
        
    def secrity(self):
        indef = "FFFFFFF" #TODO Получать индефитикатор
        session = "13:05" #TODO Получать текущию сессию
        log = "Log"
        
        indef_text = f"<div align='center' style='font-size: 20px;'>Индефитикатор: {indef}</div>"
        session_text = f"<div align='center' style='font-size: 20px;'>Текущая сессия: {session}</div>"
        
        
        self.secrity_indef.setText(indef_text)
        self.secrity_session.setText(session_text)
        self.secrity_log_text.setText(log)
        self.secrity_log.placeholderText()

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.setLayout(layout)