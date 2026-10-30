"""Build the beginner-friendly ClashCheck graphical interface."""  # Explain the purpose of this file.

# Import Python's built-in graphical interface library.
import tkinter as tk  # Use the short name tk for standard interface tools.

# Import ready-made message boxes and themed widgets from tkinter.
from tkinter import messagebox, ttk  # Import pop-up boxes and modern-looking widgets.

# Import the functions that check times and timetable clashes.
from clash_logic import find_clashes, time_to_minutes  # Reuse the separate checking functions.

# Import the fixed menu choices and sample timetable.
from settings import DAYS, EXAMPLE_EVENTS, LOCATIONS  # Reuse the separate project settings.


events = []  # Store all timetable events in one simple list.
day_var = None  # Prepare a variable for the selected day.
name_var = None  # Prepare a variable for the event name.
start_var = None  # Prepare a variable for the start time.
end_var = None  # Prepare a variable for the end time.
location_var = None  # Prepare a variable for the selected location.
buffer_var = None  # Prepare a variable for the travel buffer.
table = None  # Prepare a variable for the timetable table.
result_box = None  # Prepare a variable for the result text area.


def show_result(message, colour="black"):  # Create a helper function that changes the result message.
    result_box.config(state="normal")  # Allow the program to edit the result box.
    result_box.delete("1.0", tk.END)  # Remove the previous result message.
    result_box.insert(tk.END, message)  # Insert the new result message.
    result_box.tag_add("message", "1.0", tk.END)  # Select all text in the result box.
    result_box.tag_config("message", foreground=colour)  # Apply the requested text colour.
    result_box.config(state="disabled")  # Stop the user from typing in the result box.


def refresh_table(clashing_rows=None):  # Create a function that redraws every row in the table.
    if clashing_rows is None:  # Check whether a set of problem rows was supplied.
        clashing_rows = set()  # Use an empty set when there are no known problems.

    for row_id in table.get_children():  # Visit every row currently shown in the table.
        table.delete(row_id)  # Delete the old row before rebuilding the table.

    for index, event in enumerate(events):  # Read each saved event and its list position.
        if index in clashing_rows:  # Check whether this event has a timetable problem.
            status = "Clash"  # Show Clash in the status column.
            row_tag = "clash"  # Use the red row style.
        else:  # Handle an event without a timetable problem.
            status = "OK"  # Show OK in the status column.
            row_tag = "normal"  # Use the normal row style.

        values = (  # Start creating the values displayed in one table row.
            event["day"],  # Put the day in the first column.
            event["name"],  # Put the event name in the second column.
            event["start"],  # Put the start time in the third column.
            event["end"],  # Put the end time in the fourth column.
            event["location"],  # Put the location in the fifth column.
            status,  # Put the check result in the final column.
        )  # Finish the row value group.
        table.insert("", tk.END, values=values, tags=(row_tag,))  # Add the completed row to the table.


def add_event():  # Create the action used by the Add Event button.
    event_name = name_var.get().strip()  # Read the event name and remove extra spaces.
    start_text = start_var.get().strip()  # Read the start time and remove extra spaces.
    end_text = end_var.get().strip()  # Read the end time and remove extra spaces.

    if event_name == "":  # Check whether the user forgot the event name.
        messagebox.showwarning("Missing name", "Please enter an event name.")  # Show a simple warning.
        return  # Stop this function until the user enters a name.

    try:  # Try to convert both time entries into minutes.
        start_minutes = time_to_minutes(start_text)  # Convert the start time into minutes.
        end_minutes = time_to_minutes(end_text)  # Convert the end time into minutes.
    except ValueError as error:  # Catch a missing, invalid, or badly formatted time.
        messagebox.showerror("Invalid time", str(error))  # Show the helpful error from the logic file.
        return  # Stop this function until the time is corrected.

    if end_minutes <= start_minutes:  # Check that the event finishes after it starts.
        messagebox.showwarning("Invalid time", "End time must be later than start time.")  # Explain the problem.
        return  # Stop this function until the times are corrected.

    new_event = {  # Start a dictionary for the new event.
        "day": day_var.get(),  # Save the selected day.
        "name": event_name,  # Save the cleaned event name.
        "start": start_text,  # Save the start time.
        "end": end_text,  # Save the end time.
        "location": location_var.get(),  # Save the selected location.
    }  # Finish the new event dictionary.
    events.append(new_event)  # Add the new dictionary to the event list.
    refresh_table()  # Redraw the table so the new event appears.
    name_var.set("")  # Clear the name box for the next event.
    show_result("Event added. Click Check Timetable when you are ready.", "#1f5f99")  # Show a friendly instruction.


