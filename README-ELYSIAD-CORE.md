# Elysiad: Core Design Philosophy

Elysiad is a magical, narrative-heavy, transmigration-based RPG web experience (and future app) where the player enters any fictional story world in existence — from anime and books to movies, games, and comics.

## 🧬 Core Premise
You, the player, are a persistent soul known as an **Origin Essence**. You have one true self — a custom character you design — and this identity follows you across every fictional world you enter.

At every world entry, you choose:

### 1. Canon Transmigration
- You enter as a **canonical character** (e.g., Luffy in One Piece, Klein in Lord of the Mysteries).
- You begin at the start of that character's original story.
- You follow their backstory and path — or choose to diverge and change everything.

### 2. Original Soul Entry (Your True Character)
- You play as the **original character you created**.
- This one consistent persona transmigrates into each world with a fabricated backstory and memories.
- The world believes you belong — but you know otherwise.
- You retain your appearance, personality, voice, and internal narrative across all stories.

## 🌍 World Generation
Each world is:
- A full reconstruction of the **original canonical narrative** (e.g., start of One Piece, first episode of Death Note).
- Populated with all the original characters, events, and timeline.
- A branching narrative based on your choices.

## 🧠 Transmigration System
Each world offers:
- A canonical character to embody, complete with backstory and expected fate.
- A unique in-world identity for your original character, built using your profile and adapted into that world’s lore.

> Example: In Star Wars, your Essence might appear as a padawan from an outer system — or you could take over Anakin Skywalker from the start.

## 📚 The Library of Beginnings
- The only constant across all worlds.
- Home to the **Archivist**, a mysterious figure who writes stories that become reality.
- The Archivist has written so many stories, he’s lost his own.
- **Your true mission** is to discover his hidden past by traveling to different worlds and collecting lost lore.

## 📜 Narrative Summary Format
Each world entry includes:
- A 3–4 sentence immersive summary.
- Who you will play as.
- What the story originally was — and how your presence shifts it.

## 🧩 Persistent Player Identity
Each player has a dedicated JSON profile at `data/players/{username}.json`:
```json
{
  "name": "Your name",
  "appearance": "...",
  "personality": ["loyal", "cynical"],
  "speech_style": "dry and clipped",
  "origin_essence": 12,
  "worlds_visited": ["One Piece", "Evangelion", "Lord of the Mysteries"],
  "suspicion_level": 0
}
```

This system powers:
- Personalized narrative injection.
- Character voice consistency.
- Accumulating meta-story connections between worlds.

## 😨 Suspicion System (Hidden Mechanic)
- Players build **suspicion** by acting out of character.
- Tracked silently in session and profile as `suspicion_level`.
- Certain thresholds (40, 70, 100) trigger narrative consequences:
  - World becomes wary, events shift tone
  - NPCs react coldly or confront
  - At 100: forced narrative punishment
- If suspicion reaches 100:
  - You are immediately redirected to a **Dark Souls-style death screen** (`death_screen.html`)
  - Journal is wiped
  - Suspicion resets
  - You re-enter the same world from the start
- `game_session.py` and `main_routes.py` handle this transition.
- `suspicion_events.py` detects and marks thresholds.

---

## ✅ System Updates
> A running log of newly added systems, used to keep Elysiad sessions in sync with development.

