import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Gestão de Loteria", layout="wide")
st.title("📊 Sistema de Gestão de Caixa para Lotéricas")

# Criando abas
aba1, aba2, aba3 = st.tabs(["Gestão de Caixas", "Gestão do Cofre", "Relatórios"])

# Função para carregar os dados
@st.cache_data
def load_data():
    return pd.DataFrame(columns=["Data", "Operador", "Caixa", "Entradas", "Saídas", "Saldo Final", "Venda de Bolão", "Venda de Raspadinha", "Estoque Bolão", "Estoque Raspadinha"])

df_caixas = load_data()
df_cofre = pd.DataFrame(columns=["Data", "Descrição", "Entrada", "Saída", "Saldo"])
df_relatorios = pd.DataFrame(columns=["Período", "Total Entradas", "Total Saídas", "Saldo Final"])

# ABA 1: Gestão de Caixas
with aba1:
    st.subheader("📌 Controle de Caixa")
    
    col1, col2, col3 = st.columns(3)
    data = col1.date_input("Data", datetime.today())
    operador = col2.text_input("Operador")
    caixa = col3.selectbox("Caixa", ["Caixa 1", "Caixa 2", "Caixa Interno"])
    
    col4, col5, col6 = st.columns(3)
    entradas = col4.number_input("Entradas", min_value=0.0, format="%.2f")
    saidas = col5.number_input("Saídas", min_value=0.0, format="%.2f")
    saldo_final = col6.number_input("Saldo Final", min_value=0.0, format="%.2f")
    
    col7, col8, col9, col10 = st.columns(4)
    venda_bolao = col7.number_input("Venda de Bolão", min_value=0, format="%d")
    venda_raspadinha = col8.number_input("Venda de Raspadinha", min_value=0, format="%d")
    estoque_bolao = col9.number_input("Estoque Bolão", min_value=0, format="%d")
    estoque_raspadinha = col10.number_input("Estoque Raspadinha", min_value=0, format="%d")
    
    if st.button("Salvar Registro"):
        novo_dado = pd.DataFrame([[data, operador, caixa, entradas, saidas, saldo_final, venda_bolao, venda_raspadinha, estoque_bolao, estoque_raspadinha]],
                                 columns=df_caixas.columns)
        df_caixas = pd.concat([df_caixas, novo_dado], ignore_index=True)
        st.success("Registro salvo com sucesso!")
    
    st.dataframe(df_caixas)

# ABA 2: Gestão do Cofre
with aba2:
    st.subheader("💰 Controle do Cofre")
    
    col1, col2, col3 = st.columns(3)
    data_cofre = col1.date_input("Data", datetime.today())
    descricao = col2.text_input("Descrição")
    tipo_movimentacao = col3.radio("Tipo de Movimentação", ["Entrada", "Saída"])
    
    col4 = st.columns(1)[0]
    valor = col4.number_input("Valor", min_value=0.0, format="%.2f")
    
    if st.button("Salvar Movimentação"):
        entrada = valor if tipo_movimentacao == "Entrada" else 0
        saida = valor if tipo_movimentacao == "Saída" else 0
        novo_movimento = pd.DataFrame([[data_cofre, descricao, entrada, saida, 0]], columns=df_cofre.columns)
        df_cofre = pd.concat([df_cofre, novo_movimento], ignore_index=True)
        st.success("Movimentação registrada com sucesso!")
    
    st.dataframe(df_cofre)

# ABA 3: Relatórios
with aba3:
    st.subheader("📈 Relatórios de Movimentação")
    periodo = st.selectbox("Escolha o período", ["Diário", "Semanal", "Mensal"])
    st.dataframe(df_relatorios)

