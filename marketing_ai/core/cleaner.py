# core/cleaner.py
import pandas as pd
import re

def normalize_string(s):
    """Nettoyage texte : minuscule, suppression ponctuation et espaces superflus"""
    if not isinstance(s, str):
        return ""
    s = s.lower()
    s = re.sub(r"[^\w\s]", "", s)  # supprime ponctuation
    s = re.sub(r"\s+", " ", s).strip()
    return s

def extract_trefle_data(raw_trefle_list):
    """Extraire et normaliser les données Trefle"""
    plants = []
    for item in raw_trefle_list:
        data_list = item.get("data", [])
        if not isinstance(data_list, list):
            continue
        for data in data_list:
            plant = {
                "scientific_name": normalize_string(data.get("scientific_name")),
                "common_name": normalize_string(data.get("common_name")),
                "family": normalize_string(data.get("family_common_name") or data.get("family")),
                "type": "",
                "sunlight": "",
                "watering": "",
                "cycle": "",
                "source": "trefle"
            }
            plants.append(plant)
    return plants

def extract_perenual_data(raw_perenual_list):
    """Extraire et normaliser les données Perenual"""
    plants = []
    for item in raw_perenual_list:
        data = item.get("data") or item
        if isinstance(data, list):
            for d in data:
                plants.append({
                    "scientific_name": normalize_string(d.get("scientific_name")),
                    "common_name": normalize_string(d.get("common_name")),
                    "family": normalize_string(d.get("family")),
                    "type": normalize_string(d.get("plant_type")),
                    "sunlight": normalize_string(d.get("sunlight")),
                    "watering": normalize_string(d.get("watering")),
                    "cycle": normalize_string(d.get("cycle")),
                    "source": "perenual"
                })
        else:
            plants.append({
                "scientific_name": normalize_string(data.get("scientific_name")),
                "common_name": normalize_string(data.get("common_name")),
                "family": normalize_string(data.get("family")),
                "type": normalize_string(data.get("plant_type")),
                "sunlight": normalize_string(data.get("sunlight")),
                "watering": normalize_string(data.get("watering")),
                "cycle": normalize_string(data.get("cycle")),
                "source": "perenual"
            })
    return plants

def extract_gbif_data(raw_gbif_list):
    """Extraire et normaliser les données GBIF"""
    plants = []
    for item in raw_gbif_list:
        for occ in item.get("results", []):
            plants.append({
                "scientific_name": normalize_string(occ.get("species")),
                "common_name": normalize_string(occ.get("vernacularName")),
                "family": normalize_string(occ.get("family")),
                "type": "",
                "sunlight": "",
                "watering": "",
                "cycle": "",
                #"gbif_occurrence": {
                    #"country": occ.get("country"),
                    #"year": occ.get("year"),
                    #"latitude": occ.get("decimalLatitude"),
                    #"longitude": occ.get("decimalLongitude")
                #},
                "source": "gbif"
            })
    return plants

def harmonize_all(raw_data: dict) -> pd.DataFrame:
    """
    Harmonise les données des 3 sources et retourne un DataFrame unique.
    raw_data = {
        "trefle": [...],
        "perenual": [...],
        "gbif": [...]
    }
    """
    trefle_plants = extract_trefle_data(raw_data.get("trefle", []))
    perenual_plants = extract_perenual_data(raw_data.get("perenual", []))
    gbif_plants = extract_gbif_data(raw_data.get("gbif", []))
    
    all_plants = trefle_plants + perenual_plants + gbif_plants
    
    df = pd.DataFrame(all_plants)
    
    # Supprimer doublons basés sur le nom scientifique
    df = df.drop_duplicates(subset="scientific_name", keep="first").reset_index(drop=True)
    
    return df


