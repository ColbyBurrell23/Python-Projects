
import tkinter as tk
from tkinter import ttk, messagebox

class GolfScorecardApp:
    def __init__(self, root):
        self.root = root  # Initialize the main window
        self.root.title("Welcome to Pebble Beach Resorts")  # Set window title
        self.show_welcome_screen()  # Show the welcome screen when the app starts

    def show_welcome_screen(self):
        self.welcome_screen = tk.Toplevel(self.root)  # Create a new window for welcome screen
        self.welcome_screen.title("Welcome Screen")  # Set title for the welcome screen
        welcome_message = tk.Label(self.welcome_screen, text="Welcome to Pebble Beach!", font=("Helvetica", 16))  # Create a welcome message
        welcome_message.pack(pady=20)  # Add message to the window with some padding
        next_button = tk.Button(self.welcome_screen, text="Enter", command=self.start_main_app)  # Button to enter the main app
        next_button.pack(pady=10)  # Add button with padding

    def start_main_app(self):
        self.welcome_screen.destroy()  # Close the welcome screen when the button is pressed
        self.create_scorecard()  # Call the function to create the main scorecard screen

    def create_scorecard(self):
        self.courses = {  # Define course data with par and yardage for each hole
            "Pebble Beach": {
                "Par": [4, 5, 4, 4, 3, 5, 3, 4, 4, 4, 4, 3, 4, 5, 4, 4, 3, 5],
                "Yardage": [381, 502, 390, 326, 195, 506, 109, 427, 481,
                            446, 390, 202, 403, 572, 397, 401, 208, 543]
            }
        }

        self.selected_course = tk.StringVar()  # String variable to store the selected course
        self.selected_course.set("Pebble Beach")  # Set default course to Pebble Beach

        ttk.Label(self.root, text="Select Course:").grid(row=0, column=0, columnspan=4, pady=5)  # Label for course selection
        self.course_menu = ttk.Combobox(self.root, textvariable=self.selected_course, values=list(self.courses.keys()), state="readonly")  # Dropdown for course selection
        self.course_menu.grid(row=1, column=0, columnspan=4, pady=5)  # Place the dropdown on the window
        self.course_menu.bind("<<ComboboxSelected>>", self.load_course)  # Bind course selection change to loading course

        headers = ["Hole", "Par", "Yardage", "Score"]  # Headers for the scorecard table
        for col, text in enumerate(headers):  # Loop through each header
            ttk.Label(self.root, text=text, width=10, anchor="center").grid(row=2, column=col, padx=5, pady=5)  # Create and place header labels

        self.score_entries = []  # List to hold score entry fields
        self.frame = tk.Frame(self.root)  # Create a frame to contain score entry fields
        self.frame.grid(row=3, column=0, columnspan=4)  # Place the frame below the headers

        self.load_course()  # Load the default course when app starts
        ttk.Button(self.root, text="Submit Scores", command=self.calculate_results).grid(row=22, column=0, columnspan=4, pady=10)  # Button to submit scores

    def load_course(self, event=None):
        for widget in self.frame.winfo_children():  # Remove any existing widgets in the frame
            widget.destroy()

        self.score_entries.clear()  # Clear the list of score entries
        selected_course = self.selected_course.get()  # Get the currently selected course
        par_values = self.courses[selected_course]["Par"]  # Get the par values for the selected course
        yardage_values = self.courses[selected_course]["Yardage"]  # Get the yardage values for the selected course

        for i in range(18):  # Loop through each hole
            ttk.Label(self.frame, text=f"{i+1}", width=10, anchor="center").grid(row=i, column=0)  # Display hole number
            ttk.Label(self.frame, text=f"{par_values[i]}", width=10, anchor="center").grid(row=i, column=1)  # Display par for the hole
            ttk.Label(self.frame, text=f"{yardage_values[i]}", width=10, anchor="center").grid(row=i, column=2)  # Display yardage for the hole

            entry = ttk.Entry(self.frame, width=10)  # Create an entry field for the score
            entry.grid(row=i, column=3)  # Place the entry field
            self.score_entries.append(entry)  # Add entry field to the list

    def calculate_results(self):
        try:
            total_score = 0  # Initialize total score
            selected_course = self.selected_course.get()  # Get selected course
            total_par = sum(self.courses[selected_course]["Par"])  # Calculate total par for the course

            for entry in self.score_entries:  # Loop through all score entry fields
                score = int(entry.get().strip())  # Get score from entry field and convert to integer
                if score < 0:  # Check if score is negative
                    raise ValueError("Scores must be non-negative.")  # Raise error if score is negative
                total_score += score  # Add score to total score

            difference = total_score - total_par  # Calculate the difference between total score and total par
            result_msg = f"Total Score: {total_score}\nPar for {selected_course}: {total_par}\n"  # Prepare result message

            if difference < 0:  # If score is under par
                result_msg += f"You finished {abs(difference)} under par! Great job!"  # Add message for under par
            elif difference > 0:  # If score is over par
                result_msg += f"You finished {difference} over par. Keep practicing!"  # Add message for over par
            else:  # If score is at par
                result_msg += "You finished at even par. Well played!"  # Add message for even par

            messagebox.showinfo("Results", result_msg)  # Show result message in a message box
        except ValueError:  # Handle invalid input (non-numeric or negative scores)
            messagebox.showerror("Error", "Please enter valid numeric scores for all holes.")  # Show error message

root = tk.Tk()  # Create the main window
app = GolfScorecardApp(root)  # Initialize the app
root.mainloop()  # Run the application loop