def check_timetable():  # Create the action used by the Check Timetable button.
    if len(events) == 0:  # Check whether the timetable is empty.
        messagebox.showinfo("No events", "Please add at least one event first.")  # Tell the user what to do.
        return  # Stop because there is nothing to check.

    try:  # Try to read the travel buffer as a whole number.
        travel_buffer = int(buffer_var.get())  # Convert the travel buffer text into an integer.
    except ValueError:  # Catch text that is not a whole number.
        messagebox.showerror("Invalid buffer", "Travel buffer must be a whole number.")  # Explain the input rule.
        return  # Stop until the buffer is corrected.

    if travel_buffer < 0:  # Check whether the travel buffer is negative.
        messagebox.showerror("Invalid buffer", "Travel buffer cannot be negative.")  # Explain the input rule.
        return  # Stop until the buffer is corrected.

    messages, clashing_rows = find_clashes(events, travel_buffer)  # Ask the logic file to check the timetable.
    refresh_table(clashing_rows)  # Redraw the table and colour the problem rows.

    if len(messages) == 0:  # Check whether no timetable problems were found.
        show_result("No clashes found. Your timetable looks practical.", "#137333")  # Show a green success message.
    else:  # Handle one or more timetable problems.
        heading = f"{len(messages)} problem(s) found:\n\n"  # Create a short heading for the results.
        details = "\n".join(messages)  # Put each problem message on a separate line.
        show_result(heading + details, "#b3261e")  # Show the complete result in red.


def delete_selected():  # Create the action used by the Delete Selected button.
    selected_rows = table.selection()  # Get the rows currently selected by the user.

    if len(selected_rows) == 0:  # Check whether the user selected nothing.
        messagebox.showinfo("Nothing selected", "Please select a row to delete.")  # Explain what is needed.
        return  # Stop because there is no selected event.

    selected_indexes = []  # Create a list for the selected event positions.

    for row_id in selected_rows:  # Visit every selected table row.
        selected_indexes.append(table.index(row_id))  # Save the matching list position.

    selected_indexes.sort(reverse=True)  # Sort backwards so deleting does not change later positions.

    for index in selected_indexes:  # Visit each selected position from last to first.
        del events[index]  # Remove the matching event from the list.

    refresh_table()  # Redraw the table without the deleted events.
    show_result("Selected event deleted. Check the timetable again.", "#1f5f99")  # Explain the next step.


def clear_all():  # Create the action used by the Clear All button.
    if len(events) == 0:  # Check whether there are already no events.
        show_result("The timetable is already empty.", "#1f5f99")  # Tell the user that nothing changed.
        return  # Stop because there is nothing to clear.

    answer = messagebox.askyesno("Clear timetable", "Delete all events?")  # Ask before removing every event.

    if answer:  # Continue only when the user selects Yes.
        events.clear()  # Remove every event from the list.
        refresh_table()  # Redraw the now-empty table.
        show_result("All events cleared.", "#1f5f99")  # Confirm that the timetable is empty.


