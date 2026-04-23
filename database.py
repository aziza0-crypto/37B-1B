import sqlite3


class GameDatabase:

    STATUSES = ["Хочу играть", "Играю", "Пройдено", "Брошено"]
    GENRES = ["RPG", "Шутер", "Стратегия", "Инди", "Спорт", "Мультиплеер", "Хоррор", "Другое"]

    def __init__(self, path="games.db"):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._init_tables()
        self._seed()

    def _init_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                title   TEXT NOT NULL,
                genre   TEXT,
                rating  INTEGER DEFAULT 0,
                status  TEXT DEFAULT 'Хочу играть',
                hours   INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

    def _seed(self):
        self.cursor.execute("SELECT COUNT(*) FROM games")
        if self.cursor.fetchone()[0] == 0:
            sample = [
                ("CS2", "Шутер", 6, "Играю", 337),
                ("PUBGM", "Шутер", 10, "Играю", 6000),
                ("FIFA 21", "Спорт", 10, "Пройдено", 793),
            ]
            self.cursor.executemany(
                "INSERT INTO games (title, genre, rating, status, hours) VALUES (?, ?, ?, ?, ?)",
                sample
            )
            self.conn.commit()

    def add_game(self, title: str, genre: str, rating: int, status: str, hours: int) -> int:
        if status not in self.STATUSES:
            raise ValueError("Неверный статус")

        if genre not in self.GENRES:
            raise ValueError("Неверный жанр")

        rating = max(0, min(rating, 10))

        self.cursor.execute(
            "INSERT INTO games (title, genre, rating, status, hours) VALUES (?, ?, ?, ?, ?)",
            (title, genre, rating, status, hours)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all(self) -> list:
        self.cursor.execute("SELECT * FROM games ORDER BY rating DESC")
        return self.cursor.fetchall()

    def search_by_title(self, query: str) -> list:
        self.cursor.execute(
            "SELECT * FROM games WHERE title LIKE ? ORDER BY rating DESC",
            (f"%{query}%",)
        )
        return self.cursor.fetchall()

    def filter_by_status(self, status: str) -> list:
        self.cursor.execute(
            "SELECT * FROM games WHERE status = ? ORDER BY rating DESC",
            (status,)
        )
        return self.cursor.fetchall()

    def filter_by_genre(self, genre: str) -> list:
        self.cursor.execute(
            "SELECT * FROM games WHERE genre = ? ORDER BY hours DESC",
            (genre,)
        )
        return self.cursor.fetchall()

    def delete_game(self, game_id: int):
        self.cursor.execute("DELETE FROM games WHERE id = ?", (game_id,))
        self.conn.commit()

    def get_stats(self) -> dict:
        self.cursor.execute("SELECT COUNT(*) FROM games")
        total = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT SUM(hours) FROM games")
        hours = self.cursor.fetchone()[0] or 0

        self.cursor.execute(
            "SELECT COUNT(*) FROM games WHERE status = 'Пройдено'"
        )
        completed = self.cursor.fetchone()[0] or 0

        self.cursor.execute("SELECT AVG(rating) FROM games")
        avg = self.cursor.fetchone()[0] or 0

        return {
            "total": total,
            "hours": hours,
            "completed": completed,
            "avg_rating": round(avg, 1)
        }

    def close(self):
        self.conn.close()