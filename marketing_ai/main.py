import json
import pandas as pd
from pathlib import Path
from core.fetcher import fetch_all_plants
from core.cleaner import harmonize_all
from core.analyzer import calculate_kpis, extract_keywords, save_summary, save_keywords
import os
from core.features import create_features, save_features
from core.config import MODELS_DIR
import logging
from core.model import run_ml_pipeline
from core.viz import run_visualization_pipeline

def main():
    ## Récupération des données
    queries = ["Monstera deliciosa", "Ficus lyrata"]
    data = fetch_all_plants(queries)
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    with open("data/raw/all_plants.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    ## Nettoyage des données
    raw_file = Path("data/raw/all_plants.json")
    if raw_file.exists():
        with open(raw_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        df = harmonize_all(raw_data)
        df.to_json("data/processed/plant_catalog.json", orient="records", force_ascii=False, indent=2)
        print("Catalogue nettoyé et harmonisé enregistré dans data/processed/plant_catalog.json")
    else:
        print("Fichier data/raw/all_plants.json introuvable.")
    
    ## Analyse des données nettoyées
    processed_file = Path("data/processed/plant_catalog.json")
    df = pd.read_json(processed_file)
    kpis = calculate_kpis(df)
    df_keywords = extract_keywords(df, column='common_name', top_n=50)
    save_summary(kpis, output_file=Path("reports/summary.json"))
    save_keywords(df_keywords, output_file=Path("reports/keywords.csv"))

    ## Feature Engineering (TF-IDF)
    TEXT_COLUMN = 'scientific_name' 
    X_features, vectorizer = create_features(df, text_column=TEXT_COLUMN)
    
    # Save Features và Vectorizer
    save_features(X_features, vectorizer, output_models_dir=Path(MODELS_DIR))
    
    ## Machine Learning (ML - Clustering)
    summary_path = Path("reports/summary.json")
    features_path = Path("data/processed/features.npz")
    vectorizer_path = Path("data/models/vectorizer.pkl")
    keywords_path = Path("reports/keywords.csv")
    ml_results = run_ml_pipeline(features_path, vectorizer_path)

    with open(summary_path, "r", encoding="utf-8") as f:
        summary = json.load(f)

    summary.update({
        "ml_metrics": {
            "task": ml_results['ml_task'],
            "k_clusters": ml_results['k_clusters'],
            "silhouette_score": ml_results['silhouette_score']
        },
        "ml_interpretation": ml_results['cluster_analysis']
    })
    save_summary(summary, output_file=summary_path)

    ## Data Visualization
    run_visualization_pipeline(raw_file, summary_path, keywords_path)
    
    print("\nPipeline finished.")
if __name__ == "__main__":
    main()