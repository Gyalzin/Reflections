
# Reflections

A calm, relaxed daily activity tracker. Instead of measuring productivity, Reflections helps you look back on how you spent your days.

<!-- Add a screenshot: save it in the Docs folder and uncomment the next line -->

<!-- ![Reflections timeline](Docs/screenshot.png) -->

## Why I built it

As days turn into weeks and months, people can lost awareness of how they have spent their time and the experiences that have shaped their lives. I built this project to help people become more aware on how they use their time. 

![Reflections Timeline](https://file+.vscode-resource.vscode-cdn.net/Users/gyalzindorji/Desktop/Reflections/Docs/Timeline_screenshot.png)

<!-- 2–3 sentences in your own words: the problem, and why a gentle tracker -->

## Features

- A 24-hour vertical timeline with soft time-of-day labels (Midnight, Morning, Afternoon, Evening, Night)
- Add, edit and delete activity entries, with start and end times
- Overlapping entries sit side by side so none are hidden
- Pick an existing activity or create a new one
- Optional mood (five faces) and optional notes
- Browse previous and next days, or jump back to today
- A "now" line on today's timeline, and the view scrolls to a useful spot
- Friendly validation messages and a gentle save confirmation

## Built with

Python, Flask, SQLite, HTML, CSS and a little JavaScript.

## Running it locally

1. Clone the repository and open the folder in a terminal.
2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create the database (this also adds a default "General" category):
   ```
   python -c "import db; db.init_db()"
   ```
5. Start the app:
   ```
   python main.py
   ```
6. Open http://127.0.0.1:5000 in your browser.

## Project structure

```
main.py          Flask routes
db.py            Database functions
schema.sql       Table definitions
templates/       HTML pages
static/          CSS
Docs/            Project overview and requirements
```

## Known limitations

- Time inputs are typed in Safari, which doesn't support stepping through times the way Chrome does.
- There is no login. It's a single-user app, and data stays in a local SQLite file.

## Planned for future versions

- Drag and resize entries on the timeline, and click-to-create
- Daily and weekly summaries, and insights on frequent activities
- A category picker (categories are in the database, but every activity currently uses "General")
- Implent AI for more useful inshights and summaries.

## What I learned

University taught me about the different pieces of puzzles and doing this project taught me how to connect the pieces together. The one thing that worked well was that I spent a lot of time(over 3 days) on the planning phase. This includes system design, gathering user stories, drafting a system requirements and ER diagrams.  This taught me that having a good plan and preparing well makes it easier and smoother in the development process.  One thing that I could have done better was using less AI and writing the code by myself more often. 

<!-- A few honest lines: what was hard, what you'd do differently -->
