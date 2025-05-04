from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create_character")
def create_character():
    return render_template("create_character.html")

@app.route("/submit_character", methods=["POST"])
def submit_character():
    name = request.form.get("name")
    background = request.form.get("background")
    trait = request.form.get("trait")

    print(f"Character Created: {name}, {background}, {trait}")

    return redirect(url_for("library"))

@app.route("/library")
def library():
    return render_template("library.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)