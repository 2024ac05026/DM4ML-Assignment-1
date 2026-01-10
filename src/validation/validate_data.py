import json
import pandas as pd
from pathlib import Path
from src.utils.config_loader import load_paths
from src.utils.logger import get_logger

paths = load_paths()

LOG_FILE = Path(paths["logs"]) / "validation.log"
logger = get_logger("data_validation", LOG_FILE)

RAW_PATH = Path(paths["raw"])
VALIDATED_PATH = Path(paths["validated"])


def validate_clickstream():
    logger.info("Starting clickstream data validation")

    files = RAW_PATH.glob("clickstream/*/*/*/clickstream.csv")
    reports = []

    for file in files:
        df = pd.read_csv(file)

        report = {
            "file": str(file),
            "rows": len(df),
            "missing_values": df.isnull().sum().to_dict(),
            "duplicates": int(df.duplicated().sum()),
            "invalid_events": int(~df["event_type"].isin(["view", "click", "add_to_cart"]).sum()),
            "invalid_devices": int(~df["device"].isin(["web", "mobile"]).sum())
        }

        reports.append(report)

    logger.info("Clickstream validation completed")
    return reports


def validate_products():
    logger.info("Starting product data validation")

    files = RAW_PATH.glob("products/*/*/*/products.json")
    reports = []

    for file in files:
        with open(file, "r") as f:
            data = json.load(f)

        df = pd.json_normalize(data)

        report = {
            "file": str(file),
            "rows": len(df),
            "missing_values": df[["id", "title", "price", "category"]].isnull().sum().to_dict(),
            "duplicate_product_ids": int(df["id"].duplicated().sum()),
            "invalid_price": int((df["price"] <= 0).sum()),
            "invalid_rating": int(
                (~df["rating.rate"].between(1, 5, inclusive="both")).sum()
            )
        }

        reports.append(report)

    logger.info("Product validation completed")
    return reports


if __name__ == "__main__":
    clickstream_report = validate_clickstream()
    product_report = validate_products()

    print("Clickstream Validation Report:")
    for r in clickstream_report:
        print(r)

    print("\nProduct Validation Report:")
    for r in product_report:
        print(r)
