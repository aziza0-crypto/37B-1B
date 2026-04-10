import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

class GreetingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите ваше имя...")
        
        self.greet_button = QPushButton("Поздороваться")
        self.clear_button = QPushButton("Очистить")
        
        self.result_label = QLabel("")

        
        layout = QVBoxLayout()
        layout.addWidget(self.name_input)
        layout.addWidget(self.greet_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.result_label)
        
        self.setLayout(layout)
        self.setWindowTitle("Окно приветствия")

        
        self.greet_button.clicked.connect(self.say_hello)
        self.clear_button.clicked.connect(self.clear_fields)

    def say_hello(self):
        name = self.name_input.text().strip()
        if name:
            self.result_label.setText(f"Привет, {name}!")
        else:
            self.result_label.setText("Введите имя!")

    def clear_fields(self):
        self.name_input.clear()
        self.result_label.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GreetingApp()
    window.show()
    sys.exit(app.exec())
