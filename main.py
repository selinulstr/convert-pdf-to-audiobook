from flask import Flask, render_template, redirect, request, url_for, flash
from gtts import gTTS
import os
from werkzeug.utils import secure_filename
import PyPDF2
import time

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"
language = "en"
mp3 = None


@app.route("/", methods=["GET", "POST"])
def home():
    global mp3
    mp3 = None
    if request.method == "POST":
        file_data = request.files["file"]
        file_name = secure_filename("text.pdf")
        file_data.save(os.path.join("static", file_name))
        with open("static/text.pdf", "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            converted = gTTS(text=text, lang=language, slow=False)
            time.sleep(20)
            mp3 = converted.save(savefile="static/welcome.mp3")
            return redirect(url_for("play"))

    return render_template("index.html")


@app.route("/play")
def play():
    return render_template("play.html")


if __name__ == "__main__":
    app.run(debug=True)