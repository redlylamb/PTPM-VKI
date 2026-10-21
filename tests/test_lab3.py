import unittest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from calculator import TriangleCalculator
from database import TriangleDatabase
from user_interface import ConsoleUserInterface
from external_service import EmailService
from controller import TriangleController


class TestLab3Integration(unittest.TestCase):
    def setUp(self):
        self.db = TriangleDatabase(db_name=":memory:")
        self.calc = TriangleCalculator()
        self.ui = ConsoleUserInterface()
        self.service = EmailService()
        self.controller = TriangleController(self.ui, self.db, self.calc, self.service)

    @patch('builtins.input', side_effect=['3', '3', '3'])
    @patch.object(EmailService, 'send_data')
    def test_integration_calculate_and_save_to_db(self, mock_send, mock_input):
        result_type, result_err = self.controller.process()
        self.assertEqual(result_type, "равносторонний")
        db_record = self.db.get_record(3.0, 3.0, 3.0)
        self.assertIsNotNone(db_record)
        mock_send.assert_called_once_with("Тип: равносторонний. Ошибка: ")

    @patch('builtins.input', side_effect=['3', '3', '3'])
    @patch.object(EmailService, 'send_data')
    def test_integration_get_from_db_no_recalculate(self, mock_send, mock_input):
        self.db.add_record(3.0, 3.0, 3.0, "равносторонний", "")
        result_type, result_err = self.controller.process()
        self.assertEqual(result_type, "равносторонний")

    @patch('builtins.input', side_effect=['1', '2', '5'])
    @patch.object(EmailService, 'send_data')
    def test_integration_invalid_triangle_saves_error(self, mock_send, mock_input):
        result_type, result_err = self.controller.process()
        self.assertEqual(result_type, "не треугольник")
        db_record = self.db.get_record(1.0, 2.0, 5.0)
        self.assertEqual(db_record[1], "Нарушено неравенство треугольника")


class TestLab3Unit(unittest.TestCase):
    def setUp(self):
        self.db = TriangleDatabase(db_name=":memory:")

    def test_db_add_and_get(self):
        self.db.add_record(4.0, 4.0, 4.0, "равносторонний", "")
        record = self.db.get_record(4.0, 4.0, 4.0)
        self.assertEqual(record, ("равносторонний", ""))

    def test_db_delete(self):
        self.db.add_record(5.0, 5.0, 5.0, "равносторонний", "")
        self.db.delete_record(5.0, 5.0, 5.0)
        record = self.db.get_record(5.0, 5.0, 5.0)
        self.assertIsNone(record)

    @patch('builtins.input', side_effect=['abc', '4', '5'])
    def test_ui_handles_invalid_input(self, mock_input):
        ui = ConsoleUserInterface()
        result = ui.get_input()
        self.assertEqual(result, (0.0, 0.0, 0.0))


if __name__ == "__main__":
    unittest.main()