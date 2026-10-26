import os
import sys

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", "_site"}
RAW_OPEN = "{% raw %}"
RAW_CLOSE = "{% endraw %}"


def is_opening_fence(line):
    """
    Открывающий блок кода: строка начинается с ``` и после неё есть
    непустой язык (например, ```python, ```bash, ```json).
    """
    stripped = line.lstrip()
    if not stripped.startswith("```"):
        return False
    # Убираем ``` и смотрим, что осталось
    rest = stripped[3:].strip()
    return bool(rest)


def is_closing_fence(line):
    """Закрывающий блок: строка начинается с ``` и после неё ничего нет."""
    stripped = line.lstrip()
    return stripped.startswith("```") and stripped[3:].strip() == ""


def process_file(file_path):
    """
    Читает файл, оборачивает блоки кода в {% raw %}...{% endraw %}.
    Возвращает (изменён_ли_файл, число_обёрнутых_блоков).
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except (UnicodeDecodeError, OSError):
        return False, 0

    result = []
    inside_fence = False  # мы внутри блока ```...```
    inside_raw = False  # мы внутри {% raw %}...{% endraw %}
    wrapped_blocks = 0

    for line in lines:
        if not inside_fence:
            # Вне блока кода: проверяем, не открывается ли блок
            if is_opening_fence(line) and not inside_raw:
                # Вставляем {% raw %} перед открывающим ```
                if result and result[-1].strip() == RAW_OPEN:
                    # Уже есть {% raw %} прямо перед этим — не дублируем
                    pass
                else:
                    result.append(RAW_OPEN + "\n")
                inside_raw = True
                inside_fence = True
                wrapped_blocks += 1
            result.append(line)
        else:
            # Мы внутри блока кода
            result.append(line)
            if is_closing_fence(line):
                inside_fence = False
                if inside_raw:
                    result.append(RAW_CLOSE + "\n")
                    inside_raw = False

    # Если файл изменился — записываем обратно
    new_content = "".join(result)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            old_content = f.read()
    except (UnicodeDecodeError, OSError):
        return False, 0

    if new_content != old_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True, wrapped_blocks

    return False, 0


def main():
    root_dir = input("Введите путь к папке (Enter — текущая): ").strip() or "."

    if not os.path.isdir(root_dir):
        print(f"Ошибка: папка не найдена: {root_dir}")
        sys.exit(1)

    extensions_input = input(
        "Расширения через запятую (например, .md,.txt) или Enter — все файлы: "
    ).strip()

    extensions = None
    if extensions_input:
        extensions = {
            e.strip().lower() if e.strip().startswith(".") else "." + e.strip().lower()
            for e in extensions_input.split(",")
            if e.strip()
        }

    total_files = 0
    changed_files = 0
    total_blocks = 0

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for filename in filenames:
            if extensions is not None:
                _, ext = os.path.splitext(filename)
                if ext.lower() not in extensions:
                    continue

            file_path = os.path.join(dirpath, filename)
            total_files += 1

            changed, blocks = process_file(file_path)
            if changed:
                changed_files += 1
                total_blocks += blocks
                print(f"  обёрнуто блоков: {blocks}  —  {file_path}")

    print(f"\nОбработано файлов: {total_files}")
    print(f"Изменено файлов:   {changed_files}")
    print(f"Всего обёрнуто блоков: {total_blocks}")


if __name__ == "__main__":
    main()
