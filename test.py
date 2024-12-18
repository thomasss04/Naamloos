from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Steam')
        self.setGeometry(0, 0, 500, 500)
        self.setWindowIcon(QIcon('steam.png'))

        label = QLabel('Home', self)
        label.setFont(QFont('Arial', 20))
        label.setGeometry(0, 0, 500, 100)
        label.setStyleSheet('background-color: #1e3966;'
                            'font-weight: bold;'
                            'font-style: italic;')

        label.setAlignment(Qt.AlignCenter)

        labelpic = QLabel(self)
        labelpic.setGeometry(0,0,100,100)
        pixmap = QPixmap('steam.png')
        labelpic.setPixmap(pixmap)
        labelpic.setScaledContents(True)



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()