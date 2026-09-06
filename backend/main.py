from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from strands.types.exceptions import ModelThrottledException
from backend.agent import agent
from backend.database import get_connection
from backend.tools import (
    get_students,
    create_intervention,
    verify_intervention
)

app = FastAPI(
    title="EduPilot AI",
    description="AI-powered student support and early intervention agent",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StudentSupportRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {
        "message": "EduPilot AI API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/students")
def students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, grade, attendance, average_grade, missing_assignments
        FROM students
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
@app.get("/interventions")
def interventions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            interventions.id,
            students.name,
            interventions.priority,
            interventions.reason,
            interventions.action,
            interventions.status
        FROM interventions
        JOIN students
        ON interventions.student_id = students.id
        ORDER BY interventions.id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "student_name": row[1],
            "priority": row[2],
            "reason": row[3],
            "action": row[4],
            "status": row[5]
        }
        for row in rows
    ]
@app.post("/demo-intervention")
def demo_intervention():
    # Use Hassan as the demonstration student.
    student_id = 5

    reason = (
        "Low attendance rate of 68%, "
        "average grade of 52%, and 7 missing assignments."
    )

    action = (
        "Schedule a parent-teacher conference, "
        "create an attendance recovery plan, "
        "and arrange academic tutoring."
    )

    # Create intervention
    created_message = create_intervention(
        student_id=student_id,
        priority="High",
        reason=reason,
        action=action
    )

    # Find the latest intervention for this student
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, status
        FROM interventions
        WHERE student_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (student_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {
            "status": "error",
            "message": "Intervention was not found."
        }

    intervention_id = row[0]
    intervention_status = row[1]

    # Verify intervention
    verified_message = verify_intervention(intervention_id)

    return {
        "status": "success",
        "intervention_id": intervention_id,
        "student": "Hassan",
        "priority": "High",
        "intervention_status": intervention_status,
        "created_message": created_message,
        "verified_message": verified_message
    }
@app.post("/analyze")
def analyze(request: StudentSupportRequest):
    try:
        response = agent(
            request.message,
            limits={
                "turns": 6
            }
        )

        return {
            "status": "success",
            "result": str(response)
        }

    except ModelThrottledException:
        return {
            "status": "error",
            "message": (
                "EduPilot's AI model is temporarily unavailable "
                "because the Gemini API quota has been reached. "
                "Please try again later."
            )
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"EduPilot encountered an error: {str(e)}"
        }

    except ModelThrottledException:
        return {
            "status": "error",
            "message": "EduPilot's AI model is temporarily unavailable because the Gemini API quota has been reached. Please try again later."
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"EduPilot encountered an error: {str(e)}"
        }