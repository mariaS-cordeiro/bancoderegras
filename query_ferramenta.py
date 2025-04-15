import streamlit as st
import pandas as pd
import os
from datetime import datetime
import re

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
def autenticar(usuario, senha):
    return usuario == USUARIO_CORRETO and senha == SENHA_CORRETA

# Função para destacar operadores booleanos e checar parênteses
def destacar_operadores(texto):
    texto = re.sub(r'\bOR\b', '<span style="color:green;font-weight:bold">OR</span>', texto)
    texto = re.sub(r'\bAND\b', '<span style="color:blue;font-weight:bold">AND</span>', texto)
    texto = re.sub(r'\bNEAR/\d+\b', lambda m: f'<span style="color:orange;font-weight:bold">{m.group()}</span>', texto)
    texto = re.sub(r'\bNOT\b', '<span style="color:red;font-weight:bold">NOT</span>', texto)
    return texto

def checar_parenteses(texto):
    abertura = texto.count('(')
    fechamento = texto.count(')')
    if abertura > fechamento:
        return f"⚠️ Faltam {abertura - fechamento} parêntese(s) de fechamento.", "#fff3cd"
    elif fechamento > abertura:
        return f"⚠️ Faltam {fechamento - abertura} parêntese(s) de abertura.", "#fff3cd"
    else:
        return "✓ Parênteses balanceados.", "#d4edda"

# Configuração da página
st.set_page_config(page_title="Registro de Regras Linguísticas", layout="wide")
st.title("📚 Ferramenta de Registro de Regras Linguísticas")

# Controle de sessão
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# Tela de login
if not st.session_state.autenticado:
    st.subheader("🔐 Acesso restrito")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if autenticar(usuario, senha):
            st.session_state.autenticado = True
            st.success("Login realizado com sucesso! Você agora pode acessar a ferramenta.")
        else:
            st.error("Usuário ou senha incorretos.")
    st.stop()

# Interface após login
abas = st.tabs(["Cadastrar nova entrada", "Buscar por regra linguística"])

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

    if regra:
        st.markdown("**Visualização da regra com operadores destacados (campo 'Regra linguística aplicada'):**", unsafe_allow_html=True)
        st.markdown(f"<div style='padding:10px;border:1px solid #ddd;border-radius:5px'>{destacar_operadores(regra)}</div>", unsafe_allow_html=True)

        alerta_parenteses, cor = checar_parenteses(regra)
        st.markdown(f"<div style='background-color:{cor};padding:10px;border-radius:5px'>{alerta_parenteses}</div>", unsafe_allow_html=True)

    data = st.text_input("Data do registro (opcional)", placeholder="AAAA-MM-DD")

    if st.button("Salvar entrada"):
        if projeto and analista and titulo_regra and regra:
            salvar_csv(projeto, analista, titulo_regra, regra, ferramenta, data)
        else:
            st.warning("Preencha todos os campos obrigatórios.")

with abas[1]:
    st.subheader("Buscar por regra linguística")
    nome_projeto = st.text_input("Digite o nome da regra ou projeto para buscar")

    if st.button("Buscar"):
        resultado = buscar_por_projeto(nome_projeto)
        if isinstance(resultado, str):
            st.info(resultado)
        else:
            st.dataframe(resultado, use_container_width=True)
