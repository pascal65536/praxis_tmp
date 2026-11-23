from flask import Flask, render_template, request
import re

# Регулярное выражение для проверки email
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$"
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]

        # Валидация формы
        if not EMAIL_REGEX.match(email):
            return f"Ошибка: некорректный email '{email}'", 400

        # Обработка данных формы
        msg = f"Имя пользователя: {username}, Email: {email}"
        return msg
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
