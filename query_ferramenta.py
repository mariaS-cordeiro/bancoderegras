import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Usuário e senha fixos
USUARIO_CORRETO = "dapplab@ling"
SENHA_CORRETA = "1.2.3.4"

# Caminho do arquivo CSV
csv_path = "queries_linguisticas.csv"

# Função para salvar os dados
def salvar_csv(projeto, analista, titulo_regra, regra, ferramenta, data):
    nova_linha = {
        "Projeto": projeto,
        "Analista": analista,
        "Título da Regra": titulo_regra,
        "Regra": regra,
        "Ferramenta": ferramenta,
        "Data": data or datetime.now().strftime("%Y-%m-%d")
    }

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
    else:
        df = pd.DataFrame([nova_linha])

    df.to_csv(csv_path, index=False)
    st.success("Entrada salva com sucesso!")

# Função para buscar por projeto
def buscar_por_projeto(nome_projeto):
    if not os.path.exists(csv_path):
        return "Nenhum arquivo encontrado."

    df = pd.read_csv(csv_path)
    df_filtro = df[df["Projeto"].str.contains(nome_projeto, case=False, na=False)]

    if df_filtro.empty:
        return f"Nenhuma entrada encontrada para o projeto: {nome_projeto}"
    return df_filtro

# Função de login
@st.cache_resource
def autenticar(usuario, senha):
    return usuario == USUARIO_CORRETO and senha == SENHA_CORRETA

# Interface Streamlit
st.set_page_config(page_title="Registro de Regras Linguísticas", layout="wide")
st.title("📚 Ferramenta de Registro de Regras Linguísticas")

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.subheader("🔐 Acesso restrito")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if autenticar(usuario, senha):
            st.session_state.autenticado = True
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos.")
else:
    abas = st.tabs(["Cadastrar nova entrada", "Buscar por projeto"])

    with abas[0]:
        st.subheader("Cadastrar nova entrada")
        col1, col2 = st.columns(2)
        with col1:
            projeto = st.text_input("Nome do projeto")
            analista = st.text_input("Analista responsável")
            titulo_regra = st.text_input("Título da regra")
        with col2:
            regra = st.text_area("Regra linguística aplicada")
            ferramenta = st.radio("Ferramenta utilizada", ["ELK", "FPK", "YT", "BW"])

        data = st.text_input("Data do registro (opcional)", placeholder="AAAA-MM-DD")

        if st.button("Salvar entrada"):
            if projeto and analista and titulo_regra and regra:
                salvar_csv(projeto, analista, titulo_regra, regra, ferramenta, data)
            else:
                st.warning("Preencha todos os campos obrigatórios.")

    with abas[1]:
        st.subheader("Buscar por projeto")
        nome_projeto = st.text_input("Digite o nome do projeto para buscar")

        if st.button("Buscar"):
            resultado = buscar_por_projeto(nome_projeto)
            if isinstance(resultado, str):
                st.info(resultado)
            else:
                st.dataframe(resultado, use_container_width=True)
