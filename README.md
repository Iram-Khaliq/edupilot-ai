# EduPilot AI

## Student Support & Early Intervention Agent

EduPilot AI is an AI-powered student support agent designed to help schools identify students who may be struggling academically and take timely intervention actions.

Instead of only displaying student data, EduPilot investigates student performance, prioritizes students based on risk indicators, creates intervention plans, and verifies that those interventions were successfully saved.

### Agent Workflow

**Investigate → Prioritize → Intervene → Verify**

---

## The Problem

Schools often have attendance, grades, and assignment data, but identifying students who need help can still require manual review.

This can lead to:

* Students being identified too late
* Staff spending time manually reviewing records
* Important warning signs being missed
* Interventions not being consistently recorded

EduPilot AI turns these signals into an actionable early-intervention workflow.

---

## The Solution

EduPilot AI acts as a student-support agent.

A school staff member can ask:

> "Check Grade 8 students and identify students who need academic support."

EduPilot then:

1. Investigates the student dataset.
2. Reviews attendance, grades, and missing assignments.
3. Determines each student's support priority.
4. Creates intervention plans for students requiring support.
5. Prevents duplicate active interventions.
6. Verifies that each intervention was successfully saved.
7. Produces a final summary for the school staff member.

---

## Risk Prioritization

EduPilot uses transparent rules to prioritize students.

### High Priority

A student is classified as **High** when any of these conditions apply:

* Attendance below 75%
* Average grade below 60%
* 5 or more missing assignments

### Medium Priority

A student is classified as **Medium** when any of these conditions apply:

* Attendance below 85%
* Average grade below 70%
* 3 or more missing assignments

### Low Priority

Students who do not meet the warning conditions are classified as **Low** and do not receive an intervention.

This allows the agent to focus actions on students who need the most attention.

---

## Example

For example, EduPilot may identify:

| Student | Attendance | Average Grade | Missing Work | Priority |
| ------- | ---------: | ------------: | -----------: | -------- |
| Hassan  |        68% |           52% |            7 | High     |
| Ali     |        72% |           58% |            5 | High     |
| Ahmed   |        81% |           64% |            3 | Medium   |
| Sara    |        95% |           88% |            0 | Low      |
| Fatima  |        97% |           92% |            0 | Low      |

For students requiring support, EduPilot creates an intervention and verifies that it exists in the database.

---

## Why This Is an Agent

EduPilot is designed around an action-oriented agent loop rather than a simple chatbot.

The agent can:

**Investigate**

Retrieve the relevant student information using a tool.

**Prioritize**

Reason over attendance, grades, and missing assignments to determine which students require support.

**Intervene**

Use a tool to create and save an intervention plan.

**Verify**

Use another tool to confirm that the intervention was successfully stored.

The result is an end-to-end workflow:

```text
User Request
     ↓
EduPilot Agent
     ↓
Investigate Student Data
     ↓
Analyze Risk
     ↓
Prioritize Students
     ↓
Create Interventions
     ↓
Verify Interventions
     ↓
Final Support Report
```

---

## Technology Stack

### AI / Agent

* Strands Agents SDK
* Google Gemini

### Backend

* Python
* FastAPI
* SQLite

### Frontend

* React
* Vite
* JavaScript
* CSS

### Development

* Git
* GitHub

---

## Project Structure

```text
edupilot-ai/
│
├── backend/
│   ├── agent.py
│   ├── database.py
│   ├── main.py
│   ├── tools.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
├── README.md
└── LICENSE
```

---

## Agent Tools

EduPilot currently uses three core tools.

### `get_students()`

Retrieves the Grade 8 student dataset containing:

* Student ID
* Name
* Grade
* Attendance
* Average grade
* Missing assignments

### `create_intervention()`

Creates and saves an intervention for a student.

The tool also checks for an existing active intervention to prevent duplicates.

### `verify_intervention()`

