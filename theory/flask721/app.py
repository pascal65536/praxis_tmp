from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    title = "Моя страница"
    username = "Иван"
    items = ["яблоко", "банан", "груша"]
    is_verified = True
    text = '<script>var a = 123;</script>'
    return render_template("template.html", title=title, username=username, items=items, is_verified=is_verified, text=text)


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='10.42.0.1', port=5000)
