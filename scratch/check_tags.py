import pandas as pd
df = pd.read_csv('data/processed/ami_virtu_final_paper_ready.csv')
print("Columns:", df.columns.tolist())
if 'Etiquetas_Tematicas' in df.columns:
    print("\nEtiquetas_Tematicas (first 5 non-null):")
    print(df['Etiquetas_Tematicas'].dropna().head())
    print("\nCluster_KMeans unique values:")
    if 'Cluster_KMeans' in df.columns:
        print(df['Cluster_KMeans'].unique())
    else:
        print("Cluster_KMeans NOT FOUND in this file (it is usually added during runtime).")
else:
    print("\nEtiquetas_Tematicas NOT FOUND.")
