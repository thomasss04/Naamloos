import hashlib
import shutil
import math
import matplotlib.pyplot as plt

import customtkinter as ctk
import tkinter.messagebox as tkmb
import psycopg2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QStackedWidget, QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView, QSizePolicy, QFileDialog, QDateEdit, QTimeEdit,
)
from PyQt5.QtGui import QFont, QIcon, QBrush, QPainter, QPainterPath
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer, QDate, QTime
from matplotlib.backends.backend_template import FigureCanvas

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from test import lineare_regressie2

connection_string = "host='4.234.56.16' dbname='Steam' user='postgres' password='mggfgg55'"
conn = psycopg2.connect(connection_string)
cursor = conn.cursor()


import os


class SteamApp(QMainWindow):
    def __init__(self, accountnr):
        super().__init__()
        self.accountnr = accountnr  # het account nr waarmee is ingelogd zodat alle data opgehaald kan worden
        self.setWindowTitle('Steam')
        self.setGeometry(0, 0, 1300, 700)
        self.setWindowIcon(QIcon('steamround.png'))
        self.setStyleSheet('background-color: #293e4f')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # het logo
        labelpic = QLabel(self)
        labelpic.setFixedSize(100, 100)
        pixmap = QPixmap('./steamround.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        if os.path.exists('./steamround.png') and not pixmap.isNull():
            labelpic.setPixmap(pixmap)
            labelpic.setScaledContents(True)
            labelpic.setVisible(True)
        else:
            print("Pixmap failed to load. Check the file path.")

        labelpic.move(10, 10)

        # de navigation bar, dus om naar andere pages te komen
        self.navigation = QListWidget()
        self.navigation.addItems(['Home', 'Library', 'Games', 'Friends', 'Sessions', 'Profile'])
        self.navigation.setStyleSheet("""
                    font-size: 20px;
                    font-weight: bold;
                    color: white; 
                    background-color: #293e4f;
                """)
        self.navigation.setFixedHeight(300)
        self.navigation.setFixedWidth(200)
        self.navigation.currentRowChanged.connect(self.display_page)
        main_layout.addWidget(self.navigation)

        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area)

        # de pages zelf
        self.home_page = self.home_page()
        self.library_page = self.library_page()
        self.games_page = self.games_page()
        self.friends_page = self.friends_page()
        self.sessions_page = self.sessions_page()
        self.profile_page = self.profile_page()

        self.content_area.addWidget(self.home_page)
        self.content_area.addWidget(self.library_page)
        self.content_area.addWidget(self.games_page)
        self.content_area.addWidget(self.friends_page)
        self.content_area.addWidget(self.sessions_page)
        self.content_area.addWidget(self.profile_page)

    def display_home_page(self):
        home_widget = QWidget()
        layout = QVBoxLayout(home_widget)

        # Add the plot to the layout
        layout.addWidget(self.scatter_plot())

        # Set the home widget to be the current page
        self.content_area.addWidget(home_widget)
        self.content_area.setCurrentWidget(home_widget)

    def home_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)

        # Welcome label
        welcome_label = QLabel("Welcome to the Steam App!")
        welcome_label.setStyleSheet("font-size: 30px; font-weight: bold; color: white;")
        layout.addWidget(welcome_label)

        # Add the scatter plot to the layout
        plot_canvas = self.scatter_plot()
        layout.addWidget(plot_canvas)

        return page

    def library_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)

        # dit is de search box om de games op te zoeken
        search_box = QLineEdit()
        search_box.setPlaceholderText("Enter game name to search")
        search_box.setStyleSheet("""
                    font-size: 20px;
                    font-weight: bold;
                    color: white; 
                    background-color: #293e4f;

                """)
        layout.addWidget(search_box)

        # het knopje voor het zoeken
        search_button = QPushButton("Search")
        search_button.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: white; 
            background-color: #293e4f;

        """)
        layout.addWidget(search_button)

        # dit zijn alle results
        results_table = QTableWidget()
        results_table.setColumnCount(1)
        results_table.setHorizontalHeaderLabels(["Game Name"])
        results_table.setFont(QFont("Arial", 15))

        # hiermee ziet het er een beetje goed uit
        results_table.setStyleSheet("""
            QTableWidget {
                background-color: #293e4f; 
                color: white; 
            }
            QHeaderView::section {
                background-color: #1f2a38; 
                color: white; 
                font-weight: bold; 
            }
            QTableWidget::item {
                background-color: #293e4f; 
                color: white; 
            }
        """)

        # hierdoor is het allemaal mooi gestretched
        results_table.horizontalHeader().setStretchLastSection(True)
        results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        results_table.verticalHeader().setVisible(False)
        results_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(results_table)

        # hier kan je de uren erin zetten
        hours_input = QLineEdit()
        hours_input.setPlaceholderText("Enter hours played")
        hours_input.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: white; 
            background-color: #293e4f;

        """)
        layout.addWidget(hours_input)

        # dit is de button die de game add
        add_button = QPushButton("Add Selected Game")
        add_button.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: white; 
            background-color: #293e4f;

        """)
        layout.addWidget(add_button)

        # hiermee kan je je library zien
        view_library_button = QPushButton("View Library")
        view_library_button.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: white; 
            background-color: #293e4f;

        """)
        layout.addWidget(view_library_button)

        # dit is de table van je library die je dan ziet
        library_table = QTableWidget()
        library_table.setColumnCount(2)
        library_table.setHorizontalHeaderLabels(["Game Name", "Hours Played"])
        library_table.setStyleSheet("""
                    QTableWidget {
                        background-color: #293e4f; 
                        color: white; 
                    }
                    QHeaderView::section {
                        background-color: #1f2a38; 
                        color: white; 
                        font-weight: bold; 
                    }
                    QTableWidget::item {
                        background-color: #293e4f; 
                        color: white; 
                    }
               """)
        layout.addWidget(library_table)

        library_table.horizontalHeader().setStretchLastSection(True)
        library_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        library_table.verticalHeader().setVisible(False)
        library_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(library_table)

        # hier worden de knoppen ook aan de acties gelinkt
        search_button.clicked.connect(lambda: self.search_games(search_box, results_table))
        add_button.clicked.connect(lambda: self.add_game(results_table, hours_input))
        view_library_button.clicked.connect(lambda: self.view_library(library_table))

        return page

    def games_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        page.setLayout(layout)

        # Section: Search Games
        search_label = QLabel("Search Games")
        search_label.setStyleSheet("font-size: 25px; font-weight: bold; color: white;")
        layout.addWidget(search_label)

        search_box = QLineEdit()
        search_box.setPlaceholderText("Enter game name to search")
        search_box.setStyleSheet("""
                            font-size: 20px;
                            font-weight: bold;
                            color: white; 
                            background-color: #293e4f;
                        """)
        layout.addWidget(search_box)

        search_button = QPushButton("Search")
        search_button.setStyleSheet("""
                    font-size: 20px;
                    font-weight: bold;
                    color: white; 
                    background-color: #293e4f;
                """)
        layout.addWidget(search_button)

        results_table = QTableWidget()
        results_table.setColumnCount(1)
        results_table.setHorizontalHeaderLabels(["Game Name"])
        results_table.setFont(QFont("Arial", 15))
        results_table.setStyleSheet("""
            QTableWidget {
                background-color: #293e4f;
                color: white;
            }
            QHeaderView::section {
                background-color: #1f2a38;
                color: white;
                font-weight: bold;
            }
            QTableWidget::item {
                background-color: #293e4f;
                color: white;
            }
        """)
        results_table.horizontalHeader().setStretchLastSection(True)
        results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        results_table.verticalHeader().setVisible(False)
        layout.addWidget(results_table)

        # Section: Most Played Games
        most_played_label = QLabel("Most Played Games")
        most_played_label.setStyleSheet("font-size: 25px; font-weight: bold; color: white;")
        layout.addWidget(most_played_label)

        most_played_table = QTableWidget()
        most_played_table.setColumnCount(2)
        most_played_table.setHorizontalHeaderLabels(["Game Name", "Average Hours Played"])
        most_played_table.setStyleSheet("""
            QTableWidget {
                background-color: #293e4f;
                color: white;
            }
            QHeaderView::section {
                background-color: #1f2a38;
                color: white;
                font-weight: bold;
            }
            QTableWidget::item {
                background-color: #293e4f;
                color: white;
            }
        """)
        most_played_table.horizontalHeader().setStretchLastSection(True)
        most_played_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        most_played_table.verticalHeader().setVisible(False)
        layout.addWidget(most_played_table)

        random_games_button = QPushButton("Show Random Games")
        random_games_button.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: white;
            background-color: #293e4f;
        """)
        layout.addWidget(random_games_button)

        # Add Table to Display Random Games
        random_games_table = QTableWidget()
        random_games_table.setColumnCount(3)
        random_games_table.setHorizontalHeaderLabels(["Name", "Release Date", "Price"])
        random_games_table.setStyleSheet("""
            QTableWidget {
                background-color: #293e4f;
                color: white;
            }
            QHeaderView::section {
                background-color: #1f2a38;
                color: white;
                font-weight: bold;
            }
            QTableWidget::item {
                background-color: #293e4f;
                color: white;
            }
        """)
        layout.addWidget(random_games_table)

        random_games_table.horizontalHeader().setStretchLastSection(True)
        random_games_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        random_games_table.verticalHeader().setVisible(False)

        # Connect Button to the Function
        random_games_button.clicked.connect(lambda: self.fetch_random_games(random_games_table))
        search_button.clicked.connect(lambda: self.search_games(search_box, results_table))
        self.view_most_played_games(most_played_table)

        return page

    def friends_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)

        # Section: Add a Friend
        username_input = QLineEdit()
        username_input.setPlaceholderText("Enter friend's username")
        username_input.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: white; 
            background-color: #293e4f;
        """)
        layout.addWidget(username_input)

        add_friend_button = QPushButton("Add Friend")
        add_friend_button.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: white; 
            background-color: #293e4f;
        """)
        layout.addWidget(add_friend_button)

        # Section: Friends List with Status
        friends_table = QTableWidget()
        friends_table.setColumnCount(2)
        friends_table.setHorizontalHeaderLabels(["Username", "Status"])
        friends_table.setStyleSheet("""
            QTableWidget {
                background-color: #293e4f; 
                color: white; 
            }
            QHeaderView::section {
                background-color: #1f2a38; 
                color: white; 
                font-weight: bold; 
            }
            QTableWidget::item {
                background-color: #293e4f; 
                color: white; 
            }
        """)
        layout.addWidget(friends_table)

        friends_table.horizontalHeader().setStretchLastSection(True)
        friends_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        friends_table.verticalHeader().setVisible(False)

        library_layout = QVBoxLayout()

        # Section: View Friend's Library
        view_library_button = QPushButton("View Friend's Library")
        view_library_button.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: white; 
            background-color: #293e4f;
        """)
        library_layout.addWidget(view_library_button)

        library_table = QTableWidget()
        library_table.setColumnCount(2)
        library_table.setHorizontalHeaderLabels(["Game Name", "Hours Played"])
        library_table.setStyleSheet("""
            QTableWidget {
                background-color: #293e4f; 
                color: white; 
            }
            QHeaderView::section {
                background-color: #1f2a38; 
                color: white; 
                font-weight: bold; 
            }
            QTableWidget::item {
                background-color: #293e4f; 
                color: white; 
            }
        """)
        library_table.horizontalHeader().setStretchLastSection(True)
        library_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        library_table.verticalHeader().setVisible(False)

        library_table.setFixedHeight(200)

        library_layout.addWidget(library_table)
        layout.addLayout(library_layout)

        add_friend_button.clicked.connect(lambda: self.add_friend(username_input, friends_table))
        view_library_button.clicked.connect(lambda: self.view_friend_library(friends_table, library_table))

        self.view_friends_with_status(friends_table)

        return page

    def sessions_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        # Section: Your Planned Sessions
        section_label = QLabel("Your Planned Sessions")
        section_label.setStyleSheet("""
                    font-size: 20px;
                    font-weight: bold;
                    color: white; 
                    background-color: #293e4f;
                """)
        layout.addWidget(section_label)

        your_sessions_table = QTableWidget()
        your_sessions_table.setColumnCount(4)
        your_sessions_table.setHorizontalHeaderLabels(["Game", "Date", "Time", "Description"])
        your_sessions_table.setStyleSheet("""
                    QTableWidget {
                        background-color: #293e4f; 
                        color: white; 
                    }
                    QHeaderView::section {
                        background-color: #1f2a38; 
                        color: white; 
                        font-weight: bold; 
                    }
                    QTableWidget::item {
                        background-color: #293e4f; 
                        color: white; 
                    }
                """)
        your_sessions_table.horizontalHeader().setStretchLastSection(True)
        your_sessions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        your_sessions_table.verticalHeader().setVisible(False)
        layout.addWidget(your_sessions_table)
        self.view_your_sessions(your_sessions_table)

        # Section: Friends' Planned Sessions
        section_label = QLabel("Friends' Planned Sessions")
        section_label.setStyleSheet("""
                    font-size: 20px;
                    font-weight: bold;
                    color: white; 
                    background-color: #293e4f;
                """)
        layout.addWidget(section_label)

        friends_sessions_table = QTableWidget()
        friends_sessions_table.setColumnCount(4)
        friends_sessions_table.setHorizontalHeaderLabels(["Friend", "Game", "Date", "Time"])
        friends_sessions_table.setStyleSheet("""
                            QTableWidget {
                                background-color: #293e4f; 
                                color: white; 
                            }
                            QHeaderView::section {
                                background-color: #1f2a38; 
                                color: white; 
                                font-weight: bold; 
                            }
                            QTableWidget::item {
                                background-color: #293e4f; 
                                color: white; 
                            }
                        """)
        friends_sessions_table.horizontalHeader().setStretchLastSection(True)
        friends_sessions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        friends_sessions_table.verticalHeader().setVisible(False)
        layout.addWidget(friends_sessions_table)
        self.view_friends_sessions(friends_sessions_table)

        # Section: Plan a New Session
        section_label = QLabel("Plan Your Gaming Session")
        section_label.setStyleSheet("""
                    font-size: 20px;
                    font-weight: bold;
                    color: white; 
                    background-color: #293e4f;
                """)
        layout.addWidget(section_label)

        game_input = QLineEdit()
        game_input.setPlaceholderText("Enter game name")
        game_input.setStyleSheet("""
                    font-size: 20px;
                    font-weight: bold;
                    color: white; 
                    background-color: #293e4f;
                """)
        layout.addWidget(game_input)

        date_input = QDateEdit()
        date_input.setCalendarPopup(True)
        date_input.setDate(QDate.currentDate())
        date_input.setStyleSheet("""
                    font-size: 20px;
                    font-weight: bold;
                    color: white; 
                    background-color: #293e4f;
                """)
        layout.addWidget(date_input)

        time_input = QTimeEdit()
        time_input.setTime(QTime.currentTime())
        time_input.setStyleSheet("""
                    font-size: 20px;
                    font-weight: bold;
                    color: white; 
                    background-color: #293e4f;
                """)
        layout.addWidget(time_input)

        description_input = QLineEdit()
        description_input.setPlaceholderText("Add a description (optional)")
        description_input.setStyleSheet("""
                    font-size: 20px;
                    font-weight: bold;
                    color: white; 
                    background-color: #293e4f;
                """)
        layout.addWidget(description_input)

        plan_button = QPushButton("Plan Session")
        plan_button.setStyleSheet("""
                    font-size: 20px;
                    font-weight: bold;
                    color: white; 
                    background-color: #293e4f;
                """)
        plan_button.clicked.connect(lambda: self.plan_game_session(game_input, date_input, time_input, description_input))
        layout.addWidget(plan_button)

        return page


    def profile_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        page.setLayout(layout)

        # layout van avatar en username
        avatar_layout = QHBoxLayout()
        avatar_layout.setAlignment(Qt.AlignLeft)

        # avatar
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(100, 100)

        self.load_avatar()  # hier load hij een al bestaande avatar of nieuwe avatar
        avatar_layout.addWidget(self.avatar_label)

        # dit is de username die wordt opgehaald
        username = self.fetch_username()
        username_label = QLabel(f"Welcome, {username}")
        username_label.setStyleSheet("font-size: 25px; font-weight: bold; color: white;")
        avatar_layout.addWidget(username_label)

        layout.addLayout(avatar_layout)

        # knop voor de avatar om te uploaden
        upload_avatar_button = QPushButton("Upload Avatar")
        upload_avatar_button.setIcon(QIcon("upload_icon.png"))
        upload_avatar_button.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: white;
            background-color: #3a4e5f;
            border-radius: 10px;
            padding: 10px;
        """)
        upload_avatar_button.clicked.connect(self.upload_avatar)
        layout.addWidget(upload_avatar_button)

        layout.addSpacing(20)

        title_label = QLabel("Profile Settings")
        title_label.setStyleSheet("font-size: 30px; font-weight: bold; color: white;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # hiermee verander je je password
        password_label = QLabel("Change Password:")
        password_label.setStyleSheet("font-size: 20px; color: white;")
        layout.addWidget(password_label)

        password_input = QLineEdit()
        password_input.setPlaceholderText("Enter new password")
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setStyleSheet("""
            font-size: 18px;
            color: white;
            background-color: #1f2a38;
            border-radius: 10px;
            padding: 10px;
        """)
        layout.addWidget(password_input)

        change_password_button = QPushButton("Change Password")
        change_password_button.setIcon(QIcon("lock_icon.png"))
        change_password_button.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: white;
            background-color: #3a4e5f;
            border-radius: 10px;
            padding: 10px;
        """)
        layout.addWidget(change_password_button)

        # knop om uit te loggen
        logout_button = QPushButton("Logout")
        logout_button.setIcon(QIcon("logout_icon.png"))
        logout_button.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: white;
            background-color: #d9534f;
            border-radius: 10px;
            padding: 10px;
        """)
        layout.addWidget(logout_button)

        change_password_button.clicked.connect(lambda: self.change_password(password_input))
        logout_button.clicked.connect(self.logout)

        return page



    def lineare_regressie1(listX, listY, itterations, learningrate):
        a = 0
        b = 0
        for i in range(itterations):
            for j in range(len(listX)):
                error = (a + b * listX[j]) - listY[j]
                a = a - error * learningrate * 10000
                b = b - error * learningrate * listX[j]
        print(error, a, b)
        return a, b

    def lineare_regressie2(listX, listY, itterations, learningrate):
        a = 0
        b = 0
        for i in range(itterations):
            errorA = 0
            errorB = 0
            SSE = 0
            for j in range(len(listX)):
                errorA = errorA + 2 * a + 2 * b * listX[j] - 2 * listY[j]
                errorB = errorB + 2 * a * listX[j] - 2 * listY[j] * listX[j] + 2 * b * listX[j] ** 2
                SSE = SSE + ((a + b * listX[j]) - listY[j]) ** 2
            if abs(errorA) > 10:
                a = a - errorA * learningrate
            if abs(errorB) > 100000:
                b = b - min(abs(SSE / errorB), abs(errorB)) * errorB / abs(errorB) * learningrate
        return a, b

    def scatter_plot(self):
        # Create a Matplotlib figure and axis
        figure = Figure()
        ax = figure.add_subplot(111)

        # Data retrieval from the database
        owners = []
        ratio = []
        release_date = []
        query = """
            SELECT appid, name, release_date, positive_ratings, negative_ratings, owners, price
            FROM games
            WHERE positive_ratings > 0 AND (negative_ratings + positive_ratings > 50)
        """
        cursor.execute(query)
        data = cursor.fetchall()

        # Process the data for plotting
        for game in data:
            ratio.append((game[-4] / (game[-4] + game[-3])) * game[-2] ** (1 / 32))
            release_date.append(
                (int(str(game[2])[0:4]) - 1970) * 372 +
                (int(str(game[2])[5:7]) - 1) * 31 +
                int(str(game[2])[-2:]) - 1
            )

        # Plot the scatter plot and regression line
        ax.scatter(release_date, ratio, s=0.5, color='blue', label='Game Ratings')
        A, B = lineare_regressie2(release_date, ratio, 10000, 0.000001)
        xpoints = [min(release_date), max(release_date)]
        ypoints = [A + B * min(release_date), A + B * max(release_date)]
        ax.plot(xpoints, ypoints, color='red', label='Regression Line')

        # Customize the plot
        ax.set_title("Game Ratings Over Time")
        ax.set_xlabel("Release Date (Days Since Jan 1, 1970)")
        ax.set_ylabel("Positive Rating Ratio")
        ax.legend()

        # Create a canvas to embed the plot in PyQt
        canvas = FigureCanvas(figure)
        canvas.draw()  # This ensures the plot is rendered
        return canvas

    def fetch_random_games(self, table_widget):
        # Clear the table
        table_widget.setRowCount(0)

        # SQL query to get 5 random games
        query = """
            SELECT name, release_date, price
            FROM games
            ORDER BY RANDOM()
            LIMIT 5;
        """
        cursor.execute(query)
        games = cursor.fetchall()

        # Populate the table with random games
        table_widget.setRowCount(len(games))
        for row_index, game in enumerate(games):
            for col_index, value in enumerate(game):
                table_widget.setItem(row_index, col_index, QTableWidgetItem(str(value)))

    def plan_game_session(self, game_input, date_input, time_input, description_input):
        game_name = game_input.text()
        session_date = date_input.date().toString("yyyy-MM-dd")
        session_time = time_input.time().toString("HH:mm:ss")
        description = description_input.text()

        if not game_name:
            QMessageBox.warning(self, "Error", "Please enter a game name.")
            return

        query = """
            INSERT INTO game_sessions (accountnr, game_name, session_date, session_time, description)
            VALUES (%s, %s, %s, %s, %s);
        """
        try:
            cursor.execute(query, (self.accountnr, game_name, session_date, session_time, description))
            conn.commit()
            QMessageBox.information(self, "Success", "Gaming session planned!")
            game_input.clear()
            description_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to plan session: {str(e)}")

    def view_your_sessions(self, your_sessions_table):
        your_sessions_table.setRowCount(0)

        query = """
            SELECT game_name, session_date, session_time, description
            FROM game_sessions
            WHERE accountnr = %s
            ORDER BY session_date, session_time;
        """
        cursor.execute(query, (self.accountnr,))
        sessions = cursor.fetchall()

        for row_num, (game_name, session_date, session_time, description) in enumerate(sessions):
            your_sessions_table.insertRow(row_num)
            your_sessions_table.setItem(row_num, 0, QTableWidgetItem(game_name))
            your_sessions_table.setItem(row_num, 1, QTableWidgetItem(session_date.strftime("%Y-%m-%d")))
            your_sessions_table.setItem(row_num, 2, QTableWidgetItem(session_time.strftime("%H:%M")))
            your_sessions_table.setItem(row_num, 3, QTableWidgetItem(description or "No description"))

    def view_friends_sessions(self, friends_sessions_table):
        friends_sessions_table.setRowCount(0)

        query = """
            SELECT a.username, s.game_name, s.session_date, s.session_time
            FROM game_sessions s
            JOIN friends f ON s.accountnr = f.accountnr2
            JOIN accounts a ON f.accountnr2 = a.accountnr
            WHERE f.accountnr1 = %s
            ORDER BY s.session_date, s.session_time;
        """
        cursor.execute(query, (self.accountnr,))
        sessions = cursor.fetchall()

        for row_num, (username, game_name, session_date, session_time) in enumerate(sessions):
            friends_sessions_table.insertRow(row_num)
            friends_sessions_table.setItem(row_num, 0, QTableWidgetItem(username))
            friends_sessions_table.setItem(row_num, 1, QTableWidgetItem(game_name))
            friends_sessions_table.setItem(row_num, 2, QTableWidgetItem(session_date.strftime("%Y-%m-%d")))
            friends_sessions_table.setItem(row_num, 3, QTableWidgetItem(session_time.strftime("%H:%M")))

    def update_status(self, username, status):
        update_query = "UPDATE accounts SET status = %s WHERE username = %s;"
        cursor.execute(update_query, (status, username))
        conn.commit()

    def view_friends_with_status(self, friends_table):
        friends_table.setRowCount(0)

        query = """
            SELECT a.username, a.status
            FROM accounts a
            JOIN friends f ON a.accountnr = f.accountnr2
            WHERE f.accountnr1 = %s;
        """
        cursor.execute(query, (self.accountnr,))
        friends = cursor.fetchall()

        for row_num, (username, status) in enumerate(friends):
            friends_table.insertRow(row_num)
            friends_table.setItem(row_num, 0, QTableWidgetItem(username))

            # Create a status label with color coding
            status_label = QLabel("Online" if status == "online" else "Offline")
            status_label.setStyleSheet(
                "color: green;" if status == "online" else "color: red;"
            )
            friends_table.setCellWidget(row_num, 1, status_label)

    def load_avatar(self):
        avatar_path = f"./avatars/user_{self.accountnr}.png"
        if os.path.exists(avatar_path):
            pixmap = QPixmap(avatar_path)
        else:
            pixmap = QPixmap("./default_avatar.png")

        # hier wordt de avatar geresized
        pixmap = pixmap.scaled(self.avatar_label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        # hier wordt hij rond gemaakt
        mask = QPixmap(self.avatar_label.size())
        mask.fill(Qt.transparent)

        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, self.avatar_label.width(), self.avatar_label.height())
        painter.setBrush(QBrush(pixmap))
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        self.avatar_label.setPixmap(mask)

    def upload_avatar(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Avatar", "", "Image Files (*.png *.jpg *.jpeg)",
                                                   options=options)

        if file_path:
            if not os.path.exists("./avatars"):
                os.makedirs("./avatars")

            # hier wordt de avatar gesaved
            new_avatar_path = f"./avatars/user_{self.accountnr}.png"
            shutil.copy(file_path, new_avatar_path)
            self.load_avatar()
            tkmb.showinfo("Success", "Avatar uploaded successfully!")

    def fetch_username(self):
        query = "SELECT username FROM accounts WHERE accountnr = %s;"
        cursor.execute(query, (self.accountnr,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return "User"

    def add_game(self, results_table, hours_input):
        selected_row = results_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a game to add.")
            return

        # hier wordt de geselecteerde rij gepakt
        game_name_item = results_table.item(selected_row, 0)
        if not game_name_item:
            QMessageBox.warning(self, "Error", "Invalid game selection.")
            return

        gamenr = game_name_item.data(Qt.UserRole)  # hier wordt de gamenr aan de data gelinkt
        if gamenr is None:
            QMessageBox.warning(self, "Error", "Invalid game selection.")
            return

        # hier kan je de uren opschrijven
        try:
            hours = int(hours_input.text())
            if hours < 0:
                raise ValueError("Hours cannot be negative.")
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid non-negative number for hours.")
            return

        try:
            conn = psycopg2.connect(connection_string)
            cursor = conn.cursor()

            # hier wordt de game aan de library toegevoegd
            cursor.execute(
                """
                INSERT INTO library (accountnr, gamenr, hours)
                VALUES (%s, %s, %s)
                ON CONFLICT (accountnr, gamenr) DO UPDATE
                SET hours = EXCLUDED.hours
                """,
                (self.accountnr, gamenr, hours),
            )
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Game added to library successfully!")
        except psycopg2.Error as e:
            QMessageBox.warning(self, "Error", f"Could not add game: {e}")

    def search_games(self, search_box, results_table):
        search_query = search_box.text()
        if not search_query.strip():
            QMessageBox.warning(self, "Error", "Please enter a valid game name to search.")
            return

        try:
            conn = psycopg2.connect(connection_string)
            cursor = conn.cursor()

            # hiermee kan je games opzoeken
            cursor.execute(
                """
                SELECT appid, name
                FROM games
                WHERE name ILIKE %s
                """,
                (f"%{search_query}%",)
            )
            search_results = cursor.fetchall()
            conn.close()

            # hier wordt dan alles laten zien
            results_table.setRowCount(len(search_results))
            results_table.setColumnCount(1)
            results_table.setHorizontalHeaderLabels(["Game Name"])
            for row, (appid, name) in enumerate(search_results):
                item = QTableWidgetItem(name)
                item.setData(Qt.UserRole, appid)
                results_table.setItem(row, 0, item)

        except psycopg2.Error as e:
            QMessageBox.warning(self, "Error", f"Error searching games: {e}")

    def add_friend(self, username_input, friends_table):
        friend_username = username_input.text()

        try:
            conn = psycopg2.connect(connection_string)
            cursor = conn.cursor()

            # hier wordt het accountnr opgezocht van de vriend die je wil adden
            cursor.execute(
                """
                SELECT accountnr
                FROM accounts
                WHERE username = %s
                """,
                (friend_username,),
            )
            result = cursor.fetchone()

            if not result:
                QMessageBox.warning(self, "Error", "No user found with that username.")
                return

            friend_accountnr = result[0]

            # hier wordt dan je eigen accountnr met het accountnr van je vriend gekoppeld
            cursor.execute(
                """
                INSERT INTO friends (accountnr1, accountnr2)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                """,
                (self.accountnr, friend_accountnr),
            )
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", f"{friend_username} has been added as a friend!")
            self.view_friends(friends_table)  # hier wordt de friendlist geupdate

        except psycopg2.Error as e:
            QMessageBox.warning(self, "Error", f"Could not add friend: {e}")

    def view_most_played_games(self, games_table):
        games_table.setRowCount(0)

        query = """
            SELECT name, average_playtime
            FROM games
            GROUP BY name, average_playtime
            ORDER BY average_playtime DESC
            LIMIT 10;
        """
        cursor.execute(query)
        games = cursor.fetchall()

        for row_num, (name, average_playtime) in enumerate(games):
            games_table.insertRow(row_num)
            games_table.setItem(row_num, 0, QTableWidgetItem(name))
            games_table.setItem(row_num, 1, QTableWidgetItem(f"{average_playtime:.2f}"))

    def filter_games(self, search_text, games_table):
        for row in range(games_table.rowCount()):
            item = games_table.item(row, 0)
            if search_text.lower() in item.text().lower():
                games_table.setRowHidden(row, False)
            else:
                games_table.setRowHidden(row, True)

    def start_status_check(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.view_friends)
        self.timer.start(5000)  # Check every 5 seconds

    def closeEvent(self, event):
        self.logout()
        event.accept()




    def view_friends(self, friends_table):
        try:
            conn = psycopg2.connect(connection_string)
            cursor = conn.cursor()

            # hiermee kan je vrienden op username opzoeken
            cursor.execute(
                """
                SELECT a.username
                FROM friends f
                JOIN accounts a ON f.accountnr2 = a.accountnr
                WHERE f.accountnr1 = %s
                """,
                (self.accountnr,)
            )
            friends = cursor.fetchall()
            conn.close()

            # hier worden dan de vrienden neergezet
            friends_table.setRowCount(len(friends))
            friends_table.setHorizontalHeaderLabels(["Username"])
            for row, (username,) in enumerate(friends):
                friends_table.setItem(row, 0, QTableWidgetItem(username))

        except psycopg2.Error as e:
            QMessageBox.warning(self, "Error", f"Error loading friends list: {e}")

    def view_library(self, library_table):
        try:
            conn = psycopg2.connect(connection_string)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT g.name, l.hours
                FROM library l
                JOIN games g ON l.gamenr = g.appid
                WHERE l.accountnr = %s
                """,
                (self.accountnr,)
            )
            library_results = cursor.fetchall()
            conn.close()

            library_table.setColumnCount(2)
            library_table.setHorizontalHeaderLabels(["Game Name", "Hours Played"])
            library_table.setRowCount(len(library_results))
            for row, (gamename, hours) in enumerate(library_results):
                library_table.setItem(row, 0, QTableWidgetItem(gamename))
                library_table.setItem(row, 1, QTableWidgetItem(str(hours)))

        except psycopg2.Error as e:
            QMessageBox.warning(self, "Error", f"Error loading library: {e}")

    def view_friend_library(self, friends_table, library_table):
        # hier wordt ervoor gezorgd dat er iemand is geselecteerd
        selected_row = friends_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a friend to view their library.")
            return

        friend_username = friends_table.item(selected_row, 0).text().strip()
        if not friend_username:
            QMessageBox.warning(self, "Error", "Invalid friend selection.")
            return

        try:
            conn = psycopg2.connect(connection_string)
            cursor = conn.cursor()

            # hier wordt de library van de friend geladen
            cursor.execute(
                """
                SELECT g.name, l.hours
                FROM library l
                JOIN games g ON l.gamenr = g.appid
                WHERE l.accountnr = (
                    SELECT accountnr
                    FROM accounts
                    WHERE username = %s
                )
                """,
                (friend_username,)
            )
            friend_library = cursor.fetchall()
            conn.close()

            # hier wordt dan de library van de friend gedisplayed
            library_table.setRowCount(len(friend_library))
            library_table.setColumnCount(2)
            library_table.setHorizontalHeaderLabels(["Game Name", "Hours Played"])
            for row, (game_name, hours) in enumerate(friend_library):
                library_table.setItem(row, 0, QTableWidgetItem(game_name))
                library_table.setItem(row, 1, QTableWidgetItem(str(hours)))

            if not friend_library:
                QMessageBox.information(self, "Info", f"{friend_username} has no games in their library.")

        except psycopg2.Error as e:
            QMessageBox.warning(self, "Error", f"Error loading friend's library: {e}")

    def display_page(self, index):
        self.content_area.setCurrentIndex(index)

    def logout(self):
        query = "DELETE FROM active_sessions WHERE accountnr = %s;"
        cursor.execute(query, (self.accountnr,))
        conn.commit()
        self.close()
        print("Logging out...")



    def change_password(self, password_input):
        new_password = password_input.text()

        if not new_password:
            QMessageBox.critical(self, "Error", "Password cannot be empty.")
            return

        # hier wordt het nieuwe password gechecked
        if (
                len(new_password) < 8
                or not any(char.isdigit() for char in new_password)
                or not any(char.isupper() for char in new_password)
        ):
            QMessageBox.critical(
                self,
                "Error",
                "Password must:\n"
                "- Be at least 8 characters long\n"
                "- Contain at least 1 digit and 1 uppercase letter",
            )
            return

        hashed_password = hashlib.sha1(new_password.encode('utf-8')).hexdigest()

        # hier wordt het password geupdate
        update_query = "UPDATE accounts SET passwordhash = %s WHERE accountnr = %s;"
        try:
            cursor.execute(update_query, (hashed_password, self.accountnr))
            conn.commit()
            QMessageBox.information(self, "Success", "Password changed successfully!")
            password_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to change password: {str(e)}")


