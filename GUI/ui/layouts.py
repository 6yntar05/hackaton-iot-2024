
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPlainTextEdit, QComboBox , QPushButton, QCheckBox, QProgressBar
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap

from libs.system import Media, Session, Notify


serial = QSerialPort()
serialinfo = QSerialPortInfo()
serial.setBaudRate(115200)


print(F"INFO: {str(serial.portName)}")
portList = []
ports = QSerialPortInfo().availablePorts()
for port in ports:
    portList.append(port.portName())
print(portList)

R = 120
G = 120
B = 50

Bright = 100

def RGB_to_CCT(R, G, B):
    # Конвертация значений RGB в диапазоне [0, 255] в диапазон [0, 1]
    R /= 255
    G /= 255
    B /= 255

    # Перевод значений RGB в XYZ
    X = 0.4124564 * R + 0.3575761 * G + 0.1804375 * B
    Y = 0.2126729 * R + 0.7151522 * G + 0.0721750 * B
    Z = 0.0193339 * R + 0.1191920 * G + 0.9503041 * B

    # Вычисление координат Цветовой температуры (Chromaticity Coordinates)
    x = X / (X + Y + Z)
    y = Y / (X + Y + Z)

    # Вычисление цветовой температуры по координатам
    n = (x - 0.3320) / (0.1858 - y)
    CCT = 449 * n**3 + 3525 * n**2 + 6823.3 * n + 5520.33

    return int(round(CCT, -2))

class EnvironmentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.lbl_time = QLabel()
        layout.addWidget(self.lbl_time)

        self.lbl_color_temp = QLabel()
        layout.addWidget(self.lbl_color_temp)

        self.security_widget = SecurityWidget()
        self.security_widget.brightnessChanged.connect(self.updateBrightness)

        lamp_layout = QHBoxLayout()  # Создаем горизонтальный лейаут для лампы и яркости
        self.icon_label = QLabel()
        lamp_layout.addWidget(self.icon_label)

        self.lbl_lamp = QLabel()  # Создаем отдельный QLabel для отображения яркости
        lamp_layout.addWidget(self.lbl_lamp)

        layout.addLayout(lamp_layout)  # Добавляем горизонтальный лейаут в вертикальный

        self.mediabar = QLabel()
        layout.addWidget(self.mediabar)
        self.progress_bar = QProgressBar()  # Создаем QProgressBar
        self.progress_bar.setStyleSheet("""
    QProgressBar {
        border: none;
        text-align: center;
        min-width: 10px; /* Минимальная ширина прогрессбара */
    }
    QProgressBar::chunk {
        background-color: #4CAF50; /* Цвет прогресса */
        width: 1px; /* Ширина прогресса */
    }
""")
        layout.addWidget(self.progress_bar)  # Добавляем его в вертикальный лейаут

        self.time_and_temp()

        self.setLayout(layout)
        
    def time_and_temp(self):
        current_time = "00:00:00"
        color_temperature = str(RGB_to_CCT(R,G,B))+"K"

        time_text = f"<div align='left' style='font-size: 16px;'>Время сессии: {current_time}</div>"
        temp_text = f"<div align='left' style='font-size: 16px;'>Цветовая температура: {color_temperature}</div>"
        

        self.lbl_time.setText(time_text)
        self.lbl_color_temp.setText(temp_text)

        #print(Media.getTrack())
        #(status, title, artist, progress, duration) = Media.getTrack()
        if (True):
            mediabar_text = f"<div align='center' style='font-size: 16px;'> Ничего не воспроизводится </div>"
            self.mediabar.setText(mediabar_text)
            self.progress_bar.setVisible(False)
        else:
            mediabar_text = f"<div align='center' style='font-size: 16px;'> Известен - С названием </div>"
            self.mediabar.setText(mediabar_text)
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(50)

        icon_pixmap = QPixmap("res/lamp.png")
        self.icon_label.setPixmap(icon_pixmap)

    def updateBrightness(self, brightness):
        lamp_procent = f"{brightness}%"
        lamp_text = f"<div align='left' style='font-size: 16px;'>Яркость: {lamp_procent}</div>"
        self.lbl_lamp.setText(lamp_text)
    

    #Протестировать 
    """
    def update_session_time(self):
        session_time_seconds = Session.getSessionTime()
        session_time_text = self.format_time(session_time_seconds)
        self.lbl_time.setText(f"<div align='left' style='font-size: 16px;'>Время сессии: {session_time_text}</div>")
        QTimer.singleShot(1000, self.update_session_time) 

    def format_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    """
