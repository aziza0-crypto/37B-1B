import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QListWidget)

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        
        self.setWindowTitle("To-Do List by Geeks")
        self.setFixedSize(400, 300)

        
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Введите новую задачу...")
        
        self.add_button = QPushButton("Добавить")
        self.delete_button = QPushButton("Удалить выбранное")
        
        self.task_list = QListWidget()

        
        layout = QVBoxLayout()
        
        
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.add_button)
        
        layout.addLayout(input_layout)
        layout.addWidget(self.task_list)
        layout.addWidget(self.delete_button)
        
        self.setLayout(layout)

        
        self.add_button.clicked.connect(self.add_task)
        self.delete_button.clicked.connect(self.delete_task)
        
        
        self.task_input.returnPressed.connect(self.add_task)

    def add_task(self):
        task_text = self.task_input.text().strip()
        if task_text:
            self.task_list.addItem(task_text)
            self.task_input.clear()

    def delete_task(self):
        
        current_item = self.task_list.currentItem()
        if current_item:
            
            row = self.task_list.row(current_item)
            self.task_list.takeItem(row)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec())
