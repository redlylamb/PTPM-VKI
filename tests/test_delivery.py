import unittest
import sys
import os
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from delivery_service import calculate_delivery_cost


class TestDelivery(unittest.TestCase):

    #валидация

    def test_weight_below_minimum_returns_error(self):
        #вес < 0.1 кг = ошибка (-1, "0000-00-00")
        self.assertEqual(calculate_delivery_cost(0.05, 100, "обычный"), (-1, "0000-00-00"))

    def test_distance_above_maximum_returns_error(self):
        #дистанция > 5000 км = ошибка
        self.assertEqual(calculate_delivery_cost(1, 5001, "обычный"), (-1, "0000-00-00"))

    def test_invalid_package_type_returns_error(self):
        #неизвестный тип посылки = ошибка
        self.assertEqual(calculate_delivery_cost(1, 100, "секретный"), (-1, "0000-00-00"))

    #базовая стоимость

    def test_base_cost_light_short_distance(self):
        #200 + 1*5 = 205
        cost, _ = calculate_delivery_cost(1, 1, "обычный")
        self.assertEqual(cost, 205)

    def test_weight_between_5_and_20_applies_1_2(self):
        #(200 + 100*5) * 1.2 = 840
        cost, _ = calculate_delivery_cost(10, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_weight_above_20_applies_1_5(self):
        #(200 + 100*5) * 1.5 = 1050
        cost, _ = calculate_delivery_cost(30, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_fragile_package_adds_300(self):
        #200 + 1*5 + 300 = 505
        cost, _ = calculate_delivery_cost(1, 1, "хрупкий")
        self.assertEqual(cost, 505)

    def test_dangerous_package_adds_1000(self):
        #200 + 1*5 + 1000 = 1205
        cost, _ = calculate_delivery_cost(1, 1, "опасный")
        self.assertEqual(cost, 1205)

    #экспресс

    def test_express_costs_more_than_normal(self):
        #экспресс должен быть дороже обычной доставки
        normal_cost, _ = calculate_delivery_cost(1, 100, "обычный", is_express=False)
        express_cost, _ = calculate_delivery_cost(1, 100, "обычный", is_express=True)
        self.assertGreater(express_cost, normal_cost)

    def test_express_short_distance_takes_at_least_one_day(self):
        #экспресс не может доставляться 0 дней
        _, date_str = calculate_delivery_cost(1, 100, "обычный", is_express=True)
        start = datetime.date(2026, 9, 3)
        delivered = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        self.assertGreaterEqual((delivered - start).days, 1)


if __name__ == "__main__":
    unittest.main()