from flask import Flask

app = Flask(__name__)


@app.route("/user/<username>")
def show_user_profile(username):
    # Доступ к значению username из URL
    return f"Привет, {username}!"


if __name__ == "__main__":
    app.run(debug=True)
