from flask import Flask, render_template, redirect, url_for, request
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(256)


class MyForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def root():
    form = MyForm()
    if request.method == "POST":
        if form.validate_on_submit():
            return "Форма успешно отправлена!"
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
