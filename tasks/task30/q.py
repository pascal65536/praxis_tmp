import json
import sys
import io
import importlib
from pathlib import Path
from contextlib import redirect_stdout

BASE_DIR = Path(__file__).resolve().parent
CHECK_FILE = BASE_DIR / "check.json"
MAX_ERRORS_TO_SHOW = 5
MAX_VALUE_LENGTH = 700


def format_value(value):
    """Возвращает представление значения ограниченной длины."""
    text = repr(value)
    if len(text) > MAX_VALUE_LENGTH:
        return text[:MAX_VALUE_LENGTH] + "..."
    return text


def load_tests():
    """Загружает и проверяет структуру тестов."""
    with CHECK_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("В check.json должен находиться JSON-объект.")
    
    if "tests" not in data:
        raise ValueError("В check.json отсутствует поле 'tests'.")
    
    tests = data["tests"]
    if not isinstance(tests, list):
        raise ValueError("Поле 'tests' должно быть списком.")
    if not tests:
        raise ValueError("Файл check.json не содержит тестов.")

    required_fields = {"id", "code", "expected"}
    for position, test in enumerate(tests, start=1):
        if not isinstance(test, dict):
            raise ValueError(f"Тест №{position} должен быть JSON-объектом.")
        missing = required_fields - test.keys()
        if missing:
            fields = ", ".join(sorted(missing))
            raise ValueError(f"В тесте №{position} отсутствуют поля: {fields}.")
        if not isinstance(test["code"], str):
            raise ValueError(f"Поле 'code' в тесте {test['id']} должно быть строкой.")
        if not isinstance(test["expected"], str):
            raise ValueError(f"Поле 'expected' в тесте {test['id']} должно быть строкой.")

    return data


def run_tests(data):
    """Запускает тесты и возвращает количество успехов и список ошибок."""
    try:
        module = importlib.import_module("student")
    except ImportError as error:
        return 0, [{
            "id": 0,
            "error": f"Не удалось импортировать student.py: {error}",
        }]
    except Exception as error:
        return 0, [{
            "id": 0,
            "error": f"Ошибка при импорте student.py: {type(error).__name__}: {error}",
        }]

    tests = data["tests"]
    passed = 0
    failures = []

    for position, test in enumerate(tests, start=1):
        test_id = test.get("id", position)
        code = test["code"]
        expected_output = test["expected"]

        # Создаём контекст с импортированными именами из student.py
        context = {name: getattr(module, name) for name in dir(module) if not name.startswith("_")}
        
        # Добавляем встроенные функции
        context.update({
            "print": print,
            "sum": sum,
            "max": max,
            "min": min,
            "len": len,
            "range": range,
            "list": list,
            "dict": dict,
            "set": set,
            "tuple": tuple,
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
        })

        # Перехватываем stdout
        output_buffer = io.StringIO()
        try:
            with redirect_stdout(output_buffer):
                exec(code, context)
        except Exception as error:
            failures.append({
                "id": test_id,
                "code": code,
                "error": f"{type(error).__name__}: {error}",
            })
            continue

        actual_output = output_buffer.getvalue()

        if actual_output != expected_output:
            failures.append({
                "id": test_id,
                "code": code,
                "expected": expected_output,
                "actual": actual_output,
                "error": "Вывод не совпадает с ожидаемым.",
            })
            continue

        passed += 1

    return passed, failures


def print_failures(failures):
    """Выводит информацию о первых непройденных тестах."""
    print("\nНепройденные тесты:")
    for failure in failures[:MAX_ERRORS_TO_SHOW]:
        print("\n" + "=" * 60)
        print(f"Тест {failure['id']}")
        
        if "code" in failure:
            print(f"Код:\n{failure['code']}")
        
        print(f"Причина: {failure['error']}")
        
        if "expected" in failure:
            print(f"Ожидалось:\n{failure['expected']}")
            print(f"Получено:\n{failure['actual']}")

    remaining = len(failures) - MAX_ERRORS_TO_SHOW
    if remaining > 0:
        print(f"\nЕщё ошибок: {remaining}.")


def main():
    try:
        data = load_tests()
    except FileNotFoundError:
        print(f"Ошибка проверки: файл не найден: {CHECK_FILE}")
        return 2
    except json.JSONDecodeError as error:
        print(f"Ошибка в формате check.json: {error}")
        return 2
    except (OSError, ValueError) as error:
        print(f"Ошибка загрузки тестов: {error}")
        return 2

    passed, failures = run_tests(data)
    total = len(data["tests"])
    print(f"Пройдено тестов: {passed} из {total}.")

    if failures:
        print_failures(failures)
        print("\nРешение пока не проходит все проверки.")
        return 1

    print("Все тесты пройдены успешно!")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nПроверка прервана пользователем.")
        sys.exit(130)