import unittest
from src.database import DatabaseRepository
from src.parser import ForumParser


class TestForumParser(unittest.TestCase):
    """Тесты для класса ForumParser на реальной странице Habr."""

    TEST_URL = "https://habr.com/ru/articles/801809/"

    def setUp(self) -> None:
        self.parser = ForumParser()

    def test_parse_real_page_structure(self) -> None:
        """Проверяет парсинг реальной статьи Хабра и корректность типов извлеченных полей."""
        comments = self.parser.parse_page(self.TEST_URL)

        # На этой статье есть комментарии, список не должен быть пустым
        self.assertIsInstance(comments, list)
        self.assertGreater(len(comments), 0)

        # Проверяем структуру и типы первого комментария
        first = comments[0]
        self.assertIn("id", first)
        self.assertIn("name", first)
        self.assertIn("message", first)

        self.assertIsInstance(first["id"], int)
        self.assertIsInstance(first["name"], str)
        self.assertTrue(len(first["name"]) > 0)
        self.assertIsInstance(first["message"], str)
        self.assertTrue(len(first["message"]) > 0)

    def test_parse_and_save_to_db(self) -> None:
        """Проверяет сквозной сценарий: парсинг реального сайта и сохранение в БД."""
        comments = self.parser.parse_page(self.TEST_URL)
        self.assertGreater(len(comments), 0)

        with DatabaseRepository(":memory:") as repo:
            saved_count = self.parser.save_to_db(comments, repo)
            self.assertEqual(saved_count, len(comments))

            # Проверяем, что первый комментарий реально лежит в БД
            first_comment = comments[0]
            db_record = repo.get_by_id(first_comment["id"])

            self.assertIsNotNone(db_record)
            self.assertEqual(db_record["name"], first_comment["name"])
            self.assertEqual(db_record["message"], first_comment["message"])

    def test_parse_non_existent_page(self) -> None:
        """Проверяет, что при ошибке 404 парсер не падает и возвращает пустой список."""
        bad_url = "https://habr.com/ru/articles/999999999999/"
        comments = self.parser.parse_page(bad_url)
        self.assertEqual(comments, [])


if __name__ == "__main__":
    unittest.main()