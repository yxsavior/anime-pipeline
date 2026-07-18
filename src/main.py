import logging

from src.ingestion.extract import extract_api_data
from src.transformation.transform import transform_data
from src.transformation.validation import print_validation_report, save_validated_data

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    TARGET_DATE = '2026-07-18'
    
    # ingestão (salva em data/raw com a data de hoje)
    logging.info("Step 1: Extracting data from API...")
    # extract_api_data()
    
    # transformação (lê dados de uma pasta específica em data/raw)
    logging.info(f"Step 2: Transforming raw data for date: {TARGET_DATE}")
    transformed_data = transform_data(TARGET_DATE)
    
    # valida e mostra o resumo no console
    logging.info("Step 3: Showing validation summary...")
    print_validation_report(transformed_data)
    
    # salva em data/processed
    logging.info(f"Step 4: Saving validated data for date: {TARGET_DATE}")
    save_validated_data(transformed_data, TARGET_DATE)

    logging.info(f"Pipeline completed successfully.")

if __name__ == "__main__":
    main()