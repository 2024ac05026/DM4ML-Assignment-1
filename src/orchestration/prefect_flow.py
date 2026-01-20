from prefect import flow, task, get_run_logger
import subprocess
import sys
from pathlib import Path
import logging
from prefect.logging import get_logger as get_prefect_logger

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "pipeline.log"

# Create file handler
file_handler = logging.FileHandler(LOG_FILE, mode="a")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
)

# Attach handler to Prefect loggers
prefect_logger = logging.getLogger("prefect")
prefect_logger.setLevel(logging.INFO)
prefect_logger.addHandler(file_handler)

# (Optional) Also attach to root so subprocess logs are captured
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(file_handler)


@task(retries=1, retry_delay_seconds=60)
def ingest_clickstream():
    logger = get_run_logger()
    subprocess.run(
        [sys.executable, "-m", "src.ingestion.ingest_clickstream"],
        check=True
    )
    logger.info("Clickstream ingestion completed")


@task(retries=1, retry_delay_seconds=60)
def ingest_products():
    logger = get_run_logger()
    subprocess.run(
        [sys.executable, "-m", "src.ingestion.ingest_products_api"],
        check=True
    )
    logger.info("Product ingestion completed")


@task
def validate_data():
    logger = get_run_logger()
    subprocess.run(
        [sys.executable, "-m", "src.validation.validate_data"],
        check=True
    )
    logger.info("Data validation completed")


@task
def prepare_data():
    logger = get_run_logger()
    subprocess.run(
        [sys.executable, "-m", "src.preparation.clean_and_prepare"],
        check=True
    )
    logger.info("Data preparation completed")


@task
def feature_engineering():
    logger = get_run_logger()
    subprocess.run(
        [sys.executable, "-m", "src.transformation.feature_engineering"],
        check=True
    )
    logger.info("Feature engineering completed")


@task
def feature_store_demo():
    logger = get_run_logger()
    subprocess.run(
        [sys.executable, "-m", "src.feature_store.demo_feature_retrieval"],
        check=True
    )
    logger.info("Feature store retrieval demo completed")


@task
def train_model():
    logger = get_run_logger()
    subprocess.run(
        [sys.executable, "-m", "src.models.train_model"],
        check=True
    )
    logger.info("Model training completed")


@task
def evaluate_model():
    logger = get_run_logger()
    subprocess.run(
        [sys.executable, "-m", "src.models.evaluate_model"],
        check=True
    )
    logger.info("Model evaluation completed")


@flow(name="dm4ml_recommendation_pipeline")
def recommendation_pipeline():
    ingest_clickstream()
    ingest_products()
    validate_data()
    prepare_data()
    feature_engineering()
    feature_store_demo()
    train_model()
    evaluate_model()


if __name__ == "__main__":
    recommendation_pipeline()
