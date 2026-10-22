from study import (
    Wallet,
    Triangle,
    Circle,
    calculate_total_perimeter,
    Vector2D,
    Employee,
    Manager,
)
import pytest
import math


# --- Тесты Задачи 1 (Инкапсуляция) ---
def test_wallet_initialization():
    w = Wallet(1000)
    assert w.get_balance() == 1000
    w_neg = Wallet(-500)
    assert w_neg.get_balance() == 0, "Баланс не может быть отрицательным при создании"


def test_wallet_operations():
    w = Wallet(100)
    assert w.deposit(50) is True
    assert w.get_balance() == 150
    assert w.deposit(-10) is False
    assert w.get_balance() == 150
    assert w.withdraw(50) is True
    assert w.get_balance() == 100
    assert w.withdraw(200) is False
    assert w.withdraw(-10) is False
    assert w.get_balance() == 100


# --- Тесты Задачи 2 (Полиморфизм) ---
def test_polymorphism_perimeter():
    t = Triangle(3, 4, 5)
    c = Circle(10)
    shapes = [t, c, Triangle(1, 1, 1)]
    # Ожидаемая сумма: 12 + 62.8318... + 3
    expected = 12 + (2 * math.pi * 10) + 3
    assert math.isclose(calculate_total_perimeter(shapes), expected, rel_tol=1e-5)


# --- Тесты Задачи 3 (Dunder-методы) ---
def test_vector_add():
    v1 = Vector2D(1, 2)
    v2 = Vector2D(3, 4)
    v3 = v1 + v2
    assert v3.x == 4 and v3.y == 6
    assert v1.x == 1, "Исходный вектор не должен изменяться"


def test_vector_mul():
    v = Vector2D(2, 3)
    v2 = v * 3
    assert v2.x == 6 and v2.y == 9


def test_vector_eq_and_str():
    v1 = Vector2D(5, 10)
    v2 = Vector2D(5, 10)
    assert v1 == v2
    assert str(v1) == "(5, 10)"


def test_vector_not_implemented():
    v = Vector2D(1, 1)
    # Проверяем, что при сложении с неподходящим типом не падает с TypeError,
    # а корректно обрабатывается (или падает с правильным TypeError от Python)
    with pytest.raises(TypeError):
        _ = v + "string"


# --- Тесты Задачи 4 (Наследование) ---
def test_manager_inheritance():
    m = Manager("Alice", 50000, 5)
    assert m.name == "Alice"
    assert m.base_salary == 50000
    assert hasattr(m, "team_size") and m.team_size == 5
    # Бонус: 10% от 50000 (5000) + 5% от 50000 за каждого из 5 членов (12500) = 17500
    assert m.calculate_bonus() == 17500.0
    # Проверка, что используется super() (косвенно, через наличие атрибутов родителя)
    assert isinstance(m, Employee)
