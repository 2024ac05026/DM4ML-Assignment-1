FEATURE_REGISTRY = {
    "v1": {
        "user_features": {
            "source": "user_features",
            "features": {
                "total_interactions": "Count of user interactions",
                "avg_interaction_score": "Average interaction strength per user"
            }
        },
        "item_features": {
            "source": "item_features",
            "features": {
                "total_interactions": "Total interactions for item",
                "avg_interaction_score": "Average interaction strength for item",
                "avg_rating": "Average product rating"
            }
        },
        "user_item_features": {
            "source": "user_item_features",
            "features": {
                "interaction_count": "User-item interaction count",
                "total_interaction_score": "Cumulative interaction score"
            }
        }
    }
}
