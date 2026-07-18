import json
from pathlib import Path

def save_json_file(data, directory, filename):
    # salva um dicionário python como json no diretório especificado
    output_dir = Path(directory)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = output_dir / filename
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4,
        )