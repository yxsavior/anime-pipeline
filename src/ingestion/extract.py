import json
import time
import logging
from src.config import settings
from src.ingestion.api_client import get_top_anime
from datetime import date
from pathlib import Path

def extract_top_anime():

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

            # salvar JSON recebido
            save_raw_data(data, page, output_dir)

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


def save_raw_data(data, page, output_dir):
    # definir o caminho do arquivo JSON a ser salvo, incluindo o diretório RAW_DATA_DIR e o nome do arquivo com base na página atual
    file_path = output_dir / f"top_anime_page_{page}.json"

    # salvar JSON recebido
    with open(
        # define o caminho do arquivo JSON a ser salvo, incluindo o diretório RAW_DATA_DIR e o nome do arquivo com base na página atual
        file_path, "w", encoding="utf-8"
    ) as f:
        json.dump(
            data, # salva o conteúdo do dicionário data no arquivo JSON
            f, # define o arquivo de destino para salvar o JSON
            ensure_ascii=False, # garante que os caracteres especiais sejam preservados no arquivo JSON
            indent=4, # formata o JSON com indentação de 4 espaços para melhor legibilidade
        )

# logica de extração de dados da API de top anime
#começar extração
# criar pasta raw
# enquanto existir página:
#     página = 1
#     chamar API
#     salvar JSON recebido
#     verificar se existe próxima página
#     se não existir:
#         parar
#     esperar alguns segundos
#     página += 1
# terminar
