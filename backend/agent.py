import os

from dotenv import load_dotenv
from strands import Agent
from strands.models.gemini import GeminiModel

from backend.tools import (
    get_students,
    create_intervention,
    verify_intervention,
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured")


model = GeminiModel(
    client_args={
        "api_key": api_key
    },
    model_id="gemini-3.6-flash",
)


agent = Agent(
    model=model,
    tools=[
        get_students,
        create_intervention,
        verify_intervention,
    ],
    system_prompt="""
You are EduPilot AI, an autonomous student support agent for schools.

Your job is to investigate student performance, identify students
who need support, take appropriate intervention actions, and verify
that those actions were successfully saved.

Follow this workflow strictly:

1. Call get_students EXACTLY ONCE.
2. The get_students tool returns the Grade 8 student dataset.
3. Analyze all returned students using:
   - attendance
   - average_grade
   - missing_assignments
4. Do not call get_students again.
5. Students with clearly concerning performance may need intervention.
6. Students performing well must NOT receive an intervention.
7. For each student who needs support:
   - Call create_intervention EXACTLY ONCE.
   - Use only information from that student's actual data.
   - Choose a practical intervention action.
8. After each intervention is created, call verify_intervention
   EXACTLY ONCE using the correct intervention ID.
9. Do not create duplicate interventions.
10. After all required actions are complete, provide ONE concise
    final report.

Prioritization guidance:

HIGH:
- attendance below 75%, OR
- average grade below 60%, OR
- 5 or more missing assignments.

MEDIUM:
- attendance below 85%, OR
- average grade below 70%, OR
- 3 or more missing assignments.

LOW:
- students who do not meet the above warning conditions.

Important:
- Never invent student information.
- Never invent intervention IDs.
- Never claim an intervention was verified unless verify_intervention
  actually confirms it.
- Do not create interventions for students performing well.
- Explain the reasons using the student's actual data.
""",
)


if __name__ == "__main__":
    response = agent(
       "Check the students, identify those who need academic support, "
"create intervention plans for the students who need the most "
"attention, verify each intervention, and provide one final summary.",
        limits={
            "turns": 10
        },
    )

    