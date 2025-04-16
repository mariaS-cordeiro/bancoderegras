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
            st.markdown(f"<div style='padding:10px;border:1px solid #ddd;border-radius:5px'>{regra}</div>", unsafe_allow_html=True);border:1px solid #ddd;border-radius:5px'>{regra_destacada}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='padding:10px;border:1px solid #ddd;border-radius:5px'>{regra}</div>", unsafe_allow_html=True)

                alerta_parenteses, cor = checar_parenteses(regra)
                st.markdown(f"<div style='background-color:{cor};padding:10px;border-radius:5px'>{alerta_parenteses}</div>", unsafe_allow_html=True);padding:10px;border-radius:5px'>{alerta_parenteses}</div>", unsafe_allow_html=True)

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
            for idx, row in resultado.iterrows():
                with st.expander(f"📄 {row['Título da Regra']} – {row['Projeto']}"):
                    st.markdown(f"**Regra:** `{row['Regra']}`")
                    st.markdown(f"**Analista:** {row['Analista']} | **Ferramenta:** {row['Ferramenta']} | **Data:** {row['Data']}")
                    st.markdown("**Abrir em:**")

                    conteudo_encoded = row['Regra'].replace(' ', '%20').replace('\n', '%0A')
                    bloco_nota_link = f"data:text/plain,{conteudo_encoded}"
                    google_docs_link = f"https://drive.google.com/drive/folders/14PxmRK90jiYs2RfZsjrvqtHMyYiDEADY"
                    onedrive_link = "https://onedrive.live.com/edit.aspx"

                    st.markdown(f"- [📄 Baixar bloco de notas]({bloco_nota_link})")
                    st.markdown(f"- [📝 Criar novo Google Docs com esse título]({google_docs_link})")
                    st.markdown(f"- [☁️ Abrir OneDrive para colar]({onedrive_link})")
