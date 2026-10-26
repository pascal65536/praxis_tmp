import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
TEST_FILE = BASE_DIR / "check.json"
SAMPLE_FILE = BASE_DIR / "data" / "sample.log"
EXPECTED_SAMPLE_FILE = BASE_DIR / "expected_sample.json"
STUDENT_FILE = BASE_DIR / "student.py"
MAX_ERRORS_TO_SHOW = 10
MAX_VALUE_LENGTH = 1200
CLI_TIMEOUT = 20


try:
    from student import solve, analyze_task_durations, top_classes
except Exception as error:
    print("Не удалось загрузить student.py.")
    print(f"{type(error).__name__}: {error}")
    print("Проверьте имя файла, синтаксис и код вне функций.")
    raise SystemExit(2)


def load_json(path):
    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def values_match(actual, expected):
    """Сравнивает значения вместе с типами, включая вложенные структуры."""
    if type(actual) is not type(expected):
        return False

    if isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(
            values_match(actual[key], expected[key]) for key in expected
        )

    if isinstance(expected, list):
        return len(actual) == len(expected) and all(
            values_match(actual_item, expected_item)
            for actual_item, expected_item in zip(actual, expected)
        )

    return actual == expected


def format_value(value):
    text = repr(value)
    if len(text) > MAX_VALUE_LENGTH:
        return text[:MAX_VALUE_LENGTH] + "..."
    return text


def validate_tests(tests):
    if not isinstance(tests, list) or not tests:
        raise ValueError("В check.json должен находиться непустой список тестов.")

    allowed_kinds = {"base", "durations", "classes"}
    identifiers = set()

    for position, test in enumerate(tests, start=1):
        if not isinstance(test, dict):
            raise ValueError(f"Тест №{position} должен быть JSON-объектом.")

        missing = {"id", "kind", "input", "output"} - test.keys()
        if missing:
            raise ValueError(
                f"В тесте №{position} отсутствуют поля: {', '.join(sorted(missing))}."
            )

        if test["kind"] not in allowed_kinds:
            raise ValueError(f"Неизвестный тип теста: {test['kind']!r}.")

        if not isinstance(test["input"], str):
            raise ValueError(f"Поле input в тесте {test['id']!r} должно быть строкой.")

        if test["id"] in identifiers:
            raise ValueError(f"Повторяется идентификатор теста: {test['id']!r}.")
        identifiers.add(test["id"])


def run_test(test):
    kind = test["kind"]
    test_input = test["input"]

    if kind == "base":
        return solve(test_input)
    if kind == "durations":
        return analyze_task_durations(test_input)
    if kind == "classes":
        return top_classes(test_input, test.get("limit", 10))

    raise ValueError(f"Неизвестный тип теста: {kind!r}")


def run_cli_check(expected):
    """Проверяет файловый интерфейс в отдельном процессе."""
    with tempfile.TemporaryDirectory(prefix="lab3-check-") as directory:
        report_path = Path(directory) / "report.json"
        environment = os.environ.copy()
        environment["PYTHONUTF8"] = "1"
        environment["PYTHONIOENCODING"] = "utf-8"

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(STUDENT_FILE),
                    str(SAMPLE_FILE),
                    str(report_path),
                ],
                cwd=BASE_DIR,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=CLI_TIMEOUT,
                env=environment,
            )
        except subprocess.TimeoutExpired:
            return {
                "id": "sample-cli",
                "error": f"Программа не завершилась за {CLI_TIMEOUT} секунд.",
            }
        except OSError as error:
            return {
                "id": "sample-cli",
                "error": f"Не удалось запустить student.py: {error}",
            }

        if result.returncode != 0:
            details = (result.stderr or result.stdout).strip()
            return {
                "id": "sample-cli",
                "error": (
                    f"student.py завершился с кодом {result.returncode}.\n"
                    f"Вывод: {details or 'отсутствует'}"
                ),
            }

        try:
            actual = load_json(report_path)
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            return {
                "id": "sample-cli",
                "error": f"Не удалось прочитать JSON-отчёт: {error}",
            }

        if not values_match(actual, expected):
            return {
                "id": "sample-cli",
                "error": "Отчёт для data/sample.log не совпадает с expected_sample.json.",
                "expected": expected,
                "actual": actual,
            }

    return None


def print_failures(failures):
    print("\nНепройденные проверки:")

    for failure in failures[:MAX_ERRORS_TO_SHOW]:
        print("\n" + "=" * 68)
        print(f"Проверка: {failure['id']}")
        print(failure["error"])

        if "expected" in failure:
            print(f"Ожидалось: {format_value(failure['expected'])}")
            print(f"Получено:  {format_value(failure['actual'])}")

    remaining = len(failures) - MAX_ERRORS_TO_SHOW
    if remaining > 0:
        print(f"\nЕщё ошибок: {remaining}.")


def main():
    advanced = False
    if len(sys.argv) == 2 and sys.argv[1] == "--advanced":
        advanced = True
    elif len(sys.argv) != 1:
        print("Использование: python check.py [--advanced]")
        return 2

    try:
        tests = load_json(TEST_FILE)
        validate_tests(tests)
        expected_sample = load_json(EXPECTED_SAMPLE_FILE)
        if not isinstance(expected_sample, dict):
            raise ValueError("В expected_sample.json должен находиться JSON-объект.")
        if not SAMPLE_FILE.is_file():
            raise FileNotFoundError(f"Файл не найден: {SAMPLE_FILE}")
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(f"Ошибка комплекта проверки: {error}")
        return 2

    selected_kinds = {"base"}
    if advanced:
        selected_kinds.update({"durations", "classes"})

    passed = 0
    total = 0
    failures = []

    for test in tests:
        if test["kind"] not in selected_kinds:
            continue

        total += 1
        try:
            actual = run_test(test)
        except Exception as error:
            failures.append(
                {
                    "id": test["id"],
                    "error": f"{type(error).__name__}: {error}",
                }
            )
            continue

        if values_match(actual, test["output"]):
            passed += 1
        else:
            failures.append(
                {
                    "id": test["id"],
                    "error": "Результат не совпадает с ожидаемым.",
                    "expected": test["output"],
                    "actual": actual,
                }
            )

    total += 1
    cli_failure = run_cli_check(expected_sample)
    if cli_failure is None:
        passed += 1
    else:
        failures.append(cli_failure)

    mode = "базовая + дополнительная" if advanced else "базовая"
    print(f"Режим проверки: {mode}.")
    print(f"Пройдено проверок: {passed} из {total}.")

    if failures:
        print_failures(failures)
        print("\nРешение пока не проходит все выбранные проверки.")
        return 1

    print("Все выбранные проверки пройдены успешно!")
    if not advanced:
        print("Дополнительные части проверяются командой: python check.py --advanced")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nПроверка прервана пользователем.")
        sys.exit(130)
