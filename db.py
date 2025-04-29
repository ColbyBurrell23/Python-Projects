import sqlite3
import json

DB_NAME = "golf.db"

def connect():
    return sqlite3.connect(DB_NAME)

def setup_database():
    with connect() as conn:
        cursor = conn.cursor()

        # Updated rounds table with tee_played column
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS rounds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course TEXT NOT NULL,
            date TEXT NOT NULL,
            tee_played TEXT,
            total_score INTEGER,
            putts INTEGER,
            fairways_hit INTEGER,
            gir INTEGER,
            hole_scores TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            total_par INTEGER
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS course_holes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            hole_number INTEGER NOT NULL,
            par INTEGER,
            blue_yardage INTEGER,
            white_yardage INTEGER,
            red_yardage INTEGER
        )
        """)
        conn.commit()

# ----------------- ROUND FUNCTIONS -----------------

def add_round(course, date, tee_played=None, total_score=None, putts=None, fairways_hit=None, gir=None, hole_scores=None):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO rounds (course, date, tee_played, total_score, putts, fairways_hit, gir, hole_scores)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (course, date, tee_played, total_score, putts, fairways_hit, gir, hole_scores))
        conn.commit()

def get_all_rounds():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT course, date, total_score, tee_played FROM rounds")
        return cursor.fetchall()

def get_all_rounds_with_id():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, course, date, total_score FROM rounds")
        return cursor.fetchall()

def delete_round(round_id):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rounds WHERE id = ?", (round_id,))
        conn.commit()

# ----------------- COURSE FUNCTIONS -----------------

def add_course(name, location=None, total_par=None):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO courses (name, location, total_par)
            VALUES (?, ?, ?)
        """, (name, location, total_par))
        conn.commit()

def get_all_courses():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, location, total_par FROM courses")
        return cursor.fetchall()

def get_course_names():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM courses")
        return [row[0] for row in cursor.fetchall()]

def update_course(old_name, new_name, location, total_par):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE courses SET name = ?, location = ?, total_par = ? WHERE name = ?", (new_name, location, total_par, old_name))
        cursor.execute("UPDATE course_holes SET course_name = ? WHERE course_name = ?", (new_name, old_name))
        cursor.execute("UPDATE rounds SET course = ? WHERE course = ?", (new_name, old_name))
        conn.commit()

def delete_course(name):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM courses WHERE name = ?", (name,))
        cursor.execute("DELETE FROM course_holes WHERE course_name = ?", (name,))
        cursor.execute("DELETE FROM rounds WHERE course = ?", (name,))
        conn.commit()

# ----------------- HOLE LAYOUT FUNCTIONS -----------------

def save_course_layout(course_name, hole_data):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM course_holes WHERE course_name = ?", (course_name,))
        for hole in hole_data:
            cursor.execute("""
                INSERT INTO course_holes (course_name, hole_number, par, blue_yardage, white_yardage, red_yardage)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                course_name,
                hole["hole"],
                hole.get("par"),
                hole.get("blue"),
                hole.get("white"),
                hole.get("red")
            ))
        conn.commit()

def get_course_layout(course_name):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT hole_number, par, blue_yardage, white_yardage, red_yardage
            FROM course_holes
            WHERE course_name = ?
            ORDER BY hole_number
        """, (course_name,))
        return cursor.fetchall()
