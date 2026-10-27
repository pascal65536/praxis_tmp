import json
import sys
from pathlib import Path

from student import solve

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
        tests = json.load(file)

    if not isinstance(tests, list):
        raise ValueError("В check.json должен находиться список тестов.")

    if not tests:
        raise ValueError("Файл check.json не содержит тестов.")

    required_fields = {"id", "input", "output"}

    for position, test in enumerate(tests, start=1):
        if not isinstance(test, dict):
            raise ValueError(f"Тест №{position} должен быть JSON-объектом.")

        missing = required_fields - test.keys()

        if missing:
            fields = ", ".join(sorted(missing))
            raise ValueError(f"В тесте №{position} отсутствуют поля: {fields}.")

        if not isinstance(test["input"], str):
            raise ValueError(f"Поле input в тесте {test['id']} должно быть строкой.")

    return tests


def run_tests(tests):
    """Запускает тесты и возвращает количество успехов и список ошибок."""
    passed = 0
    failures = []

    for position, test in enumerate(tests, start=1):
        test_id = test.get("id", position)
        test_input = test["input"]
        expected = test["output"]

        try:
            actual = solve(test_input)
        except Exception as error:
            failures.append(
                {
                    "id": test_id,
                    "input": test_input,
                    "error": f"{type(error).__name__}: {error}",
                }
            )
            continue

        if type(actual) is not type(expected):
            failures.append(
                {
                    "id": test_id,
                    "input": test_input,
                    "expected": expected,
                    "actual": actual,
                    "error": (
                        f"Неверный тип результата: ожидался "
                        f"{type(expected).__name__}, получен "
                        f"{type(actual).__name__}."
                    ),
                }
            )
            continue

        if actual != expected:
            failures.append(
                {
                    "id": test_id,
                    "input": test_input,
                    "expected": expected,
                    "actual": actual,
                    "error": "Результат не совпадает с ожидаемым.",
                }
            )
            continue

        passed += 1

    return passed, failures


def print_failures(failures):
    """Выводит информацию о первых непройденных тестах."""
    print("\nНепройденные тесты:")

    for failure in failures[:MAX_ERRORS_TO_SHOW]:
        print("\n" + "=" * 60)
        print(f"Тест {failure['id']}")
        print(f"Вход: {format_value(failure['input'])}")
        print(f"Причина: {failure['error']}")

        if "expected" in failure:
            print(f"Ожидалось: {format_value(failure['expected'])}")
            print(f"Получено:  {format_value(failure['actual'])}")

    remaining = len(failures) - MAX_ERRORS_TO_SHOW

    if remaining > 0:
        print(f"\nЕщё ошибок: {remaining}.")


def main():
    try:
        tests = load_tests()
    except FileNotFoundError:
        print(f"Ошибка проверки: файл не найден: {CHECK_FILE}")
        return 2
    except json.JSONDecodeError as error:
        print(f"Ошибка в формате check.json: {error}")
        return 2
    except (OSError, ValueError) as error:
        print(f"Ошибка загрузки тестов: {error}")
        return 2

    passed, failures = run_tests(tests)
    total = len(tests)

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
