import pandas as pd
df_raw = pd.read_excel('data/raw/Formulario de Investigación Académica Doctoral - BIU(823).xlsx')

# Consent and virtual filter
consent_col = df_raw.columns[6]
virtual_col = df_raw.columns[8]
df_filt = df_raw[(df_raw[consent_col].astype(str).str.upper().str.strip() == "ACEPTO PARTICIPAR") & 
                 (df_raw[virtual_col].astype(str).str.strip().str.upper().isin(["SÍ", "SI"]))].copy().reset_index(drop=True)
df_filt['ID_Estudiante'] = [f'STU_{str(i).zfill(4)}' for i in range(1, len(df_filt) + 1)]

# The 30 Likert items in raw excel are columns 9 to 38
raw_likert_cols = df_filt.columns[9:39]

# Let's map raw Likert string to numbers
mapping = {
    'Totalmente en desacuerdo': 1, 'En desacuerdo': 2, 'Neutral': 3,
    'De acuerdo': 4, 'Totalmente de acuerdo': 5,
    'Nunca': 1, 'Raramente': 2, 'A veces': 3, 'Frecuentemente': 4, 'Siempre': 5,
    '1': 1, '2': 2, '3': 3, '4': 4, '5': 5
}

df_likert_num = df_filt[raw_likert_cols].apply(lambda col: col.map(mapping))

stu_list = ['STU_0002', 'STU_0004', 'STU_0005', 'STU_0041', 'STU_0049', 'STU_0052', 'STU_0080', 'STU_0086', 'STU_0095', 'STU_0113', 'STU_0252', 'STU_0372']
for s in stu_list:
    row_idx = df_filt[df_filt['ID_Estudiante'] == s].index[0]
    row_vals = df_likert_num.iloc[row_idx]
    print(f"{s}: raw_var={row_vals.var()}, unique_raw={row_vals.dropna().unique()}, NaNs={row_vals.isna().sum()}")
