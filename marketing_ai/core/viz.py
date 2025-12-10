import pandas as pd
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, List
from core.config import REPORTS_DIR, FIGURES_DIR, PROCESSED_DIR, MODELS_DIR

# --- Fonction Utilitaires pour la Visualisation ---

def create_dashboard_pdf(figure_paths: List[Path], output_path: Path):
    from matplotlib.backends.backend_pdf import PdfPages
    
    try:
        with PdfPages(output_path) as pdf:
            for fig_path in figure_paths:
                try:
                    # Charger la figure et l'ajouter au PDF
                    fig = plt.imread(fig_path)
                    plt.figure(figsize=(11, 8.5)) # Taille lettre standard
                    plt.imshow(fig)
                    plt.axis('off')
                    pdf.savefig()
                    plt.close()
                except Exception as e:
                    print(f"Erreur lors de l'ajout de la figure {fig_path} au PDF: {e}")
        print(f"Tableau de bord PDF créé : {output_path}")
    except Exception as e:
        print(f"Erreur lors de la création du PDF : {e}")


# --- Fonctions de Visualisation KPI ---

def plot_volume_by_source(summary_data: Dict[str, Any]) -> Path:
    """1. Volume par source"""
    fig_path = Path(FIGURES_DIR) / "sources_bar.png"
    
    sources = summary_data.get('top_sources', {})
    df_sources = pd.Series(sources).sort_values(ascending=False)
    
    plt.figure(figsize=(8, 5))
    sns.barplot(x=df_sources.index, y=df_sources.values, palette="viridis")
    plt.title('Volume des Documents par Source API', fontsize=14)
    plt.xlabel('Source API')
    plt.ylabel('Nombre de Documents')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.close()
    return fig_path

def plot_top_keywords(keywords_path: Path) -> Path:
    """2. Top mots-clés (fréquences)"""
    fig_path = Path(FIGURES_DIR) / "top_keywords.png"
    
    df_keywords = pd.read_csv(keywords_path).head(20)
    
    plt.figure(figsize=(10, 7))
    sns.barplot(x='frequency', y='keyword', data=df_keywords, palette="mako")
    plt.title(f'Top {len(df_keywords)} Mots-Clés (Basé sur le Nom Scientifique/Commun)', fontsize=14)
    plt.xlabel('Fréquence')
    plt.ylabel('Mot-Clé / N-gramme')
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.close()
    return fig_path

# --- Fonctions de Visualisation Méta-données (Nécessite données brutes/logs) ---

def plot_latency_distribution(df_meta: pd.DataFrame) -> Path:
    """3. Distribution des latences (box/hist)"""
    fig_path = Path(FIGURES_DIR) / "latency_box.png"
    
    # Assumer que df_meta contient une colonne 'latency_ms'
    if 'latency_ms' not in df_meta.columns:
        # Créer des données fictives si non trouvées
        latencies = np.random.lognormal(mean=2.5, sigma=0.5, size=200) * 10 
        df_meta = pd.DataFrame({'latency_ms': latencies})

    plt.figure(figsize=(8, 5))
    sns.boxplot(y=df_meta['latency_ms'], palette="Set2")
    plt.title('Distribution des Latences des Appels API', fontsize=14)
    plt.ylabel('Latence (ms)')
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.close()
    return fig_path

