import discord
from discord.ext import commands
import openai
import os
import json
import threading
import datetime
from flask import Flask, render_template, jsonify, redirect
import re

# ======== Persistent Storage =========
USER_FILE = "users.json"
GLOBAL_FILE = "global_state.json"

def load_json(filename, default):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default, f)
    with open(filename, "r") as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

users = load_json(USER_FILE, {})
global_state = load_json(GLOBAL_FILE, {
    "last_event_time": None,
    "current_event": None,
})

def save_users(): save_json(USER_FILE, users)
def save_global(): save_json(GLOBAL_FILE, global_state)

def get_user(uid, name=None):
    uid = str(uid)
    if uid not in users:
        users[uid] = {
            "Name": name or "",
            "Tier": "10-C (Human)",
            "HP": 100,
            "Origin Essence": 0,
            "Inventory": [],
            "Story": {"chapter": 1, "scene": 1, "history": []},
            "LastStory": ""
        }
        save_users()
    return users[uid]

# ======= OPENAI GPT Setup =======
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
client_ai = openai.OpenAI(api_key=OPENAI_API_KEY)

ELY_PROMPT = """
World: Elysiad is a multiverse where anime and web novel worlds overlap.
You are the game master/narrator. The player is a solo human, with no powers, and explores worlds, discovers lore, makes choices, and gradually grows stronger.

Mechanics:
- For each scene, present 5 choices:
  - 1 leads to death (not obvious)
  - 1 progresses story
  - 2 are world-building (lore, bring user back to choose)
  - 1 is random (good/bad by dice roll)
- Roll 1d100: if <50, negative outcome, if >=50, positive.
- Show the result, then present next scene.
- At the end of each scene, summarize key stats: Tier, HP, Origin Essence, Inventory.

Context:
- The world can be affected by current global events: {GLOBAL_EVENT}
- Player's journey so far: {HISTORY}

Respond in a light-novel style.
Present next set of 5 choices at the end of the message (list as "Choices: 1. ... 2. ... etc.")
"""

# ========== GLOBAL EVENTS ==========
EVENT_INTERVAL = 60 * 60  # Every hour (in seconds)

def next_event_time():
    if not global_state["last_event_time"]:
        return 0
    last = datetime.datetime.fromisoformat(global_state["last_event_time"])
    return (last + datetime.timedelta(seconds=EVENT_INTERVAL) - datetime.datetime.utcnow()).total_seconds()

def time_until_next_event():
    seconds = max(int(next_event_time()), 0)
    return seconds

def generate_global_event():
    prompt = (
        "Invent a new global event for a multiverse crossover of anime/webnovel worlds. "
        "Give: Event Name, World(s), and Description (1-2 sentences, no commentary)."
    )
    response = client_ai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=200,
        temperature=1.2
    )
    lines = response.choices[0].message.content.splitlines()
    name, world, desc = "Event", "Unknown", ""
    for l in lines:
        if "Event Name:" in l: name = l.split(":",1)[1].strip()
        if "World(s):" in l: world = l.split(":",1)[1].strip()
        if "Description:" in l: desc = l.split(":",1)[1].strip()
    event = f"{name} [{world}]: {desc}"
    global_state["current_event"] = event
    global_state["last_event_time"] = datetime.datetime.utcnow().isoformat()
    save_global()
    print("New global event:", event)
    return event

def auto_event_scheduler():
    while True:
        if next_event_time() <= 0:
            ev = generate_global_event()
        threading.Event().wait(60)

threading.Thread(target=auto_event_scheduler, daemon=True).start()

# ========== DISCORD BOT ==========
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Elysiad Bot Online as {bot.user}")

@bot.command()
async def start(ctx):
    u = get_user(ctx.author.id, ctx.author.display_name)
    u["Name"] = ctx.author.display_name
    save_users()
    await ctx.send(f"{ctx.author.mention}, your Elysiad solo adventure begins! Use `!choose <number>` to pick choices.")

