# i11.py
name = [f"Студент{i:02d}" for i in range(1, 21)]
grade = [[i % 5 + 1 for _ in range(5)] for i in range(1, 21)]
ret = calc(name, grade)
