import sqlite3

DB_NAME = "edupilot.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            grade TEXT NOT NULL,
            attendance INTEGER NOT NULL,
            average_grade INTEGER NOT NULL,
            missing_assignments INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interventions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            priority TEXT NOT NULL,
            reason TEXT NOT NULL,
            action TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    students = [
        (1, "Ali", "Grade 8", 72, 58, 5),
        (2, "Sara", "Grade 8", 95, 88, 0),
        (3, "Ahmed", "Grade 8", 81, 64, 3),
        (4, "Fatima", "Grade 8", 97, 92, 0),
        (5, "Hassan", "Grade 8", 68, 52, 7),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO students
        (id, name, grade, attendance, average_grade, missing_assignments)
        VALUES (?, ?, ?, ?, ?, ?)
    """, students)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_database()
    print("EduPilot database initialized.")