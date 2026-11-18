import sqlite3
from typing import Any, Dict, List, Optional


class DatabaseRepository:
    """Репозиторий для работы с таблицей comments в SQLite."""

    MAX_NAME_LENGTH = 256
    MAX_MESSAGE_LENGTH = 8096

    def __init__(self, db_path: str = ":memory:") -> None:
        """Инициализирует подключение к БД и создает таблицу при необходимости."""
        if not isinstance(db_path, str) or not db_path.strip():
            raise ValueError("Путь к базе данных должен быть непустой строкой.")

        self.db_path = db_path
        # Используем постоянное соединение, чтобы корректно работала БД в памяти (':memory:')
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self) -> None:
        """Создает таблицу comments с ограничениями на уровне БД."""
        query = """
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL CHECK(length(name) <= 256),
            message TEXT NOT NULL CHECK(length(message) <= 8096)
        );
        """
        with self._conn:
            self._conn.execute(query)

    def _validate_id(self, comment_id: Any) -> None:
        """Проверяет, что ID является целым числом (исключая bool)."""
        if isinstance(comment_id, bool) or not isinstance(comment_id, int):
            raise TypeError("comment_id должен быть целым числом (int).")

    def _validate_name(self, username: Any) -> None:
        """Проверяет тип и длину логина пользователя."""
        if not isinstance(username, str):
            raise TypeError("username должен быть строкой (str).")
        if not username.strip():
            raise ValueError("username не может быть пустым.")
        if len(username) > self.MAX_NAME_LENGTH:
            raise ValueError(
                f"Длина username не должна превышать {self.MAX_NAME_LENGTH} символов."
            )

    def _validate_message(self, message: Any) -> None:
        """Проверяет тип и длину текста сообщения."""
        if not isinstance(message, str):
            raise TypeError("message должен быть строкой (str).")
        if len(message) > self.MAX_MESSAGE_LENGTH:
            raise ValueError(
                f"Длина message не должна превышать {self.MAX_MESSAGE_LENGTH} символов."
            )

    def get_by_id(self, comment_id: int) -> Optional[Dict[str, Any]]:
        """Возвращает запись по ID в виде словаря или None, если запись не найдена."""
        self._validate_id(comment_id)

        query = "SELECT id, name, message FROM comments WHERE id = ?;"
        cursor = self._conn.execute(query, (comment_id,))
        row = cursor.fetchone()

        return dict(row) if row else None

    def get_by_name(self, username: str) -> List[Dict[str, Any]]:
        """Возвращает список всех записей указанного пользователя."""
        if not isinstance(username, str):
            raise TypeError("username должен быть строкой (str).")

        query = "SELECT id, name, message FROM comments WHERE name = ?;"
        cursor = self._conn.execute(query, (username,))
        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    def add(self, comment_id: int, username: str, message: str) -> bool:
        """Валидирует данные и добавляет новую запись в БД. Возвращает True при успехе."""
        self._validate_id(comment_id)
        self._validate_name(username)
        self._validate_message(message)

        query = "INSERT INTO comments (id, name, message) VALUES (?, ?, ?);"
        try:
            with self._conn:
                self._conn.execute(query, (comment_id, username, message))
            return True
        except sqlite3.IntegrityError as exc:
            raise ValueError(f"Запись с id={comment_id} уже существует.") from exc

    def update(self, comment_id: int, new_message: str) -> bool:
        """Обновляет текст сообщения у существующей записи. Возвращает True, если запись обновлена."""
        self._validate_id(comment_id)
        self._validate_message(new_message)
        query = "UPDATE comments SET message = ? WHERE id = ?;"
        with self._conn:
            cursor = self._conn.execute(query, (new_message, comment_id))

        return cursor.rowcount > 0

    def delete(self, comment_id: int) -> bool:
        """Удаляет запись по ID. Возвращает True, если запись была удалена."""
        self._validate_id(comment_id)

        query = "DELETE FROM comments WHERE id = ?;"
        with self._conn:
            cursor = self._conn.execute(query, (comment_id,))

        return cursor.rowcount > 0

    def close(self) -> None:
        """Закрывает соединение с базой данных."""
        self._conn.close()

    def __enter__(self) -> "DatabaseRepository":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()