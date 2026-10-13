# Контрольная работа 1

**Вариант 8. Ромейко Матвей Дмитриевич.**

Исходники и результаты находятся в `IGI/KR1`. На main сохранена полная
структура, отдельные ветки: IGI, STRWEB, IGI-KR1, IGI-IPR1, STRWEB-KR1, STRWEB-IPR1.

## Запуск

```bash
git clone https://github.com/VPG1/IGI_LABS_ROMEYKO.git 353501_ROMEIKO_8
cd 353501_ROMEIKO_8
git submodule update --init --recursive
python3 -m pip install -r requirements.txt
cd IGI/KR1
python3 Task2/main.py
python3 Task2/main.py --input Task2/input.txt --output Task2/results/result.txt --password C00l_Pass
python3 Task4/main.py --side 5 --color skyblue --label "Вариант 8" --output Task4/results/pentagon.png
python3 -m unittest discover -s tests -v
docker build -f Task3/Dockerfile -t kr1-variant8:1.0 .
docker run --rm -e TEXT="Вариант 8, 2026" kr1-variant8:1.0
```

Без графического окна используйте `--no-show` в задании 4.
В меню 2А доступны пользовательский ввод и генератор. В 2Б текст считывается
из UTF-8 файла, все результаты сохраняются и архивируются через zipfile.

Группа 353501, номер в журнале 8. Базовая папка 353501_ROMEIKO_8.
Преподаватель: Жвакина Анна Васильевна. Вариант 8.

Площадь правильного пятиугольника со стороной 5 равна 43.0119350147.
Проверены 26 тестов и все требуемые команды Docker.

Переименование remote показано как `origin` -> `coursework` -> `origin`.
Учебный проект geometric_lib подключен как подмодуль.

## Правила анализа

Слова выделяются по `\b\w+\b`; повторы и начальная l сравниваются без регистра.
Прописные слова состоят только из букв латиницы или кириллицы. Пароль
проверяется по учебному условию: ASCII буквы, цифры, `_`, не менее 8 символов,
обязательны верхний и нижний регистр и цифра. Предложения делятся по `.?!`;
побудительные определяются формально по `!`, у `?` приоритет.

## Документация

- https://git-scm.com/docs/git-log
- https://docs.docker.com/reference/cli/docker/
- https://docs.python.org/3/library/abc.html
- https://docs.python.org/3/library/zipfile.html
