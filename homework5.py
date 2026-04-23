import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt

class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()
        
    
        self.rates = {
            "USD": 1.0,
            "EUR": 0.92,  
            "KGS": 87.5  
        }
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Конвертер валют (из USD)')
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()

        self.label_instruction = QLabel('Введите сумму в USD:')
        self.input_amount = QLineEdit()
        self.input_amount.setPlaceholderText("Например: 100")
        
        
        self.label_result = QLabel('Результат: 0.00')
        self.label_result.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        self.label_result.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.btn_to_kgs = QPushButton('В сомы (KGS)')
        self.btn_to_eur = QPushButton('В евро (EUR)')
        self.btn_clear = QPushButton('Очистить')

        
        self.btn_to_kgs.setMinimumHeight(40)
        self.btn_to_eur.setMinimumHeight(40)

    
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.btn_to_kgs)
        buttons_layout.addWidget(self.btn_to_eur)

        
        layout.addWidget(self.label_instruction)
        layout.addWidget(self.input_amount)
        layout.addLayout(buttons_layout)
        layout.addWidget(self.btn_clear)
        layout.addStretch()
        layout.addWidget(self.label_result)
        layout.addStretch()

        self.setLayout(layout)

    
        self.btn_to_kgs.clicked.connect(lambda: self.convert("KGS"))
        self.btn_to_eur.clicked.connect(lambda: self.convert("EUR"))
        self.btn_clear.clicked.connect(self.clear_fields)

    def convert(self, target_currency):
        try:
            
            raw_text = self.input_amount.text().strip().replace(',', '.')
            
            if not raw_text:
                raise ValueError("Пустое поле")
                
            amount = float(raw_text)
            
            if amount < 0:
                raise ValueError("Отрицательное число")
            
            
            result = amount * self.rates[target_currency]
            
            self.label_result.setText(f"Результат: {result:.2f} {target_currency}")
            
        except ValueError:
            QMessageBox.warning(self, "Ошибка ввода", "Введите положительное числовое значение!")
            self.input_amount.clear()
            self.label_result.setText("Результат: 0.00")

    def clear_fields(self):
        self.input_amount.clear()
        self.label_result.setText("Результат: 0.00")
        self.input_amount.setFocus()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CurrencyConverter()
    ex.show()
    sys.exit(app.exec())

