import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from ui.main_ui import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = QWidget()
    w.setFixedSize(500,300)
    w.setWindowTitle("Aarch : WorkSE")
    
    main_layout = QVBoxLayout(w)  
    
   
    MainUI = MainWindow()
    main_layout.addWidget(MainUI)
   
    w.setLayout(main_layout)
    w.show()
    sys.exit(app.exec_())