import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

# Função para tratar as colunas de diferentes anos
def tratativa_base_passos_magicos(df, year_list):
    combined_df = pd.DataFrame()

    for year in year_list:
        # Filtra as colunas que terminam com o ano especificado
        cols_with_year = [col for col in df.columns if col.endswith(f'_{year}')]

        # Cria novas colunas sem o ano
        new_columns = ['NOME', 'ANO'] + [col[:-5] for col in cols_with_year]

        # Cria um novo DataFrame temporário
        temp_df = pd.DataFrame(columns=new_columns)

        # Preenche o novo DataFrame com os dados correspondentes
        for index, row in df.iterrows():
            new_row = [row['NOME'], year] + [row[col] for col in cols_with_year]
            temp_df.loc[index] = new_row

        # Adiciona os dados processados ao DataFrame combinado
        combined_df = pd.concat([combined_df, temp_df], ignore_index=True)

    return combined_df

# Função para tratar a coluna FASE_TURMA para o ano de 2020
def tratar_fase_turma(df):
    df.loc[df['ANO'] == '2020', 'FASE'] = df['FASE_TURMA'].str[0]
    df.loc[df['ANO'] == '2020', 'TURMA'] = df['FASE_TURMA'].str[1:]
    return df

# Função para limpar o dataset removendo linhas e colunas indesejadas
def cleaning_dataset(df):
    _df = df.dropna(subset=df.columns.difference(['NOME', 'ANO']), how='all')  # Drop linhas com NaN em todas as colunas exceto 'NOME' e 'ANO'
    _df = _df[~_df.isna().all(axis=1)]  # Remove linhas com apenas NaN
    return _df

# Função para manter apenas as colunas sem valores nulos
def drop_null_columns(df):
    df = df.dropna(axis=1, how='any')  # Drop colunas com qualquer valor nulo
    return df

# Função para restaurar colunas específicas de outro DataFrame
def restore_columns(df, df_source, columns):
    for col in columns:
        df.loc[:, col] = df_source[col]
    return df

# Função para arredondar as colunas para 2 casas decimais
def round_columns(df, columns):
    df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')
    df[columns] = df[columns].round(2)
    return df

# Função para filtrar valores indesejados em uma coluna específica
def filter_unwanted_values(df, column, unwanted_values):
    df = df[~df[column].isin(unwanted_values)]
    return df

# Pipeline para executar todas as funções
def pipeline_passos_magicos(df, year_list, colunas_para_arredondar, valores_indesejados):
    df_combined = tratativa_base_passos_magicos(df, year_list)
    df_combined = tratar_fase_turma(df_combined)
    df_cleaned = cleaning_dataset(df_combined)
    df_cleaned = drop_null_columns(df_cleaned)
    
    # Restaurar colunas
    df_cleaned = restore_columns(df_cleaned, df_combined, ['PONTO_VIRADA', 'INDICADO_BOLSA'])
    
    # Arredondar colunas numéricas
    df_cleaned = round_columns(df_cleaned, colunas_para_arredondar)
    
    # Filtrar valores indesejados na coluna 'PEDRA'
    df_final = filter_unwanted_values(df_cleaned, 'PEDRA', valores_indesejados)
    
    return df_final

