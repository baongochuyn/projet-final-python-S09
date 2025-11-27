# fetcher.py
import requests
import logging
from . import config
from pattern.LoggerSingleton import LoggerSingleton

logger = LoggerSingleton()

# ------------------ TREFLE ------------------ #
def fetch_trefle_plants(query: str, page: int = 1) -> dict:
    """Récupère les plantes Trefle selon un nom ou mot-clé"""
    
    params = {
        "token": config.TREFLE_TOKEN,
        "q": query,
        "page": page
    }
    resp = requests.get(config.TREFLE_BASE_URL, params=params)
    resp.raise_for_status()
    logger.log(f"Trefle: {query} récupéré avec succès")
    return resp.json()

# ------------------ PERENUAL ------------------ #
def fetch_perenual_species_list(query: str = None, page: int = 1) -> dict:
    """Liste des espèces Perenual, filtrées par query"""
    url = f"{config.PERENUAL_BASE_URL}/species-list"
    params = {"key": config.PERENUAL_KEY, "page": page}
    if query:
        params["q"] = query
    resp = requests.get(url, params=params)
    resp.raise_for_status()

    logger.log(f"Perenual liste: {query if query else 'toutes'} récupérée")
    return resp.json()


# def fetch_perenual_species_details(species_id: int) -> dict:
    """Récupère les détails d'une espèce Perenual"""
 #   url = f"{config.PERENUAL_BASE_URL}/species/details/{species_id}"
 #   params = {"key": config.PERENUAL_KEY}
 #   resp = requests.get(url, params=params)
 #   resp.raise_for_status()
 #   logger.log(f"Perenual détails: espèce {species_id} récupérée")
 #   return resp.json()

# ------------------ GBIF ------------------ #
def fetch_gbif_species_occurrence(scientific_name: str, limit: int = 50) -> dict:
    """Récupère les occurrences GBIF pour une espèce scientifique"""
    params = {"scientificName": scientific_name, "limit": limit}
    resp = requests.get(config.GBIF_BASE_URL, params=params)
    resp.raise_for_status()
    logger.log(f"GBIF occurrences: {scientific_name} récupéré")
    return resp.json()

# ------------------ FETCH ALL ------------------ #
def fetch_all_plants(query_list: list):
    """Récupère toutes les données des 3 APIs pour une liste de plantes"""
    all_data = {"trefle": [], "perenual": [], "gbif": []}
    
    for query in query_list:
        # Trefle
        try:
            trefle_data = fetch_trefle_plants(query)
            all_data["trefle"].append(trefle_data)
        except Exception as e:
            print(f"Erreur Trefle pour {query}: {e}")
            logger.log(f"Erreur Trefle pour {query}: {e}")
        
        # Perenual
        try:
            perenual_list = fetch_perenual_species_list(query)
            all_data["perenual"].append(perenual_list)
            if perenual_list["data"]:
                species_id = perenual_list["data"][0]["id"]
                # details = fetch_perenual_species_details(species_id)
                # all_data["perenual"].append(details)
        except Exception as e:
            print(f"Erreur Perenual pour {query}: {e}")
            logger.log(f"Erreur Perenual pour {query}: {e}")
        
        # GBIF
        try:
            gbif_data = fetch_gbif_species_occurrence(query)
            all_data["gbif"].append(gbif_data)
        except Exception as e:
            print(f"Erreur GBIF pour {query}: {e}")
            logger.log(f"Erreur GBIF pour {query}: {e}")
    
    return all_data
