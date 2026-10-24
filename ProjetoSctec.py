import pandas as pd
import csv
import re
from datetime import datetime

#Essas são as variaveis mais importantes do projeto:filetoload determina que arquivo o programa abre,cleanfile decide qual arquivo é salvo,nulldisguise ajuda a identificar nulls disfarçados, e numcolumns ajuda a limpar colunas com numeros
filetoload ="Base_Varejo.csv"
cleanfile = "VarejoLimpo.csv"
nulldisguise= {"#N/D", "#N/A", "N/A", "NA", "NULL", "NONE", "NAN", "-", "--", "?", "","UNDEFINED","UNNAMED"}
numcolumns = ["CO_ID", "CL_ID", "CL_EC", "CL_FHL", "PR_ID"]



def removeduplicates():
    df.drop_duplicates(inplace=True)

def showrows():
    pd.set_option('display.max_rows', 5)
    print(df.to_string())

def showtypes():
    print(df.dtypes)

def shownumberofrows():
    print(len(df))

def agrupargenero():
    print("\n--- Agrupamento 1: Total de Compras por Gênero ---")
    vendas_por_genero = df.groupby("CL_GENERO").size().reset_index(name="Total_Compras")
    vendas_por_genero = vendas_por_genero.sort_values(
        by="Total_Compras", ascending=False
    )
    print(vendas_por_genero.to_string(index=False))

def turndatetodatetime():
    df['DATA'] = pd.to_datetime(df['DATA'],dayfirst=True)

def removeemptycolumns():
    df.replace('', pd.NA, inplace=True)
    df.dropna(axis=1, how='all', inplace=True)


turndatetodatetime()
showtypes()
removeemptycolumns()

showtypes()

shownumberofrows()

showstatistics()

Describestatistics()