# dit is de login page
class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title("Steam Login")
        self.iconbitmap("steam_logo_round.ico")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        frame = ctk.CTkFrame(master=self)
        frame.pack(pady=20, padx=40, fill="both", expand=True)

        ctk.CTkLabel(master=frame, text="Login or Register", font=ctk.CTkFont(size=16)).pack(
            pady=12, padx=10
        )

        self.user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
        self.user_entry.pack(pady=12, padx=10)

        self.user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
        self.user_pass.pack(pady=12, padx=10)

        login_button = ctk.CTkButton(master=frame, text="Login", command=self.login_action)
        login_button.pack(pady=12, padx=10)

        signup_button = ctk.CTkButton(master=frame, text="Register", command=self.signup_action)
        signup_button.pack(pady=12, padx=10)

    def login_action(self):
        username = self.user_entry.get()
        password = self.user_pass.get()

        if self.login(username, password):
            tkmb.showinfo("Success", "Logged in successfully!")

            # hier wordt de accountnr opgehaald als je goed bent in gelogd
            accountnr_query = "SELECT accountnr FROM accounts WHERE username = %s;"
            cursor.execute(accountnr_query, (username,))
            accountnr = cursor.fetchone()
            query = "UPDATE accounts SET status = 'online' WHERE accountnr = %s;"
            cursor.execute(query, (accountnr,))
            conn.commit()
            if accountnr:
                self.open_main_app(accountnr[0])
            else:
                tkmb.showerror("Error", "Account number not found!")
        else:
            tkmb.showerror("Error", "Invalid username or password!")

    def signup_action(self):
        username = self.user_entry.get()
        password = self.user_pass.get()
        # hier wordt er gekeken of het password wel aan alle eisen voldoet
        if (
                len(password) < 8
                or not any(char.isdigit() for char in password)
                or not any(char.isupper() for char in password)
        ):
            tkmb.showerror(
                "Error",
                "Password must:\n"
                "- Be at least 8 characters long\n"
                "- Contain at least 1 digit and 1 uppercase letter",
            )
            return

        success, message = self.create_account(username, password)
        if success:
            tkmb.showinfo("Success", message)
        else:
            tkmb.showerror("Error", message)

    def login(self, username, password):
        query = 'SELECT passwordhash FROM accounts WHERE username = %s;'
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result is None:
            return False

        hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        return result[0] == hashed_password

    def create_account(self, username, password):
        check_query = 'SELECT username FROM accounts WHERE username = %s;'
        cursor.execute(check_query, (username,))
        if cursor.fetchone() is not None:
            return False, 'Username already exists.'

        hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        create_query = 'INSERT INTO accounts (username, passwordhash) VALUES (%s, %s);'
        cursor.execute(create_query, (username, hashed_password))
        conn.commit()

        return True, 'Account successfully created!'

    def open_main_app(self, accountnr):
        self.withdraw()  # hier wordt de login page gesloten en de main app geopend
        app = QApplication([])
        main_window = SteamApp(accountnr)
        main_window.show()
        app.exec_()


if __name__ == "__main__":
    login_page = LoginPage()
    login_page.mainloop()
    conn.close()