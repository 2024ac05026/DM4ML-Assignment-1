from src.feature_store.get_features import (
    get_user_features,
    get_item_features,
    get_user_item_features
)

def demo_feature_retrieval():
    print("=== Feature Store Demo (Version v1) ===\n")

    # -------------------------------
    # User-level feature retrieval
    # -------------------------------
    user_id = "U1"
    print(f"User Features for user_id = {user_id}")
    user_features = get_user_features(user_id, version="v1")
    print(user_features, "\n")

    # -------------------------------
    # Item-level feature retrieval
    # -------------------------------
    product_id = 3
    print(f"Item Features for product_id = {product_id}")
    item_features = get_item_features(product_id, version="v1")
    print(item_features, "\n")

    # -------------------------------
    # User-Item feature retrieval
    # -------------------------------
    print(
        f"User-Item Features for user_id = {user_id}, product_id = {product_id}"
    )
    user_item_features = get_user_item_features(
        user_id, product_id, version="v1"
    )
    print(user_item_features)


if __name__ == "__main__":
    demo_feature_retrieval()
