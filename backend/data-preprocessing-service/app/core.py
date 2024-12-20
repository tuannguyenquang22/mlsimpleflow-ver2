import pandas as pd
from typing import Optional
from sklearn.preprocessing import LabelEncoder


def can_convert(series: pd.Series, from_dtype, to_dtype):
    if from_dtype == to_dtype:
        return True
    try:
        series.astype(to_dtype)
        return True
    except:
        return False


def correcting_dtype(df: pd.DataFrame, desired_dtype: Optional[dict] = None):
    message = ""
    if desired_dtype is None:
        return df, message

    for col, dtype in desired_dtype.items():
        if col in df.columns:
            if can_convert(df[col], df[col].dtype, dtype):
                df[col] = df[col].astype(dtype)
            else:
                message += f"ERROR:Column {col} cannot be converted to {dtype};"

    return df, message


def detect_problem_type(series: pd.Series):
    if series.nunique() == 2 and series.dtype == "object":
        return "BINARY"
    elif series.nunique() > 2 and series.dtype == "object":
        return "MULTICLASS"
    elif series.dtype == "int64" or series.dtype == "float64":
        return "REGRESSION"
    else:
        return "UNKNOWN"


def preprocessing_dataset(
    df: pd.DataFrame,
    target: str,
    desired_dtype: Optional[dict] = None,
    missing_cols_threshold: float = 0.8,
    missing_rows_threshold: float = 0.05,
    auto_impute: bool = True,
):
    messages = ""
    trainable = True
    df = df.copy()

    df, dtype_messages = correcting_dtype(df, desired_dtype)
    if dtype_messages:
        messages += dtype_messages
        trainable = False
        return df, messages, trainable, "UNKNOWN"

    problem_type = detect_problem_type(df[target])
    if problem_type == "UNKNOWN":
        trainable = False
        messages += f"ERROR:Cannot detect problem type for target column {target};"
        return df, messages, trainable, "UNKNOWN"

    missing_rate = df.isnull().mean()
    drop_cols = missing_rate[missing_rate >= missing_cols_threshold].index.tolist()
    if drop_cols:
        messages += "INFO:Automate dropping columns {drop_cols} with high missing values ratio;"
        df = df.drop(drop_cols, axis=1)

    medium_missing = missing_rate[(missing_rate >= missing_rows_threshold) & (missing_rate < missing_cols_threshold)].index.tolist()
    if medium_missing and not auto_impute:
        trainable = False
        for col in medium_missing:
            messages += f"ERROR:Column {col} has missing values ratio of {missing_rate[col]:.2f}, consider filling missing values with appropriate values;"

    if medium_missing and auto_impute:
        for col in medium_missing:
            if df[col].dtype == "object":
                df[col] = df[col].fillna(df[col].mode()[0])
                messages += f"INFO:Automate filling missing values with mode value for column {col};"
            else:
                df[col] = df[col].fillna(df[col].mean())
                messages += f"INFO:Automate filling missing values with mean value for column {col};"

    low_missing = missing_rate[(missing_rate < missing_rows_threshold) & (missing_rate > 0)].index.tolist()
    if low_missing:
        messages += f"INFO:Automate dropping columns {low_missing} with low missing values ratio;"
        for col in low_missing:
            df = df[~df[col].isnull()]


    constant_cols = [col for col in df.columns if df[col].nunique() == 1]
    if constant_cols:
        messages += f"INFO:Automate dropping columns {constant_cols} with constant values;"
        df = df.drop(constant_cols, axis=1)


    unique_cols = [col for col in df.columns if df[col].nunique() > 0.9 * df.shape[0]]
    if unique_cols:
        messages += f"INFO:Automate dropping columns {unique_cols} with high unique values ratio;"
        df = df.drop(unique_cols, axis=1)


    # Handle dropping duplicates
    if df.duplicated().sum() > 0:
        messages += "INFO:Automate dropping duplicated rows;"
        df = df.drop_duplicates()


    # Handle boolean features encoding
    for col in df.columns:
        if col == target:
            continue
        if df[col].dtype == "object" and df[col].nunique() == 2:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            messages += f"INFO:Automate encoding column {col} with binary values;"


    # Handle category features encoding
    for col in df.columns:
        if col == target:
            continue

        if df[col].dtype == "object" and df[col].nunique() > 2:
            # This is category features
            top_values = df[col].value_counts().index[:15]
            df[col] = df[col].apply(lambda x: x if x in top_values else "Other")
            dummies = pd.get_dummies(df[col], prefix=col)
            df = pd.concat([df.drop(columns=[col]), dummies], axis=1)
            messages += f"INFO:Automate encoding column {col} with top 15 most frequent values;"


    # Handle target encoding (for BINARY or MULTICLASS)
    if df[target].dtype == "object":
        le = LabelEncoder()
        df[target] = le.fit_transform(df[target].astype(str))
        messages += f"INFO:Automate encoding target column {target};"


    # Handle datetime feature
    for col in df.columns:
        if col == target:
            continue
        try:
            dt = pd.to_datetime(df[col], format="%Y-%m-%d", errors="raise")
            df[col+"_year"] = dt.dt.year
            df[col+"_month"] = dt.dt.month
            df[col+"_day"] = dt.dt.day
            df = df.drop(columns=[col])
            messages += f"INFO:Automate encoding column {col} with datetime values;"
        except:
            pass

    return df, messages, trainable, problem_type