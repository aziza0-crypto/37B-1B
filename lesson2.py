#1 код
# import sys 
# from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

# app = QApplication(sys.argv)

# window = QMainWindow()
# window.setWindowTitle("Наше первое окно")
# window.resize(400, 300)

# label = QLabel("Привет, PyQt6", window)
# label.move(150, 130)

# window.show()
# sys.exit(app.exec())

#2 код

# import sys

# from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton

# app = QApplication(sys.argv)
# window = QMainWindow()
# window.setWwindow("Плохой пример Дуукомпазиции")
# window.resize(400, 300)

# label = QLabel("Счет 0", window)

# label.move(160, 100)
# label.resize(100, 30)


# count = 0

# button = QPushButton("Нажать", window)

# def on_click(): 
#     global count
#     count += 1
#     label.setText(f"Счет: {count}")

# button.clicked.connect(on_click)
# window.show()
# sys.exir(app.exec())

#3 код
# import sys
# from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.count = 0 
#         self.init_ui()

#     def init_ui(self):
#         self.setWiwndowTitle("Хороший пример Дукомпозиции")
#         self.resize(400, 300)

#         self.label = QLabel("Счет: 0", self)
#         self.label.move(160, 100)
#         self.label.resize(100. 30)

#         self.button.click(self.on_button_click)

#     def on_button_click(self):
#         self.count += 1
#         self.label.setText(f"Счет: {self.count}")

# def main():
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exet(app.exec())

#     if __name__ == '__main__':
#         main()

#4 код
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QPushButton, QLabel, QLineEdit
)

class SignalDemo(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Сигналы и слоты")
        self.resize(450, 250)

        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Введите имя...")
        self.input.move(50, 50)
        self.input.resize(200, 35)

        self.btn = QPushButton("Поздороваться", self)
        self.btn.move(270, 50)
        self.btn.resize(140, 35)

        self.label = QLabel("", self)
        self.label.move(50, 120)
        self.label.resize(350, 40)

        self.btn.clicked.connect(self.greet)


        self.input.returnPressed.connect(self.greet)

    def greet(self):
        name = self.input.text().strip()
        if name:
            self.label.setText(f"Привет, {name}! Добро пожаловать в PyQt6!")
        else:
            self.label.setText("Введите имя!")


def main():
    app = QApplication(sys.argv)
    w = SignalDemo()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
