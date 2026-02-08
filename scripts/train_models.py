import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from scripts.build_dataset import build_dataset


def evaluate_model(name, model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    return {
        "model": name,
        "accuracy": accuracy_score(y_test, preds),
        "precision": precision_score(y_test, preds, zero_division=0),
        "recall": recall_score(y_test, preds, zero_division=0),
        "f1_score": f1_score(y_test, preds, zero_division=0)
    }


def train_and_compare():
    X, y = build_dataset()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    results = []

    results.append(
        evaluate_model(
            "Logistic Regression",
            LogisticRegression(max_iter=1000),
            X_train, X_test, y_train, y_test
        )
    )

    results.append(
        evaluate_model(
            "Decision Tree",
            DecisionTreeClassifier(random_state=42),
            X_train, X_test, y_train, y_test
        )
    )

    results.append(
        evaluate_model(
            "Random Forest",
            RandomForestClassifier(n_estimators=100, random_state=42),
            X_train, X_test, y_train, y_test
        )
    )

    results_df = pd.DataFrame(results)
    print("\nModel Comparison:\n")
    print(results_df)

    return results_df


if __name__ == "__main__":
    train_and_compare()
