import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit,
    QLabel, QComboBox, QSpinBox, QMessageBox, QHeaderView, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from database import GameDatabase

STATUS_COLORS = {
    "Играю": "#d4edda",
    "Пройдено": "#cce5ff",
    "Хочу играть": "#fff3cd",
    "Брошено": "#f8d7da",
}


class GameVault(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = GameDatabase()
        self.setWindowTitle("Моя библиотека игр")
        self.resize(900, 600)

        self.init_ui()
        self.load_table()
        self.update_stats()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        root.addLayout(self._build_header())
        root.addLayout(self._build_filters())
        root.addWidget(self._build_table())

        root.addWidget(self._build_divider("Добавить игру"))
        root.addLayout(self._build_add_form())

    def _build_header(self):
        layout = QHBoxLayout()

        title = QLabel("GameVault")
        title.setStyleSheet("font-size:20px; font-weight:bold;")
        layout.addWidget(title)
        layout.addStretch()

        self.lbl_total = QLabel()
        self.lbl_hours = QLabel()
        self.lbl_completed = QLabel()
        self.lbl_avg = QLabel()

        for lbl in [self.lbl_total, self.lbl_hours, self.lbl_completed, self.lbl_avg]:
            lbl.setStyleSheet(
                "background:#f0f0f0; padding:4px 10px; border-radius:8px; font-size:12px;"
            )
            layout.addWidget(lbl)

        return layout

    def _build_filters(self):
        layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию")
        self.search_input.textChanged.connect(self.on_search)

        self.filter_status = QComboBox()
        self.filter_status.addItem("Все статусы")
        self.filter_status.addItems(GameDatabase.STATUSES)
        self.filter_status.currentTextChanged.connect(self.on_filter)

        self.filter_genre = QComboBox()
        self.filter_genre.addItem("Все жанры")
        self.filter_genre.addItems(GameDatabase.GENRES)
        self.filter_genre.currentTextChanged.connect(self.on_filter)

        btn_reset = QPushButton("Сбросить")
        btn_reset.clicked.connect(self.reset_filters)

        layout.addWidget(QLabel("Поиск:"))
        layout.addWidget(self.search_input)
        layout.addWidget(QLabel("Статус:"))
        layout.addWidget(self.filter_status)
        layout.addWidget(QLabel("Жанр:"))
        layout.addWidget(self.filter_genre)
        layout.addWidget(btn_reset)

        return layout

    def _build_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Название", "Жанр", "Рейтинг", "Статус", "Часов"]
        )

        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        self.table.doubleClicked.connect(self.on_double_click)

        return self.table

    def _build_add_form(self):
        layout = QHBoxLayout()

        self.inp_title = QLineEdit()
        self.inp_title.setPlaceholderText("Название игры")

        self.inp_genre = QComboBox()
        self.inp_genre.addItems(GameDatabase.GENRES)

        self.inp_rating = QSpinBox()
        self.inp_rating.setRange(1, 10)

        self.inp_status = QComboBox()
        self.inp_status.addItems(GameDatabase.STATUSES)

        self.inp_hours = QSpinBox()
        self.inp_hours.setRange(0, 99999)

        btn_add = QPushButton("Добавить")
        btn_add.clicked.connect(self.add_game)

        btn_del = QPushButton("Удалить")
        btn_del.clicked.connect(self.delete_selected)

        layout.addWidget(self.inp_title)
        layout.addWidget(self.inp_genre)
        layout.addWidget(self.inp_rating)
        layout.addWidget(self.inp_status)
        layout.addWidget(self.inp_hours)
        layout.addWidget(btn_add)
        layout.addWidget(btn_del)

        return layout

    def _build_divider(self, text):
        frame = QFrame()
        layout = QHBoxLayout(frame)

        lbl = QLabel(text)
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)

        layout.addWidget(lbl)
        layout.addWidget(line)

        return frame

    def load_table(self, rows=None):
        if rows is None:
            rows = self.db.get_all()

        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            values = [
                row["id"], row["title"], row["genre"],
                f"{'★'*row['rating']} ({row['rating']})",
                row["status"], row["hours"]
            ]

            for j, val in enumerate(values):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                color = STATUS_COLORS.get(row["status"], "#ffffff")
                item.setBackground(QColor(color))

                self.table.setItem(i, j, item)

    def update_stats(self):
        stats = self.db.get_stats()
        self.lbl_total.setText(f"Игр: {stats['total']}")
        self.lbl_hours.setText(f"Часов: {stats['hours']}")
        self.lbl_completed.setText(f"Пройдено: {stats['completed']}")
        self.lbl_avg.setText(f"Средний рейтинг: {stats['avg_rating']}")

    def add_game(self):
        title = self.inp_title.text().strip()
        if not title:
            QMessageBox.warning(self, "Ошибка", "Введите название!")
            return

        self.db.add_game(
            title=title,
            genre=self.inp_genre.currentText(),
            rating=self.inp_rating.value(),
            status=self.inp_status.currentText(),
            hours=self.inp_hours.value()
        )

        self.load_table()
        self.update_stats()

    def delete_selected(self):
        row = self.table.currentRow()
        if row < 0:
            return

        game_id = int(self.table.item(row, 0).text())

        reply = QMessageBox.question(
            self, "Удаление", "Удалить игру?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_game(game_id)
            self.load_table()
            self.update_stats()

    def on_double_click(self):
        self.delete_selected()

    def on_search(self, text):
        if text.strip():
            self.load_table(self.db.search_by_title(text))
        else:
            self.on_filter()

    def on_filter(self):
        status = self.filter_status.currentText()
        genre = self.filter_genre.currentText()

        if status != "Все статусы":
            rows = self.db.filter_by_status(status)
        elif genre != "Все жанры":
            rows = self.db.filter_by_genre(genre)
        else:
            rows = self.db.get_all()

        self.load_table(rows)

    def reset_filters(self):
        self.search_input.clear()
        self.filter_status.setCurrentIndex(0)
        self.filter_genre.setCurrentIndex(0)
        self.load_table()

    def closeEvent(self, event):
        self.db.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    w = GameVault()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
