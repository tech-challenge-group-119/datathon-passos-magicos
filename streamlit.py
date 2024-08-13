#Importação das bibliotecas
import streamlit as st 
import pandas as pd
from alimentacao_dados import *
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from joblib import load
import plotly.express as px


# Configurações Gerais da Página
st.set_page_config(page_title="Tech Challenge - Passos Mágicos & FIAP - Grupo 119", layout="wide")

st.markdown("""
<style>
.custom-card {
    text-align: center;
    margin: 20px;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.15); /* Sombra para dar um efeito elevado */
    font-size: 20px;
    background-color: #333333; /* Cor de fundo dos cartões */
    color: #FFFFFF; /* Cor do texto */
}
.custom-card .value {
    font-size: 30px;
    font-weight: bold;
}
.custom-card .label {
    font-size: 18px;
    color: #BBBBBB; /* Cor do rótulo */
    margin-top: 5px;
}
.custom-hr {
    border: 0;
    height: 1px;
    background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
}
.small-text {
    font-size: 14px;
    color: #666666;
}
.stNumberInput > div {
    padding: 5px;
    width: 100px;  /* Ajuste o valor conforme necessário */
}
</style>
""", unsafe_allow_html=True)


#Atualizando os dados
df_passos_magicos = pd.read_csv(r'C:/Programas Python/Datathon/Base de dados - Passos Mágicos/PEDE_PASSOS_DATASET_FIAP.csv', sep = ';')
year_list = ['2020', '2021', '2022']
colunas_para_arredondar = ['INDE', 'IAA', 'IEG', 'IPS', 'IDA', 'IPP', 'IPV', 'IAN']
valores_indesejados = ['#NULO!', 'D9891/2A']

# Executar o pipeline completo
df_pm_not_nulls = pipeline_passos_magicos(df_passos_magicos, year_list, colunas_para_arredondar, valores_indesejados)


## BLOCO 1 - INTRODUÇÃO
# --- Página Inicial
st.write('# I. Análise e Previsibilidade de Desempenho - Alunos Passos Mágicos')
st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)

# Texto de contexto
st.markdown("""
<p class="small-text">
            
A Associação Passos Mágicos dedica-se à transformação da vida de crianças e jovens de baixa renda da cidade de Embu-Guaçu, desde o ano de 1992,
proporcionando melhores oportunidades de vida para aqueles que mais precisam.

O projeto oferece educação de qualidade, apoio psicológico e psicopedagógico, além da promoção de uma visão ampliada do mundo e do protagonismo juvenil.

Dentro da instituição, existem indicadores criados com base nos princípios do projeto e que são usados para acompanhar o desenvolvimento do aluno.

Com base nisso, esse painel visa entregar dois modelos de Machine Learning:
<ul>
    <li>Previsibilidade do ponto de virada.</li>
    <li>Previsibilidade da indicação para uma bolsa de estudos.</li>
</ul>
</p>
""", unsafe_allow_html=True)

## BLOCO 2 - ANÁLISE DOS DADOS
st.write('# II. Conhecendo os dados')

st.markdown("""
<p>Para entendimento dos próximos passos, vamos passar rapidamente a definição e como é feita a coleta dos indicadores que compõem a construção da Pedra-Conceito:</p>
<ul>
    <li><strong>IAN - Indicador de Adequação de Nível:</strong> através de registros administrativos</li>
    <li><strong>IDA - Indicador de Desempenho Acadêmico:</strong> através de provas ao longo do período</li>
    <li><strong>IEG - Indicador de Engajamento:</strong> através de registros de entrega de lições de casa e de voluntariado</li>
    <li><strong>IAA - Indicador de Autoavaliação:</strong> através de um questionário individual</li>
    <li><strong>IPS - Indicador Psicossocial:</strong> através de um questionário individual</li>
    <li><strong>IPP - Indicador Psicopedagógico:</strong> através de um questionário individual e avaliação dos professores e pedagogos</li>
    <li><strong>IPV - Indicador do Ponto de Virada:</strong> através de um questionário individual e avaliação dos professores e pedagogos</li>
</ul>
<p>Esses 7 indicadores compõem o INDE - ÍNDICE DE DESENVOLVIMENTO EDUCACIONAL que, por sua vez está diretamente relacionado à classificação em pedras, de acordo com classificação:</p>
<ul>
    <li><strong>Pedra-Conceito Quartzo:</strong> 3.302 ≤ INDE ≤ 6.109</li>
    <li><strong>Pedra-Conceito Ágata:</strong> 3.11 ≤ INDE ≤ 7.154</li>
    <li><strong>Pedra-Conceito Ametista:</strong> 7.154 ≤ INDE ≤ 8.198</li>
    <li><strong>Pedra-Conceito Quartzo:</strong> 8.198 < INDE ≤ 9.442</li>
</ul>
""", unsafe_allow_html=True)

