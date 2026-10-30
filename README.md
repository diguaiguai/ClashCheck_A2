# ClashCheck

## Simple Project Description

ClashCheck is a beginner Python desktop application for students. It helps a user enter classes, work shifts, and study sessions, then checks whether the events overlap or leave too little travel time between different locations.

The project is intentionally simple. The user enters the timetable manually, chooses a travel buffer such as 20 minutes, and presses **Check Timetable**. Problem events are highlighted in red and a short explanation is shown below the table.

## Simplified Scope

- Manual timetable entry only.
- Checks events on the same day.
- Finds overlapping event times.
- Checks a fixed travel-time buffer between different physical locations.
- Treats online events as not requiring travel.
- Uses local sample data and does not need the internet.

The project does not use live traffic data, maps, user accounts, databases, or automatic timetable imports. These features were removed so the prototype is realistic for a beginner.

## Files

- `main.py` starts the application.
- `interface.py` creates the tkinter interface and buttons.
- `clash_logic.py` contains the time and clash-checking functions.
- `settings.py` stores menu choices and example events.
- `test_logic.py` checks the main logic with four simple tests.

## How to Run

Open Terminal in this folder and run:

```bash
python3 main.py
```

To run the tests:

```bash
python3 test_logic.py
```

No extra Python libraries are required because the project only uses built-in Python modules.
