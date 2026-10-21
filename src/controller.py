from calculator import TriangleCalculator
from database import TriangleDatabase
from user_interface import BaseUserInterface
from external_service import BaseExternalService

class TriangleController:
    def __init__(self, ui: BaseUserInterface, db: TriangleDatabase, 
                 calc: TriangleCalculator, service: BaseExternalService):
        self.ui = ui
        self.db = db
        self.calc = calc
        self.service = service

    def process(self) -> tuple[str, str]:
        a, b, c = self.ui.get_input()
        record = self.db.get_record(a, b, c)

        if record:
            t_type, err = record
        else:
            t_type, err = self.calc.calculate(a, b, c)
            self.db.add_record(a, b, c, t_type, err)

        message = f"Тип: {t_type}. Ошибка: {err}"
        self.service.send_data(message)
        return t_type, err