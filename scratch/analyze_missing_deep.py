import pandas as pd
import numpy as np

# Load paper_ready dataset (N=729)
df_729 = pd.read_csv('data/processed/real_ami_virtu_final_paper_ready_823.csv')

critico_cols = [f'C{i}' for i in range(1, 11)]
tecnico_cols = [f'T{i}' for i in range(1, 11)]
participativo_cols = [f'P{i}' for i in range(1, 11)]
ami_items = critico_cols + tecnico_cols + participativo_cols

print("=== 1. ANALISIS DE MISSING DATA EN N=729 ===")
missing_by_item = df_729[ami_items].isnull().sum()
total_cells = len(df_729) * len(ami_items)
total_missing = missing_by_item.sum()

print(f"Total celdas: {total_cells}, Total missing: {total_missing} ({total_missing/total_cells*100:.2f}%)")
print("\nMissing por dimension:")
print(f"Critico (C1-C10): {missing_by_item[critico_cols].sum()} / {len(df_729)*10} ({missing_by_item[critico_cols].sum()/(len(df_729)*10)*100:.2f}%)")
print(f"Tecnico (T1-T10): {missing_by_item[tecnico_cols].sum()} / {len(df_729)*10} ({missing_by_item[tecnico_cols].sum()/(len(df_729)*10)*100:.2f}%)")
print(f"Participativo (P1-P10): {missing_by_item[participativo_cols].sum()} / {len(df_729)*10} ({missing_by_item[participativo_cols].sum()/(len(df_729)*10)*100:.2f}%)")

print("\nMissing detallado por item:")
for col in ami_items:
    n_miss = df_729[col].isnull().sum()
    pct = n_miss / len(df_729) * 100
    print(f"  {col}: {n_miss} ({pct:.2f}%)")

print("\n=== 2. DISTRIBUCION DE MISSING POR ESTUDIANTE (N=729) ===")
missing_per_student = df_729[ami_items].isnull().sum(axis=1)
print(missing_per_student.value_counts().sort_index())

print("\nDistribucion por estudiante en Critico:")
print(df_729[critico_cols].isnull().sum(axis=1).value_counts().sort_index())

print("\nDistribucion por estudiante en Tecnico:")
print(df_729[tecnico_cols].isnull().sum(axis=1).value_counts().sort_index())

# Check how many students have 0 missing vs some missing
n_complete = (missing_per_student == 0).sum()
print(f"\nEstudiantes con escala 100% completa: {n_complete} ({n_complete/len(df_729)*100:.2f}%)")
print(f"Estudiantes con al menos 1 missing: {(missing_per_student > 0).sum()} ({(missing_per_student > 0).sum()/len(df_729)*100:.2f}%)")
