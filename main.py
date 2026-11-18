from src.database import DatabaseRepository
from src.parser import ForumParser

if __name__ == "__main__":
    # Ссылка на любую статью с комментариями на Хабре
    url = "https://habr.com/ru/articles/801809/" 

    # 1. Инициализируем БД (можно использовать файл 'habr.db' вместо ':memory:', чтобы сохранить данные)
    db = DatabaseRepository("habr.db")
    
    # 2. Запускаем парсер
    parser = ForumParser()
    comments = parser.parse_page(url)
    
    # 3. Сохраняем в БД
    parser.save_to_db(comments, db)
    
    # 4. Проверяем, что сохранилось (выводим первые 2 записи из БД)
    print("\nПример данных из БД:")
    for comment in comments[:2]:
        print(f"ID: {comment['id']}")
        print(f"Автор: {comment['name']}")
        print(f"Текст (первые 100 символов): {comment['message'][:100]}...")
        print("-" * 40)
    
    db.close()