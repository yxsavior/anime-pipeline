import logging
from src.ingestion.extract import extract_top_anime


def main():
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    )

    extract_top_anime()


if __name__ == "__main__":
    main()