import discord
from discord.ext import commands
import json
import os

DATA_FILE = "users.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

users = load_users()

def get_user(user_id, name=None):
    user_id = str(user_id)
    if user_id not in users:
        users[user_id] = {
            "Name": name or "",
            "Tier": "10-C (Human)",
            "HP": 100,
            "Origin Essence": 0,
            "Inventory": [],
            "Story": {
                "chapter": 1,
                "scene": 1
            }
        }
        save_users(users)
    return users[user_id]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command()
async def start(ctx):
    u = get_user(ctx.author.id, ctx.author.display_name)
    u["Name"] = ctx.author.display_name
    save_users(users)
    await ctx.send(f"{ctx.author.mention}, your Elysiad solo journey begins! Use `!choose <number>` to make choices.")

@bot.command()
async def stats(ctx):
    u = get_user(ctx.author.id)
    embed = discord.Embed(title=f"{u['Name']}'s Stat Sheet", color=discord.Color.blue())
    embed.add_field(name="Tier", value=u['Tier'], inline=False)
    embed.add_field(name="HP", value=u['HP'], inline=True)
    embed.add_field(name="Origin Essence", value=u['Origin Essence'], inline=True)
    embed.add_field(name="Inventory", value=", ".join(u["Inventory"]) if u["Inventory"] else "Empty", inline=False)
    embed.add_field(name="Story Progress", value=f"Chapter {u['Story']['chapter']}, Scene {u['Story']['scene']}", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def choose(ctx, number: int):
    u = get_user(ctx.author.id)
    # Example logic: just advances scene. Replace with your own adventure logic.
    u["Story"]["scene"] += 1
    save_users(users)
    await ctx.send(f"{ctx.author.mention} advances to Scene {u['Story']['scene']} (Choice {number} selected)!")

# For the dashboard: simple Flask API
from flask import Flask, render_template, jsonify
import threading
import datetime

app = Flask(__name__)

def get_time_until_next_event():
    now = datetime.datetime.utcnow()
    next_hour = (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    return (next_hour - now).seconds

@app.route("/")
def home():
    all_users = load_users()
    return render_template("dashboard.html", users=all_users, time_left=get_time_until_next_event())

@app.route("/user/<user_id>")
def user_sheet(user_id):
    all_users = load_users()
    u = all_users.get(user_id)
    if not u:
        return "User not found", 404
    return render_template("char_sheet.html", user=u)

@app.route("/api/timer")
def timer():
    return jsonify({"seconds": get_time_until_next_event()})

def run_dashboard():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    # Start Flask dashboard in background
    threading.Thread(target=run_dashboard, daemon=True).start()
    bot.run(os.environ["DISCORD_TOKEN"])
