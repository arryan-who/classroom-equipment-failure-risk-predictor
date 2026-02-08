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

## Model Comparison & Selection

Three traditional machine learning models were evaluated:
- Logistic Regression
- Decision Tree
- Random Forest

Models were compared using Accuracy, Precision, Recall, and F1-score.
Logistic Regression showed the best balance between predictive performance and interpretability and was selected as the deployment model.

## Evaluation Metrics

Model performance was evaluated using:
- Accuracy
- Precision
- Recall
- F1-score

These metrics provide a balanced understanding of failure prediction performance, especially in cases of class imbalance.

## Maintenance & Retraining Plan

The system is designed to support periodic retraining as new equipment usage and maintenance data becomes available.
Synthetic data generation allows testing of retraining workflows during development.
Model retraining and dashboard updates are planned as part of the end-term implementation.
