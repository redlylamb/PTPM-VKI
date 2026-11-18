import unittest
from src.database import DatabaseRepository


class TestDatabaseRepository(unittest.TestCase):
    """Модульные тесты для класса DatabaseRepository."""

    def setUp(self) -> None:
        self.repo = DatabaseRepository(":memory:")

    def tearDown(self) -> None:
        self.repo.close()

    # --- Тесты для add ---
    def test_add_success(self) -> None:
        result = self.repo.add(1, "user_one", "<p>Привет мир</p>")
        self.assertTrue(result)

        record = self.repo.get_by_id(1)
        self.assertIsNotNone(record)
        self.assertEqual(record["name"], "user_one")
        self.assertEqual(record["message"], "<p>Привет мир</p>")

    def test_add_duplicate_id_raises_error(self) -> None:
        self.repo.add(10, "user_one", "Первое сообщение")
        with self.assertRaises(ValueError):
            self.repo.add(10, "user_two", "Дубликат ID")

    def test_add_validation_errors(self) -> None:
        with self.assertRaises(ValueError):
            self.repo.add(2, "a" * 257, "Текст")

        with self.assertRaises(ValueError):
            self.repo.add(3, "valid_user", "x" * 8097)

        with self.assertRaises(TypeError):
            self.repo.add(True, "valid_user", "Текст")

    # --- Тесты для get_by_id ---
    def test_get_by_id_existing(self) -> None:
        self.repo.add(42, "alice", "Тестовый текст")
        record = self.repo.get_by_id(42)
        self.assertEqual(record, {"id": 42, "name": "alice", "message": "Тестовый текст"})

    def test_get_by_id_not_found(self) -> None:
        record = self.repo.get_by_id(9999)
        self.assertIsNone(record)

    # --- Тесты для get_by_name ---
    def test_get_by_name_multiple_records(self) -> None:
        self.repo.add(1, "bob", "Первый коммент")
        self.repo.add(2, "alice", "Чужой коммент")
        self.repo.add(3, "bob", "Второй коммент")

        bob_records = self.repo.get_by_name("bob")
        self.assertEqual(len(bob_records), 2)
        self.assertEqual(bob_records[0]["id"], 1)
        self.assertEqual(bob_records[1]["id"], 3)

    def test_get_by_name_empty(self) -> None:
        records = self.repo.get_by_name("non_existent_user")
        self.assertEqual(records, [])

    # --- Тесты для update ---
    def test_update_existing_success(self) -> None:
        self.repo.add(5, "charlie", "Старый текст")
        updated = self.repo.update(5, "Новый текст")
        self.assertTrue(updated)

        record = self.repo.get_by_id(5)
        self.assertEqual(record["message"], "Новый текст")

    def test_update_non_existent_returns_false(self) -> None:
        updated = self.repo.update(777, "Текст в никуда")
        self.assertFalse(updated)

    def test_update_too_long_message_raises_error(self) -> None:
        self.repo.add(6, "charlie", "Нормальный текст")
        with self.assertRaises(ValueError):
            self.repo.update(6, "z" * 8097)

    # --- Тесты для delete ---
    def test_delete_existing_success(self) -> None:
        self.repo.add(8, "dave", "Удаляемое сообщение")
        deleted = self.repo.delete(8)
        self.assertTrue(deleted)
        self.assertIsNone(self.repo.get_by_id(8))

    def test_delete_non_existent_returns_false(self) -> None:
        deleted = self.repo.delete(8888)
        self.assertFalse(deleted)


if __name__ == "__main__":
    unittest.main()