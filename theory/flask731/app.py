from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print(request.form)
        
        username = request.form["username"]
        email = request.form["email"]

        # Обработка данных формы
        msg = f"Имя пользователя: {username}, Email: {email}"

        print(msg)
        return msg
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
