from sklearn.ensemble import (
    RandomForestRegressor,
    RandomForestClassifier,
    ExtraTreesRegressor,
    ExtraTreesClassifier
)
from sklearn.linear_model import Ridge, LogisticRegression

models = {
    "linear": {
        "regression": Ridge(),
        "classification": LogisticRegression(),
    },
    "random_forest": {
        "regression": RandomForestRegressor(),
        "classification": RandomForestClassifier(),
    },
    "extra_trees": {
        "regression": ExtraTreesRegressor(),
        "classification": ExtraTreesClassifier(),
    },
}