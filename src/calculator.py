class TriangleCalculator:
    def calculate(self, a: float, b: float, c: float) -> tuple[str, str]:
        if not (a > 0 and b > 0 and c > 0):
            return "не треугольник", "Стороны должны быть больше нуля"
        if a + b <= c or a + c <= b or b + c <= a:
            return "не треугольник", "Нарушено неравенство треугольника"
        if a == b == c:
            return "равносторонний", ""
        if a == b or b == c or a == c:
            return "равнобедренный", ""
        return "разносторонний", ""