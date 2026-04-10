 # import sqlite3
#
# conn = sqlite3.connect("academy.db")
#
# cursor = conn.cursor()
#
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS students (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         age INTEGER,
#         city TEXT
#     )
# """)
#
# cursor.execute(
#     "INSERT INTO students (name, age, city) VALUES (?, ?, ?)",
#     ("Азиза", 18, "Ош")
# )
# cursor.execute(
#     "INSERT INTO students (name, age, city) VALUES (?, ?, ?)",
#     ("Ислам", 18, "Ош")
# )
# cursor.execute(
#     "INSERT INTO students (name, age, city) VALUES (?, ?, ?)",
#     ("АБдуллох", 18, "Ош")
# )
#
# conn.commit()
#
# cursor.execute("SELECT * FROM students")
# rows = cursor.fetchall()
#
# print("Все студенты:")
# for row in rows:
#     print(row)
# conn.close()

import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit,
    QLabel, QMessageBox
)

class Database:
    def __init__(self, path="geeks.db"):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self._init()

    def _init(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                city TEXT
            )
        """)
        self.cursor.execute("SELECT COUNT(*) FROM students")
        if self.cursor.fetchone()[0] == 0:
            data = [
                ("Ажибек", 22, "Ош"),
                ("Тимур", 22, "Бишкек"),
                ("Эмили", 19, "Москва"),
            ]
            self.cursor.executemany(
                "INSERT INTO students (name, age, city) VALUES (?, ?, ?)", data
            )
            self.conn.commit()

    def get_all(self):
        self.cursor.execute("SELECT * FROM students ORDER BY id")
        return self.cursor.fetchall()

    def add(self, name, age, city):
        self.cursor.execute(
            "INSERT INTO students (name, age, city) VALUES (?, ?, ?)",
            (name, age, city)
        )
        self.conn.commit()

    def close(self):
        self.conn.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setWindowTitle("Студенты - база данных")
        self.resize(600, 480)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Список студентов:"))

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Имя", "Возраст", "Город"])
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        layout.addWidget(QLabel("Добавить студента:"))
        form_layout = QHBoxLayout()

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Имя")

        self.input_age = QLineEdit()
        self.input_age.setPlaceholderText("Возраст")
        self.input_age.setMaximumWidth(70)

        self.input_city = QLineEdit()
        self.input_city.setPlaceholderText("Город")

        btn_add = QPushButton("Добавить")
        btn_add.clicked.connect(self.add_student)

        btn_refresh = QPushButton("Обновить")
        btn_refresh.clicked.connect(self.load_data)

        form_layout.addWidget(self.input_name)
        form_layout.addWidget(self.input_age)
        form_layout.addWidget(self.input_city)
        form_layout.addWidget(btn_add)
        form_layout.addWidget(btn_refresh)
        layout.addLayout(form_layout)

        

    def load_data(self):
        rows = self.db.get_all()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    def add_student(self):
        name = self.input_name.text().strip()
        age = self.input_age.text().strip()
        city = self.input_city.text().strip()

        if not name or not age or not city:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return
        if not age.isdigit():
            QMessageBox.warning(self, "Ошибка", "Возраст должен быть числом")
            return

        self.db.add(name, int(age), city)
        self.input_name.clear()
        self.input_age.clear()
        self.input_city.clear()
        self.load_data()

    def closeEvent(self, event):
        self.db.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

