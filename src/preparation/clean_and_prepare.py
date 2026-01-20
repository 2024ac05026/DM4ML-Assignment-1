import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

from src.utils.config_loader import load_paths

paths = load_paths()

RAW_PATH = Path(paths["raw"])
PROCESSED_PATH = Path(paths["processed"])
PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
EDA_PATH = PROCESSED_PATH / "eda"
EDA_PATH.mkdir(parents=True, exist_ok=True)


def load_clickstream():
    files = RAW_PATH.glob("clickstream/*/*/*/clickstream.csv")
    return pd.concat([pd.read_csv(f) for f in files], ignore_index=True)


def load_products():
    files = RAW_PATH.glob("products/*/*/*/products.json")
    products = []
    for f in files:
        with open(f) as file:
            products.extend(json.load(file))
    return pd.json_normalize(products)


def prepare_data():
    clicks = load_clickstream()
    products = load_products()

    # Basic cleaning
    clicks.dropna(subset=["user_id", "product_id"], inplace=True)

    # Event encoding
    event_map = {"view": 1, "click": 2, "add_to_cart": 3}
    clicks["event_score"] = clicks["event_type"].map(event_map)

    # Merge
    df = clicks.merge(products, left_on="product_id", right_on="id", how="inner")

    # Encode category
    le = LabelEncoder()
    df["category_encoded"] = le.fit_transform(df["category"])

    # Normalize price
    scaler = MinMaxScaler()
    df["price_normalized"] = scaler.fit_transform(df[["price"]])

    # Timestamp features
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour

    return df


def run_eda(df):
    # Interaction distribution
    plt.figure()
    df["event_type"].value_counts().plot(kind="bar", title="Interaction Types")
    plt.tight_layout()
    plt.savefig(EDA_PATH / "interaction_distribution.png")
    plt.close()

    # Item popularity
    plt.figure()
    df["product_id"].value_counts().head(10).plot(
        kind="bar", title="Top 10 Most Interacted Products"
    )
    plt.tight_layout()
    plt.savefig(EDA_PATH / "top_products.png")
    plt.close()

    # User-item sparsity
    interaction_matrix = df.pivot_table(
        index="user_id",
        columns="product_id",
        values="event_score",
        fill_value=0
    )

    sparsity = 1.0 - (
        interaction_matrix.astype(bool).sum().sum()
        / (interaction_matrix.shape[0] * interaction_matrix.shape[1])
    )

    print(f"Sparsity of interaction matrix: {sparsity:.2f}")


if __name__ == "__main__":
    final_df = prepare_data()
    run_eda(final_df)

    output_file = PROCESSED_PATH / "prepared_interactions.csv"
    final_df.to_csv(output_file, index=False)

    print(f"Prepared dataset saved at {output_file}")
