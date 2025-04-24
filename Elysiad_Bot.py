import discord
from discord.ext import commands
import openai
import random
from collections import defaultdict, Counter
import re
import threading
import time
import datetime
import asyncio
from flask import Flask, render_template_string, request, redirect

# ====== CONFIGURATION ======
import os
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")


client_ai = openai.OpenAI(api_key=OPENAI_API_KEY)

ELY_PROMPT = """[ ... (your big prompt from previous messages, as before) ... ]"""

# ========== STATE STORAGE ==========
PARTY_STATES = {}
USER_STATS = defaultdict(lambda: {
    "Name": "",
    "Tier": "10-B",
    "Attack Potency": "10-B (Human Level)",
    "Speed": "Athletic Human",
    "Lifting Strength": "Average Human",
    "Striking Strength": "10-B (Human)",
    "Durability": "10-B (Human)",
    "Stamina": "Above Average",
    "Range": "Standard melee",
    "Intelligence": "Average",
    "Weaknesses": "No powers, no experience",
    "Origin Essence": 0,
    "HP": 10,
    "Luck": 1,
    "Stealth": 1,
    "Inventory": []
})

GLOBAL_STATE = {
    "world_boss_alive": True,
    "plague_active": False,
    "dragon_released": False,
}

def build_global_state_block():
    s = "[GLOBAL STATE]\n"
    for k, v in GLOBAL_STATE.items():
        s += f"{k}: {v}\n"
    return s

def build_party_block(party, channel):
    names = []
    for uid in party["members"]:
        if USER_STATS[uid]["Name"]:
            names.append(USER_STATS[uid]["Name"])
        else:
            member = channel.guild.get_member(uid)
            USER_STATS[uid]["Name"] = member.display_name if member else str(uid)
            names.append(USER_STATS[uid]["Name"])
    return ', '.join(names)

def build_story_prompt(party_state, global_state, channel):
    base_prompt = ELY_PROMPT
    global_str = "\n" + build_global_state_block()
    base_prompt = base_prompt + global_str
    for entry in party_state["history"]:
        base_prompt += f"\nParty chose: {entry['choice']}\n{entry['story']}"
    return base_prompt

async def get_next_scene(party_state, global_state, channel, user_input=None):
    conversation = build_story_prompt(party_state, global_state, channel)
    if user_input:
        conversation += f"\nParty chose: {user_input}"
    response = client_ai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": conversation}],
        max_tokens=900,
        temperature=0.9
    )
    return response.choices[0].message.content

def get_party(channel_id):
    if channel_id not in PARTY_STATES:
        PARTY_STATES[channel_id] = {
            "members": set(),
            "history": [],
            "chapter": 1,
            "origin_essence": 0,
            "last_choices": "",
            "votes": {},
            "shop": [],
            "recap": ""
        }
    return PARTY_STATES[channel_id]

# === AI-GENERATED SHOP ===
async def build_shop_ai():
    shop_prompt = (
        "Generate 3 unique, powerful but balanced shop items, each from a different famous anime or web novel universe (for example: One Piece, Naruto, Lord of the Mysteries, Shadow Slave, Solo Leveling, Bleach, etc.). "
        "For each item, provide:\n"
        "- Name\n- The world it's from (in parentheses)\n- Short description (one sentence)\n- Stat affected (HP, Luck, Stealth, or Origin Essence)\n- Amount changed (integer)\n- Price in Origin Essence (between 10 and 50)\n"
        "Format each item on a new line as:\n"
        "Name (World) — Description [Stat: effect] (Price: XX)\n"
        "No commentary, just the 3 items in this format."
    )
    response = client_ai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": shop_prompt}],
        max_tokens=300,
        temperature=1
    )
    shop_text = response.choices[0].message.content

    # Parse items using regex
    pattern = r"^(.*?) \((.*?)\) — (.*?) \[Stat: (\w+) ?[:=] ?([-\d]+)\] \(Price: (\d+)\)"
    items = []
    for line in shop_text.strip().split('\n'):
        m = re.match(pattern, line.strip())
        if m:
            items.append({
                "name": m.group(1).strip(),
                "world": m.group(2).strip(),
                "desc": m.group(3).strip(),
                "stat": m.group(4).strip(),
                "amount": int(m.group(5)),
                "price": int(m.group(6)),
            })
    if not items:
        items = [
            {"name": "Backup Potion", "world": "Generic", "desc": "Restores HP.", "stat": "HP", "amount": 10, "price": 10}
        ]
    return items

