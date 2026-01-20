import pickle
import pandas as pd
import mlflow
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import LabelEncoder
from sqlalchemy import create_engine

from src.utils.config_loader import load_db_config

MODEL_PATH = "src/models/svd_model.pkl"

db = load_db_config()["postgres"]
DB_URL = (
    f"postgresql://{db['user']}:{db['password']}"
    f"@{db['host']}:{db['port']}/{db['database']}"
)
engine = create_engine(DB_URL)


def main():
    df = pd.read_sql("SELECT * FROM user_item_features", engine)

    user_enc = LabelEncoder()
    item_enc = LabelEncoder()

    df["user_idx"] = user_enc.fit_transform(df["user_id"])
    df["item_idx"] = item_enc.fit_transform(df["product_id"])

    interaction_matrix = df.pivot_table(
        index="user_idx",
        columns="item_idx",
        values="total_interaction_score",
        fill_value=0
    )

    svd = TruncatedSVD(n_components=10, random_state=42)

    with mlflow.start_run():
        mlflow.log_param("model", "TruncatedSVD")
        mlflow.log_param("n_components", 10)
        mlflow.log_param("training_source", "postgres:user_item_features")

        user_factors = svd.fit_transform(interaction_matrix)

        with open(MODEL_PATH, "wb") as f:
            pickle.dump(
                {
                    "model": svd,
                    "user_encoder": user_enc,
                    "item_encoder": item_enc,
                    "interaction_matrix": interaction_matrix
                },
                f
            )

        mlflow.log_artifact(MODEL_PATH)
        print("Model trained and saved successfully")


if __name__ == "__main__":
    main()
