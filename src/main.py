import logging
from datetime import date

from src.ingestion.extract import extract_api_data
from src.transformation.transform import transform_data
from src.transformation.validation import print_validation_report, save_validated_data
from src.loading.postgres import load_data

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    TARGET_DATE = date.today().isoformat() # formato: '2026-07-20'
    
    # ingestão (salva em data/raw com a data de hoje)
    logging.info("Step 1/5: Extracting data from API...")
    extract_api_data()
    
    # transformação (lê dados de uma pasta específica em data/raw)
    logging.info(f"Step 2/5: Transforming raw data for date: {TARGET_DATE}")
    transformed_data = transform_data(TARGET_DATE)
    
    # valida e mostra o resumo no console
    logging.info("Step 3/5: Showing validation summary...")
    print_validation_report(transformed_data)
    
    # salva em data/processed
    logging.info(f"Step 4/5: Saving validated data for date: {TARGET_DATE}")
    save_validated_data(transformed_data, TARGET_DATE)

    # carrega os dados no PostgreSQL
    logging.info(f"Step 5/5: Loading data into PostgreSQL for date: {TARGET_DATE}")
    load_data(TARGET_DATE)

    logging.info("Pipeline completed successfully.")

if __name__ == "__main__":
    main()