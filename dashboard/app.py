import streamlit as st
import pandas as pd
import joblib
import numpy as np
from pathlib import Path
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(
    page_title="Classroom Equipment Failure Risk Dashboard",
    layout="wide"
)

DATA_PATH = Path("experiments/equipment_failure_dataset.csv")
MODEL_PATHS = {
    "Logistic Regression": Path("models/logistic_regression_model.pkl"),
    "Decision Tree": Path("models/decision_tree_model.pkl"),
    "Random Forest": Path("models/random_forest_model.pkl"),
}

FEATURES = [
    "equipment_age",
    "days_since_last_maintenance",
    "room_temperature",
    "humidity",
    "power_fluctuations",
    "dust_level"
]

TARGET = "failure_occurred"

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

# -------------------------
# LOAD MODELS
# -------------------------
models = {}
for name, path in MODEL_PATHS.items():
    if path.exists():
        models[name] = joblib.load(path)

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to",
    ["Data Summary & EDA", "Model Comparison", "Prediction Demo"]
)

# =========================
# SECTION 1: EDA
# =========================
if section == "Data Summary & EDA":
    st.title("📊 Data Summary & Exploratory Analysis")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Failure Distribution")
        st.bar_chart(df[TARGET].value_counts())

    with col2:
        st.subheader("Equipment Age Distribution")
        st.bar_chart(df["equipment_age"].value_counts().sort_index())

    st.subheader("Failure Rate vs Equipment Age")
    failure_by_age = (
        df.groupby("equipment_age")[TARGET]
        .mean()
        .reset_index()
        .rename(columns={TARGET: "failure_rate"})
    )
    st.line_chart(failure_by_age.set_index("equipment_age"))

    st.info(
        "Observation: The dataset is imbalanced, with fewer failure cases. "
        "This motivates evaluating models using Precision, Recall, and F1-score "
        "instead of accuracy alone."
    )

# =========================
# SECTION 2: MODEL COMPARISON
# =========================
elif section == "Model Comparison":
    st.title("📈 Model Comparison")

    X = df[FEATURES]
    y = df[TARGET]

    results = []

    for name, model in models.items():
        y_pred = model.predict(X)

        results.append({
            "Model": name,
            "Accuracy": accuracy_score(y, y_pred),
            "Precision": precision_score(y, y_pred, zero_division=0),
            "Recall": recall_score(y, y_pred, zero_division=0),
            "F1 Score": f1_score(y, y_pred, zero_division=0)
        })

    results_df = pd.DataFrame(results).set_index("Model")
    st.dataframe(results_df.style.format("{:.3f}"))

    st.success(
        "Logistic Regression provides the best balance between interpretability "
        "and performance on this dataset, making it suitable for deployment in "
        "a university setting."
    )

# =========================
# SECTION 3: PREDICTION DEMO
# =========================
else:
    st.title("🔮 Failure Risk Prediction Demo")

    model_name = st.selectbox(
        "Select Model",
        list(models.keys())
    )
    model = models[model_name]

    st.subheader("Input Equipment Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        equipment_age = st.number_input("Equipment Age (years)", 0, 50, 5)
        maintenance_days = st.number_input("Days Since Last Maintenance", 0, 365, 60)

    with col2:
        temperature = st.number_input("Room Temperature (°C)", 10.0, 40.0, 27.0)
        humidity = st.number_input("Humidity (%)", 20.0, 90.0, 60.0)

    with col3:
        power_fluctuations = st.number_input("Power Fluctuations / Month", 0, 30, 5)
        dust_level = st.number_input("Dust Level (0–10)", 0.0, 10.0, 5.0)

    if st.button("Predict Failure Risk"):
        input_df = pd.DataFrame([[
            equipment_age,
            maintenance_days,
            temperature,
            humidity,
            power_fluctuations,
            dust_level
        ]], columns=FEATURES)

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]

        if prediction == 1:
            st.error(f"⚠️ Failure Risk Detected (Probability: {probability:.2%})")
        else:
            st.success(f"✅ Low Failure Risk (Probability: {probability:.2%})")

