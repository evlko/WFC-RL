import json
import os

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.discriminant_analysis import StandardScaler


class Evaluator:
    @staticmethod
    def load_metadata(folder_path: str) -> pd.DataFrame:
        meta_data = []
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".json"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "r") as f:
                    data = json.load(f)
                    meta = data.get("meta", {})
                    meta["file_name"] = file_name
                    meta_data.append(meta)

        df = pd.DataFrame(meta_data)
        return df

    @staticmethod
    def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
        numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns
        scaler = StandardScaler()
        df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
        return df

    @staticmethod
    def cluster_data(num_clusters: int = 3) -> pd.DataFrame:
        pass
