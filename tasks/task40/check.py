"""
Тестирующая система для student.py.
Сравнивает результат выполнения setup-файлов (i1.py, i2.py...) с эталонами (o1.py, o2.py...).
"""

import json
import sys
import math
import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def load_literal(file_path: Path):
    """Безопасно загружает JSON или Python-литерал (список/словарь) из файла."""
    content = file_path.read_text(encoding="utf-8").strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Если не строгий JSON, пробуем распарсить как Python-литерал
        return ast.literal_eval(content)


def diff(actual, expected, path="ret"):
    """Рекурсивное сравнение структур с корректной обработкой float."""
    if isinstance(expected, dict) and isinstance(actual, dict):
        if set(expected.keys()) != set(actual.keys()):
            return f"{path}: ключи не совпадают. Ожидалось {list(expected.keys())}, получено {list(actual.keys())}"
        for k in expected:
            err = diff(actual[k], expected[k], f"{path}[{k}]")
            if err:
                return err
        return None

    if isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            return f"{path}: длина списка {len(actual)} вместо {len(expected)}"
        for i, (a, e) in enumerate(zip(actual, expected)):
            err = diff(a, e, f"{path}[{i}]")
            if err:
                return err
        return None

    if isinstance(expected, float) and isinstance(actual, (int, float)):
        if not math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9):
            return f"{path}: ожидалось {expected}, получено {actual}"
        return None

    if actual == expected:
        return None

    return f"{path}: ожидалось {expected!r}, получено {actual!r}"


def main():
    check_file = BASE_DIR / "check.json"
    if not check_file.exists():
        print(f"❌ Ошибка: файл {check_file} не найден.")
        return 2

    try:
        tests = json.loads(check_file.read_text(encoding="utf-8"))["tests"]
    except Exception as e:
        print(f"❌ Ошибка чтения {check_file}: {e}")
        return 2

    student_file = BASE_DIR / "student.py"
    if not student_file.exists():
        print("❌ Ошибка: файл student.py не найден.")
        return 2

    # Загружаем код студента один раз
    student_code = student_file.read_text(encoding="utf-8")

    passed = 0
    for test in tests:
        test_id = test["id"]
        setup_file = BASE_DIR / test["setup"]
        expected_file = BASE_DIR / test["expected_file"]

        if not setup_file.exists():
            print(f"⚠️ Тест {test_id}: файл setup '{setup_file.name}' не найден.")
            continue
        if not expected_file.exists():
            print(f"⚠️ Тест {test_id}: файл expected '{expected_file.name}' не найден.")
            continue

        # Свежий namespace для каждого теста (изоляция)
        ns = {"__name__": "__main__"}

        try:
            # 1. Внедряем функции студента в пространство имен
            exec(compile(student_code, "student.py", "exec"), ns)
            # 2. Выполняем setup-файл (например, i1.py), который определит переменные и вызовет ret = ...
            exec(
                compile(
                    setup_file.read_text(encoding="utf-8"),
                    setup_file.name,
                    "exec",
                ),
                ns,
            )

            if "ret" not in ns:
                print(
                    f"❌ Тест {test_id}: FAIL. Переменная 'ret' не была создана в {setup_file.name}"
                )
                continue

            # 3. Загружаем ожидаемый результат из o*.py
            expected = load_literal(expected_file)

            # 4. Сравниваем
            error = diff(ns["ret"], expected)
            if error:
                print(f"❌ Тест {test_id}: FAIL")
                print(f"   Причина: {error}")
                # print(f"\n\n{ns['ret']}\n\n")
                # return 3
            else:
                print(f"✅ Тест {test_id}: PASS")
                passed += 1

        except Exception as e:
            print(f"💥 Тест {test_id}: ERROR")
            print(f"   Исключение: {type(e).__name__}: {e}")

    print(f"\n{'='*50}")
    print(f"Итог: пройдено {passed} из {len(tests)} тестов.")
    return 0 if passed == len(tests) else 1


if __name__ == "__main__":
    sys.exit(main())
