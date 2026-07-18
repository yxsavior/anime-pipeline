from pathlib import Path

from src.config import settings
from src.utils.storage import save_json_file

"""Bloco de validações seguindo a lógica de validação de dados do validation.ipynb.
Cada função é responsável por validar um aspecto específico dos dados transformados."""

# validação de campos obrigatórios de animes, gêneros, temas e estúdios
def validate_required_fields(table_name, transformed_data, validation_results, required_field):
    for record in transformed_data.get(table_name, []):
        if record.get('mal_id') is None or record.get(required_field) is None:
            validation_results['required_fields'][table_name]['invalids'].append(record)

# validação de duplicados (garantir que chaves naturais não aparecem duas vezes em animes)
def validate_duplicates(transformed_data, validation_results):
    anime_ids = set()
    for anime in transformed_data.get('animes', []):
        if anime['mal_id'] not in anime_ids:
            anime_ids.add(anime['mal_id'])
        else:
            validation_results['duplicates']['animes']['invalids'].append(anime)

# popular IDs únicos no set (necessária para validação de relacionamentos)
def populate_unique_ids(key, transformed_data):
    id_set = set()
    for record in transformed_data.get(key, []):
        if 'mal_id' in record:
            id_set.add(record['mal_id'])
    return id_set

# validação de atributos de anime (score, episodes, year e scored_by)
def validate_attribute(attribute_name, transformed_data, validation_rule, validation_results):
    for anime in transformed_data.get('animes', []):
        if anime.get(attribute_name) is not None and not validation_rule(anime[attribute_name]):
            validation_results['attributes'][attribute_name]['invalids'].append(anime)

# validação de relacionamentos (integridade referencial)
def validate_relationships(table, key, transformed_data, validation_results, anime_ids, related_ids):
    for relationship in transformed_data.get(table, []):
        if relationship.get('anime_mal_id') not in anime_ids or relationship.get(key) not in related_ids:
            validation_results['relationships'][table]['invalids'].append(relationship)

# -------------------------------------------------------------------------------------------------------------------------

"""Bloco da função principal de validação. Orquestra todas as validações acima."""
def validate(transformed_data):
    validation_results = {
        "required_fields": {
            'animes': {'total': len(transformed_data.get('animes', [])), 'invalids': []},
            'genres': {'total': len(transformed_data.get('genres', [])), 'invalids': []},
            'themes': {'total': len(transformed_data.get('themes', [])), 'invalids': []},
            'studios': {'total': len(transformed_data.get('studios', [])), 'invalids': []}
        },
        "duplicates": {
            "animes": {'total': len(transformed_data.get('animes', [])), 'invalids': []}
        },
        "relationships": {
            'anime_genres': {'total': len(transformed_data.get('anime_genres', [])), 'invalids': []},
            'anime_themes': {'total': len(transformed_data.get('anime_themes', [])), 'invalids': []},
            'anime_studios': {'total': len(transformed_data.get('anime_studios', [])), 'invalids': []}
        },
        "attributes": {
            'score': {'total': len(transformed_data.get('animes', [])), 'invalids': []},
            'episodes': {'total': len(transformed_data.get('animes', [])), 'invalids': []},
            'year': {'total': len(transformed_data.get('animes', [])), 'invalids': []},
            'scored_by': {'total': len(transformed_data.get('animes', [])), 'invalids': []}   
        }
    }

    # validações de campos obrigatórios
    validate_required_fields('animes', transformed_data, validation_results, 'title')
    validate_required_fields('genres', transformed_data, validation_results, 'name')
    validate_required_fields('themes', transformed_data, validation_results, 'name')
    validate_required_fields('studios', transformed_data, validation_results, 'name')

    # validação de duplicados em animes
    validate_duplicates(transformed_data, validation_results)

    # coleta dos IDs únicos pra usar nas validações de relacionamentos
    anime_ids = populate_unique_ids('animes', transformed_data)
    genre_ids = populate_unique_ids('genres', transformed_data)
    theme_ids = populate_unique_ids('themes', transformed_data)
    studio_ids = populate_unique_ids('studios', transformed_data)

    # validações de relacionamentos
    validate_relationships('anime_genres', 'genre_mal_id', transformed_data, validation_results, anime_ids, genre_ids)
    validate_relationships('anime_themes', 'theme_mal_id', transformed_data, validation_results, anime_ids, theme_ids)
    validate_relationships('anime_studios', 'studio_mal_id', transformed_data, validation_results, anime_ids, studio_ids)

    # validações de atributos usando as expressões lambdas em vez de funções separadas
    validate_attribute('score', transformed_data, lambda x: 0 <= x <= 10, validation_results)
    validate_attribute('episodes', transformed_data, lambda x: x >= 0, validation_results)
    validate_attribute('year', transformed_data, lambda x: 1960 <= x < 2027, validation_results)
    validate_attribute('scored_by', transformed_data, lambda x: x >= 0, validation_results)

    return validation_results

# -------------------------------------------------------------------------------------------------------------------------
"""Bloco de resumo dos resultados de validação.
Imprime no console o total de registros e o total de registros inválidos por chave."""
def print_validation_report(transformed_data):
    validation_results = validate(transformed_data)
    for key, data in validation_results.items():
        print(f"\nKey: {key}")
        print(f"{'Table':<15} | {'Total':<5} | {'Invalids'}")

        for table_name, table_data in data.items():
            total = table_data.get('total', 0)
            invalids = len(table_data.get('invalids', []))
            print(f"{table_name.upper():<15} | {total:<5} | {invalids}")

    if len(validation_results['duplicates']['animes']['invalids']) > 0:
        print("\nDuplicates found:")
        for anime in validation_results['duplicates']['animes']['invalids']:
            print(f"mal_id: {anime['mal_id']} | Title: {anime['title']}")

# -------------------------------------------------------------------------------------------------------------------------      
"""Salva os dados prontos pro PostgreSQL em data/processed."""
def save_validated_data(transformed_data, date):
    output_dir = Path(settings.PROCESSED_DATA_DIR) / date
    
    for table_name, records in transformed_data.items():
        save_json_file(
            data=records,
            directory=output_dir,
            filename=f"{table_name}.json"
        )