import os
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from .build_dataset import build_dataset


def train_model():
    # Load dataset from SQL / generator
    X, y = build_dataset()                                  # build dataset(): SQL joins, Feature Engineering, Encoding, Feature/Target Seperation

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(  
        X,
        y,
        test_size=0.25,                                     
        random_state=42,
        stratify=y
    )

    # Finalized baseline model
    model = LogisticRegression(max_iter=1000)

    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Evaluation
    print("Model evaluation metrics:")
    print(f"Accuracy : {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"Recall   : {recall_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"F1-score : {f1_score(y_test, y_pred, zero_division=0):.4f}")

    # Save model
    os.makedirs("models", exist_ok=True)                        
    joblib.dump(model, "models/logistic_regression_model.pkl")

    print("Model saved to models/logistic_regression_model.pkl")


if __name__ == "__main__":
    train_model()
