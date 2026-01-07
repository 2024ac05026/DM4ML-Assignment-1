import json
import time
from datetime import datetime
from pathlib import Path
from src.utils.logger import get_logger

LOG_FILE = "logs/ingestion.log"
logger = get_logger("product_ingestion", LOG_FILE)

RAW_DATA_PATH = Path("data/raw/products")
MOCK_API_FILE = Path("data/source_files/products.json")  # simulated API


def ingest_products(retries=3):
    attempt = 0

    while attempt < retries:
        try:
            logger.info("Starting product API ingestion")

            with open(MOCK_API_FILE, "r") as f:
                products = json.load(f)

            today = datetime.now()
            target_dir = RAW_DATA_PATH / today.strftime("%Y/%m/%d")
            target_dir.mkdir(parents=True, exist_ok=True)

            target_file = target_dir / "products.json"
            with open(target_file, "w") as f:
                json.dump(products, f, indent=2)

            logger.info(f"Product data ingested successfully at {target_file}")
            return

        except Exception as e:
            attempt += 1
            logger.error(f"Attempt {attempt} failed: {e}")
            time.sleep(2)

    logger.error("Product ingestion failed after retries")
    raise RuntimeError("Product ingestion failed")


if __name__ == "__main__":
    ingest_products()
