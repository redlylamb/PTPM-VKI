import logging
import re
from typing import Any, Dict, List, Optional
import requests
from bs4 import BeautifulSoup, Tag

from src.database import DatabaseRepository

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class ForumParser:
    """Парсер для извлечения комментариев с форумов и статей (на примере Habr)."""

    def __init__(self) -> None:
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,*/*;q=0.8"
            ),
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }

    def _prepare_url(self, url: str) -> str:
        """
        Если передана ссылка на статью Хабра без '/comments/',
        автоматически добавляет этот сегмент, так как комментарии рендерятся там.
        """
        clean_url = url.strip()
        if "habr.com" in clean_url and "/articles/" in clean_url:
            base_url = clean_url.rstrip("/")
            if not base_url.endswith("/comments"):
                return f"{base_url}/comments/"
        return clean_url

    def _extract_comment_id(self, article: Tag) -> Optional[int]:
        """Извлекает числовой ID комментария из атрибутов тега или ссылки-якоря."""
        # Вариант 1: ID в атрибуте самого тега article (например, id="comment_26625359" или id="26625359")
        raw_id = str(article.get("id", ""))
        digits = re.sub(r"\D", "", raw_id)
        if digits:
            return int(digits)

        # Вариант 2 (запасной): ID в ссылке на комментарий (например, href="#comment_26625359")
        link_tag = article.find("a", class_="tm-comment__link")
        if link_tag and link_tag.get("href"):
            href_digits = re.sub(r"\D", "", str(link_tag.get("href")))
            if href_digits:
                return int(href_digits)

        return None

    def parse_html(self, html: str) -> List[Dict[str, Any]]:
        """
        Разбирает переданную HTML-строку и извлекает список комментариев.
        Вынесено в отдельный метод для удобного модульного тестирования на фикстурах.
        """
        if not html or not html.strip():
            logger.warning("Передан пустой HTML.")
            return []

        soup = BeautifulSoup(html, "lxml")
        articles = soup.find_all("article", class_="tm-comment-thread__comment")

        if not articles:
            logger.warning(
                "Комментарии на странице не найдены. "
                "Возможно, их нет или изменилась HTML-разметка."
            )
            return []

        parsed_data: List[Dict[str, Any]] = []

        for article in articles:
            # 1. Извлекаем ID комментария
            comment_id = self._extract_comment_id(article)
            if comment_id is None:
                continue

            # 2. Извлекаем логин автора
            author_tag = article.find("a", class_="tm-user-info__username")
            name = author_tag.get_text(strip=True) if author_tag else "Unknown"

            # 3. Извлекаем текст сообщения с сохранением внутренней HTML-разметки
            message_tag = article.find("div", class_="tm-comment__body-content")
            if message_tag:
                message = message_tag.decode_contents().strip()
            else:
                message = ""

            parsed_data.append(
                {
                    "id": comment_id,
                    "name": name,
                    "message": message,
                }
            )

        logger.info(f"Успешно извлечено комментариев: {len(parsed_data)}")
        return parsed_data

    def parse_page(self, url: str) -> List[Dict[str, Any]]:
        """
        Скачивает HTML-страницу по указанному URL и извлекает комментарии.
        Возвращает список словарей вида: [{'id': int, 'name': str, 'message': str}, ...].
        """
        target_url = self._prepare_url(url)
        logger.info(f"Запрос к странице: {target_url}")

        try:
            response = requests.get(target_url, headers=self.headers, timeout=15)
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.error(f"Сетевая ошибка при загрузке {target_url}: {exc}")
            return []

        return self.parse_html(response.text)

    def save_to_db(
        self, parsed_data: List[Dict[str, Any]], repository: DatabaseRepository
    ) -> int:
        """
        Сохраняет список распарсенных комментариев в БД через DatabaseRepository.
        Возвращает количество успешно сохраненных записей.
        """
        if not parsed_data:
            logger.info("Нет данных для сохранения в БД.")
            return 0

        saved_count = 0
        for item in parsed_data:
            try:
                repository.add(
                    comment_id=item["id"],
                    username=item["name"],
                    message=item["message"],
                )
                saved_count += 1
            except (ValueError, TypeError) as exc:
                # Пропускаем дубликаты ID или комментарии, превышающие лимит символов
                logger.warning(f"Комментарий ID={item.get('id')} пропущен: {exc}")
            except Exception as exc:
                logger.error(
                    f"Непредвиденная ошибка при сохранении ID={item.get('id')}: {exc}"
                )

        logger.info(f"Сохранено в БД: {saved_count} из {len(parsed_data)} записей.")
        return saved_count


if __name__ == "__main__":
    # Быстрая проверка работы на реальной статье
    TEST_URL = "https://habr.com/ru/articles/801809/"
    parser = ForumParser()
    comments = parser.parse_page(TEST_URL)

    with DatabaseRepository(":memory:") as db:
        parser.save_to_db(comments, db)
        if comments:
            first_id = comments[0]["id"]
            print("\nПример первой записи из БД:")
            print(db.get_by_id(first_id))