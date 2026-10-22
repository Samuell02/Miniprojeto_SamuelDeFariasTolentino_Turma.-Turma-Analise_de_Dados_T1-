import pandas as pd


df = pd.read_csv('Base Varejo.csv',sep=';')
print(df.head())
def showstatistics():
    print("Média")
    print(df['CL_FHL'].mean())
    print("Mediana"),
    print(df['CL_FHL'].median()),
    print("Desvio Padrão")
    print(df['CL_FHL'].std()),
    print("Moda")
    print(df['CL_FHL'].mode())
    print("Maximo")
    print(df['CL_FHL'].max())
    print("Minimo")
    print(df['CL_FHL'].min()),
    print("Contagem")
    print(df['CL_FHL'].count())
    print("Quartis")
    print(df['CL_FHL'].quantile([0.25, 0.50, 0.75]))

def Describestatistics():
    print("Estatisticas completas")
    print(df.describe())





def removeduplicates():
    df.drop_duplicates(inplace=True)

def showrows():
    pd.set_option('display.max_rows', 5)
    print(df.to_string())

def showtypes():
    print(df.dtypes)

def shownumberofrows():
    print(len(df))

def turndatetodatetime():
    df['DATA'] = pd.to_datetime(df['DATA'],dayfirst=True)

def removeemptyrows():
    df.dropna(axis=1, how='all', inplace=True)


turndatetodatetime()
showtypes()
removeemptyrows()


showtypes()

shownumberofrows()

showstatistics()

Describestatistics()
