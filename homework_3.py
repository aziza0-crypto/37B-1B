import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        
        self.result_label = QLabel("Здесь появится ваш текст")
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Введите что-нибудь...")
        
        self.display_button = QPushButton("Вывести текст")
        self.exit_button = QPushButton("Закрыть приложение")

        
        layout = QVBoxLayout()
        layout.addWidget(self.result_label)
        layout.addWidget(self.user_input)
        layout.addWidget(self.display_button)
        layout.addWidget(self.exit_button)
        
        self.setLayout(layout)
        self.setWindowTitle("Графическое приложение PyQt6")
        self.resize(300, 150) 

        
        self.display_button.clicked.connect(self.update_label)
        self.exit_button.clicked.connect(self.close) 

    def update_label(self):
        
        text = self.user_input.text()
        if text.strip():
            self.result_label.setText(text)
        else:
            self.result_label.setText("Поле пустое!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec())
