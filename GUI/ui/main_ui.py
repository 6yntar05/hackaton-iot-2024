from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget, QMessageBox, QSpacerItem, QSizePolicy, QLabel, QStackedWidget
from PyQt5.QtCore import Qt
from ui.layouts import EnvironmentWidget, SecurityWidget, SettingsWidget

class TransparentStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        #background_label = QLabel(self)
        #background_pixmap = QPixmap("res/comp.png")
        #background_label.setPixmap(background_pixmap)
        #background_label.resize(background_pixmap.size())
        #background_label.move(0, 0)

        self.setLayout(layout)

        # Создаем QVBoxLayout для кнопок слева
        buttons_layout = QVBoxLayout()

        # Создаем кнопки для переключения между виджетами
        self.btn_environment = QPushButton("🖥️  Окружение")
        self.btn_environment.setDisabled(True)
        self.btn_environment.clicked.connect(self.show_environment)
        #self.btn_environment.setStyleSheet("text-align: left; padding-left: 20px;")
        buttons_layout.addWidget(self.btn_environment)

        self.btn_security = QPushButton("🛡️  Безопасность")
        self.btn_security.clicked.connect(self.show_security)
        #self.btn_security.setStyleSheet("text-align: left; padding-left: 20px;")
        buttons_layout.addWidget(self.btn_security)

        self.btn_settings = QPushButton("⚙️  Настройки")
        self.btn_settings.clicked.connect(self.show_settings)
        #self.btn_settings.setStyleSheet("text-align: left; padding-left: 20px;")
        buttons_layout.addWidget(self.btn_settings)
        
        # Растягиваемый разделитель между настройками и информацией
        spacer_item = QSpacerItem(0, 500, QSizePolicy.Minimum, QSizePolicy.Expanding)
        buttons_layout.addItem(spacer_item)
        
        self.btn_info = QPushButton("🗒️  Информация")
        self.btn_info.clicked.connect(self.show_info)
        #self.btn_info.setStyleSheet("text-align: left; padding-left: 20px;")
        buttons_layout.addWidget(self.btn_info)

        # Растягиваем кнопки по всей доступной ширине
        buttons_layout.addStretch(1)

        layout.addLayout(buttons_layout)

        self.stacked_widget = QStackedWidget()
        #self.stacked_widget.setStyleSheet("background-color: transparent;")
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
Aarch: WorkSE App
Version prev-22.04.24
By AArch64 team (⸝⸝ᵕᴗᵕ⸝⸝)
""")
        mbox.setStandardButtons(QMessageBox.Ok)
        mbox.exec_()