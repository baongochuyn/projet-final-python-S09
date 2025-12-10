# core/features.py
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path
import pickle
from scipy.sparse import save_npz, spmatrix
from core.config import NGRAM_RANGE, PROCESSED_DIR, MODELS_DIR

def create_features(df: pd.DataFrame, text_column: str = 'scientific_name') -> tuple[spmatrix, TfidfVectorizer]:
   
    corpus = df[text_column].fillna("").astype(str).tolist()
    vectorizer = TfidfVectorizer(
        ngram_range=NGRAM_RANGE,
        token_pattern=r'\b\w+\b' 
    )
    
    X = vectorizer.fit_transform(corpus)    
    return X, vectorizer


def save_features(X: spmatrix, vectorizer: TfidfVectorizer, output_models_dir: Path = MODELS_DIR):
    
    output_models_dir.mkdir(exist_ok=True, parents=True)
    features_dir = output_models_dir.parent / "processed" # data/processed
    features_dir.mkdir(exist_ok=True, parents=True)
    
    vectorizer_path = output_models_dir / "vectorizer.pkl"
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)

    features_path = features_dir / "features.npz"
    save_npz(features_path, X)
