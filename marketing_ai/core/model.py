# core/model.py
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
from scipy.sparse import load_npz, spmatrix
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from typing import Dict, Any, List
from core.config import RANDOM_STATE, K_CLUSTERS, MODELS_DIR


def load_features(features_path: Path, vectorizer_path: Path) -> tuple[spmatrix, Any]:
    try:
        X = load_npz(features_path)
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        print(f"Features loaded: X shape={X.shape}")
        return X, vectorizer
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Required file not found for ML: {e}")

def train_kmeans_clustering(X: spmatrix) -> KMeans:
   
    kmeans = KMeans(
        n_clusters=K_CLUSTERS, 
        random_state=RANDOM_STATE, 
        n_init=10
    )
    
    # train
    kmeans.fit(X)
    return kmeans

def evaluate_clustering(X: spmatrix, model: KMeans) -> float:
    
    if X.shape[0] <= K_CLUSTERS or K_CLUSTERS < 2:
         return 0.0
         
    # Calcul Silhouette Score
    score = silhouette_score(X, model.labels_)
    print(f"Silhouette Score (K={model.n_clusters}): {score:.4f}")
    return score

def get_top_cluster_terms(model: KMeans, vectorizer: TfidfVectorizer, top_n: int = 10) -> List[Dict[str, Any]]:

    center_matrix = model.cluster_centers_ 
    
    feature_names = vectorizer.get_feature_names_out()
    
    cluster_reports = []

    for i in range(model.n_clusters):
        center_vector = center_matrix[i, :]
        top_indices = center_vector.argsort()[:-top_n - 1:-1]
        
        top_terms = []
        for index in top_indices:
            term = feature_names[index]
            weight = center_vector[index]
            top_terms.append({"term": term, "weight": round(weight, 4)})
        
        cluster_reports.append({
            "cluster_id": i,
            "size": int(np.sum(model.labels_ == i)),
            "top_terms": top_terms
        })
        
    return cluster_reports

def save_model(model: KMeans, output_path: Path):
    output_path.parent.mkdir(exist_ok=True, parents=True)
    with open(output_path, 'wb') as f:
        pickle.dump(model, f)

def run_ml_pipeline(features_path: Path, vectorizer_path: Path) -> Dict[str, Any]:
    X, vectorizer = load_features(features_path, vectorizer_path)
    model = train_kmeans_clustering(X)
    
    # evaluate
    silhouette = evaluate_clustering(X, model)
    
    # analyse
    cluster_analysis = get_top_cluster_terms(model, vectorizer)
    
    save_model(model, MODELS_DIR / "model.pkl")
    
    return {
        "ml_task": "Clustering (KMeans)",
        "k_clusters": model.n_clusters,
        "silhouette_score": round(silhouette, 4),
        "cluster_analysis": cluster_analysis
    }