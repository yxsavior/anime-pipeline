import logging
from src.ingestion.extract import extract_top_anime
from src.transformation.transform import transform
from src.transformation.validation import validation_summary

def main():
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    )

    date = '2026-07-03'
    extract_top_anime()
    transformed_data = transform(date)
    validation_summary(transformed_data)

if __name__ == "__main__":
    main()