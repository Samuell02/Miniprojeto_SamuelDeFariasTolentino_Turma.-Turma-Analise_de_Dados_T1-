import pandas as pd

df = pd.read_csv('Base Varejo.csv',sep=';')
print(df.head())

pd.set_option('display.max_rows', 5)


print(df.to_string())