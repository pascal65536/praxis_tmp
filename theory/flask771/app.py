from flask import Flask, render_template, send_from_directory


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"


@app.route("/uploads/<path:filename>")
def uploads_folder(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload")
def upload():
    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
