import math


# === ЗАДАЧА 1 ===
class Wallet:
    def __init__(self, inital_balance):
        pass  # Ваш код

    def deposit(self, amount):
        pass  # Ваш код

    def withdraw(self, amount):
        pass  # Ваш код

    def get_balance(self):
        pass  # Ваш код


# === ЗАДАЧА 2 ===
class Triangle:
    def __init__(self, a, b, c):
        pass  # Ваш код

    def perimeter(self):
        pass  # Ваш код


class Circle:
    def __init__(self, r):
        pass  # Ваш код

    def perimeter(self):
        pass  # Ваш код


def calculate_total_perimeter(shapes):
    pass  # Ваш код


# === ЗАДАЧА 3 ===
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        pass  # Ваш код

    def __mul__(self, other):
        pass  # Ваш код

    def __eq__(self, other):
        pass  # Ваш код

    def __hash__(self):
        pass  # Ваш код

    def __str__(self):
        pass  # Ваш код


# === ЗАДАЧА 4 ===
class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def calculate_bonus(self):
        return self.base_salary * 0.10


class Manager(Employee):
    pass  # Ваш код
