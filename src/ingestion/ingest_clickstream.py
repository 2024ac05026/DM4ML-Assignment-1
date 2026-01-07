import shutil
from datetime import datetime
from pathlib import Path
from src.utils.logger import get_logger
from src.utils.config_loader import load_paths

paths = load_paths()

LOG_FILE = Path(paths["logs"]) / "ingestion.log"
logger = get_logger("clickstream_ingestion", LOG_FILE)

RAW_DATA_PATH = Path(paths["raw"]) / "clickstream"
SOURCE_FILE = Path(paths["source_files"]) / "clickstream.csv"


def ingest_clickstream():
    try:
        logger.info("Starting clickstream ingestion")

        today = datetime.now()
        target_dir = RAW_DATA_PATH / today.strftime("%Y/%m/%d")
        target_dir.mkdir(parents=True, exist_ok=True)

        target_file = target_dir / "clickstream.csv"
        shutil.copy(SOURCE_FILE, target_file)

        logger.info(f"Clickstream data ingested successfully at {target_file}")

    except Exception as e:
        logger.error(f"Clickstream ingestion failed: {e}")
        raise


if __name__ == "__main__":
    ingest_clickstream()
