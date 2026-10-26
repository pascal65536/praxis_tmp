import json
import sys
from pathlib import Path


def solve(text):
    """Возвращает статистический отчёт по содержимому журнала."""
    pass  # Ваш код


# === ДОПОЛНИТЕЛЬНАЯ ЧАСТЬ 1 ===
def analyze_task_durations(text):
    """Возвращает количество и среднюю длительность завершённых задач."""
    pass  


# === ДОПОЛНИТЕЛЬНАЯ ЧАСТЬ 2 ===
def top_classes(text, limit=10):
    """Возвращает рейтинг запрашиваемых классов."""
    pass 


def main():
    if len(sys.argv) != 3:
        print("Использование: python student.py <входной_лог> <выходной_json>")
        return 2

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    try:
        # utf-8-sig читает обычный UTF-8 и удаляет BOM, если он есть.
        text = input_path.read_text(encoding="utf-8-sig")
        report = solve(text)

        with output_path.open("w", encoding="utf-8", newline="\n") as file:
            json.dump(report, file, ensure_ascii=False, indent=2, sort_keys=True)
            file.write("\n")
    except (OSError, UnicodeError, TypeError, ValueError) as error:
        print(f"Ошибка: {type(error).__name__}: {error}")
        return 1

    print(f"Отчёт сохранён: {output_path}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nВыполнение прервано пользователем.")
        sys.exit(130)