st.markdown("""
Dito isso, vamos analisar a distribuição de alunos em cada Pedra-Conceito por ano
            """)

# Criando o gráfico para a distribuição de alunos por classificação de pedras e ano
color_map = {
    '2020': 'orange',
    '2021': 'blue',
    '2022': 'purple'
}
fig = px.bar(df_pm_not_nulls, 
             x='PEDRA', 
             color='ANO',  # Agrupa as barras por ano
             barmode='group',  # Exibe as barras agrupadas (em vez de empilhadas)
             title='Distribuição de Alunos por Classificação de Pedras e Ano', 
             labels={'PEDRA': 'Pedras', 'count': 'Qtdade Aluno'}, 
             category_orders={"PEDRA": df_pm_not_nulls['PEDRA'].value_counts().index},
             color_discrete_map=color_map)

# Atualizando o layout do gráfico para melhorar a visualização
fig.update_layout(
    xaxis_title='Pedras',
    yaxis_title='Qtdade Aluno'
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
Além disso, plotamos a evolução das pedras ao longo dos anos para facilitar o entendimento
            """)

df_grouped = df_pm_not_nulls.groupby(['ANO', 'PEDRA']).size().reset_index(name='Quantidade')
# Criando o gráfico de linha para mostrar a evolução da quantidade de alunos por pedra ao longo dos anos
fig = px.line(df_grouped, 
              x='ANO', 
              y='Quantidade', 
              color='PEDRA',  # Similar ao hue no Seaborn
              markers=True,  # Adiciona marcadores aos pontos de dados
              title='Quantidade de Alunos por Tipo de Pedra ao Longo dos Anos',
              labels={'ANO': 'Ano', 'Quantidade': 'Quantidade de Alunos', 'PEDRA': 'Tipo de Pedra'})

# Atualizando o layout do gráfico
fig.update_layout(
    xaxis_title='Ano',
    yaxis_title='Quantidade de Alunos',
    legend_title_text='Tipo de Pedra',
    template='plotly'
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)

## BLOCO 2 - ANÁLISE DOS DADOS
st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
st.write('# III. Construindo o Modelo de Previsão de Ponto de Virada')



st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
#análise das primeiras bases
#storytelling da criação do modelo com explicações pertinentes
#modelo e performance
#deploy do modelo e utilização


# BLOCO 4: Deploy do modelo
st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
st.write('# 4. Fazer a previsão de Indicação de Bolsa')

# Carregar o modelo treinado
modelo = load('modelo_svm.joblib')
def fazer_previsao(ipp, ipv):
    # Cria um dataframe com as features
    dados = pd.DataFrame({'IPP': [ipp], 'IPV': [ipv]})
    # Faz a previsão
    previsao = modelo.predict(dados)
    return previsao[0]

ipp_input = st.text_input('Insira o valor de IPP (usando o ponto como separador decimal)', '5.0')
ipv_input = st.text_input('Insira o valor de IPV (usando o ponto como separador decimal)', '5.0')

# Converter as entradas para float
try:
    ipp = float(ipp_input)
    ipv = float(ipv_input)
except ValueError:
    st.error("Por favor, insira um número válido.")


# Fazer a previsão
if st.button('Fazer Previsão'):
    resultado = fazer_previsao(ipp, ipv)
    st.write(f'A previsão de bolsa é: {resultado}')



# BLOCO 4: FINALIZAÇÃO
st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
st.write('# 5. Links Úteis')

st.markdown('[Repositório no Github](https://github.com/tech-challenge-group-119/datathon-passos-magicos)')
st.markdown('[Documentação do Plotly](https://plotly.com/python/)')

st.write('#### Equipe 119')
st.write('##### Bruna Batista do Carmo Abreu - RM 351370')
st.write('##### Sérgio Luiz Velloso Filho - RM 351371')




