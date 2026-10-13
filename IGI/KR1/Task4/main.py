"""Control work 1: Task 4, Pentagon interface, variant 8.
Version: 1.0. Author: Romeiko Matvey Dmitrievich. Date: 2026-10-13.
Purpose: Validate user values, test the classes and repeat figure creation.
"""

import argparse
import math
from pathlib import Path
from figure_color import FigureColor
from pentagon import RegularPentagon


def read_side():
    """Read a positive finite side and retry invalid numeric input."""
    while True:
        try:
            value = float(input("Длина стороны a: ").replace(",", "."))
            if not math.isfinite(value) or value <= 0:
                raise ValueError("non-positive or non-finite")
            return value
        except ValueError:
            print("Введите конечное положительное число.")


def read_color():
    """Read a valid color through the same validation used by the class."""
    while True:
        try:
            return FigureColor(input("Цвет (blue, red, #23A6C8): ")).color
        except ValueError as error:
            print(error)


def interactive():
    """Create, display and save as many figures as the user requests."""
    while True:
        try:
            pentagon = RegularPentagon(read_side(), read_color())
            label = input("Подпись фигуры: ")
            output = input("Файл [results/pentagon.png]: ").strip() or "results/pentagon.png"
            print(pentagon.describe())
            print("Сохранено:", pentagon.draw(label, output, show=True))
        except (OSError, ValueError) as error:
            print("Ошибка:", error)
        if input("Повторить? (д/н): ").strip().casefold() not in {"д", "да", "y", "yes"}:
            return


def main():
    """Provide interactive input or reproducible CLI figure generation."""
    parser = argparse.ArgumentParser(description="Правильный пятиугольник, вариант 8")
    parser.add_argument("--side", type=float)
    parser.add_argument("--color", default="skyblue")
    parser.add_argument("--label", default="Вариант 8")
    parser.add_argument("--output", type=Path, default=Path("results/pentagon.png"))
    parser.add_argument("--no-show", action="store_true", help="Сохранить без окна графика")
    args = parser.parse_args()
    try:
        if args.no_show:
            import matplotlib
            matplotlib.use("Agg")
        if args.side is None:
            interactive()
        else:
            pentagon = RegularPentagon(args.side, args.color)
            print(pentagon.describe())
            print("Сохранено:", pentagon.draw(args.label, args.output, show=not args.no_show))
    except (KeyboardInterrupt, EOFError):
        print("\nПрограмма завершена.")
    except (ValueError, OSError) as error:
        parser.exit(1, "Ошибка: {}\n".format(error))


if __name__ == "__main__":
    main()
