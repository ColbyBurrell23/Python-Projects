from tkinter import *
import datetime
import calendar

root = Tk()
root.title("Age Calculator")
root.geometry("400x200")


def calculateage():
    try:
        year = int(YearVariable.get())  # Convert year to integer

        # Handle month input (check if it's a number or a valid month name)
        month_input = MonthVariable.get().strip()
        if month_input.isdigit():
            month = int(month_input)
        else:
            month = {v.lower(): k for k, v in enumerate(calendar.month_name) if v}[month_input.lower()]

        day = int(DayVariable.get())  # Convert day to integer

        # Validate date
        birthdate = datetime.datetime(year, month, day)
        age = datetime.datetime.now() - birthdate
        ageyears = round(age.days / 365, 2)

        Label(text=f"{NameVariable.get()} your age is {ageyears}").grid(row=6, column=1)

    except (ValueError, KeyError):
        Label(text="Invalid date! Enter valid numbers or month names.").grid(row=6, column=1)


# Labels
Label(root, text="Your Name").grid(row=1, column=1, padx=90)
Label(root, text="Year").grid(row=2, column=1, padx=90)
Label(root, text="Month").grid(row=3, column=1, padx=90)
Label(root, text="Day").grid(row=4, column=1, padx=90)

# Input Variables
NameVariable = StringVar()
YearVariable = StringVar()
MonthVariable = StringVar()
DayVariable = StringVar()

# Entry Fields
Entry(root, textvariable=NameVariable).grid(row=1, column=2)
Entry(root, textvariable=YearVariable).grid(row=2, column=2)
Entry(root, textvariable=MonthVariable).grid(row=3, column=2)
Entry(root, textvariable=DayVariable).grid(row=4, column=2)

# Submit Button
Button(root, text="Submit", command=calculateage).grid(row=5, column=1)

root.mainloop()
