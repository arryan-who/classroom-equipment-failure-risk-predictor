import sys
import os
import pandas as pd

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))       # Ensure we can import from the project root
sys.path.insert(0, PROJECT_ROOT)                                                    # Add project root to Python path for imports

from .build_dataset import build_dataset                                            # Import the dataset building function to create the dataset from the raw SQL data

def export_dataset():                                                               # Main function to build the dataset and export it as a CSV file for use in the dashboard and model training
    X, y = build_dataset()
    df = X.copy()
    df["failure_occurred"] = y

    os.makedirs("experiments", exist_ok=True)                                       # Create experiments directory if it doesn't exist to store the exported dataset

    df.to_csv("experiments/equipment_failure_dataset.csv", index=False)             # Export the dataset to a CSV file for use in the dashboard and model training, allowing for easy access and analysis without needing to query the database directly each time
    print("Dataset exported to experiments/equipment_failure_dataset.csv")          

if __name__ == "__main__":                                  
    export_dataset()
