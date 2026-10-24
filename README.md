Miniprojeto de analise de dados python para o curso sctec.

O Projeto atravessa as seguintes etapas para tratar e limpar a base de dados: 

  1.Abre o arquivo Base_Varejo.csv como um dicionario usando Dictreader.

2.Mostra os primeiros rows com o showrows(), o tipo dos rows com showtype(), e a quantidade de rows com shownumberofrows()

3. Texto é limpo por cleantext,que bota todas as letras em maiusculo,elimina espaços extras e nas pontas,cleaninteger que pega só os digitos e converte pra int, e se nao for digito converte pra none, e cleandecimal,que converteria preços para float,formataria eles corretamente, e removeria o "R$", porém, a base não tem preços entao acabou não sendo usado.
4. searchnull() procura nulos escondidos na base crua. Ele olha os valores distintos de cada coluna e marca o que parece vazio  de acordo com a variavel nulldisguise (#N/D, N/A, NULL, "-", "?" e parecidos),e identifique o que não são números em colunas que deveriam ter apenas numeros. Ele achou #N/D em PR_CAT e PR_NOME e uma coluna sem nome no final,que foi generada por ;;;;. a função countnull() conta quantos '#N/D" tem em cada coluna, resultando em 3650 nas colunas PR_CAT e PR_NOME.
5. removeemptycolumns() apaga a coluna sem nome. Antes da limpeza começar são  guardados o n_start (830000 linhas em total), n_dup (96553 linhas totalmente iguais) e n_nulls (3650 nulls em forma de  #N/D), pra usar no relatorio final,antes que eles sejam removidos na limpeza .
6. applyunique() aplica as funções de limpeza só nos valores distintos de cada coluna, e depois espalha o resultado pra todas as linhas, muito mais eficiente que linha por linha. cleantext aplica-se nas colunas CL_GENERO, CL_SEG, PR_CAT e PR_NOME, e cleaninteger aplica-se nas colunas  CO_ID, CL_ID, CL_EC, CL_FHL e PR_ID (viram Int64). turndatetodatetime() usa convertdata() para converter a coluna DATA em datetime, que usa datetime.strptime no formato dia/mes/ano(Em ingles,fica DD/MM/YYYY). Se a data for impossivel ela vira NaT pra não crashar o programa, e nenhuma data ficou invalida.
7. Os nulos são tratados com if/else em replacecatnull() e replacenamenull(): se o valor for #N/D ou vazio vira "SEM CATEGORIA" ou "SEM NOME", caso contrario não muda. Foi preenchido e não removido porque  apagar as linhas tiraria compras de verdade. Não existem dimensões fisicas nessa base, então os nulos que importavam eram só em PR_CAT e PR_NOME. Depois o searchnull() roda de novo e retorna {}, o que mostra que não sobrou nada suspeito.
8. validatepurchases() confere a regra do CO_ID: cada compra tem que ter um cliente só e uma data só. Deu 18471 compras e 0 inconsistentes, dando a entender que CO_ID repetidos são produto de varios items na mesma compra .
9. itemquantity() agrupa pelas colunas todas e guarda na coluna QUANTIDADE quantas vezes uma linha igual aparece. As 830000 linhas viram 733447, e a soma de QUANTIDADE não deixa de ser 830000, então não há perda de vendas. Isso parte de um unico principio: cada linha igual dentro da mesma compra é o mesmo produto.
10. shopclients fica com uma linha por cliente (1000 clientes) e showstatistics() e describestatistics() a ultilizam para calcular o numero de filhos,assim pessoas que compram mais não pesam mais, pra quem compra mais não pesar mais na media. 
11. groupgender() agrupa por genero (itens, compras, clientes e itens por compra) e groupcat() agrupa por categoria com a porcentagem de cada uma. Mulheres tem  432576 itens, 9615 compras e 519 clientes. Homens tem 397424 itens, 8856 compras e 481 clientes. Alimentos correspondem a  52.4% dos itens, higiene a 18.7% e limpeza a 17.6%.
12. No final é impresso o relatorio com os contadores (registros de antes e  depois da limpeza, duplicatas, #N/D substituidos, compras, clientes e periodo) e a base limpa é salva em df_limpo.csv.

Reflexão sobre ETL e qualidade de dados:
 
ETL é o processo de pegar dado bruto e deixar pronto pra analise, em 3 partes. 

Extract(Extrair) é a parte onde os dados são recebidos em sua forma mais bruta.Nesse projeto, isso aparece como a leitura do csv com Dictreader.
 


Transform(Transformar) é o process de pegar os dados e modifica-los para ser mais coerente,ter mais integridade, e ser melhor ultilizado por outros programas.Isso acontece a partir de : as funções de limpeza de texto e numeros inteiros e decimais (cleantext,cleaninteger e cleandecimal) a conversão das datas para o formato datetime, o if/else dos nulos que os substitui por "Sem Categoria" ou "Sem Nome", a validação do CO_ID a e a criação da QUANTIDADE. 

Load é salvar a base ,limpa e processada,  em df_limpo.csv, agora em um estado ideal para a visualização no excel e leitura para.
 
Qualidade de dados se refere a confiabilidade dos mesmos na hora de tomar decisões. Na base apareceram 4 problemas: 3650 #N/D,que não eram detectaveis por isna() porque tecnicamente não eram nulos, 96553 linhas iguais, datas e ids que eram texto ao inves de datetime e int, e confirmar que cada CO_ID tem um cliente e uma data só). Sem a limpeza o #N/D virava uma categoria falsa nas tabelas, e apagar as duplicatas sem pensar tiraria muitas vendas verdadeiras.  o diagnostico vem antes da limpeza, porque a base não tinha nenhuma celula vazia e mesmo assim tinha nulos.
 
 
 


Conclusões:
1.Não há dados de preços para os produtos.
Existe dados para os ids dos produtos,compras,clientes,generos, mas não o preço do produto em si
2. Mulheres Compram uma quantidade extremamente similar a homens(44.99 contra 44.88 itens dos homens),mais tem mais clientes mulheres que clientes homens, o que resulta em elas tendo um maior numero de itens e compras .
3. Devido a nao ter uma coluna de quantidades para ver quanto de cada item foi comprado, foi nescessaria a criação de uma.