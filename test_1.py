import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,QTabelWidget,
    QTableWidgetItem, QPushButton, QLainEdit,
    QLabel, QMessageBox
)

def connect_db():
    return sqlite3.connect("tasks.db")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL

""")
    conn.commit()
    conn.closed()

class MainWindow(QWidget):
    def __init__(self):  
        super().__init__()
        init_db()
        self.init_ui()
        self.load_tasks()
    
    def init_ui(self):
        self.setWindowTitle("Менеджер задач")
        self.resize(400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("ВВедите задачу:")
        self.input_task = QLainEdit()

           
        self.btn_add = QPushButton("Добавить")
        self.btn_delete = QPushButton("Удалить выбранную")

        self.list_widget = QListWidget()

        layout.add.Widget(self.label)
        layout.add.Widget(self.input_task)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_delete)
        layout.addLayout(btn_layout)

        layout.add.Widget(self.list_widget)
        self.setLayout(layout)

        self.btn_add.clicked.connect(self.add_task)
        self.btn_delete.clicked.connect(self.delete_task)

    def load_tasks(self):
        self.list_widget.clear()
        tasks = self.get_tasks()
        for task_id, text in tasks:

            self.list_widget.additem(text)
            self.list_widget.item(self.list_widget.count() - 1).setDate(Qt.ItemDataRole.UserRole, task_id)
        
    def get_tasks(self):
        """Получает список всех задач из БД."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, text FROM tasks")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_task(self):
        """Добавляет задачу в базу и обновляет интерфейс."""
        text = self.input_task.text().strip()
       
        if text:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (text) VALUES (?)", (text,))
            conn.commit()
            conn.close()
            
            self.input_task.clear()
            self.load_tasks()
        else:
            QMessageBox.warning(self, "Ошибка", "Текст задачи не может быть пустым!")

    def delete_task(self):
        """Удаляет выбранную задачу по её ID."""
        selected_item = self.list_widget.currentItem()
        if selected_item:
        
            task_id = selected_item.data(Qt.ItemDataRole.UserRole)
            
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            conn.close()
            
            self.load_tasks()
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу для удаления!")  

if __name__ == "__main__":  
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())







        













    


