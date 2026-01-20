import pandas as pd
from sqlalchemy import create_engine

from src.utils.config_loader import load_db_config
from src.feature_store.registry import FEATURE_REGISTRY

db = load_db_config()["postgres"]

DB_URL = (
    f"postgresql://{db['user']}:{db['password']}"
    f"@{db['host']}:{db['port']}/{db['database']}"
)

engine = create_engine(DB_URL)


def get_user_features(user_id, version="v1"):
    table = FEATURE_REGISTRY[version]["user_features"]["source"]
    query = f"SELECT * FROM {table} WHERE user_id = %(user_id)s"
    return pd.read_sql(query, engine, params={"user_id": user_id})


def get_item_features(product_id, version="v1"):
    table = FEATURE_REGISTRY[version]["item_features"]["source"]
    query = f"SELECT * FROM {table} WHERE product_id = %(product_id)s"
    return pd.read_sql(query, engine, params={"product_id": product_id})


def get_user_item_features(user_id, product_id, version="v1"):
    table = FEATURE_REGISTRY[version]["user_item_features"]["source"]
    query = (
        f"SELECT * FROM {table} "
        f"WHERE user_id = %(user_id)s AND product_id = %(product_id)s"
    )
    return pd.read_sql(
        query,
        engine,
        params={"user_id": user_id, "product_id": product_id},
    )
