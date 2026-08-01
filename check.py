import pandas as pd
df = pd.read_excel('data/raw/Formulario de Investigación Académica Doctoral - BIU(823).xlsx', sheet_name='Sheet1')
print(df.iloc[:, 5].unique())
print(df.iloc[:, 7].unique())
