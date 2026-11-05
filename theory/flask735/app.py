from flask import Flask, render_template, redirect, url_for, request
from form import DemoForm
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(256)


@app.route("/", methods=["GET", "POST"])
def root():
    form = DemoForm()
    if request.method == "POST" and form.validate_on_submit():
        return "Форма успешно отправлена!"
    else:
        print(form.errors)
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
