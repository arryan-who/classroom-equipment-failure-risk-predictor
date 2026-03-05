import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = "data/equipment_failure.db"

def build_dataset():
    conn = sqlite3.connect(DB_PATH)                                             # Connect to the SQLite database containing the raw data

    query = """
        SELECT
            e.equipment_id,                                                     
            e.equipment_type,                                                   
            (strftime('%Y', 'now') - e.installation_year) AS equipment_age,     
            c.capacity,                                                         
            u.hours_used_per_week,                                                                       
            m.last_maintenance_months,                                             
            m.maintenance_type,                                                 
            f.failure_occurred                                                  
        FROM equipment e
        JOIN classrooms c ON e.classroom_id = c.classroom_id                    
        JOIN usage_logs u ON e.equipment_id = u.equipment_id                    
        JOIN maintenance_history m ON e.equipment_id = m.equipment_id           
        JOIN failure_events f ON e.equipment_id = f.equipment_id                
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Encode categorical variables
    
    df["maintenance_type"] = df["maintenance_type"].map({                       # Encode maintenance type as binary (0 for Preventive, 1 for Corrective) to capture the increased failure risk associated with corrective maintenance
        "Preventive": 0,
        "Corrective": 1
    })                                                      

    df = pd.get_dummies(df, columns=["equipment_type"], drop_first=True)        # One-hot encode equipment type to allow models to learn different failure patterns associated with different equipment types

    X = df.drop(columns=["failure_occurred", "equipment_id"])                   # Feature matrix excluding target and identifier columns
    y = df["failure_occurred"]                                                  # Target vector indicating failure occurrence

    return X, y                                                                 # Return feature matrix and target vector

if __name__ == "__main__":                                                      # Test the dataset building function
    X, y = build_dataset()                                                      # Build the dataset
    print("Feature matrix shape:", X.shape)                                     # Print the shape of the feature matrix
    print("Target vector shape:", y.shape)                                      # Print the shape of the target vector


