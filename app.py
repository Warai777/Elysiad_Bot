@app.route("/")
def login_page_redirect():
    return redirect(url_for("login_page"))
