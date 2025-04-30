import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import os
import random
import requests
from datetime import date
from database.db import init_db, insert_application, get_all_applications, update_application, delete_application

users = {
    "BUS472": "1234"
}

resume_path = ""
cover_path = ""
selected_app_id = None

interview_questions = [
    "Tell me about yourself. (Include your background, experience, and skills relevant to the position)",
    "What are your strengths? (Provide specific examples and relate them to the job requirements)",
    "What are your weaknesses? (Be honest but focus on how you’re working to improve them)",
    "Why do you want this job? (Talk about your passion for the company’s mission and how it aligns with your goals)",
    "Where do you see yourself in five years? (Discuss your career growth and how the company fits into your plans)",
    "Why should we hire you? (Highlight your unique skills and how you can contribute to the company)",
    "Describe a challenging project you worked on. (Talk about the situation, your approach, and the outcome)",
    "How do you handle tight deadlines? (Provide an example of how you’ve managed deadlines in the past)",
    "Tell me about a time you failed. (Be honest, and focus on what you learned from the experience)",
    "How do you prioritize tasks? (Explain your approach and give an example of how you've managed multiple tasks)",
    "Describe a time you showed leadership. (Provide a specific example, focusing on your leadership qualities)",
    "How do you handle feedback? (Discuss your openness to feedback and how you’ve applied it for improvement)",
    "What’s your ideal work environment? (Describe the type of environment where you thrive and feel most productive)",
    "Tell me about a time you had a conflict at work. (Discuss how you handled it, focusing on resolution and communication)",
    "What motivates you? (Discuss what drives you, and how that aligns with the company’s values)",
    "How do you stay organized? (Talk about your organizational strategies and how they’ve helped you be efficient)",
    "How do you handle pressure? (Describe how you’ve managed stress in the past and maintained productivity)",
    "What’s your biggest professional achievement? (Share a significant achievement, and explain why it’s important to you)",
    "Why are you leaving your current job? (Be honest but professional, focusing on the positive reasons for change)",
    "What are you passionate about? (Discuss what excites you, and how that aligns with the job you’re applying for)"
] * 5  # 100 questions

