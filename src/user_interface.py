from abc import ABC, abstractmethod

class BaseUserInterface(ABC):
    @abstractmethod
    def get_input(self) -> tuple[float, float, float]:
        pass

class ConsoleUserInterface(BaseUserInterface):
    def get_input(self) -> tuple[float, float, float]:
        try:
            a = float(input("Сторона A: "))
            b = float(input("Сторона B: "))
            c = float(input("Сторона C: "))
            return a, b, c
        except ValueError:
            return 0.0, 0.0, 0.0