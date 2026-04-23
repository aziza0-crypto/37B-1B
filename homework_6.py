import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QComboBox,QPushButton, QListWidget)

class TaskListApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWidgetTitle("Task List by Geeks")
        self.setFixedSize(400, 300)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Ведите задачу ....")

        self.priority_combo = QComboBox()
        self.priority_combo.addItems["Высокий", "Средний", "Низкий"]

        self.add_button = QPushButton("Добавить")
        self.delete__button = QPushButton("Удалить выбронное")

        self.task_list = QLisrWidget()

        layout = QVBoxLayout

        top_layout = QVBoxLayout()
        top_layout.addWidget(self.task_input)
        top_layout.addWidget(self.priority_combo)

        layout.addlayout(top_layout)
        layout.addWidget(self.add_button)
        layout.addWidget(self.task_list)
        layout.addWidget(self.delete__button)

        self.setLayout(layout)

        self.add_button.clicked.connect(self.add_task)
        self.delete_button.clicked.connect(self.delete_button)
    
    def add_task(self):
        task_text = self.task_input.text().strip()
        priority = self.priority_combo.currenText()

        if task_text:
            full_task_string = f"[{priority}] {task_text}"
            self.task_list.addItem(full_task_string)

            self.task_input.clear()

    def delete_task(self):
        current_item = self.task_list.currentItem()
        if current_item:
            row = self.task_list.row(current_item)
            self.task_list.takeItem(row)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskListApp()
    window.show()
    sys.exit(app.exec())

