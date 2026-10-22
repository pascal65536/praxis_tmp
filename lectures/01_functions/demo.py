# add two
def calc(a, b):
    return a + b


print(calc(1, 3))


# divide two
def divide(a, b):
    return a / b


print(divide(123, 10))


# add seven
def multiple(a, b, c, d, e, f, g):
    return a * b * c * d * e * f * g


print(multiple(1, 2, 3, 4, 5, 6, 7))


# add all
def multiple_all(*data):
    result = 1
    for d in data:
        result *= d
    return result


print(multiple_all(1, 2, 3, 4, 5, 6, 7))


# Стоимость со скидкой
def price(a, b, sale):
    return a * b / 100 * (100 - sale)


print(price(23, 73, 0))
print(price(23, 73, 1))
print(price(23, 73, 10))


# Стоимость со скидкой, дефолтный параметр
def price_defaullt(a, b, sale=0):
    return a * b / 100 * (100 - sale)


print(price_defaullt(23, 73))
print(price_defaullt(23, 73, sale=1))
print(price_defaullt(23, 73, sale=10))


# Стоимость со скидкой, именованные параметры
def price_named(count, cost, sale=0):
    return count * cost / 100 * (100 - sale)


print(price_named(count=23, cost=73))
print(price_named(count=23, sale=1, cost=73))
print(price_named(sale=10, count=23, cost=73))


# Разные типы, список
def price_shopping_lst(msg, *data, sale=0):
    tax = 0
    for d in data:
        tax += d[0] * d[1] / 100 * (100 - sale)
    return f"{msg}: {tax:.2f}"


shopping_lst = [
    (23, 73),
    (1, 100),
    (10, 1),
]

print(price_shopping_lst("Итого", *shopping_lst, sale=2))


# Разные типы, словарь
def price_shopping_json(msg, **data):
    result = []
    result.append(msg)
    for k, v in data.items():
        result.append(f'{v["name"]}: {v["cost"] * v["count"]}')
    return "\n".join(result)


shopping_json = {
    "1": {"name": "potatoes", "cost": 10, "count": 10},
    "2": {"name": "tomato", "cost": 20, "count": 20},
    "3": {"name": "apple", "cost": 30, "count": 30},
    "4": {"name": "orange", "cost": 40, "count": 40},
    "5": {"name": "pineaple", "cost": 50, "count": 50},
}

print(price_shopping_json("Список покупок", **shopping_json))


# В общем виде
def price_all(msg, *args, sale=0, **kwargs):
    print(f"{msg=}")
    print(f"{sale=}")
    print(f"{args=}")
    print(f"{kwargs=}")


print(price_all("Список покупок", sale=10, *shopping_lst, **shopping_json))
