import math
import sys


try:
    from student import (
        Wallet,
        Triangle,
        Circle,
        calculate_total_perimeter,
        Vector2D,
        Employee,
        Manager,
    )
except Exception as error:
    print("Не удалось загрузить student.py.")
    print(f"{type(error).__name__}: {error}")
    print("Проверьте имя файла, имена классов и код вне методов.")
    raise SystemExit(2)


TESTS = []


def test(group, title):
    """Регистрирует проверку в общем списке."""
    def decorator(function):
        TESTS.append((group, title, function))
        return function

    return decorator


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def require_equal(actual, expected, message=""):
    if actual != expected:
        prefix = f"{message}\n" if message else ""
        raise AssertionError(
            f"{prefix}Ожидалось: {expected!r}\nПолучено: {actual!r}"
        )


def require_close(actual, expected, message=""):
    if not isinstance(actual, (int, float)) or not math.isclose(
        actual, expected, rel_tol=1e-9, abs_tol=1e-9
    ):
        prefix = f"{message}\n" if message else ""
        raise AssertionError(
            f"{prefix}Ожидалось значение, близкое к {expected!r}.\n"
            f"Получено: {actual!r}"
        )


# === ЗАДАЧА 1: WALLET ===


@test("1. Wallet", "Создание кошелька и защищённый баланс")
def test_wallet_initialization():
    wallet = Wallet(1000)
    require_equal(wallet.get_balance(), 1000)
    require(hasattr(wallet, "_balance"), "Отсутствует атрибут _balance.")
    require_equal(wallet._balance, 1000)

    negative = Wallet(-500)
    require_equal(negative.get_balance(), 0)


@test("1. Wallet", "Пополнение счёта")
def test_wallet_deposit():
    wallet = Wallet(100)

    require(wallet.deposit(50) is True, "Успешный deposit() должен вернуть True.")
    require_equal(wallet.get_balance(), 150)

    require(wallet.deposit(-10) is False, "deposit(-10) должен вернуть False.")
    require(wallet.deposit(0) is False, "deposit(0) должен вернуть False.")
    require_equal(wallet.get_balance(), 150, "Баланс изменился после неверного пополнения.")


@test("1. Wallet", "Снятие средств и недостаточный баланс")
def test_wallet_withdraw():
    wallet = Wallet(100)

    require(wallet.withdraw(40) is True, "Успешный withdraw() должен вернуть True.")
    require_equal(wallet.get_balance(), 60)

    require(wallet.withdraw(200) is False, "Недостаточный баланс: ожидался False.")
    require(wallet.withdraw(-10) is False, "withdraw(-10) должен вернуть False.")
    require(wallet.withdraw(0) is False, "withdraw(0) должен вернуть False.")
    require_equal(wallet.get_balance(), 60, "Баланс изменился после неверного снятия.")


@test("1. Wallet", "Снятие всей доступной суммы")
def test_wallet_withdraw_all():
    wallet = Wallet(75)
    require(wallet.withdraw(75) is True, "Разрешено снять всю доступную сумму.")
    require_equal(wallet.get_balance(), 0)
    require(wallet.withdraw(1) is False, "Снятие с пустого кошелька должно вернуть False.")


# === ЗАДАЧА 2: ФИГУРЫ ===


@test("2. Фигуры", "Периметры треугольника и окружности")
def test_shape_perimeters():
    require_equal(Triangle(3, 4, 5).perimeter(), 12)
    require_equal(Triangle(1.5, 2.5, 3).perimeter(), 7)
    require_close(Circle(10).perimeter(), 2 * math.pi * 10)


@test("2. Фигуры", "Суммарный периметр списка фигур")
def test_total_perimeter():
    shapes = [Triangle(3, 4, 5), Circle(10), Triangle(1, 1, 1)]
    expected = 12 + 2 * math.pi * 10 + 3
    require_close(calculate_total_perimeter(shapes), expected)


@test("2. Фигуры", "Пустой список фигур")
def test_empty_shapes():
    require_equal(calculate_total_perimeter([]), 0)


@test("2. Фигуры", "Полиморфизм без проверки конкретного класса")
def test_duck_typing():
    class AdditionalShape:
        def perimeter(self):
            return 7.5

    shapes = [AdditionalShape(), Triangle(2, 3, 4)]
    require_close(calculate_total_perimeter(shapes), 16.5)


# === ЗАДАЧА 3: VECTOR2D ===


@test("3. Vector2D", "Сложение векторов и неизменность исходных объектов")
def test_vector_add():
    first = Vector2D(1, 2)
    second = Vector2D(3, 4)
    result = first + second

    require_equal((result.x, result.y), (4, 6))
    require(result is not first and result is not second, "__add__ должен создать новый вектор.")
    require_equal((first.x, first.y), (1, 2))
    require_equal((second.x, second.y), (3, 4))


