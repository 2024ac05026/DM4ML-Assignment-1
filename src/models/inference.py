import pickle
import numpy as np

MODEL_PATH = "src/models/svd_model.pkl"


def recommend(user_id, top_k=5):
    with open(MODEL_PATH, "rb") as f:
        artifacts = pickle.load(f)

    model = artifacts["model"]
    user_enc = artifacts["user_encoder"]
    item_enc = artifacts["item_encoder"]
    interaction_matrix = artifacts["interaction_matrix"]

    user_idx = user_enc.transform([user_id])[0]
    scores = model.transform(interaction_matrix) @ model.components_

    top_items = np.argsort(scores[user_idx])[::-1][:top_k]
    return item_enc.inverse_transform(top_items)


if __name__ == "__main__":
    print("Recommendations for U1:")
    print(recommend("U1"))
