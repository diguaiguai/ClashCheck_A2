"""Start the ClashCheck beginner project."""  # Explain the purpose of this file.


# Import the function that builds the graphical interface.
from interface import create_window  # Bring the window-building function into this file.


# Build the complete ClashCheck window.
app = create_window()  # Create the ClashCheck application window.

# Keep the window open and wait for the user to click buttons.
app.mainloop()  # Keep checking for clicks until the user closes the window.
