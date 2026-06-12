import pandas as pd
import os

df = pd.read_csv('data/processed/ami_virtu_final_paper_ready.csv')
print("Columns:", df.columns.tolist())
print("\nSample Analisis_Cuali:")
print(df['Analisis_Cuali'].head())
print("\nSample BC1 (Original Text):")
print(df['BC1'].head())
