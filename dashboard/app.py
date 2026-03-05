import streamlit as st
import pandas as pd
import joblib
import numpy as np
from pathlib import Path
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# CONFIG

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


#FEATURES = [
#    "equipment_age",
#    "days_since_last_maintenance",
#    "room_temperature",
#    "humidity",
#    "power_fluctuations",
#    "dust_level"
#]


TARGET = "failure_occurred"


# LOAD DATA

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()


# LOAD MODELS

models = {}
for name, path in MODEL_PATHS.items():
    if path.exists():
        models[name] = joblib.load(path)


# SIDEBAR

st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to",
    ["Data Summary & EDA", "Model Comparison", "Prediction Demo"]
)


# SECTION 1: EDA

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


# SECTION 2: MODEL COMPARISON

elif section == "Model Comparison":
    st.title("📈 Model Comparison")

    st.markdown(
        "This section evaluates trained models on the full dataset using "
        "the same feature schema they were trained on."
    )

    results = []

    for name, model in models.items():
        # feature names from trained models
        model_features = list(model.feature_names_in_)

        # Align dataset to model featuresp
        X = df[model_features]
        y = df[TARGET]

        # Predict
        y_pred = model.predict(X)

        # Compute metrics
        results.append({
            "Model": name,
            "Accuracy": accuracy_score(y, y_pred),
            "Precision": precision_score(y, y_pred, zero_division=0),
            "Recall": recall_score(y, y_pred, zero_division=0),
            "F1 Score": f1_score(y, y_pred, zero_division=0)
        })

    results_df = (
        pd.DataFrame(results)
        .set_index("Model")
        .style.format("{:.3f}")
    )

    st.dataframe(results_df)

    st.success(
        "All models are evaluated using their respective trained feature schemas, "
        "ensuring a fair and valid comparison."
    )

    st.info(
        "Note: Metrics are computed on the full dataset for comparative analysis. "
        "Train–test evaluation is performed during model training."
    )



# SECTION 3: PREDICTION DEMO

else:
    st.title("💡 Failure Risk Prediction Demo")

    # Select model
    model_name = st.selectbox(
        "Select Model",
        list(models.keys())
    )
    model = models[model_name]

    # feature names from trained model
    FEATURES = list(model.feature_names_in_)

    st.subheader("Input Equipment Details")

    col1, col2, col3 = st.columns(3)

    # COLUMN 1 
    with col1:
        equipment_age = st.number_input(
            "Equipment Age (years)",
            min_value=0,
            max_value=12,
            value=5
        )

        capacity = st.number_input(
            "Classroom Capacity",
            min_value=10,
            max_value=300,
            value=60
        )

    # COLUMN 2
    with col2:
        hours_used_per_week = st.number_input(
            "Hours Used Per Week",
            min_value=0,
            max_value=168,
            value=20
        )

        last_maintenance_months = st.number_input(
            "Months Since Last Maintenance",
            min_value=0,
            max_value=36,
            value=6
        )

    # COLUMN 3
    with col3:
        maintenance_type_label = st.selectbox(
            "Maintenance Type",
            ["Preventive", "Corrective"]
        )

        maintenance_type = 1 if maintenance_type_label == "Corrective" else 0

        equipment_type = st.selectbox(
            "Equipment Type",
            ["Projector", "Microphone", "Smart Board", "Air Conditioner"]
        )

    # One-hot encode equipment type
    equipment_type_features = {
        "equipment_type_Microphone": 0,
        "equipment_type_Projector": 0,
        "equipment_type_Smart Board": 0,
    }

    if equipment_type in ["Microphone", "Projector", "Smart Board"]:
        equipment_type_features[f"equipment_type_{equipment_type}"] = 1
    # Air Conditioner is the dropped reference category

    # Build input dataframe 
    input_data = {
        "equipment_age": equipment_age,
        "capacity": capacity,
        "hours_used_per_week": hours_used_per_week,
        "last_maintenance_months": last_maintenance_months,
        "maintenance_type": maintenance_type,
    }

    input_data.update(equipment_type_features)

    input_df = pd.DataFrame([input_data])

    # Ensure correct column order and presence
    input_df = input_df[FEATURES]

    # Prediction
    if st.button("Predict Failure Risk"):
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]

        if prediction == 1:
            st.error(
                f"⚠️ Failure Risk Detected\n\n"
                f"Predicted Probability: {probability:.2%}"
            )
        else:
            st.success(
                f"✅ Low Failure Risk\n\n"
                f"Predicted Probability: {probability:.2%}"
            )

        st.info(
            "Note: This prediction demo uses the feature schema of the trained "
            "baseline model. Environmental features are planned for integration "
            "in the next phase."
        )


