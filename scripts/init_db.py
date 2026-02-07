import sqlite3
import os

DB_PATH = "data/equipment_failure.db"

def initialize_database():
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Classroom information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classrooms (
            classroom_id INTEGER PRIMARY KEY,
            building TEXT NOT NULL,
            floor INTEGER,
            capacity INTEGER
        );
    """)

    # Equipment installed in classrooms
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            equipment_id INTEGER PRIMARY KEY,
            classroom_id INTEGER,
            equipment_type TEXT,
            installation_year INTEGER,
            brand TEXT,
            FOREIGN KEY (classroom_id) REFERENCES classrooms(classroom_id)
        );
    """)

    # Weekly usage logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_logs (
            usage_id INTEGER PRIMARY KEY,
            equipment_id INTEGER,
            hours_used_per_week REAL,
            semester_phase TEXT,
            FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
        );
    """)

    # Maintenance history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenance_history (
            maintenance_id INTEGER PRIMARY KEY,
            equipment_id INTEGER,
            last_maintenance_months INTEGER,
            maintenance_type TEXT,
            FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
        );
    """)

    # Failure events (target label)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS failure_events (
            failure_id INTEGER PRIMARY KEY,
            equipment_id INTEGER,
            failure_occurred INTEGER,
            semester INTEGER,
            FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
        );
    """)

    conn.commit()
    conn.close()

    print("Database schema created successfully.")

if __name__ == "__main__":
    initialize_database()
