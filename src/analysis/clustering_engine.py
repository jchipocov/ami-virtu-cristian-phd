import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import os

class ClusteringEngine:
    """
    Motor No Supervisado (Segmentación).
    Contiene un ensamble de algoritmos esféricos (K-Means/Ward) 
    y no paramétricos/basados en densidad (DBSCAN/GMM) para flexibilidad extrema.
    """

    def __init__(self, n_clusters=3):
        # Empezamos asumiendo 3 conglomerados exploratorios
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        
        # 1. Modelos Jerárquicos y Paramétricos (Esféricos/Convexos)
        self.jerarquico = AgglomerativeClustering(n_clusters=self.n_clusters, linkage='ward')
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        
        # 2. Modelos Basados en Densidad (DBSCAN tuneado para granularidad)
        self.dbscan = DBSCAN(eps=0.35, min_samples=5)
        self.gmm = GaussianMixture(n_components=self.n_clusters, covariance_type='full', random_state=42)

    def run_clustering(self, df_scored: pd.DataFrame) -> pd.DataFrame:
        """
        Inyecta la membresía del ensamble completo. 
        Implementa el flujo secuencial Jerárquico -> K-Means (Refinado).
        """
        df_valid = df_scored[df_scored.get('Flag_Inconsistencia', False) == False].copy()
        features = ['Score_Critico', 'Score_Tecnico', 'Score_Participativo']
        X = df_valid[features].dropna()
        X_scaled = self.scaler.fit_transform(X)
        
        # 1. Jerárquico (Ward) para explorar estructura
        df_valid['Cluster_Jerarquico'] = self.jerarquico.fit_predict(X_scaled)
        
        # 2. K-Means "Refinado" usando los centroides del Jerárquico como semilla
        # Calculamos centroides del jerárquico
        h_centroids = df_valid.groupby('Cluster_Jerarquico')[features].mean().values
        # Re-escalar centroides para que coincidan con X_scaled
        h_centroids_scaled = self.scaler.transform(h_centroids)
        
        self.kmeans = KMeans(n_clusters=self.n_clusters, init=h_centroids_scaled, n_init=1, random_state=42)
        df_valid['Cluster_KMeans'] = self.kmeans.fit_predict(X_scaled)
        
        # 3. Otros algoritmos del ensamble (Sensibilidad)
        df_valid['Cluster_DBSCAN'] = self.dbscan.fit_predict(X_scaled)
        df_valid['Cluster_GMM'] = self.gmm.fit_predict(X_scaled)
        
        return df_valid

    def validate_clustering(self, df_scored: pd.DataFrame):
        """Genera gráficos de Codo y Silueta para justificar la elección de K."""
        features = ['Score_Critico', 'Score_Tecnico', 'Score_Participativo']
        X = df_scored[features].dropna()
        X_scaled = self.scaler.fit_transform(X)
        
        output_dir = 'data/outputs/clustering_validation'
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Método del Codo
        distortions = []
        K_range = range(2, 8)
        for k in K_range:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            km.fit(X_scaled)
            distortions.append(km.inertia_)
        
        plt.figure(figsize=(8, 4))
        plt.plot(K_range, distortions, 'bx-')
        plt.xlabel('k')
        plt.ylabel('Distorsión (Inertia)')
        plt.title('Método del Codo (Elbow Method)')
        plt.savefig(f'{output_dir}/elbow_plot.png', dpi=150)
        plt.close()
        
        # 2. Análisis de Silueta
        sil_scores = []
        for k in K_range:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = km.fit_predict(X_scaled)
            sil_scores.append(silhouette_score(X_scaled, labels))
            
        plt.figure(figsize=(8, 4))
        plt.plot(K_range, sil_scores, 'go-')
        plt.xlabel('k')
        plt.ylabel('Silhouette Score')
        plt.title('Análisis de Silueta por K')
        plt.savefig(f'{output_dir}/silhouette_plot.png', dpi=150)
        plt.close()
        
        return {
            'k_range': list(K_range),
            'distortions': [float(d) for d in distortions],
            'silhouette_scores': [float(s) for s in sil_scores]
        }

    def get_cluster_profiles(self, df_clustered: pd.DataFrame) -> dict:
        """Calcula el perfil promedio de cada dimensión para todos los algoritmos del ensamble."""
        features = ['Score_Critico', 'Score_Tecnico', 'Score_Participativo']
        algorithms = {
            'K-Means': 'Cluster_KMeans',
            'Jerarquico-Ward': 'Cluster_Jerarquico',
            'DBSCAN': 'Cluster_DBSCAN',
            'GMM': 'Cluster_GMM'
        }
        
        results = {}
        for algo_name, col in algorithms.items():
            if col in df_clustered.columns:
                # Filtrar ruido para DBSCAN (-1)
                df_filtered = df_clustered[df_clustered[col] != -1]
                profiles = df_filtered.groupby(col)[features].mean().to_dict('index')
                risk_prev = df_filtered.groupby(col)['Riesgo_Total'].mean().to_dict()
                counts = df_clustered[col].value_counts().to_dict()
                results[algo_name] = {
                    'profiles': profiles,
                    'risk_prev': risk_prev,
                    'counts': counts
                }
        
        return {
            'status': 'success',
            'algorithms': results
        }
