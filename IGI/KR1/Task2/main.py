"""Control work 1: Text analysis menu, variant 8.
Version: 1.0. Author: Romeiko Matvey Dmitrievich. Date: 2026-10-13.
Purpose: Run Task 2A and Task 2B with reusable validated input.
"""

import argparse
import json
import logging
from pathlib import Path
import zipfile
from task2a import count_digits
from init_data import init_from_input, init_from_generator
from utils import read_integer, read_nonempty
from file_io import analyze_file, format_results


def run_task2a():
    """Initialize a user-sized list and count digits in each text line."""
    count = read_integer("Количество строк: ", 1)
    method = read_integer("1 - ввод, 2 - генератор: ", 1, 2)
    lines = []
    if method == 1:
        init_from_input(lines, count)
    else:
        length = read_integer("Длина генерируемой строки: ", 1)
        init_from_generator(lines, count, length)
    for index, text in enumerate(lines, 1):
        print("{}. {!r} -> цифр: {}".format(index, text, count_digits(text)))


def run_task2b(input_path, output_path, password):
    """Display all file-analysis results and the archived member metadata."""
    results, metadata = analyze_file(input_path, output_path, password)
    print(format_results(results))
    print("Информация о файле в ZIP:")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


def run_menu():
    """Allow repeated task execution and recover from specific input/file errors."""
    while True:
        print("\nВариант 8\n1 - Задание 2А: количество цифр\n2 - Задание 2Б: анализ файла\n0 - Выход")
        choice = read_integer("Выбор: ", 0, 2)
        if choice == 0:
            return
        try:
            if choice == 1:
                run_task2a()
            else:
                source = read_nonempty("Исходный файл UTF-8: ")
                output = read_nonempty("Файл результата: ")
                password = input("Пароль для проверки: ")
                run_task2b(source, output, password)
        except (ValueError, UnicodeError, OSError, zipfile.BadZipFile) as error:
            print("Ошибка: {}. Можно повторить задание.".format(error))


def main():
    """Select an interactive menu or a reproducible command-line workflow."""
    parser = argparse.ArgumentParser(description="Контрольная 1, вариант 8")
    parser.add_argument("--input", type=Path, help="Исходный UTF-8 файл для 2Б")
    parser.add_argument("--output", type=Path, default=Path("results/result.txt"))
    parser.add_argument("--password", default="", help="Строка для проверки по учебным правилам")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING,
                        format="%(levelname)s: %(message)s")
    try:
        if args.input:
            run_task2b(args.input, args.output, args.password)
        else:
            run_menu()
    except (KeyboardInterrupt, EOFError):
        print("\nПрограмма завершена.")
    except (ValueError, UnicodeError, OSError, zipfile.BadZipFile) as error:
        parser.exit(1, "Ошибка: {}\n".format(error))


if __name__ == "__main__":
    main()
