import sqlite3
import random
from datetime import datetime

DB_PATH = "data/equipment_failure.db"

def generate_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert classrooms
    
    classrooms = [
        ("Block A", 1, 60),
        ("Block A", 2, 80),
        ("Block B", 1, 50),
        ("Block B", 3, 100),
        ("Block C", 2, 120),
    ]

    cursor.executemany("""
        INSERT INTO classrooms (building, floor, capacity)          
        VALUES (?, ?, ?)
    """, classrooms)

    # Insert equipments

    equipment_types = ["Projector", "Microphone", "Smart Board", "Air Conditioner"]     
    brands = ["BrandX", "BrandY", "BrandZ"]                                 # Different brands can have varying reliability, which can influence failure rates

    equipment_records = []
    current_year = datetime.now().year

    for classroom_id in range(1, len(classrooms) + 1):
        for _ in range(3):                                                  # 3 equipment per classroom
            equipment_records.append((
                classroom_id,
                random.choice(equipment_types),         
                random.randint(current_year - 12, current_year - 1),
                random.choice(brands)
            ))

    cursor.executemany("""
        INSERT INTO equipment (classroom_id, equipment_type, installation_year, brand)
        VALUES (?, ?, ?, ?)
    """, equipment_records)

    equipment_ids = [row[0] for row in cursor.execute("SELECT equipment_id FROM equipment")] # Get all equipment IDs for usage, maintenance & failure logic

    # Usage, maintenance & failure logic

    for eq_id in equipment_ids:
        hours_used = random.uniform(5, 45)                                  # Average weekly usage hours
        semester_phase = random.choice(["Start", "Mid", "End"])             # Semester phase can influence usage patterns
        maintenance_gap = random.randint(1, 24)                             # Months since last maintenance
        maintenance_type = random.choice(["Preventive", "Corrective"])      # Type of last maintenance

        cursor.execute("""
            INSERT INTO usage_logs (equipment_id, hours_used_per_week, semester_phase)
            VALUES (?, ?, ?)
        """, (eq_id, hours_used, semester_phase))                           # Log usage patterns which can influence failure risk

        cursor.execute("""
            INSERT INTO maintenance_history (equipment_id, last_maintenance_months, maintenance_type)
            VALUES (?, ?, ?)
        """, (eq_id, maintenance_gap, maintenance_type))                    # Log maintenance history which is a critical factor in failure prediction

        # Failure probability (interpretable)
        
        failure_probability = 0.08                                          # Base failure probability

        if hours_used > 30:     
            failure_probability += 0.2  
        if maintenance_gap > 12:                                            # Longer gap since last maintenance increases failure risk         
            failure_probability += 0.2  
        if maintenance_type == "Corrective":                                # Corrective maintenance indicates a previous failure, increasing future failure risk
            failure_probability += 0.15  

        # ACs fail more frequently under stress
        cursor.execute("SELECT equipment_type FROM equipment WHERE equipment_id = ?", (eq_id,))
        eq_type = cursor.fetchone()[0]

        if eq_type == "Air Conditioner":                                    # ACs are more sensitive to environmental factors and usage patterns, leading to higher failure rates under stress
            failure_probability += 0.15 

        failure_occurred = 1 if random.random() < failure_probability else 0  # Simulate failure occurrence based on calculated probability

        cursor.execute("""
            INSERT INTO failure_events (equipment_id, failure_occurred, semester)
            VALUES (?, ?, ?)
        """, (eq_id, failure_occurred, random.randint(1, 8)))               # Log failure events with semester information for potential temporal analysis

    conn.commit()
    conn.close()

    print("Synthetic data generated successfully.")

if __name__ == "__main__":
    generate_data()
