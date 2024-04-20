import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPlainTextEdit, QComboBox , QPushButton, QCheckBox
import datetime
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
import sys


serial = QSerialPort()
serialinfo = QSerialPortInfo()
serial.setBaudRate(115200)


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
        
        self.security_indef = QLabel()
        layout.addWidget(self.security_indef)
        
        self.security_log_text = QLabel("Логи")
        layout.addWidget(self.security_log_text)
        
        self.security_log = QPlainTextEdit()
        layout.addWidget(self.security_log)

        self.setLayout(layout)

        self.security()

    def onRead(self):
        while (serial.bytesAvailable()):
            rx = serial.readLine()
            rxs = str(rx)

            lines = rxs.split('\\r\\n')
            for line in lines:
                parts = line.split(':')
                if len(parts) == 2:
                    key = parts[0].strip() 
                    value = parts[1].strip()  
                    print(f'{key}: {value}')
                    if key == "b'RFID":
                        self.security_log.appendPlainText(f"RFID:{value}")
                        indef_text = f"<div align='center' style='font-size: 20px;'>Индефитикатор: {value}</div>" 
                        self.security_indef.setText(indef_text)
                    elif key == "b'MEDIA":
                        self.security_log.appendPlainText(f"MEDIA:{value}")
                    elif key == "b'VOLUME":
                        self.security_log.appendPlainText(f"VOLUME:{value}")
                    elif key == "b'BRIGHT":
                        self.security_log.appendPlainText(f"BRIGHT:{value}")
                    elif key == "b'TIME":
                        self.security_log.appendPlainText(f"TIME:{value}")
                    elif key == "b'LAMP":
                        self.security_log.appendPlainText(f"LAMP:{value}")

    def security(self):
        self.security_log_text.setText("Логи")
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
            file_path = sys.argv[0]
            file_name = file_path.split('\\')[-1]
            path = '%userprofile%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\'
            os.system(f'copy "{file_path}" "{path}{file_name}"')   

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
    
    
        

       