# Classroom Equipment Failure Risk Predictor

A machine learning project that predicts the **risk of classroom equipment failure** using operational and environmental data.  
The project demonstrates a complete **end-to-end ML workflow**: data generation → feature engineering → model training → evaluation → deployment attempt.

---

## 📌 Project Overview

Educational institutions depend on classroom equipment such as projectors, smart boards, microphones, and AC systems.  
Unexpected failures disrupt lectures and increase maintenance overhead.

This project aims to **predict equipment failure risk** using historical and synthetic operational data, enabling **preventive maintenance planning**.

---

## 🎯 Objectives

- Generate realistic synthetic classroom equipment data
- Engineer operational and environmental features
- Train and compare traditional machine learning models
- Evaluate models using standard classification metrics
- Demonstrate a local deployment-ready dashboard
- Maintain clean, modular, and version-controlled code

---

## 🧠 Features Used (Aligned with CSV & Models)

The model is trained using the following features:

| Feature Name | Description |
|-------------|-------------|
| `equipment_age` | Age of the equipment (years) |
| `days_since_last_maintenance` | Days since last maintenance |
| `room_temperature` | Room temperature (°C) |
| `humidity` | Relative humidity (%) |
| `power_fluctuations` | Monthly power fluctuation count |
| `dust_level` | Dust exposure level (0–10) |
| `failure` | Target variable (0 = No failure, 1 = Failure) |

> Note: Feature schema evolution during experimentation caused inference-time mismatch in the dashboard. This is documented and scheduled for resolution in the next phase.

---

## 🗂️ Project Structure

classroom-equipment-failure-risk-predictor/
│
├── data/
│   └── equipment_failure.db        # SQLite database
│
├── experiments/
│   ├── equipment_failure_dataset.csv
│   └── model_comparison.ipynb      # EDA + model comparison
│
├── models/
│   └── logistic_regression_model.pkl
│
├── scripts/
│   ├── __init__.py
│   ├── generate_data.py            # Synthetic data generator
│   ├── build_dataset.py            # Feature construction
│   ├── export_dataset.py           # CSV export
│   ├── init_db.py                  # Database initialization
│   ├── train_model.py              # Single-model training
│   └── train_models.py             # Multi-model comparison
│
├── dashboard/
│   └── app.py                      # Streamlit dashboard (local demo)
│
├── README.md
├── requirements.txt
└── .gitignore

---

## 📊 Exploratory Data Analysis (EDA)

EDA includes:
- Failure vs non-failure distribution
- Feature-wise distributions
- Environmental impact analysis
- Maintenance interval patterns

EDA is intentionally implemented in a **Jupyter notebook** to keep the dashboard lightweight.

---

## 🖥️ Dashboard (Local Demo)

A Streamlit dashboard was implemented to demonstrate:
- Equipment failure risk prediction
- Data summary and visualizations
- Model comparison section

### Current Status
- UI and navigation render correctly
- EDA visualizations load
- Prediction currently throws a feature-schema mismatch error

### Reason
The trained model expects an earlier feature encoding version.  
This is a known **ML deployment issue (feature drift)** and is planned to be resolved via retraining.

---

## 🧪 How to Run the Project

### 1. Install Dependencies
pip install -r requirements.txt

### 2. Generate Database
python -m scripts.generate_data
python -m scripts.export_dataset

### 3. Train Models
python -m scripts.train_models

### 4. Run DashBoard
streamlit run dashboard/app.py

## 🧪 Limitations & Future Works

- Align training and inference feature schemas
- Retrain models with finalized feature set
- Add ensemble model tuning
- Enable batch CSV scoring
- Deploy dashboard on cloud (Streamlit Cloud / Azure)
