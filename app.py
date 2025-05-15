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

@app.route("/choose_world")
def choose_world():
    return render_template("choose_world.html")

@app.route("/journal")
def journal():
    player_info = session.get("player")
    if not player_info:
        return redirect(url_for("login_page"))

    from player import load_player
    from lore_manager import get_lore_pages, unlock_lore
    from archivist_lore import ARCHIVIST_LORE

    player = load_player(player_info["name"])
    for i in range(len(ARCHIVIST_LORE)):
        unlock_lore(player, i)
    lore_pages = get_lore_pages(player, page_index=0)
    return render_template("journal.html", player=player,
                           left_page=lore_pages["left"], right_page=lore_pages["right"],
                           page_info=lore_pages)

@app.route("/get_lore_page")
def get_lore_page():
    player_info = session.get("player")
    if not player_info:
        return jsonify({"error": "No player found"}), 401

    from player import load_player
    from lore_manager import get_lore_pages, unlock_lore
    from archivist_lore import ARCHIVIST_LORE

    page_index = int(request.args.get("page", 0))
    player = load_player(player_info["name"])
    for i in range(len(ARCHIVIST_LORE)):
        unlock_lore(player, i)
    lore_pages = get_lore_pages(player, page_index=page_index)
    return jsonify({"left": lore_pages["left"], "right": lore_pages["right"],
                    "current_page": lore_pages["current_page"], "total_pages": lore_pages["total_pages"]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
