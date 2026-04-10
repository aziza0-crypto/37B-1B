import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QLineEdit, QPushButton,
    QCheckBox, QRadioButton, QComboBox,
    QSpinBox, QTextEdit, QVBoxLayout
)

class Widgets(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Все базовые виджеты")
        self.resize(400, 500)
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        layout.addWidget(QLabel("QLabel - просто текст"))

        self.line = QLineEdit()
        self.line.setPlaceholderText("QLineEdit - введите текст...")
        layout.addWidget(self.line)

        btn = QPushButton("QPushButton - нажми меня")
        btn.clicked.connect(self.on_btn)
        layout.addWidget(btn)

        self.check = QCheckBox("QCheckBox - согласен с условиями")
        layout.addWidget(self.check)

        layout.addWidget(QLabel("QRadioButton"))
        self.radio_m = QRadioButton("Мужской")
        self.radio_f = QRadioButton("Женский")
        self.radio_m.setChecked(True)
        layout.addWidget(self.radio_m)
        layout.addWidget(self.radio_f)

        self.combo = QComboBox()
        self.combo.addItems(["Python", "Go", "Java", "JavaScript", "C++"])
        layout.addWidget(self.combo)

        self.spin = QSpinBox()
        self.spin.setRange(0, 100)
        self.spin.setValue(18)
        layout.addWidget(QLabel("QSpinBox - возраст:"))
        layout.addWidget(self.spin)

        self.text = QTextEdit()
        self.text.setPlaceholderText("QTextEdit - многострочный текст...")
        self.text.setMaximumHeight(80)
        layout.addWidget(self.text)

        self.result = QLabel("Нажми кнопку чтобы увидеть значения")
        self.result.setWordWrap(True)
        layout.addWidget(self.result)

    def on_btn(self):
        gender = "Мужской" if self.radio_m.isChecked() else "Женский"
        info = (
            f"Текст: {self.line.text()}\n"
            f"Чекбокс: {self.check.isChecked()}\n"
            f"Пол: {gender}\n"
            f"Язык: {self.combo.currentText()}\n"
            f"Возраст: {self.spin.value()}\n"
            f"Описание: {self.text.toPlainText()[:30]}..."
        )
        self.result.setText(info)

def main():
    app = QApplication(sys.argv)
    w = Widgets()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
