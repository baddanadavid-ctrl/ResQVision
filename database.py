
import sqlite3
from pathlib import Path
from datetime import datetime

# Database file location
DB_PATH = Path(__file__).parent / "resqvision.db"


# Connect to database
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Create incident table
def init_db():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS incidents (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            disaster_type TEXT NOT NULL,

            location TEXT NOT NULL,

            description TEXT,

            affected_people INTEGER DEFAULT 0,

            severity TEXT NOT NULL,

            status TEXT DEFAULT 'Pending',

            created_at TEXT NOT NULL

        )
    """)
    columns = [
        row["name"]
        for row in conn.execute(
            "PRAGMA table_info(incidents)"
        ).fetchall()
    ]

    if "latitude" not in columns:
        conn.execute(
            "ALTER TABLE incidents ADD COLUMN latitude REAL"
        )

    if "longitude" not in columns:
        conn.execute(
            "ALTER TABLE incidents ADD COLUMN longitude REAL"
        )

    conn.execute("""
        CREATE TABLE IF NOT EXISTS rescue_teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            members INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Available'
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS rescue_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_id INTEGER NOT NULL,
            team_id INTEGER NOT NULL,
            assigned_at TEXT NOT NULL,
            status TEXT DEFAULT 'Assigned',
            FOREIGN KEY (incident_id) REFERENCES incidents(id),
            FOREIGN KEY (team_id) REFERENCES rescue_teams(id)
        )
    """)

    conn.commit()
    conn.close()


# Add new incident

def add_incident(
    title,
    disaster_type,
    location,
    description,
    affected_people,
    severity,
    latitude,
    longitude
):

    conn = get_connection()

    conn.execute("""
        INSERT INTO incidents (
            title,
            disaster_type,
            location,
            description,
            affected_people,
            severity,
            status,
            created_at,
            latitude,
            longitude
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        disaster_type,
        location,
        description,
        affected_people,
        severity,
        "Pending",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        latitude,
        longitude
    ))

    conn.commit()
    conn.close()

# Retrieve all incidents
def get_incidents():

    conn = get_connection()

    incidents = conn.execute("""
        SELECT * FROM incidents
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in incidents]


# Update incident status
def update_incident_status(incident_id, new_status):

    allowed_statuses = [
        "Pending",
        "Under Investigation",
        "Resolved"
    ]

    if new_status not in allowed_statuses:
        raise ValueError("Invalid incident status")

    conn = get_connection()

    conn.execute("""
        UPDATE incidents
        SET status = ?
        WHERE id = ?
    """, (new_status, incident_id))

    conn.commit()
    conn.close()


# Initialize database
init_db()

def add_rescue_team(team_name, specialization, members):
    conn = get_connection()

    conn.execute("""
        INSERT INTO rescue_teams
        (team_name, specialization, members, status)
        VALUES (?, ?, ?, 'Available')
    """, (team_name, specialization, members))

    conn.commit()
    conn.close()


def get_rescue_teams():
    conn = get_connection()

    teams = conn.execute(
        "SELECT * FROM rescue_teams ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return [dict(team) for team in teams]


def update_team_status(team_id, new_status):
    allowed_statuses = ["Available", "Assigned", "Unavailable"]

    if new_status not in allowed_statuses:
        raise ValueError("Invalid team status")

    conn = get_connection()

    conn.execute(
        "UPDATE rescue_teams SET status = ? WHERE id = ?",
        (new_status, team_id)
    )

    conn.commit()
    conn.close()

  
def assign_rescue_team(incident_id, team_id):
    conn = get_connection()

    try:
        conn.execute("BEGIN IMMEDIATE")

        team = conn.execute(
            "SELECT status FROM rescue_teams WHERE id = ?",
            (team_id,)
        ).fetchone()

        if team is None:
            raise ValueError("Rescue team not found.")

        if team["status"] != "Available":
            raise ValueError("This rescue team is not available.")

        existing = conn.execute(
            "SELECT id FROM rescue_assignments WHERE incident_id = ?",
            (incident_id,)
        ).fetchone()

        if existing is not None:
            raise ValueError("This incident already has an assignment.")

        conn.execute("""
            INSERT INTO rescue_assignments
            (incident_id, team_id, assigned_at, status)
            VALUES (?, ?, datetime('now'), 'Assigned')
        """, (incident_id, team_id))

        conn.execute(
            "UPDATE rescue_teams SET status = 'Assigned' WHERE id = ?",
            (team_id,)
        )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


    conn.commit()
    conn.close()


def get_rescue_assignments():
    conn = get_connection()

    assignments = conn.execute("""
        SELECT
            rescue_assignments.id,
            rescue_assignments.incident_id,
            rescue_assignments.team_id,
            rescue_assignments.assigned_at,
            rescue_assignments.status,
            incidents.title,
            incidents.location,
            incidents.severity,
            rescue_teams.team_name,
            rescue_teams.specialization
        FROM rescue_assignments
        JOIN incidents
            ON rescue_assignments.incident_id = incidents.id
        JOIN rescue_teams
            ON rescue_assignments.team_id = rescue_teams.id
        ORDER BY rescue_assignments.id DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in assignments]

def update_rescue_assignment(assignment_id, new_status):
    allowed_statuses = ["Assigned", "In Progress", "Completed"]

    if new_status not in allowed_statuses:
        raise ValueError("Invalid assignment status")

    conn = get_connection()

    assignment = conn.execute(
        "SELECT team_id FROM rescue_assignments WHERE id = ?",
        (assignment_id,)
    ).fetchone()

    if assignment is None:
        conn.close()
        raise ValueError("Assignment not found")

    conn.execute(
        "UPDATE rescue_assignments SET status = ? WHERE id = ?",
        (new_status, assignment_id)
    )

    if new_status == "Completed":
        conn.execute(
            "UPDATE rescue_teams SET status = 'Available' WHERE id = ?",
            (assignment["team_id"],)
        )

    conn.commit()
    conn.close()
