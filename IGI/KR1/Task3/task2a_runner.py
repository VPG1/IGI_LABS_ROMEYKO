"""Control work 1: Docker runner for Task 2A, variant 8.
Version: 1.0. Author: Romeiko Matvey Dmitrievich. Date: 2026-10-13.
Purpose: Pass text via arguments, environment, stdin or a mounted file.
"""

import argparse
import os
from pathlib import Path
from task2a import count_digits


def main():
    """Resolve one text source, count digits and optionally save the result."""
    parser = argparse.ArgumentParser(description="Задание 2А, вариант 8")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--text", help="Текст непосредственно в аргументе")
    group.add_argument("--file", type=Path, help="Файл UTF-8 с текстом")
    parser.add_argument("--output", type=Path, help="Путь для результата")
    args = parser.parse_args()
    try:
        if args.text is not None:
            text = args.text
        elif args.file is not None:
            text = args.file.read_text(encoding="utf-8-sig")
        elif "TEXT" in os.environ:
            text = os.environ["TEXT"]
        else:
            text = input("Введите текст: ")
        result = "Количество цифр: {}".format(count_digits(text))
        print(result)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(result + "\n", encoding="utf-8")
    except (OSError, UnicodeError, EOFError) as error:
        parser.exit(1, "Ошибка: {}\n".format(error))


if __name__ == "__main__":
    main()
