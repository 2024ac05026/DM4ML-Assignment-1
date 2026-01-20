import pickle
import numpy as np
import pandas as pd
import mlflow
from sqlalchemy import create_engine
from sklearn.metrics import precision_score, recall_score

from src.utils.config_loader import load_db_config

MODEL_PATH = "src/models/svd_model.pkl"

db = load_db_config()["postgres"]
DB_URL = (
    f"postgresql://{db['user']}:{db['password']}"
    f"@{db['host']}:{db['port']}/{db['database']}"
)
engine = create_engine(DB_URL)


def precision_recall_at_k(true_items, pred_items, k=5):
    pred_items = pred_items[:k]
    true_set = set(true_items)
    pred_set = set(pred_items)

    tp = len(true_set & pred_set)
    precision = tp / k if k else 0
    recall = tp / len(true_set) if true_set else 0
    return precision, recall


def main():
    with open(MODEL_PATH, "rb") as f:
        artifacts = pickle.load(f)

    svd = artifacts["model"]
    interaction_matrix = artifacts["interaction_matrix"]

    scores = svd.transform(interaction_matrix) @ svd.components_

    test_items = {}
    for user in interaction_matrix.index:
        items = interaction_matrix.loc[user][interaction_matrix.loc[user] > 0]
        if len(items) > 1:
            test_items[user] = [items.index[-1]]

    precisions, recalls = [], []

    for user, true_items in test_items.items():
        ranked_items = np.argsort(scores[user])[::-1]
        p, r = precision_recall_at_k(true_items, ranked_items)
        precisions.append(p)
        recalls.append(r)

    precision_at_5 = np.mean(precisions)
    recall_at_5 = np.mean(recalls)

    with mlflow.start_run():
        mlflow.log_metric("precision_at_5", precision_at_5)
        mlflow.log_metric("recall_at_5", recall_at_5)

    print(f"Precision@5: {precision_at_5:.4f}")
    print(f"Recall@5: {recall_at_5:.4f}")


if __name__ == "__main__":
    main()
