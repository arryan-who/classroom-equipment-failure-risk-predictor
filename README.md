# Classroom Equipment Failure Risk Predictor

This project builds a production-ready machine learning pipeline to predict the risk of classroom equipment failure in a university setting.

## Objectives
- Store operational data in a SQL database
- Train and evaluate traditional ML models
- Provide a dashboard for analysis and predictions
- Support periodic model retraining
- Maintain reproducibility and version control

## Tech Stack
- Python
- SQLite
- scikit-learn
- Streamlit

## Repository Structure
data/        - SQL database created via scripts (not committed)
scripts/     - Data generation, training, retraining scripts
models/      - Serialized models (ignored in git)
dashboard/   - Interactive Streamlit dashboard
