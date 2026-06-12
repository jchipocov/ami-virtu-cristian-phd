import pandas as pd
df = pd.read_csv('data/processed/ami_virtu_final_paper_ready.csv')
cols = [c for c in df.columns if c.startswith('B')]
print("Qualitative columns found:", cols)
if cols:
    print("\nSample values for", cols[0])
    print(df[cols[0]].head())
else:
    print("\nNo qualitative columns (BC1, BT1, etc.) found.")
