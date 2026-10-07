import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import laba1


class TestLaba1(unittest.TestCase):

    #triangle

    def test_triangle_equilateral(self):
        #3 одинаковые стороны ="равносторонний"
        self.assertEqual(laba1.triangle(3, 3, 3), "равносторонний")

    def test_triangle_isosceles(self):
        #2 сттороны - "равнобедренный"
        self.assertEqual(laba1.triangle(3, 3, 4), "равнобедренный")

    def test_triangle_scalene(self):
        #3 разные стороны = "разносторонний"
        self.assertEqual(laba1.triangle(3, 4, 5), "разносторонний")

    def test_triangle_inequality_violation(self):
        #стороны 1, 2, 3 не могут образовать треугольник ="не треугольник"
        self.assertEqual(laba1.triangle(1, 2, 3), "не треугольник")

    def test_triangle_non_positive_side(self):
        #отрицательная длина стороны = "не треугольник"
        self.assertEqual(laba1.triangle(-1, 2, 2), "не треугольник")

    #coordss

    def test_coordss_returns_three_points_for_valid_triangle(self):
        #3 угла — 3 координаты
        coords = laba1.coordss(3, 4, 5)
        self.assertEqual(len(coords), 3)

    def test_coordss_handles_degenerate_triangle_without_crash(self):
        #стороны 1, 1, 2 — это не треугольник, а просто линия; программа НЕ должна сломаться, а вернуть метку ошибки
        result = laba1.coordss(1, 1, 2)
        self.assertEqual(result, [(-1, -1), (-1, -1), (-1, -1)])

    #classify

    def test_classify_valid_triangle(self):
        #ввод нормальных чисел = тип "разносторонний" и 3 координаты
        t, coords = laba1.classify("3", "4", "5")
        self.assertEqual(t, "разносторонний")
        self.assertEqual(len(coords), 3)

    def test_classify_non_numeric_returns_error_marker(self):
        #ввод буквы вместо чисел — программа не должна ломаться - вернёт пустой тип и метку ошибки
        t, coords = laba1.classify("abc", "4", "5")
        self.assertEqual(t, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_classify_none_input_returns_error_marker(self):
        #вообще ничего не ввожу (None) — программа должна это выдержать и вернуть метку ошибки, а не упасть
        t, coords = laba1.classify(None, "4", "5")
        self.assertEqual(t, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])


if __name__ == "__main__":
    unittest.main()