from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/user")
@app.route("/user/")
@app.route("/user/<username>")
def user(username="Неизвестный пользователь"):
    return render_template("user.html", username=username)


if __name__ == "__main__":
    app.run(debug=True)