- `signup.html`: Now supports password confirmation and show/hide toggles with styling that matches the login screen.
- `structured_lore.py`: Fetch lore by world, phase, and tag for dynamic narrative drops.
- `timeline_log.py`: Merged timeline logging and shard saving into one system.
- `lore_manager.py`: Now unlocks lore tagged to "Library of Beginnings" only (no Library of Echoes).
- `journal_dynamic.html`: Lore filter dropdown updated to only show "Library of Beginnings".
- `world_templates.py`: Generates procedurally themed worlds by tier and tone.
- `ai_behavior.py`: Refactored to define NPCBehavior — modular loyalty/mood system.
- `companion_manager.py`: Companion now inherits from NPCBehavior for unified NPC simulation.
- `routes/user_routes.py`: `/profile` shows and now edits the user's soulbound profile.
- `routes/emporium_routes.py`: Connects to item generation and shows `/emporium` UI.
- `routes/chapter_routes.py`: Loads user-specific chapter logs to `/chapters` timeline.
- `auth_routes.py`: Integrated with `user_auth.py` for real login/signup and error feedback.
- `user_auth.py`: Adds profile creation on signup and per-user storage in `data/players/`.
- `profile.html`: Editable player appearance, personality, speech style with live save.
- `base.html`: Displays styled flash messages for error/success UX.
- `entry_mode_select.html` → `/begin-world`: Entry mode setup for canon or original character.
- `routes/world_routes.py` → `/begin-world`: Caches world and entry mode, starts session.
- `main_routes.py` → `/enter_world`: Loads narrative welcome scene.
- `main_routes.py` → `/death`: Detects phase = ResetRequired, wipes session journal, resets suspicion.
- `death_screen.html`: Styled as Dark Souls “YOU DIED” screen with delayed return link.

---

## 🧩 Full Feature & File Reference

### 🌍 World & Lore
- `world_templates.py`: Procedural world generator by tone and tier.
- `structured_lore.py`: Provides lore fragments by world, phase, and tag.
- `archivist_lore.py`: Canon metanarrative fragments written by the Archivist.
- `lore_tracker.py`: Class for unlocking, storing, and retrieving lore.
- `lore_manager.py`: Manages default lore flow, paging, and filtering.
- `timeline_log.py`: Logs major in-world events as timeline shards.

### 🎮 Gameplay Systems
- `game_session.py`: Master object tracking current world, journal, suspicion, companions.
- `mission_manager.py`: Handles mission phases and mission-related lore.
- `action_handler.py`: Applies action tags and outcomes, modifies suspicion.
- `combat_manager.py`: Simple combat resolution logic.
- `combat_story_manager.py`: Generates narrated outcomes of combat.
- `roll_engine.py`: Dice logic and resolution interpreter.

### 🧠 Character & Behavior
- `player.py`: Loads/stores persistent Origin Essence profile.
- `companion_manager.py`: Manages companions, generation, reactions.
- `ai_behavior.py`: NPCBehavior logic for moods, suspicion, loyalty.
- `suspicion_events.py`: Triggers story events on suspicion thresholds.
- `data/players/`: One JSON profile per user for persistent identity.

### 📖 Journal & Chapter Log
- `journal_dynamic.html`: Main journal UI with flipping pages and tabs.
- `journal_routes.py`: Backend routes for journal access and tab handling.
- `chapter_saver.py`: Formats and stores narrated events per chapter.
- `chapter_routes.py`: Renders chapters from disk into a scrollable timeline.

### 👤 User/Auth Routes
- `auth_routes.py`: Signup/login using bcrypt + flash messages.
- `user_routes.py`: Profile view and live editable identity fields.
- `user_auth.py`: Creates and validates user creds, manages profile saves.

### 🛒 Emporium
- `emporium_generator.py`: Item generator logic for the magical shop.
- `emporium_routes.py`: Renders `/emporium` using generated shop items.

### 🏛️ UI / Templates
- `templates/world_scene.html`: Main world interaction screen.
- `templates/entry_mode_select.html`: Choose canon vs origin entry.
- `templates/library.html`: Visual hub for world selection (Library of Beginnings).
- `templates/death_screen.html`: Death/reset screen for suspicion overflow.
- `templates/signup.html`: Styled form with password confirm + toggle visibility.
- `templates/profile.html`: Editable player profile with appearance, traits.
- `templates/chapters.html`: Timeline of story chapters saved per player.
- `static/styles.css`, `journal_page_flip.css`: Antique magical UI + page animations.

### 💾 Save / Load
- `save_routes.py`: Save and load session files.
- `data/lore_fragments/`: Folder for per-world lore fragments.
- `data/cached_worlds.json`: Likely stores procedurally generated world cache.

---

This README defines the permanent design blueprint for the Elysiad Helper GPT. It should be loaded and referenced whenever a session starts to maintain immersive consistency and narrative integrity.