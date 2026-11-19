from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
)
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from forms import RegistrationForm, LoginForm
from utils import load_json, save_json
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(256)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    users_dct = load_json("data", "user.json")
    user_dct = users_dct.get(str(user_id))
    user_obj = User(str(user_id), user_dct["username"], user_dct["password"])
    return user_obj


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    users_dct = load_json("data", "user.json")
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        for key, user in users_dct.items():
            if user["username"] == username and user["password"] == password:
                user_obj = User(key, username, password)
                login_user(user_obj)
                return redirect(url_for("index"))
    else:
        print(form.errors)
    return render_template("login.html", form=form)


@app.route("/hidden")
@login_required
def hidden():
    return f"Если вы можете прочитать эту надпись, значит вы авторизованный пользователь. Привет, {current_user.username}!"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/edit/", methods=["GET", "POST"])
@login_required
def edit():
    form = RegistrationForm(obj=current_user)
    if request.method == "POST" and form.validate_on_submit():
        user_dct = load_json("data", "user.json")
        for ids, user in user_dct.items():
            if user["username"] != form.username.data:
                continue
        else:
            ids = str(len(user_dct) + 1)
        new_user = {
            "username": form.username.data,
            "password": form.password.data,
            "confirm": form.confirm.data,
        }
        user_dct[ids] = new_user
        # Запишем не таясь пароль в открытом виде. Чисто в учебных целях
        save_json("data", "user.json", user_dct)
        return "Пользователь зарегистрирован!"
    return render_template("register.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    user_dct = load_json("data", "user.json")
    if request.method == "POST" and form.validate_on_submit():
        new_user = {
            "username": form.username.data,
            "password": form.password.data,
            "confirm": form.confirm.data,
        }
        user_dct[form.username.data] = new_user
        # Запишем не таясь пароль в открытом виде. Чисто в учебных целях
        save_json("data", "user.json", user_dct)
        return "Пользователь зарегистрирован!"
    else:
        print(form.errors)
    return render_template("register.html", form=form)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
