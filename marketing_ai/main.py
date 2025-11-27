import json
import pandas as pd
from pathlib import Path
from core.fetcher import fetch_all_plants
from core.cleaner import harmonize_all
from core.analyzer import calculate_kpis, extract_keywords, save_summary, save_keywords
import os

def main():
    ## Récupération des données
    queries = ["Monstera deliciosa", "Ficus lyrata"]
    data = fetch_all_plants(queries)
    os.makedirs("marketing_ai/data/raw", exist_ok=True)
    os.makedirs("marketing_ai/data/processed", exist_ok=True)
    with open("marketing_ai/data/raw/all_plants.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    ## Nettoyage des données
    raw_file = Path("marketing_ai/data/raw/all_plants.json")
    if raw_file.exists():
        with open(raw_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        df = harmonize_all(raw_data)
        df.to_json("marketing_ai/data/processed/plant_catalog.json", orient="records", force_ascii=False, indent=2)
        print("Catalogue nettoyé et harmonisé enregistré dans marketing_ai/data/processed/plant_catalog.json")
    else:
        print("Fichier marketing_ai/data/raw/all_plants.json introuvable.")
    
    ## Analyse des données nettoyées
    processed_file = Path("marketing_ai/data/processed/plant_catalog.json")
    df = pd.read_json(processed_file)
    kpis = calculate_kpis(df)
    df_keywords = extract_keywords(df, column='common_name', top_n=50)
    save_summary(kpis, output_file=Path("marketing_ai/reports/summary.json"))
    save_keywords(df_keywords, output_file=Path("marketing_ai/reports/keywords.csv"))

if __name__ == "__main__":
    main()