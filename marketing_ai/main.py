import json
from pathlib import Path
from core.fetcher import fetch_all_plants
from core.cleaner import harmonize_all
import os

def main():
    queries = ["Monstera deliciosa", "Ficus lyrata"]
    data = fetch_all_plants(queries)
    os.makedirs("marketing_ai/data/raw", exist_ok=True)
    os.makedirs("marketing_ai/data/processed", exist_ok=True)
    with open("marketing_ai/data/raw/all_plants.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    raw_file = Path("marketing_ai/data/raw/all_plants.json")
    if raw_file.exists():
        with open(raw_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        df = harmonize_all(raw_data)
        df.to_json("marketing_ai/data/processed/plant_catalog.json", orient="records", force_ascii=False, indent=2)
        print("Catalogue nettoyé et harmonisé enregistré dans marketing_ai/data/processed/plant_catalog.json")
    else:
        print("Fichier marketing_ai/data/raw/all_plants.json introuvable.")

if __name__ == "__main__":
    main()