def search_jobs_api(query):
    url = "https://jsearch.p.rapidapi.com/search"
    params = {"query": query, "page": "1", "num_pages": "1"}
    headers = {
        "X-RapidAPI-Key": "0952aef349msh86d7018e54ba170p1589e6jsn9cc03bc58f51",
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.json().get("data", [])
    except Exception as e:
        print("API error:", e)
        return []

def show_main_app():
    global resume_path, cover_path, selected_app_id
    init_db()
    root = tk.Tk()
    root.title("Job Application Tracker")
    root.geometry("850x550")
    root.configure(bg="#f1f8e9")  # Background color for the main app screen

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    # ------------------ Application Form Tab ------------------
    form_tab = tk.Frame(notebook, bg="#f1f8e9")  # Application form tab background color
    notebook.add(form_tab, text="Application Form")
    form_frame = tk.Frame(form_tab, padx=10, pady=10, bg="#f1f8e9")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Company Name", bg="#f1f8e9", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="e")
    company_entry = tk.Entry(form_frame, font=("Helvetica", 12), bg="#e8f5e9")  # Light green text box
    company_entry.grid(row=0, column=1)

    tk.Label(form_frame, text="Job Title", bg="#f1f8e9", font=("Helvetica", 12, "bold")).grid(row=1, column=0, sticky="e")
    title_entry = tk.Entry(form_frame, font=("Helvetica", 12), bg="#e8f5e9")
    title_entry.grid(row=1, column=1)

    tk.Label(form_frame, text="Date Applied", bg="#f1f8e9", font=("Helvetica", 12, "bold")).grid(row=2, column=0, sticky="e")
    date_entry = DateEntry(form_frame, width=18, font=("Helvetica", 12), background="lightblue")
    date_entry.grid(row=2, column=1)

    tk.Label(form_frame, text="Status", bg="#f1f8e9", font=("Helvetica", 12, "bold")).grid(row=3, column=0, sticky="e")
    status_var = tk.StringVar()
    status_menu = ttk.Combobox(form_frame, textvariable=status_var, values=["Applied", "Interview Scheduled", "Offer Received", "Rejected"], font=("Helvetica", 12))
    status_menu.grid(row=3, column=1)

    tk.Label(form_frame, text="Job Description", bg="#f1f8e9", font=("Helvetica", 12, "bold")).grid(row=4, column=0, sticky="ne")
    description_entry = tk.Text(form_frame, height=4, width=40, font=("Helvetica", 12), bg="#e8f5e9")
    description_entry.grid(row=4, column=1)

    tk.Label(form_frame, text="Follow-Up Date", bg="#f1f8e9", font=("Helvetica", 12, "bold")).grid(row=5, column=0, sticky="e")
    follow_up_entry = DateEntry(form_frame, width=18, font=("Helvetica", 12), background="lightblue")
    follow_up_entry.grid(row=5, column=1, sticky="w")

    resume_label = tk.Label(form_frame, text="No file selected", bg="#f1f8e9", font=("Helvetica", 12))
    cover_label = tk.Label(form_frame, text="No file selected", bg="#f1f8e9", font=("Helvetica", 12))

    def upload_resume():
        global resume_path
        resume_path = filedialog.askopenfilename()
        resume_label.config(text=os.path.basename(resume_path))

    def upload_cover_letter():
        global cover_path
        cover_path = filedialog.askopenfilename()
        cover_label.config(text=os.path.basename(cover_path))

    tk.Button(form_frame, text="Upload Resume", command=upload_resume, font=("Helvetica", 12, "bold"), bg="#43a047", fg="white").grid(row=6, column=0, sticky="e")
    resume_label.grid(row=6, column=1, sticky="w")
    tk.Button(form_frame, text="Upload Cover Letter", command=upload_cover_letter, font=("Helvetica", 12, "bold"), bg="#43a047", fg="white").grid(row=7, column=0, sticky="e")
    cover_label.grid(row=7, column=1, sticky="w")

    def clear_form():
        global resume_path, cover_path, selected_app_id
        company_entry.delete(0, tk.END)
        title_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        status_var.set('')  # Reset status
        description_entry.delete("1.0", tk.END)
        follow_up_entry.set_date(date.today())
        resume_path = ""
        cover_path = ""
        resume_label.config(text="No file selected")
        cover_label.config(text="No file selected")
        selected_app_id = None

    def refresh_applications():
        app_list.delete(*app_list.get_children())
        for app in get_all_applications():
            app_list.insert('', tk.END, iid=app[0], values=(app[1], app[2], app[3], app[4], os.path.basename(app[6] or ""), os.path.basename(app[7] or ""), app[8] or "N/A"))

    def add_application():
        insert_application(company_entry.get(), title_entry.get(), date_entry.get(), status_var.get(), description_entry.get("1.0", tk.END).strip(), resume_path, cover_path, follow_up_entry.get())
        clear_form()
        refresh_applications()

    def update_selected_application():
        if selected_app_id:
            update_application(selected_app_id, company_entry.get(), title_entry.get(), date_entry.get(), status_var.get(), description_entry.get("1.0", tk.END).strip(), resume_path, cover_path, follow_up_entry.get())
            clear_form()
            refresh_applications()

    tk.Button(form_frame, text="Add Application", command=add_application, font=("Helvetica", 12, "bold"), bg="#43a047", fg="white").grid(row=8, column=0, pady=10)
    tk.Button(form_frame, text="Update Application", command=update_selected_application, font=("Helvetica", 12, "bold"), bg="#43a047", fg="white").grid(row=8, column=1, pady=10)

    # ------------------ Job Search Tab ------------------
    search_tab = tk.Frame(notebook, bg="#f1f8e9")  # Job search tab background color
    notebook.add(search_tab, text="Job Search")

    tk.Label(search_tab, text="Search for a job:", font=("Helvetica", 12), bg="#f1f8e9", fg="#33691e").pack(pady=5)
    search_entry = tk.Entry(search_tab, width=40, font=("Helvetica", 12), bg="#e8f5e9")
    search_entry.pack(pady=10)

    def search_jobs():
        query = search_entry.get()
        jobs = search_jobs_api(query)
        result_list.delete(*result_list.get_children())
        for job in jobs:
            result_list.insert("", tk.END, values=(job["job_title"], job["company_name"], job["job_posted_date"], job["location"], job["job_description"]))

    tk.Button(search_tab, text="Search", command=search_jobs, font=("Helvetica", 12, "bold"), bg="#43a047", fg="white").pack()

    result_list = ttk.Treeview(search_tab, columns=("Job Title", "Company", "Posted", "Location", "Description"), show="headings")
    result_list.heading("Job Title", text="Job Title")
    result_list.heading("Company", text="Company")
    result_list.heading("Posted", text="Posted Date")
    result_list.heading("Location", text="Location")
    result_list.heading("Description", text="Description")
    result_list.pack(fill="both", expand=True)

    # ------------------ Application List Tab ------------------
    list_tab = tk.Frame(notebook, bg="#f1f8e9")  # Application list tab background color
    notebook.add(list_tab, text="Application List")
    app_list = ttk.Treeview(list_tab, columns=("Company", "Title", "Date Applied", "Status", "Resume", "Cover Letter", "Follow-Up"), show="headings")
    app_list.heading("Company", text="Company")
    app_list.heading("Title", text="Job Title")
    app_list.heading("Date Applied", text="Date Applied")
    app_list.heading("Status", text="Status")
    app_list.heading("Resume", text="Resume")
    app_list.heading("Cover Letter", text="Cover Letter")
    app_list.heading("Follow-Up", text="Follow-Up")
    app_list.pack(fill="both", expand=True)

    def delete_selected_application():
        global selected_app_id
        selected_item = app_list.focus()
        if selected_item:
            selected_app_id = selected_item
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this application?"):
                delete_application(selected_app_id)
                clear_form()
                refresh_applications()

    delete_button = tk.Button(list_tab, text="Delete Application", command=delete_selected_application,
                              font=("Helvetica", 12, "bold"), bg="#e53935", fg="white")
    delete_button.pack(pady=10)

    refresh_applications()

    # ------------------ Mock Interview Tab ------------------
    interview_tab = tk.Frame(notebook, bg="#f1f8e9")  # Mock interview tab background color
    notebook.add(interview_tab, text="Mock Interview")

    # Label to display instructions before starting the interview
    instruction_label = tk.Label(interview_tab, text="Click to Start the Interview", wraplength=700,
                                 font=("Helvetica", 18, "bold"), bg="#f1f8e9", fg="#33691e")
    instruction_label.pack(pady=150)  # Position at the center of the screen

    # Button to start the interview, larger button
    interview_button = tk.Button(interview_tab, text="Start Interview", command=lambda: start_interview(),
                                 font=("Helvetica", 20, "bold"), bg="#43a047", fg="white", height=3, width=20)
    interview_button.pack()

    # Label to display questions after the interview starts
    question_label = tk.Label(interview_tab, text="", wraplength=700, font=("Helvetica", 14), bg="#f1f8e9",
                              fg="#33691e")
    question_label.pack(pady=50)

    # Text box for the user to input their answer (initially hidden)
    answer_text = tk.Text(interview_tab, height=5, width=60, font=("Helvetica", 12), bg="#e8f5e9")
    answer_text.pack(pady=(0, 10))
    answer_text.pack_forget()  # Initially hide the answer box

    # Button to show the next question
    def next_question():
        global question_count
        if question_count < 10:
            # Choose a random question and display it
            question = random.choice(interview_questions)
            # Ensure it's not a duplicate
            while question in answered_questions:
                question = random.choice(interview_questions)
            question_label.config(text=question)
            answered_questions.append(question)
            answer_text.delete("1.0", tk.END)  # Clear previous answer
            answer_text.pack(pady=(0, 10))  # Show the text box for answers
            question_count += 1

            # After the 10th question, change the button to "Restart"
            if question_count == 10:
                interview_button.config(text="Restart", command=restart_interview)
        else:
            restart_interview()

    # Function to start the interview
    def start_interview():
        global question_count, answered_questions
        question_count = 0
        answered_questions = []

        # Clear the initial instruction label and show the question and input box
        instruction_label.pack_forget()
        interview_button.config(text="Next Question", command=next_question)

        next_question()  # Start by showing the first question

    # Function to restart the interview
    def restart_interview():
        global question_count, answered_questions
        question_count = 0
        answered_questions = []

        # Reset everything and show the start screen
        question_label.config(text="")
        answer_text.delete("1.0", tk.END)
        answer_text.pack_forget()  # Hide the answer box
        interview_button.config(text="Start Interview", command=start_interview)

        # Bring back the instruction label
        instruction_label.pack(pady=150)


def attempt_login(username, password, window):
    if username in users and users[username] == password:
        messagebox.showinfo("Login Success", "Welcome!")
        window.destroy()
        show_main_app()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")


def show_login():
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.configure(bg="#f1f8e9")  # Login screen background color

    window_width = 400
    window_height = 300
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    login_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    login_window.resizable(False, False)

    title_label = tk.Label(login_window, text="Login", font=("Helvetica", 24, "bold"), bg="#f1f8e9", fg="#33691e")
    title_label.pack(pady=20)

    username_label = tk.Label(login_window, text="Username:", font=("Helvetica", 12), bg="#f1f8e9", fg="#558b2f")
    username_label.pack(pady=(10, 5))
    username_entry = tk.Entry(login_window, font=("Helvetica", 12), bg="#e8f5e9")
    username_entry.pack(pady=5)

    password_label = tk.Label(login_window, text="Password:", font=("Helvetica", 12), bg="#f1f8e9", fg="#558b2f")
    password_label.pack(pady=(10, 5))
    password_entry = tk.Entry(login_window, show="*", font=("Helvetica", 12), bg="#e8f5e9")
    password_entry.pack(pady=5)

    login_button = tk.Button(
        login_window,
        text="Login",
        font=("Helvetica", 12, "bold"),
        bg="#43a047",  # Green background
        fg="white",
        activebackground="#388e3c",
        activeforeground="white",
        width=15,
        command=lambda: attempt_login(username_entry.get(), password_entry.get(), login_window)
    )
    login_button.pack(pady=20)

    login_window.mainloop()

if __name__ == "__main__":
    show_login()

