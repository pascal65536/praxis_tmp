from student import solve as study
import base64

with open("teacher.b64", "r", encoding="ascii") as f:
    b64 = f.read().strip()

ns = {}
exec(compile(base64.b64decode(b64).decode("utf-8"), "<teacher>", "exec"), ns)
teach = ns["solve"]

with open("data.txt", encoding="utf8") as f:
    lines = f.readlines()

counter = 0
for line in lines:
    line = line.rstrip("\n")
    if "|" not in line:
        continue
    author_id, message = line.split("|", 1)
    message = message.strip()
    author_id = int(author_id)
    teach_response = teach(author_id, message)
    study_response = study(author_id, message)
    if teach_response != study_response:
        print(author_id)
        print(message)
        print("Teach:", teach_response)
        print("Study:", study_response)
        print("-" * 8)
        counter += 1

print(counter)
