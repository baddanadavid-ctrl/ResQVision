
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

    conn.commit()
    conn.close()


# Add new incident
def add_incident(
    title,
    disaster_type,
    location,
    description,
    affected_people,
    severity
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
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        disaster_type,
        location,
        description,
        affected_people,
        severity,
        "Pending",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
