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

@app.route("/create_character")
def create_character():
    return render_template("create_character.html")

@app.route("/submit_character", methods=["POST"])
def submit_character():
    name = request.form.get("name")
    background = request.form.get("background")
    trait = request.form.get("trait")
    session["player"] = {"name": name, "background": background, "trait": trait}
    return redirect(url_for("library"))

@app.route("/library")
def library():
    player = session.get("player")
    return render_template("library.html", player=player)
