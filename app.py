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