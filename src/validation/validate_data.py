import json
import pandas as pd
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet

from src.utils.config_loader import load_paths
from src.utils.logger import get_logger

paths = load_paths()

LOG_FILE = Path(paths["logs"]) / "validation.log"
REPORT_FILE = Path("reports") / "4_data_quality_report.pdf"

logger = get_logger("data_validation", LOG_FILE)
RAW_PATH = Path(paths["raw"])


def validate_clickstream():
    files = RAW_PATH.glob("clickstream/*/*/*/clickstream.csv")
    results = []

    for file in files:
        df = pd.read_csv(file)

        results.append({
            "Dataset": "Clickstream",
            "File": str(file),
            "Rows": len(df),
            "Missing Values": int(df.isnull().sum().sum()),
            "Duplicates": int(df.duplicated().sum()),
            "Invalid Events": int(~df["event_type"].isin(["view", "click", "add_to_cart"]).sum()),
            "Invalid Devices": int(~df["device"].isin(["web", "mobile"]).sum())
        })

    return results


def validate_products():
    files = RAW_PATH.glob("products/*/*/*/products.json")
    results = []

    for file in files:
        with open(file) as f:
            data = json.load(f)

        df = pd.json_normalize(data)

        results.append({
            "Dataset": "Products",
            "File": str(file),
            "Rows": len(df),
            "Missing Values": int(df[["id", "title", "price", "category"]].isnull().sum().sum()),
            "Duplicates": int(df["id"].duplicated().sum()),
            "Invalid Price": int((df["price"] <= 0).sum()),
            "Invalid Rating": int(
                (~df["rating.rate"].between(1, 5)).sum()
            )
        })

    return results


def generate_pdf(report_data):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(REPORT_FILE))
    elements = []

    elements.append(Paragraph("<b>Data Quality Report</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        "This report summarizes data profiling and validation checks "
        "performed on raw datasets.", styles["Normal"]
    ))
    elements.append(Spacer(1, 12))

    for dataset, records in report_data.items():
        elements.append(Paragraph(f"<b>{dataset} Validation Summary</b>", styles["Heading2"]))
        elements.append(Spacer(1, 8))

        if not records:
            continue

        table_data = [list(records[0].keys())]
        for r in records:
            table_data.append(list(r.values()))

        table = Table(table_data)
        elements.append(table)
        elements.append(Spacer(1, 16))

    doc.build(elements)


if __name__ == "__main__":
    logger.info("Starting data profiling and validation")

    clickstream_results = validate_clickstream()
    product_results = validate_products()

    generate_pdf({
        "Clickstream Data": clickstream_results,
        "Product Data": product_results
    })

    logger.info("Data quality report generated successfully")
    print(f"Data Quality Report generated at: {REPORT_FILE}")
