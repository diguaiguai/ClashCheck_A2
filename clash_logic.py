"""Check timetable times and find simple clashes."""  # Explain the purpose of this file.


def time_to_minutes(time_text):  # Create a function that changes HH:MM text into minutes.
    parts = time_text.split(":")  # Split the time into an hour part and a minute part.

    if len(parts) != 2:  # Check that the user entered exactly one colon.
        raise ValueError("Please enter time as HH:MM.")  # Stop and show a helpful error message.

    hour = int(parts[0])  # Change the hour text into a whole number.
    minute = int(parts[1])  # Change the minute text into a whole number.

    if hour < 0 or hour > 23:  # Check that the hour is between 0 and 23.
        raise ValueError("The hour must be between 00 and 23.")  # Stop when the hour is invalid.

    if minute < 0 or minute > 59:  # Check that the minute is between 0 and 59.
        raise ValueError("The minute must be between 00 and 59.")  # Stop when the minute is invalid.

    return hour * 60 + minute  # Return the total number of minutes after midnight.


def find_clashes(events, travel_buffer):  # Create a function that checks all pairs of events.
    messages = []  # Store a readable message for every problem found.
    clashing_rows = set()  # Store each problem row only once.

    for first_index in range(len(events)):  # Select the first event in a pair.
        first_event = events[first_index]  # Get the first event dictionary from the list.

        for second_index in range(first_index + 1, len(events)):  # Select every later event once.
            second_event = events[second_index]  # Get the second event dictionary from the list.

            if first_event["day"] != second_event["day"]:  # Check whether the events are on different days.
                continue  # Skip this pair because different days cannot clash.

            first_start = time_to_minutes(first_event["start"])  # Convert the first start time into minutes.
            first_end = time_to_minutes(first_event["end"])  # Convert the first end time into minutes.
            second_start = time_to_minutes(second_event["start"])  # Convert the second start time into minutes.
            second_end = time_to_minutes(second_event["end"])  # Convert the second end time into minutes.

            times_overlap = first_start < second_end and second_start < first_end  # Check whether the times overlap.

            if times_overlap:  # Handle two events that happen at the same time.
                message = (  # Start building the overlap message.
                    f'{first_event["day"]}: {first_event["name"]} overlaps '  # Add the day and first event name.
                    f'{second_event["name"]}.'  # Add the second event name.
                )  # Finish the overlap message.
                messages.append(message)  # Add the message to the results.
                clashing_rows.add(first_index)  # Mark the first row as a problem.
                clashing_rows.add(second_index)  # Mark the second row as a problem.
                continue  # Move to the next event pair because this clash is already recorded.

            if first_start < second_start:  # Check whether the first event happens earlier.
                earlier_event = first_event  # Save the first event as the earlier event.
                later_event = second_event  # Save the second event as the later event.
                earlier_end = first_end  # Save the end time of the earlier event.
                later_start = second_start  # Save the start time of the later event.
            else:  # Handle the case where the second event happens earlier.
                earlier_event = second_event  # Save the second event as the earlier event.
                later_event = first_event  # Save the first event as the later event.
                earlier_end = second_end  # Save the end time of the earlier event.
                later_start = first_start  # Save the start time of the later event.

            gap = later_start - earlier_end  # Calculate the free minutes between the two events.
            different_locations = earlier_event["location"] != later_event["location"]  # Compare the locations.
            earlier_is_online = earlier_event["location"] == "Online"  # Check whether the earlier event is online.
            later_is_online = later_event["location"] == "Online"  # Check whether the later event is online.
            travel_is_needed = different_locations and not earlier_is_online and not later_is_online  # Decide if travel is needed.

            if travel_is_needed and gap < travel_buffer:  # Check whether there is too little travel time.
                message = (  # Start building the travel warning message.
                    f'{first_event["day"]}: only {gap} minutes between '  # Add the day and available time.
                    f'{earlier_event["name"]} and {later_event["name"]}. '  # Add both event names.
                    f'{travel_buffer} minutes are required.'  # Add the required travel time.
                )  # Finish the travel warning message.
                messages.append(message)  # Add the warning to the results.
                clashing_rows.add(first_index)  # Mark the first row as a problem.
                clashing_rows.add(second_index)  # Mark the second row as a problem.

    return messages, clashing_rows  # Return both the messages and the problem row numbers.
