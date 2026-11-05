from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    BooleanField,
    TextAreaField,
    PasswordField,
    FileField,
    TelField,
    URLField,
    EmailField,
    ColorField,
    RadioField,
    Flags,
    DateField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    NumberRange,
    ValidationError,
    EqualTo,
)
import string
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(256)


choices = [
    (0, "zero"),
    (1, "one"),
    (2, "two"),
]


class DemoForm(FlaskForm):
    def validator_url(self, field):
        url = field.data
        if "vk.ru" in url or "ok.ru" in url or "vk.com" in url:
            return
        raise ValidationError("URL должен содержать ссылки на ВК или ОК.")

    def validator_username(self, field):
        username = field.data
        if set(username) <= set(string.ascii_lowercase + string.digits + "_"):
            return
        raise ValidationError(
            "Имя пользователя должно содержать только латинские буквы, цифры и подчеркивание."
        )

    username = StringField("Username", validators=[DataRequired(), validator_username])
    is_correct = BooleanField("Bool", validators=[DataRequired()])
    text = TextAreaField("Text", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    url = URLField("URL", validators=[DataRequired(), validator_url])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    color = ColorField("Color", validators=[DataRequired()])
    radio = RadioField("RadioField", validators=[DataRequired()], choices=choices)
    date = DateField("DateField", validators=[DataRequired()])
    submit = SubmitField("Submit")


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
