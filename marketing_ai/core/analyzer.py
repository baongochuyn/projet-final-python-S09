import pandas as pd
from collections import Counter
import json
import re
from pathlib import Path


def calculate_kpis(df: pd.DataFrame) -> dict:
    """Calcule les KPIs principaux sur le dataset nettoyé"""
    kpis = {'total_documents': len(df)}

    # Longueur moyenne des noms scientifiques et communs
    if 'scientific_name' in df.columns:
        kpis['avg_scientific_name_length'] = df['scientific_name'].str.split().apply(len).mean()
    if 'common_name' in df.columns:
        kpis['avg_common_name_length'] = df['common_name'].str.split().apply(len).mean()

    # Nombre de sources uniques
    if 'source' in df.columns:
        kpis['unique_sources'] = df['source'].nunique()
        kpis['top_sources'] = df['source'].value_counts().head(5).to_dict()

    return kpis


def extract_keywords(df: pd.DataFrame, column: str = 'common_name', top_n: int = 50) -> pd.DataFrame:
    """Extrait les mots-clés depuis une colonne texte"""
    if column not in df.columns:
        raise ValueError(f"Colonne '{column}' inexistante dans le DataFrame.")

    text = " ".join(df[column].dropna().astype(str).tolist()).lower()

    text = re.sub(r"[^\w\s]", "", text)

    words = text.split()
    stopwords = {"for", "the", "and", "of", "a", "an", "in", "on", "with"}
    words = [w for w in words if w not in stopwords]

    counter = Counter(words)
    most_common = counter.most_common(top_n)
    return pd.DataFrame(most_common, columns=['keyword', 'frequency'])


def save_summary(kpis: dict, output_file: Path):
    output_file.parent.mkdir(exist_ok=True, parents=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(kpis, f, ensure_ascii=False, indent=2)
    print(f"Summary saved to {output_file}")


def save_keywords(df_keywords: pd.DataFrame, output_file: Path):
    output_file.parent.mkdir(exist_ok=True, parents=True)
    df_keywords.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Keywords saved to {output_file}")


def main(processed_file: str = "marketing_ai/data/processed/plant_catalog.json"):
    df = pd.read_json(processed_file)

    kpis = calculate_kpis(df)
    df_keywords = extract_keywords(df, column='common_name', top_n=50)

    save_summary(kpis, output_file=Path("marketing_ai/reports/summary.json"))
    save_keywords(df_keywords, output_file=Path("marketing_ai/reports/keywords.csv"))


if __name__ == "__main__":
    main()
