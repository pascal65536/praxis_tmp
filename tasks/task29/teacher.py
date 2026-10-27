def solve(data):
    collect = list()
    lections = list()
    students = list()
    data_lst = data.split("|")
    s = 0
    while len(data_lst[s:]) > 0:
        lection, count = data_lst[s].split(" ")
        lections.append(lection)
        count = int(count)
        for study in data_lst[s + 1 : s + count + 1]:
            student, grade = study.split(" ")
            students.append(student)
            grade = int(grade)
            collect.append(
                {
                    "lection": lection,
                    "student": student,
                    "grade": grade,
                }
            )

        s = s + count + 1
    lections = sorted(set(lections))
    students = sorted(set(students))

    matrix = list()
    for student in students:
        matrix.append([0 for _ in lections])

    for stdgrd in collect:
        lection = lections.index(stdgrd["lection"])
        student = students.index(stdgrd["student"])
        grade = stdgrd["grade"]
        matrix[student][lection] = grade

    lections_avg = list()
    for row in range(len(lections)):
        lections_avg.append(
            (
                sum(matrix[n][row] for n in range(len(students))) / len(students),
                lections[row],
            )
        )
    students_avg = list()
    for col in range(len(students)):
        students_avg.append(
            (
                sum(matrix[col][n] for n in range(len(lections))) / len(lections),
                students[col],
            )
        )

    lc = min(lections_avg)[1]
    st = " ".join([stdn[1] for stdn in sorted(students_avg, reverse=True)])
    return f"{lc}|{st}"


if __name__ == "__main__":
    data = "Физика 4|Кузнецов 5|Морозов 3|Соколов 4|Васильев 5|Химия 3|Кузнецов 4|Морозов 2|Соколов 5|Биология 5|Васильченко 3|Кузнецов 4|Морозов 3|Соколов 5|Васильев 4|Английский 4|Кузнецов 5|Морозов 4|Соколов 3|Васильев 5"
    print(solve(data))
    print("Химия|Кузнецов Соколов Васильев Морозов Васильченко")