@bot.command()
async def stats(ctx):
    u = get_user(ctx.author.id)
    embed = discord.Embed(title=f"{u['Name']}'s Stat Sheet", color=discord.Color.purple())
    embed.add_field(name="Tier", value=u['Tier'], inline=False)
    embed.add_field(name="HP", value=u['HP'], inline=True)
    embed.add_field(name="Origin Essence", value=u['Origin Essence'], inline=True)
    embed.add_field(name="Inventory", value=", ".join(u["Inventory"]) if u["Inventory"] else "Empty", inline=False)
    embed.add_field(name="Progress", value=f"Ch. {u['Story']['chapter']}, Scene {u['Story']['scene']}", inline=False)
    await ctx.send(embed=embed)

def remove_duplicate_choices(text):
    # Finds all "Choices:" sections and only keeps the first one
    parts = re.split(r'Choices:', text)
    if len(parts) > 2:
        return parts[0] + "Choices:" + parts[1]
    return text

@bot.command()
async def choose(ctx, number: int):
    u = get_user(ctx.author.id)
    history = "\n".join(u['Story'].get("history", [])[-5:])
    prompt = ELY_PROMPT.replace("{HISTORY}", history)\
                      .replace("{GLOBAL_EVENT}", global_state.get("current_event") or "None")
    prompt += f"\nCurrent scene: Chapter {u['Story']['chapter']} Scene {u['Story']['scene']}\n"
    prompt += f"User chose: {number}"
    response = client_ai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=700,
        temperature=0.95
    )
    story = response.choices[0].message.content
    story = remove_duplicate_choices(story)   # PATCH: removes double "Choices:"
    u['Story']['history'].append(f"Choice {number}: {story[:200]}...")  # Short log, trim as needed
    u['LastStory'] = story
    u['Story']['scene'] += 1
    save_users()
    await ctx.send(f"{ctx.author.mention}:\n{story}")

@bot.command()
async def last(ctx):
    u = get_user(ctx.author.id)
    await ctx.send(f"{ctx.author.mention} Previous scene:\n{u['LastStory']}")

# ========== SHOP COMMANDS ==========
@bot.command()
async def shop(ctx):
    u = get_user(ctx.author.id)
    items = [
        {"name": "Senzu Bean", "desc": "Restore HP to full", "stat": "HP", "amt": 100-u["HP"], "cost": 10},
        {"name": "Luck Potion", "desc": "Feel lucky", "stat": "Origin Essence", "amt": 5, "cost": 20}
    ]
    u["Shop"] = items
    lines = [f"{i+1}. {x['name']} — {x['desc']} [Cost: {x['cost']} OE]" for i,x in enumerate(items)]
    save_users()
    await ctx.send("**Shop Items:**\n" + "\n".join(lines) + "\nBuy with `!buy <number>`.")

@bot.command()
async def buy(ctx, number: int):
    u = get_user(ctx.author.id)
    items = u.get("Shop", [])
    if not items or number < 1 or number > len(items):
        await ctx.send("No shop or invalid item.")
        return
    item = items[number-1]
    if u["Origin Essence"] < item["cost"]:
        await ctx.send("Not enough Origin Essence!")
        return
    u["Origin Essence"] -= item["cost"]
    if item["stat"] == "HP":
        u["HP"] = 100
    else:
        u[item["stat"]] += item["amt"]
    u["Inventory"].append(item["name"])
    save_users()
    await ctx.send(f"You bought {item['name']}!")

# ========== FLASK DASHBOARD ==========
app = Flask(__name__)

def seconds_to_clock(secs):
    m = secs // 60
    s = secs % 60
    return f"{m}:{s:02d}"

@app.route("/")
def home():
    all_users = load_json(USER_FILE, {})
    return render_template("dashboard.html",
                           users=all_users,
                           global_event=global_state.get("current_event"),
                           time_left=seconds_to_clock(time_until_next_event()))

@app.route("/user/<user_id>")
def user_sheet(user_id):
    all_users = load_json(USER_FILE, {})
    u = all_users.get(user_id)
    if not u:
        return "User not found", 404
    return render_template("char_sheet.html", user=u)

@app.route("/api/timer")
def timer():
    return jsonify({"seconds": time_until_next_event(),
                    "event": global_state.get("current_event")})

def run_dashboard():
    app.run(host="0.0.0.0", port=5000)

# Start Flask in background
threading.Thread(target=run_dashboard, daemon=True).start()

# Run the Discord bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
