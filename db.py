import sqlite3

def init_db():
    conn = sqlite3.connect("job_applications.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        job_title TEXT NOT NULL,
        date_applied TEXT,
        status TEXT,
        job_description TEXT,
        resume_path TEXT,
        cover_letter_path TEXT,
        follow_up_date TEXT
    )''')
    conn.commit()
    conn.close()

def insert_application(company, title, date_applied, status, description, resume, cover_letter, follow_up_date):
    conn = sqlite3.connect("job_applications.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO applications 
        (company_name, job_title, date_applied, status, job_description, resume_path, cover_letter_path, follow_up_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (company, title, date_applied, status, description, resume, cover_letter, follow_up_date))
    conn.commit()
    conn.close()

def get_all_applications():
    conn = sqlite3.connect("job_applications.db")
    c = conn.cursor()
    c.execute("SELECT * FROM applications")
    rows = c.fetchall()
    conn.close()
    return rows


def delete_application(app_id):
    conn = sqlite3.connect("job_applications.db")
    c = conn.cursor()
    c.execute("DELETE FROM applications WHERE id = ?", (app_id,))
    conn.commit()
    conn.close()


def update_application(app_id, company, title, date_applied, status, description, resume, cover_letter, follow_up_date):
    conn = sqlite3.connect("job_applications.db")
    c = conn.cursor()
    c.execute('''
        UPDATE applications
        SET company_name = ?, job_title = ?, date_applied = ?, status = ?, job_description = ?,
            resume_path = ?, cover_letter_path = ?, follow_up_date = ?
        WHERE id = ?
    ''', (company, title, date_applied, status, description, resume, cover_letter, follow_up_date, app_id))
    conn.commit()
    conn.close()
