from flask import Flask, request

app = Flask(__name__)


@app.route("/search")
def search():
    query = request.args.get("q", 'unknown')
    if query:
        return f"""
        <a href='https://www.google.com/search?q={query}'>https://www.google.com/search?q={query}</a>
        """
        # return f"Результаты поиска для: {query}"
    else:
        return "Введите поисковый запрос"


if __name__ == "__main__":
    app.run(debug=True)
