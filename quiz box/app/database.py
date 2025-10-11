import sqlite3
from datetime import datetime


class QuizDatabase:
    def __init__(self, db_name="data.db"):
        # Kết nối tới SQLite (nếu chưa có file sẽ tự tạo)
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        """Tạo bảng nếu chưa có"""
        query = """
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            score INTEGER NOT NULL,
            created_date TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    # Viết cho tôi document về các tham số và kiểu trả về

    def add_result(self, name, unit, score) -> int:
        """Thêm kết quả mới và trả về id của bản ghi"""
        created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = (
            "INSERT INTO results (name, unit, score, created_date) VALUES (?, ?, ?, ?)"
        )
        cursor = self.conn.execute(query, (name, unit, score, created_date))
        self.conn.commit()
        return cursor.lastrowid

    def get_result_by_id(self, result_id):
        """Lấy kết quả theo id"""
        cursor = self.conn.execute(
            "SELECT * FROM results WHERE id = ?", (result_id,)
        )
        return cursor.fetchone()

    def get_all_results(self):
        """Lấy toàn bộ dữ liệu"""
        cursor = self.conn.execute("SELECT * FROM results ORDER BY created_date DESC")
        return cursor.fetchall()

    def get_top_scores(self, limit=5):
        """Lấy top điểm cao nhất"""
        cursor = self.conn.execute(
            "SELECT name, unit, score, created_date FROM results ORDER BY score DESC LIMIT ?",
            (limit,),
        )
        return cursor.fetchall()

    def close(self):
        """Đóng kết nối"""
        self.conn.close()