class SecurityWidget(QWidget):
    #Яркость
    brightnessChanged  = pyqtSignal(float)

    #Время 
    timeChange = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.security_indef = QLabel()
        layout.addWidget(self.security_indef)

        self.security_media_button = QLabel()
        layout.addWidget(self.security_media_button)

        self.security_media_sound = QLabel()
        layout.addWidget(self.security_media_sound)
        
        self.security_log_text = QLabel("Журнал")
        layout.addWidget(self.security_log_text)
        
        self.security_log = QPlainTextEdit()
        layout.addWidget(self.security_log)

        self.setLayout(layout)

        self.security()

    buffer = ""
    def onRead(self):
        while serial.bytesAvailable():
            tmpBuffer = ""
            rx = serial.read(1)
            self.buffer += rx.decode('utf-8')
            if '\n' not in self.buffer:
                continue
            else:
                command = self.buffer.strip()
                print("Received command:", command)
                tmpBuffer = self.buffer
                self.buffer = ""

            parts = tmpBuffer.split(':')
            print(parts)
            key = parts[0].strip() 
            if key == "RFID":
                value = parts[1].strip().replace("\\r\\n", "\n")
                self.security_log.appendPlainText(f"RFID:{value}")
                indef_text = f"<div align='center' style='font-size: 20px; color: #20FF20'>Идентификатор: {value}</div>" 
                self.security_indef.setText(indef_text)
            elif key == "b'MEDIA":
                self.security_log.appendPlainText(f"MEDIA:{value}")
                media_button_text = f"<div align='center' style='font-size: 20px; color: #7FFFD4'>Медиа: {value}</div>"
                self.security_media_button.setText(media_button_text)
            elif key == "b'VOLUME":
                self.security_log.appendPlainText(f"VOLUME:{value}")
                media_sound_text = f"<div align='center' style='font-size: 20px; color: #7FFFD4'>Громкость: {value}</div>"
                self.security_media_sound.setText(media_sound_text)
            elif key == "b'BRIGHT":
                self.security_log.appendPlainText(f"BRIGHT:{value}")
                self.brightnessChanged.emit(value)
            elif key == "b'TIME":
                self.security_log.appendPlainText(f"TIME:{value}")
            elif key == "b'LAMP":
                self.security_log.appendPlainText(f"LAMP:{value}")
                R = 120
                G = 120
                B = 50
            elif key == "b'SLEEP'":
                Session.suspend() # а оно приаттачится обратно?
            elif key == "b'NOTIFY'":
                Notify.Send("Время перерыва", "Ваша сессия длится более 4 часов")
            elif key == "b'LOGTIME" or key == "b'UNLOGTIME":
                self.security_log.appendPlainText(f'LOGTIME:{value}')
                self.security_log.appendPlainText(f'UNLOGTIME:{value}')
                    

    def security(self):
        self.security_log_text.setText("Журнал")
        self.security_log.setReadOnly(True)
        serial.readyRead.connect(self.onRead)  

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.ports = QComboBox()
        layout.addWidget(self.ports)

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_port)
        layout.addWidget(self.connect_button)

        self.disconnect_button = QPushButton("Disconnect")
        self.disconnect_button.clicked.connect(self.disconnect_from_port)
        self.disconnect_button.setEnabled(False) 
        layout.addWidget(self.disconnect_button)

        self.ap = QLabel()
        layout.addWidget(self.ap)

        self.autorun = QCheckBox("Автозагрузка")
        layout.addWidget(self.autorun)

        self.settings()
        self.setLayout(layout)

    def settings(self):
        self.ports.addItems(portList)
        self.ports.currentIndexChanged.connect(self.update_selected_port_info)
        self.autorun.stateChanged.connect(self.copy_to_run)

    def update_selected_port_info(self):
        selected_port = self.ports.currentText()
        port_info_text = f"<div align='center' style='font-size: 20px;'>Выбран порт: {selected_port}</div>"
        self.ap.setText(port_info_text)
    
    def copy_to_run(self):
        if self.autorun.isChecked():
            pass
            #file_path = sys.argv[0]
            #file_name = file_path.split('\\')[-1]
            #path = '%userprofile%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\'
            #os.system(f'copy "{file_path}" "{path}{file_name}"')   

    def connect_to_port(self):
        selected_port = self.ports.currentText()
        serial.setPortName(selected_port)
        if serial.open(QIODevice.ReadWrite):
            print("Successfully connected to", selected_port)
            selected_port = self.ports.currentText()
            port_info_text = f"<div align='center' style='font-size: 20px;'>Выбран порт: {selected_port}</div>"
            self.ap.setText(port_info_text) 
            self.connect_button.setEnabled(False)  
            self.disconnect_button.setEnabled(True) 
        else:
            print("Failed to connect to", selected_port)

    def disconnect_from_port(self):
        if serial.isOpen():
            serial.close()
            self.ap.setText("<div align='center' style='font-size: 20px;'>Порт отключен</div>")
            self.connect_button.setEnabled(True)  
            self.disconnect_button.setEnabled(False) 
            print("Disconnected from port")
        else:
            print("Port is already closed")
    
    
        

       