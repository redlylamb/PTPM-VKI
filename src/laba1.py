import logging
import sys
import math
import os

#создание папку logs, если её не
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "file_txt.log")

log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file, encoding="utf-8")
    ]
)

logging.info("Логгер успешно сконфигурирован")
logging.info("Приложение запущено")


def triangle(a, b, c):
    if not (a > 0 and b > 0 and c > 0):
        return "не треугольник"
    if a + b <= c or a + c <= b or b + c <= a:
        return "не треугольник"
    if a == b == c:
        return "равносторонний"
    if a == b or b == c or a == c:
        return "равнобедренный"
    return "разносторонний"


def coordss(a, b, c, size=100):
    x = (a * a + b * b - c * c) / (2 * a)
    y = math.sqrt(max(0, b * b - x * x))
    points = [(0, 0), (a, 0), (x, y)]

    #в квадрат size x size
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    w = max(xs) - min(xs)
    h = max(ys) - min(ys)

    #если треугольник вырожденный (точки на одной линии) — возвращаем метку ошибки
    if w == 0 or h == 0:
        return [(-1, -1), (-1, -1), (-1, -1)]

    scale = min((size - 10) / w, (size - 10) / h)

    result = []
    for px, py in points:
        ix = int((px - min(xs)) * scale) + 5
        iy = size - int((py - min(ys)) * scale) - 5
        result.append((ix, iy))
    return result


def classify(a_raw, b_raw, c_raw):
    try:
        a = float(a_raw)
        b = float(b_raw)
        c = float(c_raw)
    except (ValueError, TypeError):
        logging.critical("Нечисловые данные: %r, %r, %r", a_raw, b_raw, c_raw)
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    if not (math.isfinite(a) and math.isfinite(b) and math.isfinite(c)):
        logging.critical("Некорректные числа: %r, %r, %r", a_raw, b_raw, c_raw)
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    t = triangle(a, b, c)
    logging.info("Треугольник: %s", t)

    if t == "не треугольник":
        logging.info("Числа не образуют треугольник: %s, %s, %s", a, b, c)
        return t, [(-1, -1), (-1, -1), (-1, -1)]

    coords = coordss(a, b, c)
    logging.info("Тип: %s; координаты: %s", t, coords)
    return t, coords


def main():
    a_raw = input("длина стороны A: ")
    b_raw = input("длина стороны B: ")
    c_raw = input("длина стороны C: ")

    t, coords = classify(a_raw, b_raw, c_raw)
    print(t)
    print(coords)
    logging.info("отработал метод classify:  %s %s", t, coords)


if __name__ == "__main__":
    main()