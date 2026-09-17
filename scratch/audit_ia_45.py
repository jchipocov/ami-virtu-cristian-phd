import pandas as pd
import numpy as np

df_774 = pd.read_csv('data/processed/real_hybrid_analysis_results_823.csv')
ia_excl = df_774[df_774['Indice_Coherencia'] < 0.60]
print("Coherence index value counts for excluded (N=45):")
print(ia_excl['Indice_Coherencia'].value_counts().sort_index())

print("\nCoherence index summary for all 774:")
print(df_774['Indice_Coherencia'].describe())

print("\n--- SAMPLE 5 QUALITATIVE REASONS FOR EXCLUSION ---")
for idx, row in ia_excl[['ID_Estudiante', 'Indice_Coherencia', 'Analisis_Cuali', 'Sentimiento_Academico', 'Etiquetas_Tematicas']].head(5).iterrows():
    print(f"ID: {row['ID_Estudiante']} | Coherence: {row['Indice_Coherencia']} | Sentiment: {row['Sentimiento_Academico']}")
    print(f"Tags: {row['Etiquetas_Tematicas']}")
    print(f"Explanation: {row['Analisis_Cuali']}\n")

# Check text length across the 12 open response items
cuali_cols = ['BC1', 'BC2', 'BC3', 'BC4', 'BT1', 'BT2', 'BT3', 'BT4', 'BP1', 'BP2', 'BP3', 'BP4']
df_774['Total_Text_Length'] = df_774[cuali_cols].fillna('').apply(lambda r: sum(len(str(x).strip()) for x in r), axis=1)

print("Mean total text length across 12 items:")
print(f"Included (N=729): {df_774[df_774['Indice_Coherencia'] >= 0.60]['Total_Text_Length'].mean():.1f} characters")
print(f"Excluded (N=45): {df_774[df_774['Indice_Coherencia'] < 0.60]['Total_Text_Length'].mean():.1f} characters")
