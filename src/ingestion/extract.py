import time
import logging
from pathlib import Path
from datetime import date

from src.config import settings
from src.utils.storage import save_json_file
from src.ingestion.api_client import get_top_anime

def extract_api_data():

    today = date.today().isoformat()

    # criar pasta para o dia atual dentro de RAW_DATA_DIR
    output_dir = Path(settings.RAW_DATA_DIR) / today

    # criar a pasta se não existir
    output_dir.mkdir(parents=True, exist_ok=True)

    page = 1

    logging.info("Starting top anime extraction")

    # enquanto existir página:
    while True:
        try:
            logging.info(f"Fetching page {page}")

            # chamar API
            data = get_top_anime(page)

            # salvar JSON recebido usando o storage
            save_json_file(
            data=data, 
            directory=output_dir, 
            filename=f"top_anime_page_{page}.json"
            )

            logging.info(
                f"Saved page {page} with {len(data['data'])} records"
            )

            # verificar se existe próxima página; senão, parar
            if not data['pagination']['has_next_page']:
                break

            if page >= settings.MAX_PAGES:
                logging.info(f"Reached maximum page limit of {settings.MAX_PAGES}. Stopping extraction.")
                break

            # evita exceder o limite de requisições da API
            time.sleep(settings.REQUEST_DELAY)

            page += 1

         # tratar exceções e registrar erros
        except Exception:
            logging.exception("Error during extraction")
            break

    logging.info("Extraction completed")