# ====== DISCORD BOT SETUP ======
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def joinparty(ctx):
    party = get_party(ctx.channel.id)
    party["members"].add(ctx.author.id)
    USER_STATS[ctx.author.id]["Name"] = ctx.author.display_name
    await ctx.send(f"{ctx.author.mention} has joined the party! ({len(party['members'])} total)")

@bot.command()
async def leaveparty(ctx):
    party = get_party(ctx.channel.id)
    party["members"].discard(ctx.author.id)
    await ctx.send(f"{ctx.author.mention} has left the party. ({len(party['members'])} left)")

@bot.command()
async def startparty(ctx):
    party = get_party(ctx.channel.id)
    if not party["members"]:
        await ctx.send("No party members! Others must !joinparty first.")
        return
    party['history'] = []
    party['chapter'] = 1
    party['origin_essence'] = 0
    party['votes'] = {}
    party['shop'] = []
    party['recap'] = ""
    story = await get_next_scene(party, GLOBAL_STATE, ctx.channel)
    party['last_choices'] = story
    await ctx.send(f"**Party Adventure Begins!**\n{story}")

@bot.command()
async def vote(ctx, *, choice: str):
    party = get_party(ctx.channel.id)
    if ctx.author.id not in party["members"]:
        await ctx.send("You are not in this party!")
        return
    party['votes'][ctx.author.id] = choice
    if len(party['votes']) == len(party['members']):
        counts = Counter(party['votes'].values())
        chosen = counts.most_common(1)[0][0]
        party["history"].append({"choice": chosen, "story": party["last_choices"]})
        party["chapter"] += 1
        earned = random.randint(5, 20)
        party["origin_essence"] += earned
        party["recap"] = f"Party chose: {chosen}\nEarned {earned} Origin Essence!\n"
        party["shop"] = await build_shop_ai()
        story = await get_next_scene(party, GLOBAL_STATE, ctx.channel, user_input=chosen)
        party["last_choices"] = story
        party["votes"] = {}
        await ctx.send(f"**Chapter {party['chapter']} Recap:**\n{party['recap']}\n{story}\n\nType `!shop` to see new items or `!stats` for party stats.")
    else:
        await ctx.send(f"{ctx.author.mention} voted. ({len(party['votes'])}/{len(party['members'])})")

@bot.command()
async def shop(ctx):
    party = get_party(ctx.channel.id)
    if not party["shop"]:
        await ctx.send("No shop available yet. Finish a chapter first.")
        return
    lines = [f"**Origin Essence:** {party['origin_essence']}\n**Shop Items:**"]
    for i, item in enumerate(party["shop"]):
        lines.append(
            f"{i+1}. {item['name']} ({item['world']}) — {item['desc']} "
            f"[Stat: {item['stat']} {item['amount']}] (Price: {item['price']})"
        )
    await ctx.send("\n".join(lines))

@bot.command()
async def buy(ctx, item_num: int):
    party = get_party(ctx.channel.id)
    user = USER_STATS[ctx.author.id]
    if item_num < 1 or item_num > len(party["shop"]):
        await ctx.send("Invalid item number.")
        return
    item = party["shop"][item_num - 1]
    if party["origin_essence"] < item['price']:
        await ctx.send("Not enough Origin Essence!")
        return
    party["origin_essence"] -= item['price']
    if item['stat'] in user:
        user[item['stat']] += item['amount']
        await ctx.send(
            f"{ctx.author.mention} bought {item['name']} from {item['world']}! "
            f"{item['stat']} increased by {item['amount']}."
        )
    else:
        user["Inventory"].append(item['name'])
        await ctx.send(
            f"{ctx.author.mention} bought {item['name']} from {item['world']} and added it to their inventory!"
        )
    party["shop"].pop(item_num - 1)

