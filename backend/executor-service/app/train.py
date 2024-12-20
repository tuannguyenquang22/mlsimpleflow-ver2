from sklearn.metrics import r2_score, root_mean_squared_error, mean_absolute_error, \
    mean_absolute_percentage_error, accuracy_score, f1_score, recall_score, precision_score
from sklearn.model_selection import train_test_split, cross_val_predict, cross_validate

from app.machine_learning import models
import pandas as pd


def evaluate_holdout(model, y_test, y_pred, problem_type):
    print(f"[INFO]  executor-service: Evaluating model ...")
    if problem_type == "REGRESSION":
        return {
            "r2": float(r2_score(y_test, y_pred)),
            "rmse": float(root_mean_squared_error(y_test, y_pred)),
            "mae": float(mean_absolute_error(y_test, y_pred)),
            "mape": float(mean_absolute_percentage_error(y_test, y_pred)),
        }
    elif problem_type == "BINARY":
        return {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "f1": float(f1_score(y_test, y_pred)),
            "recall": float(recall_score(y_test, y_pred)),
            "precision": float(precision_score(y_test, y_pred)),
        }
    elif problem_type == "MULTICLASS":
        return {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "f1": float(f1_score(y_test, y_pred, average='weighted')),
            "recall": float(recall_score(y_test, y_pred, average='weighted')),
            "precision": float(precision_score(y_test, y_pred, average='weighted')),
        }



def evaluate_cv(model, X, y, problem_type):
    print(f"[INFO]  executor-service: Evaluating model using cross-validation ...")
    scoring = {}

    if problem_type == "REGRESSION":
        scoring = {
            'r2': 'r2',
            'rmse': 'neg_root_mean_squared_error',
            'mae': 'neg_mean_absolute_error',
            'mape': 'neg_mean_absolute_percentage_error'
        }
    elif problem_type == "BINARY":
        scoring = {
            'accuracy': 'accuracy',
            'f1': 'f1',
            'recall': 'recall',
            'precision': 'precision'
        }
    elif problem_type == "MULTICLASS":
        scoring = {
            'accuracy': 'accuracy',
            'f1_weighted': 'f1_weighted',
            'recall_weighted': 'recall_weighted',
            'precision_weighted': 'precision_weighted'
        }
    else:
        raise ValueError(f"Unsupported problem type: {problem_type}")

    cv_results = cross_validate(model, X, y, cv=5, scoring=scoring, return_train_score=False)
    scores = {}
    for metric in scoring.keys():
        if metric in ["rmse", "mae", "mape"]:
            scores[metric] = -cv_results[f'test_{metric}'].mean()
        else:
            scores[metric] = cv_results[f'test_{metric}'].mean()

    y_pred = cross_val_predict(model, X, y, cv=5)

    return scores, y.tolist(), y_pred.tolist()


def train(file_path, task, dataset):
    print(f"[INFO]  executor-service: Start training model ...")

    if dataset["problem_type"] == "REGRESSION":
        problem_type = "regression"
    else:
        problem_type = "classification"

    request_models = task["model_names"]
    model_objects = []
    for rm in request_models:
        model_objects.append(models[rm][problem_type])

    num_rows = dataset["num_rows"]
    target_column = dataset["target_column"]
    evaluate_method = "holdout"
    if num_rows <= 700:
        evaluate_method = "cv"

    # Read dataset
    df = pd.read_csv(file_path)

    X = df.drop(target_column, axis=1)
    y = df[target_column]

    score_report = {
        "score": []
    }

    if evaluate_method == "holdout":
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        for m in model_objects:
            m.fit(X_train, y_train)
            y_pred = m.predict(X_test)
            score_report["score"].append(evaluate_holdout(m, y_test.to_numpy(), y_pred, problem_type=dataset["problem_type"]))

    if evaluate_method == "cv":
        for m in model_objects:
            scores, y_test, y_pred = evaluate_cv(m, X, y, problem_type=dataset["problem_type"])
            score_report["score"].append(scores)

    y_test_list = y_test.tolist() if evaluate_method == "holdout" else y.tolist()
    y_pred_list = y_pred.tolist()

    return score_report, y_test_list, y_pred_list