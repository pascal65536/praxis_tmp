from flask import Flask, render_template, redirect, url_for, request
import os


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "POST":
        name = request.form.get("name")
        if len(name) > 0:
            return "Форма успешно отправлена!"
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
