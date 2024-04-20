from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget, QMessageBox
from ui.layouts import EnvironmentWidget, SecurityWidget, SettingsWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        # Создаем QVBoxLayout для кнопок слева
        buttons_layout = QVBoxLayout()

        # Создаем кнопки для переключения между виджетами
        self.btn_environment = QPushButton("Окружение")
        self.btn_environment.setDisabled(True)
        self.btn_environment.clicked.connect(self.show_environment)
        buttons_layout.addWidget(self.btn_environment)

        self.btn_security = QPushButton("Безопасность")
        self.btn_security.clicked.connect(self.show_security)
        buttons_layout.addWidget(self.btn_security)

        self.btn_settings = QPushButton("Настройки")
        self.btn_settings.clicked.connect(self.show_settings)
        buttons_layout.addWidget(self.btn_settings)
        
        
        self.btn_info = QPushButton("Информация")
        self.btn_info.clicked.connect(self.show_info)
        buttons_layout.addWidget(self.btn_info)


        layout.addLayout(buttons_layout)

        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        self.environment_widget = EnvironmentWidget()
        self.stacked_widget.addWidget(self.environment_widget)

        self.security_widget = SecurityWidget()
        self.stacked_widget.addWidget(self.security_widget)

        self.settings_widget = SettingsWidget()
        self.stacked_widget.addWidget(self.settings_widget)

        self.setLayout(layout)

    def show_environment(self):
        self.stacked_widget.setCurrentWidget(self.environment_widget)
        self.btn_environment.setDisabled(True)
        self.btn_security.setDisabled(False)
        self.btn_settings.setDisabled(False)

    def show_security(self):
        self.stacked_widget.setCurrentWidget(self.security_widget)        
        self.btn_environment.setDisabled(False)
        self.btn_security.setDisabled(True)
        self.btn_settings.setDisabled(False)

    def show_settings(self):
        self.stacked_widget.setCurrentWidget(self.settings_widget)
        self.btn_environment.setDisabled(False)
        self.btn_security.setDisabled(False)
        self.btn_settings.setDisabled(True)
        
    def show_info(self):
        mbox = QMessageBox()
        mbox.setWindowTitle("Информация")
        mbox.setText("""
Создатели чудо-проги:
Толкачев Станислав - 6yntar05
Малков Антон - Sodx1
Лев Асманов 
Наше правило: btw i use arch 
""")
        mbox.setStandardButtons(QMessageBox.Ok)
        mbox.exec_()