@test("3. Vector2D", "Сложение с неподдерживаемым типом")
def test_vector_add_wrong_type():
    vector = Vector2D(1, 1)

    require(
        vector.__add__("string") is NotImplemented,
        "__add__ должен вернуть NotImplemented для неподдерживаемого типа.",
    )

    try:
        _ = vector + "string"
    except TypeError:
        return

    raise AssertionError("Операция Vector2D + string должна вызвать TypeError.")


@test("3. Vector2D", "Умножение на int и float")
def test_vector_mul():
    vector = Vector2D(2, 3)

    by_int = vector * 3
    require_equal((by_int.x, by_int.y), (6, 9))

    by_float = vector * 0.5
    require_equal((by_float.x, by_float.y), (1.0, 1.5))
    require(by_float is not vector, "__mul__ должен создать новый вектор.")
    require_equal((vector.x, vector.y), (2, 3), "Исходный вектор изменился.")


@test("3. Vector2D", "Умножение на неподдерживаемый тип")
def test_vector_mul_wrong_type():
    vector = Vector2D(2, 3)

    require(
        vector.__mul__("3") is NotImplemented,
        "__mul__ должен вернуть NotImplemented для неподдерживаемого типа.",
    )

    try:
        _ = vector * "3"
    except TypeError:
        return

    raise AssertionError("Операция Vector2D * string должна вызвать TypeError.")


@test("3. Vector2D", "Сравнение векторов")
def test_vector_equality():
    vector = Vector2D(5, 10)

    require(vector == Vector2D(5, 10), "Векторы с одинаковыми координатами должны быть равны.")
    require(vector != Vector2D(5, 11), "Векторы с разными координатами не должны быть равны.")
    require(
        vector.__eq__((5, 10)) is NotImplemented,
        "__eq__ должен вернуть NotImplemented для неподдерживаемого типа.",
    )
    require((vector == (5, 10)) is False, "Сравнение с другим типом должно вернуть False.")


@test("3. Vector2D", "Строковое представление")
def test_vector_string():
    require_equal(str(Vector2D(5, 10)), "(5, 10)")
    require_equal(str(Vector2D(-1, 2.5)), "(-1, 2.5)")


@test("3. Vector2D", "Хеширование, set и dict")
def test_vector_hash():
    first = Vector2D(1, 2)
    same = Vector2D(1, 2)
    different = Vector2D(2, 1)

    require_equal(hash(first), hash(same), "Равные векторы должны иметь одинаковый хеш.")

    vectors = {first, same, different}
    require_equal(len(vectors), 2, "Равные векторы должны считаться одним элементом set.")

    distances = {first: "исходный"}
    require_equal(distances[same], "исходный")


# === ЗАДАЧА 4: СОТРУДНИКИ ===


@test("4. Сотрудники", "Бонус базового сотрудника")
def test_employee_bonus():
    employee = Employee("Bob", 40000)
    require_equal(employee.name, "Bob")
    require_equal(employee.base_salary, 40000)
    require_close(employee.calculate_bonus(), 4000.0)


@test("4. Сотрудники", "Наследование и атрибуты менеджера")
def test_manager_initialization():
    manager = Manager("Alice", 50000, 5)

    require(isinstance(manager, Employee), "Manager должен наследоваться от Employee.")
    require_equal(manager.name, "Alice")
    require_equal(manager.base_salary, 50000)
    require_equal(manager.team_size, 5)


@test("4. Сотрудники", "Бонус менеджера")
def test_manager_bonus():
    require_close(Manager("Alice", 50000, 5).calculate_bonus(), 17500.0)
    require_close(Manager("Bob", 60000, 0).calculate_bonus(), 6000.0)
    require_close(Manager("Eve", 45000, 2).calculate_bonus(), 9000.0)


def main():
    passed = 0
    failures = []
    group_results = {}

    for group, title, function in TESTS:
        group_results.setdefault(group, [0, 0])
        group_results[group][1] += 1

        try:
            function()
        except Exception as error:
            failures.append((group, title, error))
        else:
            passed += 1
            group_results[group][0] += 1

    total = len(TESTS)
    print(f"Пройдено проверок: {passed} из {total}.\n")

    print("Результаты по задачам:")
    for group, (group_passed, group_total) in group_results.items():
        print(f"  {group}: {group_passed}/{group_total}")

    if failures:
        print("\nНепройденные проверки:")

        for group, title, error in failures:
            print("\n" + "=" * 64)
            print(f"{group}: {title}")

            if isinstance(error, AssertionError) and str(error):
                print(str(error))
            else:
                print(f"{type(error).__name__}: {error}")

        print("\nРешение пока не проходит все проверки.")
        return 1

    print("\nВсе проверки пройдены успешно!")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nПроверка прервана пользователем.")
        sys.exit(130)
