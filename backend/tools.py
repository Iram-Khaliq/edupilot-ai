from strands import tool
from backend.database import get_connection


@tool
def get_students() -> list:
    """Get all Grade 8 students with attendance, grades, and missing assignments."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, grade, attendance, average_grade, missing_assignments
        FROM students
        WHERE LOWER(REPLACE(grade, ' ', '')) = 'grade8'
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "grade": row[2],
            "attendance": row[3],
            "average_grade": row[4],
            "missing_assignments": row[5]
        }
        for row in rows
    ]


@tool
def create_intervention(
    student_id: int,
    priority: str,
    reason: str,
    action: str
) -> str:
    """Create and save an intervention plan unless one already exists."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, priority, status
        FROM interventions
        WHERE student_id = ?
        AND status = 'created'
        ORDER BY id DESC
        LIMIT 1
    """, (student_id,))

    existing = cursor.fetchone()

    if existing:
        conn.close()

        return (
            f"An active intervention already exists for student "
            f"{student_id}. Intervention ID: {existing[0]}, "
            f"Priority: {existing[1]}, Status: {existing[2]}. "
            f"No duplicate intervention was created."
        )

    cursor.execute("""
        INSERT INTO interventions
        (student_id, priority, reason, action, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        student_id,
        priority,
        reason,
        action,
        "created"
    ))

    intervention_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return (
        f"Intervention {intervention_id} created successfully "
        f"for student {student_id}."
    )


@tool
def verify_intervention(intervention_id: int) -> str:
    """Verify that an intervention was successfully saved."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, student_id, priority, status
        FROM interventions
        WHERE id = ?
    """, (intervention_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return f"Intervention {intervention_id} was not found."

    return (
        f"Intervention {row[0]} verified successfully. "
        f"Student ID: {row[1]}, "
        f"Priority: {row[2]}, "
        f"Status: {row[3]}."
    )