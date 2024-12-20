from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, ExtraTreesRegressor, ExtraTreesClassifier
from sklearn.linear_model import Ridge, LogisticRegression
import json

MODEL = {
    "linear": {
        "regression": json.dumps(Ridge().get_params()),
        "classification": json.dumps(LogisticRegression().get_params()),
    },
    "random_forest": {
        "regression": json.dumps(RandomForestRegressor().get_params()),
        "classification": json.dumps(RandomForestClassifier().get_params()),
    },
    "extra_trees": {
        "regression": json.dumps(ExtraTreesRegressor().get_params()),
        "classification": json.dumps(ExtraTreesClassifier().get_params()),
    },
}

