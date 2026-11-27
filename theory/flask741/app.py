from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Путь для сохранения загруженных файлов
app.config["UPLOAD_FOLDER"] = "uploads"
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.mkdir(app.config["UPLOAD_FOLDER"])


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]

        # Проверка, был ли выбран файл
        if file.filename == "":
            return "No selected file"

        # Сохранение файла
        file.save(f"{app.config['UPLOAD_FOLDER']}/{file.filename}")
        return "File successfully uploaded"
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
