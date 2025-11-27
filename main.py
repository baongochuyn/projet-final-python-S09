import json
from pathlib import Path
from rapport.fetcher import fetch_all_plants
from rapport.cleaner import harmonize_all

def main():
    queries = ["Monstera deliciosa", "Ficus lyrata"]
    data = fetch_all_plants(queries)
    with open("data/raw/all_plants.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    raw_file = Path("data/raw/all_plants.json")
    if raw_file.exists():
        with open(raw_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        df = harmonize_all(raw_data)
        df.to_json("data/processed/plant_catalog.json", orient="records", force_ascii=False, indent=2)
        print("Catalogue nettoyé et harmonisé enregistré dans data/processed/plant_catalog.json")
    else:
        print("Fichier raw/all_plants.json introuvable.")

if __name__ == "__main__":
    main()