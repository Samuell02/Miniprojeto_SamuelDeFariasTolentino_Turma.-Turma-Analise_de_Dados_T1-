import pandas as pd

df = pd.read_csv('Base Varejo.csv',sep=';')
pd.set_option('display.max_columns', None)
print(df.head())
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

