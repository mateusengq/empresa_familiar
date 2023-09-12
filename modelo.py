# %% [markdown]
# # Avaliação _ Empresas Familiares
# 
# Critérios:
# - Para o teste foram selecionadas as empresas com faturamento estimando entre 100 - 200 milhões

# %%
import numpy as np
import pandas as pd

# %%
# Leitura dos dados
df = pd.read_csv('dados/base_empresas.csv')

# %%
# Seleção das colunas de interesse

df_2 = df[['Empresa', 'Principais Executivos']]

# %%
# Separação das colunas
base = df_2['Principais Executivos'].str.split(",", expand = True)


# %%
print(f'A base original possui {df_2.shape} dimensoes e a nova, {base.shape}')

# %%
## Agrupando as bases

df_3 = pd.concat([df_2, base], axis = 1)

# %%
df_3.shape

# %%
# df_3

# %%
df_3 = df_3.drop(columns=['Principais Executivos'])

# %%
# Transformando o formato do dataframe para longer considerando apenas a relação empresa-aconista_x
df_4 = pd.melt(
    frame = df_3,
    id_vars = ['Empresa'],
    var_name = 'coluna_referencia',
    value_name = 'Acionista'
)

# %%
df_4.shape

# %%
df_4

# %%
# Exclusão dos valores ausentes

df_4 = df_4.dropna()

# %%
# Contagem da quantidade de acionistas de cada empresa
## qtde_acionistas_por_empresas = df_4.groupby(['Empresa'])['Empresa'].count()

qtde_acionistas_por_empresas= df_4.groupby(['Empresa']).size().reset_index(name = 'count')

# %%
qtde_acionistas_por_empresas

# %%
# Sepração dos nomes das colunas de acionistas

df_5 = df_4['Acionista'].str.split(expand = True)

# %%
df_5

# %%
# Combinando os dois dataframes

df_5 = pd.concat([df_4, df_5], axis = 1)

# %%
# Selecionando as colunas de interesse e realizando o pivot longer

df_5 = df_5.drop(columns=['coluna_referencia', 'Acionista'])

# %%
df_5

# %%
# Transformando o formato do dataframe para longer considerando apenas a relação empresa-aconista_x
df_5 = pd.melt(
    frame = df_5,
    id_vars = ['Empresa'],
    var_name = 'coluna_referencia',
    value_name = 'nome'
)

# %%
df_5 = df_5.dropna()
df_5 = df_5.drop(columns = ['coluna_referencia'])

# %%
df_5.shape

# %%
df_5

# %%
# substituir nomes
substituicoes = {
    'Vice': None,
    '(Sócio-Administrador)': None,
    '(Administrador)': None,
    '(Diretor)': None,
    'de': None,
    'da': None,
    'Sócio': None,
    '(Conselheiro)':None,
    '(Tesoureiro)':None,
    '(Administração)':None,
    '(Administração)':None,
    'e':None,
    'com':None,
    'do':None,
    'Informatica':None,
    '(Finanças)':None,
    '(Presidente)' : None,
    'Presidente)':None,
    '(Sócio)' : None,
    'Administração)': None,
    'Investidores)' : None,
    '(Investidores)' : None,
    '(Diretor)':None,
    'Diretor':None

}

## valores_a_substituir = list(substituicoes.keys())

df_5['nome'] = df_5['nome'].replace(substituicoes, regex = False)

## df_5['nome'] = df_5['nome'].replace(valores_a_substituir, None, regex=True)




# %%
resultado = df_5.groupby(['nome'])['nome'].count().reset_index(name='count')
resultado = resultado.sort_values(by='count', ascending=False)
resultado

# %%
df_5.shape

# %%
df_5 = df_5.dropna()

# %%
## removendo células com apenas um caracter

df_5 = df_5[df_5['nome'].str.len() > 1]

# %%
df_5

# %%
# Contando a quantidade de nomes por empresa

qtde_nomes_unitarios_empresa = df_5.groupby(['Empresa', 'nome']).size().reset_index(name = 'count')

# %%
qtde_nomes_unitarios_empresa

# %%
base_final = pd.merge(qtde_nomes_unitarios_empresa, qtde_acionistas_por_empresas,
on = 'Empresa', how = 'left')

# %%
base_final

# %%
filtro = base_final['Empresa'] == '10 M Group Participacoes S.A.'
base_final[filtro]

# %%
base_final['proporcao_nomes_por_qtde_socios'] = base_final['count_x']/base_final['count_y']*100

# %%
base_final[base_final['count_y'] > 2].sort_values(by='proporcao_nomes_por_qtde_socios',ascending=False)

# %%
# criando o dataframe final
# encontrando o sobrenome com o maior valor em número de ocorrências para cada empresa

idx = base_final.groupby('Empresa')['count_x'].idxmax()

# criando um novo dataframe
df_6 = base_final.loc[idx, ['Empresa', 'nome', 'count_x', 'count_y', 'proporcao_nomes_por_qtde_socios']]

# %%
df_6

# %%
df_6[df_6['count_y'] > 2].sort_values(by='proporcao_nomes_por_qtde_socios',ascending=False)

# %%
# pendencias: fazer uma análise dos nomes

mateus = 'teste'

# %%



