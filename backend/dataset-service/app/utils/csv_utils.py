import pandas as pd


def get_csv_metadata(file_path: str):
    df = pd.read_csv(file_path, low_memory=False)
    columns = df.columns.tolist()
    data_types = []
    for dtype in df.dtypes:
        data_types.append(str(dtype.name))

    num_rows = int(df.shape[0])
    return columns, data_types, num_rows