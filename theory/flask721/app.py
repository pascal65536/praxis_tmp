from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    title = "Моя страница"
    username = "Иван"
    items = ["яблоко", "банан", "груша"]
    is_verified = True
    text = '<script>var a = 123;</script>'
    return render_template("index.html", 
        title=title, 
        username=username, 
        items=items, 
        is_verified=is_verified, 
        text=text)


@app.route("/dict_tmp")
def dict_tmp():
    apple_dct = {
        "apple": "Яблоко",
        "pineapple": "Ананас",
    }
    return render_template("dict_tmp.html", apple_dct=apple_dct)


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='10.42.0.1', port=5000)
