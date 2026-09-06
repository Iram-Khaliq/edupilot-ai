import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [students, setStudents] = useState([]);
  const [studentsLoading, setStudentsLoading] = useState(true);
  const [interventions, setInterventions] = useState([]);
  const [interventionsLoading, setInterventionsLoading] = useState(true);

  const [message, setMessage] = useState(
    "Check Grade 8 students and identify students who need academic support."
  );

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/students")
      .then((response) => response.json())
      .then((data) => {
        setStudents(Array.isArray(data) ? data : []);
        setStudentsLoading(false);
      })
      .catch(() => {
        setStudentsLoading(false);
      });

    fetch("http://127.0.0.1:8000/interventions")
      .then((response) => response.json())
      .then((data) => {
        setInterventions(Array.isArray(data) ? data : []);
        setInterventionsLoading(false);
      })
      .catch(() => {
        setInterventionsLoading(false);
      });
  }, []);

  const analyzeStudents = async () => {
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      setResult(data);

      const interventionsResponse = await fetch(
        "http://127.0.0.1:8000/interventions"
      );

      const interventionsData = await interventionsResponse.json();

      setInterventions(
        Array.isArray(interventionsData) ? interventionsData : []
      );
    } catch (error) {
      setResult({
        status: "error",
        message: "Could not connect to EduPilot API.",
      });
    }

    setLoading(false);
  };

  const formatAnalysis = (text) => {
    if (!text) return "";

    return text
      .replace(/###/g, "")
      .replace(/\*\*/g, "")
      .replace(/---/g, "")
      .replace(/`/g, "")
      .replace(/\n\s*\n\s*\n/g, "\n\n")
      .trim();
  };

  const getRisk = (student) => {
    if (
      student.attendance < 75 ||
      student.average_grade < 60 ||
      student.missing_assignments >= 5
    ) {
      return "High";
    }

    if (
      student.attendance < 85 ||
      student.average_grade < 70 ||
      student.missing_assignments >= 3
    ) {
      return "Medium";
    }

    return "Low";
  };

  const highRiskCount = students.filter(
    (student) => getRisk(student) === "High"
  ).length;

  const mediumRiskCount = students.filter(
    (student) => getRisk(student) === "Medium"
  ).length;

  const lowRiskCount = students.filter(
    (student) => getRisk(student) === "Low"
  ).length;

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>EduPilot AI</h1>
          <p>Student Support & Early Intervention Agent</p>
        </div>

        <div className="status">
          <span></span>
          AI Assistant
        </div>
      </header>

      <main className="container">
        <section className="hero">
          <h2>Student Support Dashboard</h2>
          <p>
            Identify students who may need help using attendance,
            academic performance, and assignment data.
          </p>
        </section>
<section className="workflow">
  <div className="workflow-step">
    <span>1</span>
    <strong>Investigate</strong>
    <small>Student data</small>
  </div>

  <div className="workflow-arrow">→</div>

  <div className="workflow-step">
    <span>2</span>
    <strong>Prioritize</strong>
    <small>Risk analysis</small>
  </div>

  <div className="workflow-arrow">→</div>

  <div className="workflow-step">
    <span>3</span>
    <strong>Intervene</strong>
    <small>Create action</small>
  </div>

  <div className="workflow-arrow">→</div>

  <div className="workflow-step">
    <span>4</span>
    <strong>Verify</strong>
    <small>Confirm action</small>
  </div>
</section>
        <section className="stats">
          <div className="stat-card">
            <strong>{students.length}</strong>
            <span>Total Students</span>
          </div>

          <div className="stat-card high">
            <strong>{highRiskCount}</strong>
            <span>High Risk</span>
          </div>

          <div className="stat-card medium">
            <strong>{mediumRiskCount}</strong>
            <span>Medium Risk</span>
          </div>

          <div className="stat-card low">
            <strong>{lowRiskCount}</strong>
            <span>Doing Well</span>
          </div>
        </section>

        <section className="card">
          <label>Ask EduPilot</label>

          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            rows="4"
          />

          <button onClick={analyzeStudents} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Students"}
          </button>
        </section>

        <section className="card">
          <div className="section-title">
            <div>
              <h2>Student Risk Overview</h2>
              <p>Current Grade 8 student indicators</p>
            </div>
          </div>

          <div className="student-list">
            {studentsLoading ? (
              <p>Loading students...</p>
            ) : (
              students.map((student) => (
                <div className="student-row" key={student.id}>
                  <div className="student-name">
                    <strong>{student.name}</strong>
                    <span>Student ID: {student.id}</span>
                  </div>

                  <div className="metric">
                    <span>Attendance</span>
                    <strong>{student.attendance}%</strong>
                  </div>

                  <div className="metric">
                    <span>Average Grade</span>
                    <strong>{student.average_grade}%</strong>
                  </div>

                  <div className="metric">
                    <span>Missing Work</span>
                    <strong>{student.missing_assignments}</strong>
                  </div>

                 <div>
  <div className={`risk ${getRisk(student).toLowerCase()}`}>
    {getRisk(student)}
  </div>

  <small className="risk-reason">
    {student.attendance}% attendance • {student.average_grade}% grade •{" "}
    {student.missing_assignments} missing assignments
  </small>
</div>
                </div>
              ))
            )}
          </div>
        </section>

        {result && (
          <section className="card">
            <div className="section-title">
              <div>
                <h2>Latest EduPilot Analysis</h2>
                <p>AI investigation and intervention summary</p>
              </div>
            </div>

           {result.status === "success" ? (
  <div className="analysis-result">
    <div className="analysis-badge">
      ✓ Analysis completed
    </div>

    <p>{formatAnalysis(result.result)}</p>
  </div>
) : (
              <div className="analysis-result">
                <p>{result.message}</p>
              </div>
            )}
          </section>
        )}

        <section className="card">
          <div className="section-title">
            <div>
              <h2>Intervention History</h2>
              <p>Actions created and verified by EduPilot</p>
            </div>
          </div>

          {interventionsLoading ? (
            <p>Loading interventions...</p>
          ) : interventions.length === 0 ? (
            <p>No interventions have been created yet.</p>
          ) : (
            <div className="student-list">
              {interventions.map((intervention) => (
                <div
                  className="student-row intervention-row"
                  key={intervention.id}
                >
                  <div className="student-name">
                    <strong>{intervention.student_name}</strong>
                    <span>
                      Intervention ID: {intervention.id}
                    </span>
                  </div>

                  <div className="metric">
                    <span>Priority</span>
                    <div
                      className={`risk ${intervention.priority.toLowerCase()}`}
                    >
                      {intervention.priority}
                    </div>
                  </div>

                  <div className="metric intervention-detail">
                    <span>Reason</span>
                    <strong>{intervention.reason}</strong>
                  </div>

                  <div className="metric intervention-detail">
                    <span>Action</span>
                    <strong>{intervention.action}</strong>
                  </div>

                  <div className="metric">
                    <span>Status</span>
<div className="verified-status">
  ✓ Verified
</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;