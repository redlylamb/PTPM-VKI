from abc import ABC, abstractmethod

class BaseExternalService(ABC):
    @abstractmethod
    def send_data(self, data: str) -> bool:
        pass

class EmailService(BaseExternalService):
    def send_data(self, data: str) -> bool:
        # Имитация отправки
        print(f"[СЕРВЕР] Отправлены данные: {data}")
        return True