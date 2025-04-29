import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import db
import requests

class GolfApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Golf Stat Tracker")
        self.geometry("700x500")
        db.setup_database()

        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        self.stats_tab = tk.Frame(notebook)
        self.manage_tab = tk.Frame(notebook)
        self.course_tab = tk.Frame(notebook)

        notebook.add(self.stats_tab, text="🏠 Dashboard")
        notebook.add(self.manage_tab, text="📝 Manage Rounds")
        notebook.add(self.course_tab, text="🏞️ Courses")

        self.build_stats_tab()
        self.build_manage_tab()
        self.build_course_tab()

        tk.Button(self, text="📋 Start Guided Round", command=self.start_guided_round).pack(pady=8)
    def get_weather(self, location, api_key):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&units=imperial&appid={api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                desc = data['weather'][0]['description'].capitalize()
                temp = data['main']['temp']
                wind = data['wind']['speed']
                return f"{desc}, {temp:.0f}°F, Wind {wind} mph"
            else:
                return "Weather not found"
        except Exception as e:
            return f"Error: {e}"

    def build_stats_tab(self):
        for widget in self.stats_tab.winfo_children():
            widget.destroy()

        rounds = db.get_all_rounds()
        if not rounds:
            tk.Label(self.stats_tab, text="No rounds yet!").pack(pady=20)
            return

        scores = [r[2] for r in rounds if r[2] is not None]
        avg = sum(scores) / len(scores)
        best = min(scores)

        tk.Label(self.stats_tab, text=f"Rounds Played: {len(rounds)}").pack()
        tk.Label(self.stats_tab, text=f"Average Score: {avg:.1f}").pack()
        tk.Label(self.stats_tab, text=f"Best Score: {best}").pack(pady=(0, 10))

        tk.Label(self.stats_tab, text="Courses Played:").pack()
        for course in sorted(set(r[0] for r in rounds)):
            tk.Label(self.stats_tab, text=course).pack()
    def build_manage_tab(self):
        for widget in self.manage_tab.winfo_children():
            widget.destroy()

        rounds = db.get_all_rounds_with_id()
        if not rounds:
            tk.Label(self.manage_tab, text="No rounds to manage.").pack(pady=20)
            return

        for r in rounds:
            round_id, course, date, score = r
            frame = tk.Frame(self.manage_tab)
            frame.pack(fill="x", pady=2)

            info = f"{date} - {course} - {score}"
            tk.Label(frame, text=info, width=40, anchor="w").pack(side="left")
            tk.Button(frame, text="Delete", command=lambda rid=round_id: self.delete_round(rid)).pack(side="right")

    def delete_round(self, round_id):
        if messagebox.askyesno("Delete", "Are you sure you want to delete this round?"):
            db.delete_round(round_id)
            self.build_stats_tab()
            self.build_manage_tab()

    def build_course_tab(self):
        for widget in self.course_tab.winfo_children():
            widget.destroy()

        tk.Label(self.course_tab, text="Add New Course").pack(pady=10)
        form_frame = tk.Frame(self.course_tab)
        form_frame.pack()

        tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="e")
        name_entry = tk.Entry(form_frame)
        name_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="Location:").grid(row=1, column=0, sticky="e")
        location_entry = tk.Entry(form_frame)
        location_entry.grid(row=1, column=1)

        tk.Label(form_frame, text="Total Par:").grid(row=2, column=0, sticky="e")
        par_entry = tk.Entry(form_frame)
        par_entry.grid(row=2, column=1)

        def save_course():
            name = name_entry.get()
            location = location_entry.get()
            par = int(par_entry.get()) if par_entry.get().isdigit() else None
            if not name:
                messagebox.showerror("Missing Info", "Course name is required.")
                return
            db.add_course(name, location, par)
            messagebox.showinfo("Success", "Course added.")
            self.build_course_tab()

        tk.Button(form_frame, text="Save Course", command=save_course).grid(row=3, columnspan=2, pady=10)
        tk.Button(self.course_tab, text="📥 Import Course From Library", command=self.import_course_from_json).pack(pady=5)
        tk.Label(self.course_tab, text="Saved Courses:").pack(pady=5)
        for course in db.get_all_courses():
            name, location, par = course
            row = tk.Frame(self.course_tab)
            row.pack(anchor="w", padx=10, pady=2)

            text = f"{name} - {location or 'Unknown'} (Par {par or '?'})"
            tk.Label(row, text=text, width=40, anchor="w").pack(side="left")

            tk.Button(row, text="Edit", command=lambda n=name, l=location, p=par: self.edit_course_popup(n, l, p)).pack(side="left", padx=2)
            tk.Button(row, text="Delete", command=lambda n=name: self.delete_course(n)).pack(side="left", padx=2)
            tk.Button(row, text="Edit Layout", command=lambda n=name: self.open_hole_editor(n)).pack(side="left", padx=2)

    def import_course_from_json(self):
        try:
            with open("courses_data.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "courses_data.json not found.")
            return

        popup = tk.Toplevel(self)
        popup.title("Import Course From Library")

        tk.Label(popup, text="Select Course:").pack(pady=5)
        course_var = tk.StringVar()
        dropdown = ttk.Combobox(popup, textvariable=course_var, values=list(data.keys()), width=40)
        dropdown.pack(pady=5)

        def do_import():
            course_name = course_var.get()
            if course_name not in data:
                messagebox.showerror("Error", "Course not found.")
                return

            layout = data[course_name]
            total_par = sum(hole["par"] for hole in layout)
            db.add_course(course_name, location="Imported", total_par=total_par)
            db.save_course_layout(course_name, layout)
            messagebox.showinfo("Imported", f"{course_name} was imported.")
            popup.destroy()
            self.build_course_tab()

        tk.Button(popup, text="Import Course", command=do_import).pack(pady=10)

    def delete_course(self, name):
        if messagebox.askyesno("Delete", f"Delete course '{name}' and all its data?"):
            db.delete_course(name)
            self.build_course_tab()

    def edit_course_popup(self, old_name, location, par):
        win = tk.Toplevel(self)
        win.title(f"Edit Course - {old_name}")

        tk.Label(win, text="New Name:").grid(row=0, column=0)
        name_entry = tk.Entry(win)
        name_entry.insert(0, old_name)
        name_entry.grid(row=0, column=1)

        tk.Label(win, text="Location:").grid(row=1, column=0)
        location_entry = tk.Entry(win)
        location_entry.insert(0, location or "")
        location_entry.grid(row=1, column=1)

        tk.Label(win, text="Total Par:").grid(row=2, column=0)
        par_entry = tk.Entry(win)
        par_entry.insert(0, str(par or ""))
        par_entry.grid(row=2, column=1)

        def update():
            new_name = name_entry.get()
            loc = location_entry.get()
            new_par = int(par_entry.get()) if par_entry.get().isdigit() else None
            if not new_name:
                messagebox.showerror("Missing Info", "Course name is required.")
                return
            db.update_course(old_name, new_name, loc, new_par)
            win.destroy()
            self.build_course_tab()

        tk.Button(win, text="Save Changes", command=update).grid(row=3, columnspan=2, pady=10)

    def open_hole_editor(self, course_name):
        hole_win = tk.Toplevel(self)
        hole_win.title(f"Edit Layout - {course_name}")
        hole_win.geometry("700x650")

        headers = ["Hole", "Par", "Blue", "White", "Red"]
        for i, h in enumerate(headers):
            tk.Label(hole_win, text=h, font=("Helvetica", 10, "bold")).grid(row=0, column=i, padx=5)

        hole_entries = []
        for i in range(18):
            hole_number = i + 1
            tk.Label(hole_win, text=str(hole_number)).grid(row=i+1, column=0)
            par_entry = tk.Entry(hole_win, width=5)
            blue_entry = tk.Entry(hole_win, width=6)
            white_entry = tk.Entry(hole_win, width=6)
            red_entry = tk.Entry(hole_win, width=6)
            par_entry.grid(row=i+1, column=1)
            blue_entry.grid(row=i+1, column=2)
            white_entry.grid(row=i+1, column=3)
            red_entry.grid(row=i+1, column=4)
            hole_entries.append((hole_number, par_entry, blue_entry, white_entry, red_entry))
        def import_layout():
            try:
                with open("courses_data.json", "r") as f:
                    data = json.load(f)
                if course_name in data:
                    layout = data[course_name]
                    for i, hole in enumerate(layout):
                        hole_entries[i][1].delete(0, tk.END)
                        hole_entries[i][1].insert(0, hole["par"])
                        hole_entries[i][2].insert(0, hole.get("blue", ""))
                        hole_entries[i][3].insert(0, hole.get("white", ""))
                        hole_entries[i][4].insert(0, hole.get("red", ""))
                    messagebox.showinfo("Imported", "Layout imported from library.")
                else:
                    messagebox.showwarning("Not Found", "Course not found in library.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def save_layout():
            data = []
            for hole_num, par_e, blue_e, white_e, red_e in hole_entries:
                data.append({
                    "hole": hole_num,
                    "par": int(par_e.get()) if par_e.get().isdigit() else 4,
                    "blue": int(blue_e.get()) if blue_e.get().isdigit() else None,
                    "white": int(white_e.get()) if white_e.get().isdigit() else None,
                    "red": int(red_e.get()) if red_e.get().isdigit() else None
                })
            db.save_course_layout(course_name, data)
            messagebox.showinfo("Success", "Hole layout saved.")
            hole_win.destroy()

        tk.Button(hole_win, text="📥 Import From Course Library", command=import_layout).grid(row=20, columnspan=5, pady=10)
        tk.Button(hole_win, text="Save Layout", command=save_layout).grid(row=21, columnspan=5, pady=10)

    def start_guided_round(self):
        guided_win = tk.Toplevel(self)
        guided_win.title("Start Guided Round")
        guided_win.geometry("400x450")

        tk.Label(guided_win, text="Select Course:").pack()
        course_names = db.get_course_names()
        course_var = tk.StringVar()
        course_dropdown = ttk.Combobox(guided_win, textvariable=course_var, values=course_names)
        course_dropdown.pack()

        tk.Label(guided_win, text="Tee Played:").pack()
        tee_var = tk.StringVar(value="Blue")
        ttk.Combobox(guided_win, textvariable=tee_var, values=["Blue", "White", "Red"], state="readonly").pack()

        tk.Label(guided_win, text="Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(guided_win)
        date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
        date_entry.pack()

        tk.Label(guided_win, text="Location (City or ZIP):").pack()
        location_entry = tk.Entry(guided_win)
        location_entry.pack()

        hole_count_var = tk.IntVar(value=18)
        tk.Label(guided_win, text="Number of Holes:").pack()
        tk.Radiobutton(guided_win, text="9", variable=hole_count_var, value=9).pack()
        tk.Radiobutton(guided_win, text="18", variable=hole_count_var, value=18).pack()

        def begin_round():
            course = course_var.get()
            tee_color = tee_var.get()
            date = date_entry.get()
            location = location_entry.get()
            holes = hole_count_var.get()
            layout = db.get_course_layout(course)

            if not course or not location:
                messagebox.showerror("Missing Info", "Course and location are required.")
                return

            # Show weather
            weather = self.get_weather(location, "26fadaf64f5c6e0672c78a4222dfd69f")  # Replace with your actual API key
            messagebox.showinfo("Weather", f"Current weather in {location}:\n{weather}")

            guided_win.destroy()
            self.run_guided_round(course, date, holes, layout, tee_color)

        tk.Button(guided_win, text="Start Round", command=begin_round).pack(pady=10)

    def run_guided_round(self, course, date, holes, layout=None, tee_color="Blue"):
        import functools
        hole_data = []
        current_hole = 1
        score_value = tk.IntVar(value=0)
        putts_value = tk.IntVar(value=-1)
        fairway_var = tk.StringVar(value="No")
        gir_var = tk.StringVar(value="No")

        def select_score(val):
            score_value.set(val)
            update_display()

        def select_putt(val):
            putts_value.set(val)
            update_display()

        def toggle_fairway(val):
            fairway_var.set(val)
            update_display()

        def toggle_gir(val):
            gir_var.set(val)
            update_display()

        def update_display():
            hole_label.config(text=f"Hole {current_hole}")
            for i, btn in enumerate(score_buttons, start=1):
                btn.config(relief="sunken" if score_value.get() == i else "raised")

            for i, btn in enumerate(putt_buttons):
                btn.config(relief="sunken" if putts_value.get() == i else "raised")

            for val, btn in fairway_buttons.items():
                btn.config(relief="sunken" if fairway_var.get() == val else "raised")

            for val, btn in gir_buttons.items():
                btn.config(relief="sunken" if gir_var.get() == val else "raised")

            if layout and current_hole <= len(layout):
                info = layout[current_hole - 1]
                par_text = f"Par: {info[1]}"
                yards = f"Blue: {info[2] or '-'} | White: {info[3] or '-'} | Red: {info[4] or '-'}"
                layout_label.config(text=f"{par_text}   {yards}")
            else:
                layout_label.config(text="")

        def next_hole():
            nonlocal current_hole
            score = score_value.get()
            putts = putts_value.get()

            if score == 0 or putts < 0:
                messagebox.showerror("Missing Info", "Please select a score and putts.")
                return

            hole_data_entry = {
                "hole": current_hole,
                "score": score,
                "fairway": fairway_var.get() == "Yes",
                "gir": gir_var.get() == "Yes",
                "putts": putts
            }

            if len(hole_data) < current_hole:
                hole_data.append(hole_data_entry)
            else:
                hole_data[current_hole - 1] = hole_data_entry

            if current_hole == holes:
                popup.destroy()
                self.finish_guided_round(course, date, tee_color, hole_data)
            else:
                current_hole += 1
                score_value.set(0)
                putts_value.set(-1)
                fairway_var.set("No")
                gir_var.set("No")
                update_display()

        def prev_hole():
            nonlocal current_hole
            if current_hole > 1:
                current_hole -= 1
                update_display()

        popup = tk.Toplevel(self)
        popup.title("Guided Round")
        popup.geometry("450x450")

        hole_label = tk.Label(popup, text=f"Hole {current_hole}", font=("Helvetica", 16))
        hole_label.pack(pady=10)

        layout_label = tk.Label(popup, text="", font=("Helvetica", 10))
        layout_label.pack()

        # Score buttons
        score_frame = tk.LabelFrame(popup, text="Score")
        score_frame.pack(pady=5)
        score_buttons = []
        for i in range(1, 9):
            btn = tk.Button(score_frame, text=str(i), width=3, command=functools.partial(select_score, i))
            btn.grid(row=0, column=i - 1, padx=2)
            score_buttons.append(btn)

        # Putts buttons
        putt_frame = tk.LabelFrame(popup, text="Putts")
        putt_frame.pack(pady=5)
        putt_buttons = []
        for i in range(0, 5):
            btn = tk.Button(putt_frame, text=str(i), width=3, command=functools.partial(select_putt, i))
            btn.grid(row=0, column=i, padx=2)
            putt_buttons.append(btn)

        # Fairway toggle
        fairway_frame = tk.LabelFrame(popup, text="Fairway Hit")
        fairway_frame.pack(pady=5)
        fairway_buttons = {}
        for col, val in enumerate(["Yes", "No"]):
            btn = tk.Button(fairway_frame, text=val, width=6, command=functools.partial(toggle_fairway, val))
            btn.grid(row=0, column=col, padx=5)
            fairway_buttons[val] = btn

        # GIR toggle
        gir_frame = tk.LabelFrame(popup, text="GIR")
        gir_frame.pack(pady=5)
        gir_buttons = {}
        for col, val in enumerate(["Yes", "No"]):
            btn = tk.Button(gir_frame, text=val, width=6, command=functools.partial(toggle_gir, val))
            btn.grid(row=0, column=col, padx=5)
            gir_buttons[val] = btn

        nav_frame = tk.Frame(popup)
        nav_frame.pack(pady=15)

        tk.Button(nav_frame, text="⬅ Previous Hole", command=prev_hole).pack(side="left", padx=10)
        tk.Button(nav_frame, text="Next Hole ➡", command=next_hole).pack(side="left", padx=10)

        popup.bind("<Return>", lambda event: next_hole())

        update_display()

    def finish_guided_round(self, course, date, tee_played, hole_data):
        total_score = sum(h["score"] for h in hole_data)
        total_putts = sum(h["putts"] for h in hole_data)
        total_gir = sum(1 for h in hole_data if h["gir"])
        total_fw = sum(1 for h in hole_data if h["fairway"])
        hole_scores_json = json.dumps([h["score"] for h in hole_data])

        db.add_round(course, date, tee_played, total_score, total_putts, total_fw, total_gir, hole_scores_json)

        messagebox.showinfo(
            "Round Complete",
            f"Tee: {tee_played}\nScore: {total_score}\nPutts: {total_putts}\nFairways Hit: {total_fw}\nGIRs: {total_gir}"
        )

        # 🎯 Show round insights
        insights = self.generate_round_insights(hole_data)
        messagebox.showinfo("Round Insights", insights)

        self.build_stats_tab()
        self.build_manage_tab()

    def generate_round_insights(self, hole_data):
        total_holes = len(hole_data)
        scores = [h["score"] for h in hole_data]
        putts = [h["putts"] for h in hole_data]
        fairways = sum(1 for h in hole_data if h["fairway"])
        girs = sum(1 for h in hole_data if h["gir"])

        most_common_score = max(set(scores), key=scores.count)
        fewest_putts = min(putts)
        most_putts = max(putts)
        fairway_pct = fairways / total_holes * 100
        gir_pct = girs / total_holes * 100

        streak = 0
        max_streak = 0
        for s in scores:
            if s <= 4:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0

        return (
            f"Most common score: {most_common_score}\n"
            f"Putts ranged from {fewest_putts} to {most_putts}\n"
            f"Fairways hit: {fairways}/{total_holes} ({fairway_pct:.0f}%)\n"
            f"GIRs: {girs}/{total_holes} ({gir_pct:.0f}%)\n"
            f"Longest 'under-par' streak: {max_streak} holes"
        )


# Launch the app
if __name__ == "__main__":
    app = GolfApp()
    app.mainloop()