@bot.command()
async def upgradestat(ctx, stat: str):
    user = USER_STATS[ctx.author.id]
    oe = user["Origin Essence"]
    cost = 10
    if oe < cost:
        await ctx.send(f"Not enough Origin Essence! You have {oe}.")
        return
    if stat not in user:
        await ctx.send(f"Stat '{stat}' not found! Try HP, Luck, or Stealth.")
        return
    user["Origin Essence"] -= cost
    user[stat] += 1
    await ctx.send(f"{ctx.author.mention} upgraded {stat} to {user[stat]}!")

@bot.command()
async def stats(ctx):
    user = USER_STATS[ctx.author.id]
    msg = (
        f"**[Character Stats — Vs Battles Wiki Style]**\n"
        f"- Name: {user['Name']}\n"
        f"- Tier: {user['Tier']}\n"
        f"- Attack Potency: {user['Attack Potency']}\n"
        f"- Speed: {user['Speed']}\n"
        f"- Lifting Strength: {user['Lifting Strength']}\n"
        f"- Striking Strength: {user['Striking Strength']}\n"
        f"- Durability: {user['Durability']}\n"
        f"- Stamina: {user['Stamina']}\n"
        f"- Range: {user['Range']}\n"
        f"- Intelligence: {user['Intelligence']}\n"
        f"- Weaknesses: {user['Weaknesses']}\n"
        f"- Origin Essence: {user['Origin Essence']}\n"
        f"- Inventory: {', '.join(user['Inventory']) if user['Inventory'] else 'None'}\n"
        f"- HP: {user['HP']} | Luck: {user['Luck']} | Stealth: {user['Stealth']}"
    )
    await ctx.send(msg)

@bot.command()
async def partystats(ctx):
    party = get_party(ctx.channel.id)
    names = build_party_block(party, ctx.channel)
    msg = f"**[Party Stats]**\n- Chapter: {party['chapter']}\n- Origin Essence: {party['origin_essence']}\n- Members: {names}\n"
    for uid in party["members"]:
        u = USER_STATS[uid]
        msg += (
            f"\n**{u['Name']}**\n"
            f"Tier: {u['Tier']} | Potency: {u['Attack Potency']} | Speed: {u['Speed']}\n"
            f"HP: {u['HP']} | Luck: {u['Luck']} | Stealth: {u['Stealth']}\n"
            f"Inventory: {', '.join(u['Inventory']) if u['Inventory'] else 'None'}\n"
        )
    await ctx.send(msg)

# ========= GLOBAL EVENT COMMANDS =========

@bot.command()
async def setglobal(ctx, key: str, value: str):
    val = value
    if value.lower() == "true":
        val = True
    elif value.lower() == "false":
        val = False
    GLOBAL_STATE[key] = val
    await ctx.send(f"[GLOBAL STATE UPDATED] {key} set to {val}.\n(Will be reflected in all stories!)")

@bot.command()
async def globalstate(ctx):
    await ctx.send(build_global_state_block())

@bot.command()
async def broadcastglobal(ctx, *, message: str):
    sent = 0
    for channel_id in PARTY_STATES:
        channel = bot.get_channel(channel_id)
        if channel:
            try:
                await channel.send(f"**[GLOBAL EVENT]** {message}")
                sent += 1
            except Exception:
                pass
    await ctx.send(f"Broadcast sent to {sent} party channels.")

# ========= DAILY AI-GENERATED GLOBAL EVENT =========

