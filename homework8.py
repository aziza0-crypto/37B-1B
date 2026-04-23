import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTableView, QLabel, 
                             QLineEdit, QFormLayout, QMessageBox, QAbstractItemView)
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtCore import Qt

class ContactApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Контакты SQLite")
        self.resize(600, 500)

    
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("contacts.db")
        if not self.db.open():
            QMessageBox.critical(None, "Ошибка", "Не удалось открыть базу данных")
            sys.exit(1)

        self.db.exec("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT
            )
        """)

        
        self.model = QSqlTableModel(self)
        self.model.setTable("contacts")
        
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.model.select()
        
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Orientation.Horizontal, "Имя")
        self.model.setHeaderData(2, Qt.Orientation.Horizontal, "Телефон")
        self.model.setHeaderData(3, Qt.Orientation.Horizontal, "Email")

        self.init_ui()
        self.update_count()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Поиск
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по имени...")
        self.search_input.textChanged.connect(self.filter_contacts)
        main_layout.addWidget(self.search_input)

        
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        main_layout.addWidget(self.view)

        
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        form_layout.addRow("Имя:", self.name_input)
        form_layout.addRow("Телефон:", self.phone_input)
        form_layout.addRow("Email:", self.email_input)
        main_layout.addLayout(form_layout)

    
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.add_contact)
        
        
        save_btn = QPushButton("Сохранить изменения")
        save_btn.clicked.connect(self.save_changes)
        
        del_btn = QPushButton("Удалить")
        del_btn.clicked.connect(self.delete_contact)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(del_btn)
        main_layout.addLayout(btn_layout)

        self.count_label = QLabel()
        main_layout.addWidget(self.count_label)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container) 

    def filter_contacts(self, text):
        self.model.setFilter(f"name LIKE '%{text}%'")
        self.model.select()
        self.update_count()

    def add_contact(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Имя обязательно!")
            return

        row = self.model.rowCount()
        self.model.insertRow(row)
        self.model.setData(self.model.index(row, 1), name)
        self.model.setData(self.model.index(row, 2), self.phone_input.text())
        self.model.setData(self.model.index(row, 3), self.email_input.text())
        
        if self.model.submitAll():
            self.name_input.clear()
            self.phone_input.clear()
            self.email_input.clear()
            self.update_count()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось сохранить контакт")

    def save_changes(self):
        
        if self.model.submitAll():
            QMessageBox.information(self, "Успех", "Изменения сохранены!")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось сохранить")

    def delete_contact(self):
        selected = self.view.selectionModel().selectedRows()
        if not selected:
            return

        reply = QMessageBox.question(self, "Удаление", "Удалить выбранный контакт?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            for index in selected:
                self.model.removeRow(index.row())
            self.model.submitAll()
            self.update_count()

    def update_count(self):
    
        count = self.model.rowCount()
        self.count_label.setText(f"Контактов: {count}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContactApp()
    window.show()
    sys.exit(app.exec())
