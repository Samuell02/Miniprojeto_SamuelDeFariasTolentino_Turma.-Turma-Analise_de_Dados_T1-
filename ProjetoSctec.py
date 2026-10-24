import pandas as pd
import csv
import re
from datetime import datetime

#Essas são as variaveis mais importantes do projeto:filetoload determina que arquivo o programa abre,cleanfile decide qual arquivo é salvo,nulldisguise ajuda a identificar nulls disfarçados, e numcolumns ajuda a limpar colunas com numeros
filetoload ="Base_Varejo.csv"
cleanfile = "VarejoLimpo.csv"
nulldisguise= {"#N/D", "#N/A", "N/A", "NA", "NULL", "NONE", "NAN", "-", "--", "?", "","UNDEFINED","UNNAMED"}
numcolumns = ["CO_ID", "CL_ID", "CL_EC", "CL_FHL", "PR_ID"]

#Isso abre a base de dados como um dataframe usando o dictreader.
with open(filetoload, newline='', encoding='utf-8') as f:
    data = csv.DictReader(f, delimiter=";")
    df = pd.DataFrame(data)

#isso mostra os primeiro 5 rows
def showrows():
    print(df.head())
#Isso mostra os types da base
def showtypes():
    print(df.dtypes)
#isso mostra quantos rows a base tem
def shownumberofrows():
    print(len(df))

#isso eliminina espaços extras,bota tudo em maiusculo,
def cleantext(txt):
    return re.sub(r"\s+", " ", str(txt)).strip().upper()
#converte todos os digitos pra int e se nao for digito converte pra none.
def cleaninteger(txt):
    d = re.sub(r"\D", "", str(txt))
    return int(d) if d else None
#Deveria remover o "R$" dos preços, converter pra float,e formatar corretamente,porem a base de dados não tem preço entao isso nao ve uso.
def cleandecimal(txt):
    cleaneddec = re.sub(r"[^\d,.\-]", "", str(txt))
    if "," in cleaneddec:
        cleaneddec = cleaneddec.replace(".", "").replace(",", ".")
    try:
        return float(cleaneddec)
    except ValueError:
        return None
#aplica as funções de limpeza nos valores unicos ao inves de todos os valores.
def applyunique(scolumn, operation):
    maps = {v: operation(v) for v in scolumn.unique()}
    return scolumn.map(maps)

#converte uma data para datetime ou retorna NaT se não for uma data valida
def convertdata(txt):
    try:
        return datetime.strptime(txt.strip(), "%d/%m/%Y")
    except ValueError:
        return pd.NaT
#Converte todas as datas para datetime usando a função convertdata
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
