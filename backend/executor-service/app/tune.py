from sklearn.metrics import root_mean_squared_error, accuracy_score
from sklearn.model_selection import cross_val_score, train_test_split

from app.machine_learning import models
import pandas as pd
import json
from ray import tune, train
from app.train import evaluate_holdout, evaluate_cv


def build_search_space(params_config: str):
    config = json.loads(params_config)
    num_trials = config.get("num_trials", 10)
    params = {k: v for k, v in config.items() if k != "num_trials"}
    search_space = {}
    for key, value in params.items():
        if value[0] == "int":
            search_space[key] = tune.randint(value[1], value[2])
        elif value[0] == "float":
            search_space[key] = tune.uniform(value[1], value[2])
        elif value[0] == "choice":
            search_space[key] = tune.choice(value[1:])
    return search_space, num_trials


def tune_params(file_path, task, dataset):
    print(f"[INFO]  executor-service: Start tuning model ...")

    if dataset["problem_type"] == "REGRESSION":
        problem_type = "regression"
        scoring = "neg_mean_squared_error"
    else:
        problem_type = "classification"
        scoring = "accuracy"

    request_models = task["model_names"][0]
    model_object = models[request_models][problem_type]

    num_rows = dataset["num_rows"]
    target_column = dataset["target_column"]

    search_space, num_trials = build_search_space(task["model_params"][0])

    # Load the dataset
    df = pd.read_csv(file_path)

    X = df.drop(target_column, axis=1)
    y = df[target_column]

    evaluate_method = "holdout"
    if num_rows <= 700:
        evaluate_method = "cv"

    if evaluate_method == "holdout":
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    def fitness(config):
        model_object.set_params(**config)
        if evaluate_method == "cv":
            cv_scores = cross_val_score(model_object, X, y, cv=5, scoring=scoring)
            mean_score = cv_scores.mean()
            train.report({"score": mean_score})
        if evaluate_method == "holdout":
            model_object.fit(X_train, y_train)
            y_pred = model_object.predict(X_test)
            if dataset["problem_type"] == "REGRESSION":
                score = -root_mean_squared_error(y_test, y_pred)
            else:
                score = accuracy_score(y_test, y_pred)
            train.report({"score": score})

    analysis = tune.run(
        fitness,
        config=search_space,
        num_samples=num_trials,
        metric="score",
        mode="max",
        resources_per_trial={"cpu": 2},
        verbose=False,
    )

    best_trial = analysis.get_best_trial("score", "max", "last")
    best_score = best_trial.metric_analysis["score"]["max"]
    best_config = best_trial.config

    best_model = models[request_models][problem_type]
    best_model.set_params(**best_config)
    if evaluate_method == "holdout":
        best_model.fit(X_train, y_train)
        y_pred = best_model.predict(X_test)
        evaluated_score = evaluate_holdout(best_model, y_test.to_numpy(), y_pred, problem_type=dataset["problem_type"])
    elif evaluate_method == "cv":
        evaluated_score, y_test, y_pred = evaluate_cv(best_model, X, y, problem_type=dataset["problem_type"])


    trials = analysis.trials
    history = []
    for t in trials:
        t_config = t.config
        t_score = t.last_result.get("score", 0)
        if t_score:
            history.append({
                "params": t_config,
                "score": t_score,
            })


    print(f"[INFO]  executor-service: Best model parameters: {best_config}")
    print(f"[INFO]  executor-service: Best model score: {best_score}")
    score_report = {
        "metric": scoring,
        "best_score": best_score,
        "history": history,
    }

    if not isinstance(y_pred, list):
        y_pred = y_pred.tolist()

    if not isinstance(y_test, list):
        y_test = y_test.tolist()

    return score_report, y_test, y_pred