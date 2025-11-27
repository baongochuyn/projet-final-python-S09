### commande pour mettre en place env windows

git clone <URL_DU_REPO>
cd projet-final-python-S09

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

### Exécution du pipeline

Pour lancer le projet :

python marketing_ai/main.py

### Structure du projet

marketing_ai/
├── main.py # Orchestration complète du pipeline
├── core/
│ ├── config.py  
│ ├── fetcher.py  
│ ├── cleaner.py  
│ ├── analyzer.py  
│ ├── features.py  
│ ├── model.py  
│ ├── recommender.py  
│ └── viz.py  
├── data/
│ ├── raw/  
│ ├── processed/  
│ └── models/  
├── figs/  
├── logs/  
├── reports/  
└── README.md

### Le projet utilise 3 APIs gratuites fournissant des descriptions de plantes :

- Perenual – https://perenual.com

- Trefle – https://trefle.io

- API GBIF – https://api.gbif.org
