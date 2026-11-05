from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
)
from forms import RegistrationForm
import os

from utils import load_json, save_json


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(256)


@app.route("/", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    user_lst = load_json("data", "user.json")
    if request.method == "POST" and form.validate_on_submit():
        new_user = {
            "id": str(len(user_lst) + 1),
            "username": form.username.data,
            "password": form.password.data,
            "confirm": form.confirm.data,
        }
        user_lst.append(new_user)
        # Запишем не таясь пароль в открытом виде. Чисто в учебных целях
        save_json("data", "user.json", user_lst)
        return "Пользователь зарегистрирован!"
    else:
        print(form.errors)
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
