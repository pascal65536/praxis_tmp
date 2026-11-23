from flask import Flask, render_template, redirect, url_for, request
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(256)


class MyForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message="Name обязателен")])
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email обязателен"),
            Email(message="Введите корректный email"),
            Length(max=120, message="Email слишком длинный"),
        ],
    )
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def root():
    form = MyForm()
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            return f"Форма успешно отправлена! Имя: {name}, Email: {email}"
        else:
            print(form.errors)
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
