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
        mapa = {d: convertdata(d) for d in df["DATA"].unique()}
        df["DATA"] = pd.to_datetime(df["DATA"].map(mapa))
        print("Datas inválidas:", df["DATA"].isna().sum())
#Conta quantos nulls tem a partir do #N/D, que nos ja sabemos que é o null porque procuramos com o searchnull
def countnull():
    cont = (df == "#N/D").sum()
    print(cont[cont > 0].to_dict())
#Analisa toda a base de dados com o nulldisguise de refencia para identificar o null escondido.
def searchnull():
    found = {}
    for col in df.columns:
        cont = df[col].value_counts(dropna=False)
        textos = cont.index.astype(str).str.strip().str.upper()
        mask = textos.isin(nulldisguise) | cont.index.isna()
        if col in numcolumns:
            mask = mask | ~textos.str.fullmatch(r"\d+")
        nd = cont[mask]
        if len(nd) > 0:
            found[col] = {str(k): int(v) for k, v in nd.items()}
    print(found)
    return found
#Troca os nulls do PR_CAT por "SEM CATEGORIA"
def replacecatnull(cat):
    if cat == "#N/D" or cat == "":
        return "SEM CATEGORIA"
    else:
        return cat
#Troca os nulls do PR_NOME por "SEM NOME"
def replacenamenull(nome):
    if nome == "#N/D" or nome == "":
        return "SEM NOME"
    else:
        return nome
#troca as colunas vazias por NA e se livra delas depois
def removeemptycolumns():
    df.replace('', pd.NA, inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
#Coloca todos as linhas que aparecem multiplas vezes um uma só,ai o mesmo CO_ID que comprou um item multiplas vezes so aparece uma vez ao inves de ter rows duplicados
def itemquantity():
    global df
    columns = list(df.columns)
    df = (
        df.groupby(columns, as_index=False, dropna=False)
        .size()
        .rename(columns={"size": "QUANTIDADE"})
    )
#verifica a compra pra ter certeza de que cada uma pertença a apenas um cliente e uma data.
def validatepurchases():
    df.dropna(subset=["CO_ID"], inplace=True)
    df["CO_ID"] = df["CO_ID"].astype(str).str.strip()

    itemsperpurchase = df.groupby("CO_ID").size()
    print(f"Total de compras válidas : {len(itemsperpurchase)}")
    groupedpurchases = df.groupby("CO_ID").agg(n_clientes=("CL_ID", "nunique"),
                                n_datas=("DATA", "nunique"))
    print("CO_ID inconsistentes:", ((groupedpurchases ["n_clientes"] > 1) | (groupedpurchases ["n_datas"] > 1)).sum())
#Mostra todas as estatisticas de um column,uma por uma
def showstatistics(scolumn):
    print("Contagem:", scolumn.count())
    print("Média:", round(scolumn.mean(), 2))
    print("Mediana:", scolumn.median())
    print("Desvio Padrão:", round(scolumn.std(), 2))
    print("Moda:", scolumn.mode().tolist())
    print("Máximo:", scolumn.max())
    print("Mínimo:", scolumn.min())
    print("Quartis:")
    print(scolumn.quantile([0.25, 0.50, 0.75]))
#Mostra todas as estatisticas de um column,todas de uma vez
def describestatistics(scolumn):
    print("Estatisticas completas")
    print(scolumn.describe())
#mostra a porcentagem das vendas por categoria
def groupcat():
    print("Vendas por Categoria")
    r = (df.groupby("PR_CAT")["QUANTIDADE"].sum()
           .sort_values(ascending=False).to_frame("itens"))
    r["%"] = (r["itens"] / r["itens"].sum() * 100).round(1)
    print(r)
#Mostra os diferentes dados das vendas entre homens e mulheres.
def groupgender():
    print("Vendas por Genero")
    r = df.groupby("CL_GENERO").agg(
        itens=("QUANTIDADE", "sum"),
        compras=("CO_ID", "nunique"),
        clientes=("CL_ID", "nunique"),
    )  # clientes distintos
    r["itens_por_compra"] = (r["itens"] / r["compras"]).round(2)
    r = r.sort_values("itens", ascending=False)
    print(r)

#1) visao da base antes da limpeza
showrows()
shownumberofrows()
print(searchnull())
countnull()
#2 Remove colunas vazias e guarda contadores do relatório
removeemptycolumns()
n_start = len(df)                         # 830000
n_dup = int(df.duplicated().sum())          # 96553
n_nulls = int((df["PR_CAT"] == "#N/D").sum())  # 3650
showtypes()

# 3 limpeza e tratamento de tipos
for col in ["CL_GENERO", "CL_SEG", "PR_CAT", "PR_NOME"]:
    df[col] = applyunique(df[col], cleantext)
for col in ["CO_ID", "CL_ID", "CL_EC", "CL_FHL", "PR_ID"]:
    df[col] = applyunique(df[col], cleaninteger).astype("Int64")
print("Teste de Limpeza de Decimais", cleandecimal("R$ 3,40"))
turndatetodatetime()
showtypes()

#4 substituindo nulos
countnull()
df["PR_CAT"] = applyunique(df["PR_CAT"], replacecatnull)
df["PR_NOME"] = applyunique(df["PR_NOME"], replacenamenull)
print(searchnull())                         # {} = nada suspeito sobrou

#5 Regra do CO_ID
validatepurchases()

#6 transformando duplicatas em QUANTIDADE
itemquantity()
df = df.sort_values(["DATA", "CO_ID"]).reset_index(drop=True)
print("Soma de QUANTIDADE:", df["QUANTIDADE"].sum())
shopclients = df.drop_duplicates("CL_ID")
print("Clientes:", len(shopclients))
shownumberofrows()

showstatistics()

Describestatistics()