def load_example():  # Create the action used by the Load Example button.
    events.clear()  # Remove old events so the example is easy to understand.

    for example_event in EXAMPLE_EVENTS:  # Visit each sample event from the settings file.
        events.append(example_event.copy())  # Add a separate copy to the working event list.

    refresh_table()  # Draw all sample events in the table.
    show_result("Example loaded. Click Check Timetable to find the problem.", "#1f5f99")  # Guide the user.


def create_input_form(parent):  # Create the left side of the window.
    global day_var, name_var, start_var, end_var, location_var, buffer_var  # Allow this function to set shared variables.

    form = ttk.LabelFrame(parent, text="Add an Event", padding=15)  # Create a labelled frame for the input boxes.
    form.grid(row=0, column=0, sticky="nsew", padx=(0, 10))  # Place the form on the left side.
    form.columnconfigure(1, weight=1)  # Allow the input column to become wider.

    day_var = tk.StringVar(value=DAYS[0])  # Start the day menu with Monday.
    name_var = tk.StringVar()  # Create storage for the event name entry.
    start_var = tk.StringVar(value="09:00")  # Start with an example start time.
    end_var = tk.StringVar(value="10:00")  # Start with an example end time.
    location_var = tk.StringVar(value=LOCATIONS[0])  # Start the location menu with City Campus.
    buffer_var = tk.StringVar(value="20")  # Use a simple 20-minute travel rule by default.

    ttk.Label(form, text="Day:").grid(row=0, column=0, sticky="w", pady=6)  # Add the Day label.
    ttk.Combobox(form, textvariable=day_var, values=DAYS, state="readonly").grid(row=0, column=1, sticky="ew", pady=6)  # Add the day menu.
    ttk.Label(form, text="Event name:").grid(row=1, column=0, sticky="w", pady=6)  # Add the Event name label.
    ttk.Entry(form, textvariable=name_var).grid(row=1, column=1, sticky="ew", pady=6)  # Add the event name box.
    ttk.Label(form, text="Start (HH:MM):").grid(row=2, column=0, sticky="w", pady=6)  # Add the Start label.
    ttk.Entry(form, textvariable=start_var).grid(row=2, column=1, sticky="ew", pady=6)  # Add the start time box.
    ttk.Label(form, text="End (HH:MM):").grid(row=3, column=0, sticky="w", pady=6)  # Add the End label.
    ttk.Entry(form, textvariable=end_var).grid(row=3, column=1, sticky="ew", pady=6)  # Add the end time box.
    ttk.Label(form, text="Location:").grid(row=4, column=0, sticky="w", pady=6)  # Add the Location label.
    ttk.Combobox(form, textvariable=location_var, values=LOCATIONS, state="readonly").grid(row=4, column=1, sticky="ew", pady=6)  # Add the location menu.
    ttk.Label(form, text="Travel buffer:").grid(row=5, column=0, sticky="w", pady=6)  # Add the Travel buffer label.
    ttk.Entry(form, textvariable=buffer_var).grid(row=5, column=1, sticky="ew", pady=6)  # Add the buffer box.
    ttk.Label(form, text="minutes").grid(row=6, column=1, sticky="w")  # Explain the travel buffer unit.

    ttk.Button(form, text="Add Event", command=add_event).grid(row=7, column=0, columnspan=2, sticky="ew", pady=(18, 6))  # Add the main input button.
    ttk.Button(form, text="Load Example", command=load_example).grid(row=8, column=0, columnspan=2, sticky="ew", pady=6)  # Add the sample data button.