async def generate_unique_global_event():
    ai_event_prompt = (
        "Invent a brand new global event that could occur in a multiverse where famous anime and webnovel worlds overlap (such as One Piece, Bleach, Attack on Titan, Lord of the Mysteries, Solo Leveling, etc). "
        "Describe the event in 1-2 sentences, give it a unique short name (no more than 3 words), and specify which fictional world or combination of worlds inspired it. "
        "Example format:\n"
        "Event Name: [Short name]\n"
        "World(s): [e.g., Bleach/Attack on Titan]\n"
        "Description: [What happens in the world?]\n"
        "No commentary, just the event in this format."
    )
    response = client_ai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": ai_event_prompt}],
        max_tokens=250,
        temperature=1.2,
    )
    content = response.choices[0].message.content.strip()

    # Parse out event data
    event_name, event_world, event_desc = "Unknown_Event", "Unknown", "No description."
    for line in content.split('\n'):
        if line.startswith("Event Name:"):
            event_name = line.replace("Event Name:", "").strip().replace(" ", "_").lower()
        elif line.startswith("World(s):"):
            event_world = line.replace("World(s):", "").strip()
        elif line.startswith("Description:"):
            event_desc = line.replace("Description:", "").strip()

    # Store event in GLOBAL_STATE and broadcast
    GLOBAL_STATE[event_name] = True
    for channel_id in PARTY_STATES:
        channel = bot.get_channel(channel_id)
        if channel:
            try:
                asyncio.create_task(channel.send(
                    f"**[DAILY GLOBAL EVENT]**\n"
                    f"**{event_name.replace('_', ' ').title()}**\n"
                    f"World(s): {event_world}\n"
                    f"{event_desc}"
                ))
            except Exception:
                pass
    print(f"New daily global event: {event_name} ({event_world}) - {event_desc}")

def daily_event_scheduler():
    last_run = None
    while True:
        now = datetime.datetime.utcnow().date()
        if last_run != now:
            # Run once per UTC day
            asyncio.run(generate_unique_global_event())
            last_run = now
        time.sleep(3600)  # Check once an hour

threading.Thread(target=daily_event_scheduler, daemon=True).start()

# ====== FLASK DASHBOARD ======
app = Flask(__name__)

dashboard_template = '''
<!doctype html>
<title>Elysiad Bot Dashboard</title>
<h1>Elysiad World Dashboard</h1>

<h2>Global State</h2>
<ul>
{% for k,v in global_state.items() %}
  <li><b>{{k}}</b>: {{v}}</li>
{% endfor %}
</ul>
<h2>Parties</h2>
{% for cid, party in parties.items() %}
  <h3>Party in Channel {{cid}}</h3>
  <ul>
    <li>Chapter: {{party['chapter']}}</li>
    <li>Origin Essence: {{party['origin_essence']}}</li>
    <li>Members:
      {% for uid in party['members'] %}
        {{ user_stats[uid]['Name'] }}{% if not loop.last %}, {% endif %}
      {% endfor %}
    </li>
  </ul>
  <details>
    <summary>Show Member Stats</summary>
    {% for uid in party['members'] %}
      <p><b>{{user_stats[uid]['Name']}}</b>: Tier {{user_stats[uid]['Tier']}}, HP: {{user_stats[uid]['HP']}}, OE: {{user_stats[uid]['Origin Essence']}},
      Inventory:
      {% if user_stats[uid]['Inventory'] %}
        {{ user_stats[uid]['Inventory']|join(', ') }}
      {% else %}
        None
      {% endif %}
      </p>
    {% endfor %}
  </details>
{% endfor %}

'''

@app.route("/")
def dashboard():
    return render_template_string(
        dashboard_template,
        global_state=GLOBAL_STATE,
        parties=PARTY_STATES,
        user_stats=USER_STATS
    )

@app.route("/setglobal", methods=["POST"])
def setglobal():
    key = request.form["key"]
    value = request.form["value"]
    if value.lower() == "true":
        val = True
    elif value.lower() == "false":
        val = False
    else:
        val = value
    GLOBAL_STATE[key] = val
    return redirect("/")

def run_dashboard():
    app.run(port=5000)

# Start the dashboard in a new thread
threading.Thread(target=run_dashboard, daemon=True).start()

# ====== RUN THE BOT ======
bot.run(DISCORD_TOKEN)
