import sqlite3

class TriangleDatabase:
    def __init__(self, db_name=":memory:"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                side1 REAL, side2 REAL, side3 REAL,
                triangle_type TEXT, error_message TEXT,
                PRIMARY KEY (side1, side2, side3)
            )
        """)
        self.conn.commit()

    def add_record(self, a, b, c, t_type, err):
        self.cursor.execute(
            "INSERT OR REPLACE INTO triangles VALUES (?, ?, ?, ?, ?)",
            (a, b, c, t_type, err)
        )
        self.conn.commit()

    def get_record(self, a, b, c):
        self.cursor.execute(
            "SELECT triangle_type, error_message FROM triangles WHERE side1=? AND side2=? AND side3=?",
            (a, b, c)
        )
        return self.cursor.fetchone()

    def delete_record(self, a, b, c):
        self.cursor.execute(
            "DELETE FROM triangles WHERE side1=? AND side2=? AND side3=?",
            (a, b, c)
        )
        self.conn.commit()