def create_timetable(parent):  # Create the right side of the window.
    global table  # Allow this function to save the shared table widget.

    timetable_frame = ttk.LabelFrame(parent, text="My Timetable", padding=10)  # Create a labelled frame for the table.
    timetable_frame.grid(row=0, column=1, sticky="nsew")  # Place the timetable on the right side.
    timetable_frame.rowconfigure(0, weight=1)  # Allow the table to become taller.
    timetable_frame.columnconfigure(0, weight=1)  # Allow the table to become wider.

    columns = ("Day", "Event", "Start", "End", "Location", "Status")  # Define the six table columns.
    table = ttk.Treeview(timetable_frame, columns=columns, show="headings", height=13)  # Create the timetable table.

    for column in columns:  # Visit every table column name.
        table.heading(column, text=column)  # Display the column name at the top.

    table.column("Day", width=90, anchor="center")  # Set the width of the Day column.
    table.column("Event", width=140, anchor="w")  # Set the width of the Event column.
    table.column("Start", width=65, anchor="center")  # Set the width of the Start column.
    table.column("End", width=65, anchor="center")  # Set the width of the End column.
    table.column("Location", width=120, anchor="center")  # Set the width of the Location column.
    table.column("Status", width=60, anchor="center")  # Set the width of the Status column.
    table.tag_configure("clash", background="#ffd9d6", foreground="#8a1c14")  # Make problem rows light red.
    table.tag_configure("normal", background="white", foreground="black")  # Keep normal rows easy to read.
    table.grid(row=0, column=0, columnspan=3, sticky="nsew")  # Place the table inside its frame.

    scrollbar = ttk.Scrollbar(timetable_frame, orient="vertical", command=table.yview)  # Create a vertical scrollbar.
    scrollbar.grid(row=0, column=3, sticky="ns")  # Place the scrollbar beside the table.
    table.configure(yscrollcommand=scrollbar.set)  # Connect the table movement to the scrollbar.

    ttk.Button(timetable_frame, text="Delete Selected", command=delete_selected).grid(row=1, column=0, sticky="ew", padx=3, pady=(10, 0))  # Add the delete button.
    ttk.Button(timetable_frame, text="Clear All", command=clear_all).grid(row=1, column=1, sticky="ew", padx=3, pady=(10, 0))  # Add the clear button.
    ttk.Button(timetable_frame, text="Check Timetable", command=check_timetable).grid(row=1, column=2, sticky="ew", padx=3, pady=(10, 0))  # Add the check button.


def create_window():  # Create and return the complete application window.
    global result_box  # Allow this function to save the shared result text box.

    window = tk.Tk()  # Create the main application window.
    window.title("ClashCheck - Simple Timetable Checker")  # Put the project name in the title bar.
    window.geometry("1000x650")  # Set a useful starting window size.
    window.minsize(850, 560)  # Stop the window from becoming too small.

    header = tk.Frame(window, bg="#b3261e", height=90)  # Create a red project header.
    header.pack(fill="x")  # Stretch the header across the window.
    header.pack_propagate(False)  # Keep the chosen header height.
    tk.Label(header, text="ClashCheck", bg="#b3261e", fg="white", font=("Arial", 24, "bold")).pack(pady=(14, 0))  # Add the project title.
    tk.Label(header, text="A simple timetable and travel-time checker", bg="#b3261e", fg="white", font=("Arial", 11)).pack()  # Add a short description.

    main_area = ttk.Frame(window, padding=15)  # Create the main content area.
    main_area.pack(fill="both", expand=True)  # Let the main content use the available space.
    main_area.rowconfigure(0, weight=1)  # Allow the form and table to become taller.
    main_area.columnconfigure(0, weight=1)  # Give some width to the input form.
    main_area.columnconfigure(1, weight=3)  # Give more width to the timetable.

    create_input_form(main_area)  # Build the input form on the left.
    create_timetable(main_area)  # Build the timetable on the right.

    result_frame = ttk.LabelFrame(window, text="Check Result", padding=8)  # Create a frame for result messages.
    result_frame.pack(fill="x", padx=15, pady=(0, 15))  # Place the result area at the bottom.
    result_box = tk.Text(result_frame, height=5, wrap="word", font=("Arial", 11))  # Create a multi-line result box.
    result_box.pack(fill="x")  # Stretch the result box across its frame.
    show_result("Add your events, then click Check Timetable.", "#1f5f99")  # Show the first instruction.

    return window  # Give the finished window back to main.py.
