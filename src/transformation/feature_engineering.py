import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
from src.utils.config_loader import load_paths, load_db_config

paths = load_paths()

PROCESSED_FILE = Path(paths["processed"]) / "prepared_interactions.csv"

paths = load_paths()
db = load_db_config()["postgres"]

DB_URL = (
    f"postgresql://{db['user']}:{db['password']}"
    f"@{db['host']}:{db['port']}/{db['database']}"
)

engine = create_engine(DB_URL)


def load_data():
    return pd.read_csv(PROCESSED_FILE)


def generate_user_features(df):
    return (
        df.groupby("user_id")
        .agg(
            total_interactions=("event_score", "count"),
            avg_interaction_score=("event_score", "mean")
        )
        .reset_index()
    )


def generate_item_features(df):
    return (
        df.groupby("product_id")
        .agg(
            total_interactions=("event_score", "count"),
            avg_interaction_score=("event_score", "mean"),
            avg_rating=("rating.rate", "mean")
        )
        .reset_index()
    )


def generate_user_item_features(df):
    return (
        df.groupby(["user_id", "product_id"])
        .agg(
            interaction_count=("event_score", "count"),
            total_interaction_score=("event_score", "sum")
        )
        .reset_index()
    )


def write_to_db(df, table_name):
    df.to_sql(table_name, engine, if_exists="replace", index=False)


if __name__ == "__main__":
    df = load_data()

    user_features = generate_user_features(df)
    item_features = generate_item_features(df)
    user_item_features = generate_user_item_features(df)

    write_to_db(user_features, "user_features")
    write_to_db(item_features, "item_features")
    write_to_db(user_item_features, "user_item_features")

    print("Feature tables successfully created in PostgreSQL")
