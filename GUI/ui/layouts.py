from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPlainTextEdit, QComboBox , QPushButton
import datetime
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice


serial = QSerialPort()
serialinfo = QSerialPortInfo()
serial.setBaudRate(9600)
#serial.open()

print(F"INFO: {str(serial.portName)}")
portList = []
ports = QSerialPortInfo().availablePorts()
for port in ports:
    portList.append(port.portName())
print(portList)



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
    
    def onRead(self):
        rx = serial.readLine()
        rxs = str(rx)
        rxs.encode().strip()
        print(rxs)
        #self.secrity_log.appendPlainText(rxs)

    def secrity(self):
        indef = "FFFFFFF" #TODO Получать индефитикатор
        session = "13:05" #TODO Получать текущию сессию
        log = "Log"
        
        indef_text = f"<div align='center' style='font-size: 20px;'>Индефитикатор: {indef}</div>"
        session_text = f"<div align='center' style='font-size: 20px;'>Текущая сессия: {session}</div>"
        
        
        self.secrity_indef.setText(indef_text)
        self.secrity_session.setText(session_text)




        
        self.secrity_log_text.setText(log)
        self.secrity_log.setReadOnly(True)
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

        self.settings()
        self.setLayout(layout)

    def settings(self):
        self.ports.addItems(portList)
        self.ports.currentIndexChanged.connect(self.update_selected_port_info)

    def update_selected_port_info(self):
        selected_port = self.ports.currentText()
        port_info_text = f"<div align='center' style='font-size: 20px;'>Выбран порт: {selected_port}</div>"
        self.ap.setText(port_info_text)

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
    
    
        

       