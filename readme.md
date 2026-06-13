# ROK-Bot

ROK-Bot is a desktop automation app for **Rise of Kingdoms** built around emulator control, computer vision, OCR, and task scheduling.

I built it as a real product, not just a quick automation script. The repository includes the desktop client, profile and task configuration, multi-instance worker orchestration, backend-connected login flows, Discord-related tooling, computer-vision-based gameplay automation, and Windows packaging scripts.

## Disclaimer

This project was discontinued around 2 years ago after I lost interest in the game. I'm open sourcing it as a record of what I built, but it should be considered an old codebase rather than an actively maintained project.

## What This Project Is

This project automates repetitive Rise of Kingdoms routines across emulator instances while still giving the user a visual control panel to manage profiles, workers, schedules, and task behavior.

The goal was not just to auto-click a few actions, but to build a reusable automation platform with:

- A desktop UI
- Configurable task profiles
- Multiple emulator instances
- Drag-and-drop worker assignment
- Image-based state detection
- OCR-assisted screen reading
- Emulator-specific control layers
- Backend/product integrations for auth, subscriptions, updates, and notifications

## What Is Implemented

The repository already contains a broad set of automation features, including:

- Gem gathering
- Resource gathering
- City resource collection
- Resource and gathering buff usage
- Mysterious merchant purchasing
- Alliance donation
- Alliance help
- Alliance pit handling
- Alliance building help
- Barbarian fort actions
- Barbarian hunting
- Marauder hunting
- Fog exploration
- Daily VIP rewards
- Daily chest claiming
- Daily quest claiming
- Expedition reward claiming
- Mail claiming
- Material production
- Troop training
- Troop healing
- Academy research
- City upgrading
- Resource transfer between accounts

The runner also supports:

- Multiple profiles per emulator
- Task priorities
- Time-slot based execution
- Character switching
- Looping workers with cooldowns
- Reconnect and popup recovery
- Captcha solving hooks
- Discord alerts
- Remote Discord worker control

## Stack

This project combines:

- **Python** for the application and automation logic
- **Flet** for the desktop UI
- **OpenCV** for template matching and screen recognition
- **Tesseract OCR** for reading text from the game screen
- **ADB** for emulator interaction
- **BlueStacks** and **LDPlayer** support
- **Supabase** for authentication, subscriptions, announcements, updates, and backend data
- **Discord.py** for notifications and worker control utilities
- **Flask** for product-side webhook/API experiments
- **Nuitka** for Windows packaging

## How It Works

At runtime, the app:

1. logs the user in,
2. lets the user choose an emulator type,
3. loads emulator instances and profile settings,
4. builds a task list from the enabled profile configuration,
5. runs those tasks through ADB, image recognition, and OCR,
6. loops across characters, profiles, and workers when configured.

The automation layer relies heavily on:

- screenshots from the emulator,
- image templates stored in `assets/app`,
- OCR through the bundled `tesseract` folder,
- emulator-specific bridge code in `src/utils/bridge`.

On top of that automation engine, the desktop app also includes:

- login and subscription-aware UI flows,
- per-profile task settings pages,
- worker management with drag-and-drop instance assignment,
- backend-driven announcements and update delivery,
- optional Discord-based alerts and worker control.

## Repository Highlights

- [`app.py`](C:\Users\maxence\Documents\ROK-Bot\app.py): main desktop application entrypoint
- [`src/tasks`](C:\Users\maxence\Documents\ROK-Bot\src\tasks): task implementations and execution flow
- [`src/views`](C:\Users\maxence\Documents\ROK-Bot\src\views): Flet UI
- [`src/utils`](C:\Users\maxence\Documents\ROK-Bot\src\utils): bridges, settings, auth, helpers, OCR, captcha, and Discord utilities
- [`assets`](C:\Users\maxence\Documents\ROK-Bot\assets): UI and image-recognition assets
- [`schema.sql`](C:\Users\maxence\Documents\ROK-Bot\schema.sql): backend database schema dump
- [`webserver.py`](C:\Users\maxence\Documents\ROK-Bot\webserver.py): experimental webhook/API code that ended up in the main repository

## Running It

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start the desktop app:

```powershell
py app.py
```

## Notes

- The project is primarily built for **Windows**.
- The current implementation is tightly connected to a Supabase backend.
- The repository includes build helpers for producing a standalone executable.
- Some parts of the repository are clearly product-facing, while others are experiments, utilities, or legacy variants from development.
