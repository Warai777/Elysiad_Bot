from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client
import os, random
from player import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elysiad.db'
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")
db = SQLAlchemy(app)

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
reset_codes = {}

@app.route("/")
def login_page_redirect():
    return redirect(url_for("login_page"))

@app.route("/login")
def login_page():
    return render_template("home.html")

@app.route("/login", methods=["POST"])
def login():
    identifier = request.form["identifier"]
    password = request.form["password"]
    user = User.query.filter((User.email == identifier) | (User.phone == identifier)).first()
    if user and user.password == password:
        session["user"] = user.username
        return redirect(url_for("library"))
    flash("Invalid credentials")
    return redirect(url_for("login_page"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        phone = request.form["phone"]
        username = request.form["username"]
        password = request.form["password"]
        new_user = User(email=email, phone=phone, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login_page"))
    return render_template("signup_page.html")

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        identifier = request.form["identifier"]
        user = User.query.filter((User.email == identifier) | (User.phone == identifier)).first()
        if user:
            code = str(random.randint(100000, 999999))
            reset_codes[identifier] = code
            if identifier == user.email:
                message = Mail(from_email='no-reply@elysiad.com', to_emails=user.email,
                               subject='Elysiad Password Reset Code',
                               html_content=f'<p>Your code is: <strong>{code}</strong></p>')
                SendGridAPIClient(SENDGRID_API_KEY).send(message)
            else:
                Client(TWILIO_SID, TWILIO_TOKEN).messages.create(
                    body=f"Your Elysiad code is: {code}", from_=TWILIO_NUMBER, to=user.phone)
            return f"Code sent to {identifier}."
        return "Identifier not found."
    return render_template("forgot-password.html")

@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        identifier = request.form["identifier"]
        code = request.form["code"]
        new_password = request.form["new_password"]
        if reset_codes.get(identifier) == code:
            user = User.query.filter((User.email == identifier) | (User.phone == identifier)).first()
            if user:
                user.password = new_password
                db.session.commit()
                return "Password reset successful."
        return "Invalid code."
    return render_template("reset-password.html")