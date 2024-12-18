from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sqlite3

# Connect to the database (or create one if it doesn't exist)
conn = sqlite3.connect('Steam.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table
# cursor.execute('''
# -- Tabel voor vriendenrelaties tussen gebruikers
# -- Optioneel: Tabel voor gedeelde games tussen vrienden
# CREATE TABLE shared_games (
#     sharednr INTEGER PRIMARY KEY AUTOINCREMENT,   -- Uniek ID voor gedeelde games
#     friendnr INT NOT NULL,                    -- Verwijzing naar een vriendschap
#     librarynr INT NOT NULL,                        -- Verwijzing naar een game in de bibliotheek
#     FOREIGN KEY (friendnr) REFERENCES friends(friendnr) ON DELETE CASCADE,
#     FOREIGN KEY (librarynr) REFERENCES library(librarynr) ON DELETE CASCADE
# );
#
#
#
#
#
#
# ''')

# Insert data
# cursor.execute('INSERT INTO accounts (username, password) VALUES (?, ?)', ('Hitsss12', 'Hitsss12'))
# cursor.execute('INSERT INTO accounts (username, password) VALUES (?, ?)', ('Bob123456', 'Bob123456'))

# Commit changes
conn.commit()

# Query data
cursor.execute('SELECT * FROM accounts')
rows = cursor.fetchall()

# Print results
print("Users in the database:")
for row in rows:
    print(row)

# Close the connection
conn.close()





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