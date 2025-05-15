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