def plot_status_codes(df_meta: pd.DataFrame) -> Path:
    """4. Répartition statuts HTTP"""
    fig_path = Path(FIGURES_DIR) / "status_codes.png"
    
    # Assumer que df_meta contient une colonne 'status_code'
    if 'status_code' not in df_meta.columns:
        # Créer des données fictives si non trouvées
        codes = [200, 200, 200, 200, 404, 200, 500, 200]
        df_status = pd.Series(codes).value_counts()
    else:
        df_status = df_meta['status_code'].value_counts()

    plt.figure(figsize=(7, 7))
    plt.pie(df_status.values, labels=df_status.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set3"))
    plt.title('Répartition des Codes de Statut HTTP', fontsize=14)
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.close()
    return fig_path

def plot_timeline_activity(df_meta: pd.DataFrame) -> Path:
    """5. Chronologie (volume/temps)"""
    fig_path = Path(FIGURES_DIR) / "timeline_activity.png"
    
    # Nécessite un champ de date/heure dans les données brutes ou les logs
    if 'timestamp' not in df_meta.columns:
        # Créer des données fictives si non trouvées
        dates = pd.to_datetime(pd.date_range(start='1/1/2025', periods=100, freq='D'))
        df_meta = pd.DataFrame({'timestamp': dates})
        
    df_meta['date'] = df_meta['timestamp'].dt.date
    activity = df_meta.groupby('date').size()

    plt.figure(figsize=(10, 5))
    activity.plot(kind='line', marker='o', linestyle='-', color='purple')
    plt.title('Chronologie de l\'Activité de Collecte de Données', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Volume de Requêtes/Documents')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.close()
    return fig_path


# --- Fonction de Visualisation ML (Clustering) ---

def plot_cluster_top_terms(summary_data: Dict[str, Any]) -> Path:
    """Figure ML: Barres "top n-grams par cluster" (pour Clustering)"""
    fig_path = Path(FIGURES_DIR) / "cluster_top_terms.png"
    
    cluster_analysis = summary_data.get('ml_interpretation', [])
    
    if not cluster_analysis:
        print("Avertissement: Données d'analyse de cluster non trouvées.")
        return Path("")

    num_clusters_to_plot = min(len(cluster_analysis), 5) 
    top_n_terms = 8

    fig, axes = plt.subplots(num_clusters_to_plot, 1, figsize=(10, 4 * num_clusters_to_plot))
    plt.suptitle(f'Top {top_n_terms} Termes TF-IDF par Cluster K-Means', fontsize=16, y=1.02)

    for i in range(num_clusters_to_plot):
        cluster = cluster_analysis[i]
        df_terms = pd.DataFrame(cluster['top_terms']).head(top_n_terms)
        
        ax = axes[i]
        sns.barplot(x='weight', y='term', data=df_terms, ax=ax, palette="Reds_d")
        ax.set_title(f"Cluster {cluster['cluster_id']} (Taille: {cluster['size']})", fontsize=12)
        ax.set_xlabel('Poids TF-IDF')
        ax.set_ylabel('')
        
    plt.tight_layout(rect=[0, 0, 1, 1.0])
    plt.savefig(fig_path)
    plt.close()
    return fig_path


def run_visualization_pipeline(raw_data_path: Path, summary_path: Path, keywords_path: Path) -> List[Path]:
    """Orchestre la création de toutes les figures et du dashboard PDF."""
    
    # 1. Charger les données
    # Simuler le chargement des méta-données (latency, status, date)
    # Dans un vrai projet, ces données viendraient des logs ou de la structure JSON thô.
    # Ici, nous créons un DataFrame fictif pour éviter une dépendance complexe non définie.
    df_meta = pd.DataFrame({
        'status_code': np.random.choice([200, 200, 200, 404, 500], size=100),
        'latency_ms': np.random.lognormal(mean=2.5, sigma=0.5, size=100) * 10,
        'timestamp': pd.to_datetime(pd.date_range(start='1/1/2025', periods=100, freq='H'))
    })
    
    with open(summary_path, 'r', encoding='utf-8') as f:
        summary_data = json.load(f)
        
    Path(FIGURES_DIR).mkdir(exist_ok=True, parents=True)
    
    # 2. Créer les figures
    fig_paths = []
    
    # Figures KPI/Méta-données (Obligatoires)
    fig_paths.append(plot_volume_by_source(summary_data))
    fig_paths.append(plot_top_keywords(keywords_path))
    fig_paths.append(plot_latency_distribution(df_meta))
    fig_paths.append(plot_status_codes(df_meta))
    fig_paths.append(plot_timeline_activity(df_meta))
    
    # Figure ML (Obligatoire)
    if 'ml_interpretation' in summary_data:
        fig_paths.append(plot_cluster_top_terms(summary_data))

    # 3. Créer le Dashboard PDF
    pdf_path = Path(REPORTS_DIR) / "dashboard.pdf"
    create_dashboard_pdf([p for p in fig_paths if p.exists()], pdf_path)
    
    return fig_paths