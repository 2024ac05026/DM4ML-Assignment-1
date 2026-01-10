import json
import time
from datetime import datetime
from pathlib import Path

import requests

from src.utils.logger import get_logger
from src.utils.config_loader import load_paths

paths = load_paths()

LOG_FILE = Path(paths["logs"]) / "ingestion.log"
logger = get_logger("product_ingestion", LOG_FILE)

RAW_DATA_PATH = Path(paths["raw"]) / "products"
PRODUCTS_API_URL = "https://fakestoreapi.com/products"


def ingest_products(retries=3, timeout=10):
    attempt = 0

    while attempt < retries:
        try:
            logger.info("Starting product API ingestion")

            response = requests.get(PRODUCTS_API_URL, timeout=timeout)
            response.raise_for_status()

            products = response.json()

            today = datetime.now()
            target_dir = RAW_DATA_PATH / today.strftime("%Y/%m/%d")
            target_dir.mkdir(parents=True, exist_ok=True)

            target_file = target_dir / "products.json"
            with open(target_file, "w") as f:
                json.dump(products, f, indent=2)

            logger.info(
                f"Product data ingested successfully from API at {target_file}"
            )
            return

        except Exception as e:
            attempt += 1
            logger.error(f"Attempt {attempt} failed: {e}")
            time.sleep(2)

    logger.error("Product ingestion failed after retries")
    raise RuntimeError("Product ingestion failed")


if __name__ == "__main__":
    ingest_products()
