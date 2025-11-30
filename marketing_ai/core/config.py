from pathlib import Path

# Trefle API
TREFLE_BASE_URL = "https://trefle.io/api/v1/plants"
TREFLE_TOKEN = "usr-EAW8D4JlQTLyeqL01emc7iDRWR6IHSS09bxRubNZ0aY"

# Perenual API
PERENUAL_BASE_URL = "https://perenual.com/api/v2"
PERENUAL_KEY = "sk-8QbV6928332256cb313699"

# GBIF API
GBIF_BASE_URL = "https://api.gbif.org/v1/occurrence/search"

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
LOG_PATH ='/logs'
MODELS_DIR = Path("data/models")
FIGURES_DIR = "figs"
REPORTS_DIR = "reports"

RANDOM_STATE = 42      
NGRAM_RANGE = (1, 2)   # TfidfVectorizer: n-grams 
K_CLUSTERS = 7  
TEST_SIZE = 0.2 
TOP_K_RECO = 10