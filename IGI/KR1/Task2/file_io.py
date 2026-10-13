"""Control work 1: Task 2B, File and archive operations, variant 8.
Version: 1.0. Author: Romeiko Matvey Dmitrievich. Date: 2026-10-13.
Purpose: Read UTF-8 text, persist results and inspect a ZIP archive.
"""

from pathlib import Path
import json
import zipfile
from task2b import analyze_text


def read_text(path):
    """Read UTF-8 text with optional BOM, preserving line breaks."""
    return Path(path).read_text(encoding="utf-8-sig")


def format_results(results):
    """Return a readable Russian report with complete individual results."""
    statistics = results["statistics"]
    rows = [
        "КОНТРОЛЬНАЯ РАБОТА 1. ВАРИАНТ 8. ЗАДАНИЕ 2Б",
        "Слова с прописными буквами и цифрами: " +
        ", ".join(results["words_with_uppercase_and_digits"]),
        "Пароль надежный по условию задания: " +
        ("да" if results["password_is_strong"] else "нет"),
        "Количество слов из прописных букв: {}".format(results["uppercase_word_count"]),
        "Самое длинное слово на l: " + (results["longest_word_starting_l"] or "не найдено"),
        "Повторяющиеся слова: " + (", ".join(
            "{} ({})".format(word, count)
            for word, count in results["repeated_words"].items()) or "нет"),
        "Предложений всего: {}".format(statistics["total_sentences"]),
        "Повествовательных: {}".format(statistics["declarative"]),
        "Вопросительных: {}".format(statistics["interrogative"]),
        "Побудительных по знаку !: {}".format(statistics["imperative"]),
        "Средняя длина предложения (только слова): {}".format(statistics["avg_sentence_length"]),
        "Средняя длина слова: {}".format(statistics["avg_word_length"]),
        "Количество смайликов: {}".format(statistics["smiley_count"]),
    ]
    return "\n".join(rows) + "\n"


def archive_report(path):
    """Archive one result file and return verified member metadata."""
    source = Path(path)
    archive_path = source.with_suffix(".zip")
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(source, arcname=source.name)
    with zipfile.ZipFile(archive_path) as archive:
        bad_member = archive.testzip()
        if bad_member is not None:
            raise zipfile.BadZipFile("CRC failure: " + bad_member)
        member = archive.getinfo(source.name)
        return {"archive": str(archive_path), "name": member.filename,
                "size": member.file_size, "compressed_size": member.compress_size,
                "crc32": "{:08x}".format(member.CRC),
                "date_time": list(member.date_time)}


def analyze_file(input_path, output_path, password):
    """Run the full file workflow and keep source and result files distinct."""
    source, output = Path(input_path), Path(output_path)
    if output.suffix.lower() != ".txt":
        raise ValueError("Файл результата должен иметь расширение .txt.")
    if source.resolve() == output.resolve():
        raise ValueError("Файл результата должен отличаться от исходного файла.")
    if source.resolve() in {output.with_suffix(".zip").resolve(),
                            output.with_suffix(".json").resolve(),
                            output.with_name("archive_info.json").resolve()}:
        raise ValueError("Путь результата пересекается с исходным файлом.")
    results = analyze_text(read_text(source), password)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(format_results(results), encoding="utf-8")
    metadata = archive_report(output)
    output.with_suffix(".json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    output.with_name("archive_info.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return results, metadata