Checks that an intervention exists and confirms its saved status.

---

## API

The FastAPI backend exposes several endpoints.

### Health

```text
GET /health
```

Returns the API health status.

### Students

```text
GET /students
```

Returns student data.

### Interventions

```text
GET /interventions
```

Returns intervention history.

### Analyze

```text
POST /analyze
```

Sends a request to the EduPilot agent.

Example:

```json
{
  "message": "Check Grade 8 students and identify students who need academic support."
}
```

### Demo Intervention

```text
POST /demo-intervention
```

Creates a demonstration intervention for a high-risk student and verifies it.

---

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/Iram-Khaliq/edupilot-ai.git
cd edupilot-ai
```

### 2. Create a Python virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install backend dependencies

```powershell
pip install -r backend/requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key
```

Do not commit the `.env` file to GitHub.

### 5. Initialize the database

```powershell
python backend/database.py
```

### 6. Start the backend

From the project root:

```powershell
python -m uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### 7. Start the frontend

Open another PowerShell terminal:

```powershell
cd frontend
npm install
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

## Dashboard

The EduPilot dashboard provides:

* Total student count
* High-risk student count
* Medium-risk student count
* Students doing well
* Student risk overview
* Risk evidence
* AI analysis results
* Intervention history
* Verified intervention status
* Agent workflow visualization

---

## Example Agent Result

For a Grade 8 analysis, EduPilot can identify:

```text
Hassan — High Priority
Attendance: 68%
Average Grade: 52%
Missing Assignments: 7

Ali — High Priority
Attendance: 72%
Average Grade: 58%
Missing Assignments: 5

Ahmed — Medium Priority
Attendance: 81%
Average Grade: 64%
Missing Assignments: 3
```

It then creates and verifies intervention records for those students.

Students performing well, such as Sara and Fatima, do not receive unnecessary interventions.

---

## Design Principles

### Action over conversation

EduPilot is designed to perform useful work rather than simply answer questions.

### Evidence-based intervention

Intervention decisions are based on actual student data.

### No unnecessary interventions

Students who are performing well are not given interventions.

### Duplicate protection

Existing active interventions are detected before creating another one.

### Verification

The agent verifies that an intervention was successfully saved.

### Transparent reasoning

The dashboard displays the underlying attendance, grade, and missing-assignment indicators that support the risk classification.

---

## Architecture

```text
                    ┌─────────────────────┐
                    │      React UI       │
                    │  Student Dashboard  │
                    └──────────┬──────────┘
                               │
                               │ HTTP
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │       Backend       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Strands Agent     │
                    │     EduPilot AI     │
                    └──────────┬──────────┘
                               │
                    ┌──────────┼──────────┐
                    │          │          │
                    ▼          ▼          ▼
             get_students   create_     verify_
                            intervention intervention
                    │          │          │
                    └──────────┼──────────┘
                               ▼
                    ┌─────────────────────┐
                    │    SQLite Database  │
                    │                     │
                    │ Students            │
                    │ Interventions       │
                    └─────────────────────┘
```

---

## Hackathon

EduPilot AI was developed for the **Agents for Humans Hackathon**.

The project targets the **Good Neighbor Agents** track by applying agentic AI to a community need: helping schools identify students who may need support and take timely intervention actions.

The project uses the **Strands Agents SDK** as the agent framework.

---

## Future Improvements

Potential future extensions include:

* Parent/guardian communication workflows
* Teacher notifications
* More student data sources
* Assignment-level analysis
* Intervention outcome tracking
* Historical student-risk trends
* Multi-grade support
* School-wide analytics
* Additional intervention strategies

These are future directions and are not currently represented as implemented features.

---

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

## Project Goal

EduPilot AI aims to help schools move from:

**Reactive support**

to

**Early, evidence-based intervention.**

By combining student data, agentic reasoning, real actions, and verification, EduPilot turns school performance signals into an actionable support workflow.
