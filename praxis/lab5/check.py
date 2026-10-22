import requests

LONG_TITLE = "x" * 201 

# ---------- снимок состояния до тестов (для восстановления) ----------
r = requests.get("http://localhost:5000/tasks", params={"per_page": 100})
assert r.status_code == 200, "сервер не отвечает на GET /tasks"
ids_before = {t["id"] for t in r.json()["items"]}
created_ids = []         

print("=== Тесты Tasks API (http://localhost:5000) ===\n")

try:
    # ---------- 1. Корень: сервер жив, начальные значения на месте ----------
    r = requests.get("http://localhost:5000/")
    assert r.status_code == 200, f"GET / -> {r.status_code}, ожидался 200"
    assert r.json()["seed"] == len(ids_before), "seed не совпадает с числом задач"
    print("1. корень и seed ... ок")

    # ---------- 2. Список по умолчанию: обёртка с мета-информацией ----------
    r = requests.get("http://localhost:5000/tasks")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == len(ids_before)
    assert body["pages"] == 1
    assert body["per_page"] == 10
    print("2. список по умолчанию ... ок")

    # ---------- 3. Пейджинация ----------
    r = requests.get("http://localhost:5000/tasks", params={"page": 1, "per_page": 2})
    assert r.status_code == 200
    assert len(r.json()["items"]) == 2
    assert r.json()["total"] == len(ids_before)

    r = requests.get("http://localhost:5000/tasks", params={"page": 99, "per_page": 2})
    assert r.status_code == 200                   # за пределами — не ошибка, а пусто
    assert r.json()["items"] == []

    r = requests.get("http://localhost:5000/tasks", params={"page": 0})
    assert r.status_code == 400                   # невалидные параметры -> 400
    r = requests.get("http://localhost:5000/tasks", params={"per_page": 101})
    assert r.status_code == 400
    print("3. пейджинация ... ок")

    # ---------- 4. Сортировка: sort + order ----------
    r = requests.get("http://localhost:5000/tasks",
                     params={"sort": "title", "order": "asc", "per_page": 1})
    assert r.status_code == 200
    titles = [t["title"] for t in
              requests.get("http://localhost:5000/tasks", params={"sort": "title", "per_page": 100})
              .json()["items"]]
    assert titles == sorted(titles), "список не отсортирован по title asc"

    r = requests.get("http://localhost:5000/tasks",
                     params={"sort": "created_at", "order": "desc", "per_page": 1})
    first_id = r.json()["items"][0]["id"]
    assert first_id == max(ids_before), "последняя созданная должна быть первой в desc"

    r = requests.get("http://localhost:5000/tasks", params={"sort": "foo"})
    assert r.status_code == 400                   # неизвестное поле
    r = requests.get("http://localhost:5000/tasks", params={"order": "up"})
    assert r.status_code == 400                   # неизвестное направление
    print("4. сортировка ... ок")

    # ---------- 5. Фильтры: done и поиск q ----------
    r = requests.get("http://localhost:5000/tasks", params={"done": "true"})
    assert r.status_code == 200
    assert all(t["done"] for t in r.json()["items"])
    assert r.json()["total"] < len(ids_before)    # в seed есть и выполненные, и нет

    r = requests.get("http://localhost:5000/tasks", params={"q": "молоко"})
    assert len(r.json()["items"]) == 1
    assert "молоко" in r.json()["items"][0]["title"].lower()

    r = requests.get("http://localhost:5000/tasks", params={"done": "maybe"})
    assert r.status_code == 400
    print("5. фильтры ... ок")

    # ---------- 6. Создание: 201, монотонный id, значения по умолчанию ----------
    r = requests.post("http://localhost:5000/tasks", json={"title": "Новая задача"})
    assert r.status_code == 201, f"POST -> {r.status_code}, ожидался 201"
    tid = r.json()["id"]
    created_ids.append(tid)
    assert tid > max(ids_before), "id должен продолжать счётчик, а не переиспользоваться"
    assert r.json()["done"] is False              # default
    print("6. создание ... ок")

    # ---------- 7. Контроль создания: дубликаты и валидация ----------
    r = requests.post("http://localhost:5000/tasks", json={"title": "  Новая   задача "})
    assert r.status_code == 409                   # регистр и пробелы не спасают
    assert "error" in r.json()

    r = requests.post("http://localhost:5000/tasks", json={"done": True})
    assert r.status_code == 400                   # нет обязательного title

    r = requests.post("http://localhost:5000/tasks", json={"title": "   "})
    assert r.status_code == 422                   # пустое название

    r = requests.post("http://localhost:5000/tasks", json={"title": LONG_TITLE})
    assert r.status_code == 422                   # длиннее 200 символов

    r = requests.post("http://localhost:5000/tasks", data="not json",
                      headers={"Content-Type": "application/json"})
    assert r.status_code == 400                   # невалидный JSON
    print("7. контроль создания ... ок")

    # ---------- 8. Чтение одной задачи ----------
    r = requests.get("http://localhost:5000/tasks/" + str(tid))
    assert r.status_code == 200
    assert r.json()["title"] == "Новая задача"

    r = requests.get("http://localhost:5000/tasks/999999")
    assert r.status_code == 404

    r = requests.get("http://localhost:5000/tasks/abc")
    assert r.status_code == 404                   # <int:> не сработал — 404 до обработчика
    print("8. чтение ... ок")

    # ---------- 9. Обновление: PUT заменяет, PATCH — частично ----------
    r = requests.put("http://localhost:5000/tasks/" + str(tid),
                     json={"title": "Новая задача", "done": True})
    assert r.status_code == 200, f"PUT -> {r.status_code}"
    assert r.json()["done"] is True

    r = requests.put("http://localhost:5000/tasks/999999", json={"title": "x"})
    assert r.status_code == 404

    r = requests.patch("http://localhost:5000/tasks/" + str(tid), json={"done": False})
    assert r.status_code == 200
    assert r.json()["done"] is False
    assert r.json()["title"] == "Новая задача"    # PATCH не трогает остальные поля

    r = requests.patch("http://localhost:5000/tasks/" + str(tid), json={"title": "Купить молоко"})
    assert r.status_code == 409                   # переименование в чужое название

    r = requests.patch("http://localhost:5000/tasks/" + str(tid), json={"title": ""})
    assert r.status_code == 422
    print("9. обновление ... ок")

    # ---------- 10. Удаление: 204, идемпотентность, монотонность id ----------
    r = requests.delete("http://localhost:5000/tasks/" + str(tid))
    assert r.status_code == 204
    assert not r.content                          # тело пустое

    r = requests.delete("http://localhost:5000/tasks/" + str(tid))
    assert r.status_code == 404                   # повторный DELETE — уже нечего

    a = requests.post("http://localhost:5000/tasks", json={"title": "Задача А"}).json()["id"]
    b = requests.post("http://localhost:5000/tasks", json={"title": "Задача Б"}).json()["id"]
    created_ids += [a, b]
    assert b > a, "id не должны переиспользоваться после удаления"
    print("10. удаление ... ок")

    print("\nВсе тесты пройдены.")

finally:
    # ---------- восстановление состояния сервера ----------
    # удаляем всё, чего не было до прогона
    r = requests.get("http://localhost:5000/tasks", params={"per_page": 100})
    leftovers = [t["id"] for t in r.json()["items"] if t["id"] not in ids_before]
    for task_id in leftovers:
        requests.delete("http://localhost:5000/tasks/" + str(task_id))
    print(f"Состояние сервера восстановлено (удалено задач: {len(leftovers)}).")
