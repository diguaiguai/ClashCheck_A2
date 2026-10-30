"""Store the fixed choices and example timetable used by ClashCheck."""  # Explain this file.


# Create the list of weekdays displayed in the day menu.
DAYS = [  # Start the weekday list.
    "Monday",  # Add Monday to the menu.
    "Tuesday",  # Add Tuesday to the menu.
    "Wednesday",  # Add Wednesday to the menu.
    "Thursday",  # Add Thursday to the menu.
    "Friday",  # Add Friday to the menu.
]  # Finish the weekday list.


# Create the list of locations displayed in the location menu.
LOCATIONS = [  # Start the location list.
    "City Campus",  # Add City Campus as a physical location.
    "Haymarket",  # Add Haymarket as a physical location.
    "Moore Park",  # Add Moore Park as a physical location.
    "Home",  # Add Home as a physical location.
    "Online",  # Add Online, which does not require travel time.
]  # Finish the location list.


# Create sample events for the Load Example button.
EXAMPLE_EVENTS = [  # Start the sample event list.
    {  # Start the first sample event.
        "day": "Monday",  # Put the event on Monday.
        "name": "Lecture",  # Name the event Lecture.
        "start": "09:00",  # Start the lecture at 9:00 am.
        "end": "10:00",  # End the lecture at 10:00 am.
        "location": "City Campus",  # Hold the lecture at City Campus.
    },  # Finish the first sample event.
    {  # Start the second sample event.
        "day": "Monday",  # Put the event on Monday.
        "name": "Work shift",  # Name the event Work shift.
        "start": "10:10",  # Start work ten minutes after the lecture.
        "end": "12:00",  # End work at midday.
        "location": "Haymarket",  # Hold the work shift at Haymarket.
    },  # Finish the second sample event.
    {  # Start the third sample event.
        "day": "Tuesday",  # Put the event on Tuesday.
        "name": "Tutorial",  # Name the event Tutorial.
        "start": "13:00",  # Start the tutorial at 1:00 pm.
        "end": "14:00",  # End the tutorial at 2:00 pm.
        "location": "Moore Park",  # Hold the tutorial at Moore Park.
    },  # Finish the third sample event.
    {  # Start the fourth sample event.
        "day": "Tuesday",  # Put the event on Tuesday.
        "name": "Study session",  # Name the event Study session.
        "start": "14:30",  # Start studying at 2:30 pm.
        "end": "15:30",  # End studying at 3:30 pm.
        "location": "City Campus",  # Hold the study session at City Campus.
    },  # Finish the fourth sample event.
]  # Finish the example event list.
