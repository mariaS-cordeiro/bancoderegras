# -*- coding: utf-8 -*-
"""query_ferramenta.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/gist/mariaS-cordeiro/4395215814ec7cfb21bcce92e9f83f29/query_ferramenta.ipynb
"""

!pip install gradio

import gradio as gr

def salvar_query(nome, query):
    return f"Query '{nome}' salva com sucesso!"

gr.Interface(fn=salvar_query, inputs=["text", "text"], outputs="text").launch()

import gradio as gr
import json
import os
from datetime import datetime

ARQUIVO = "queries.json"

# Função para carregar queries salvas
def carregar_queries():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

# Função para salvar nova query
def salvar_query(nome, query, descricao, tags):
    if not nome or not query:
        return "Nome e expressão da query são obrigatórios."

    nova_query = {
        "nome": nome,
        "query": query,
        "descricao": descricao,
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
        "data_criacao": datetime.now().strftime("%Y-%m-%d")
    }

    queries = carregar_queries()
    queries.append(nova_query)

    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(queries, f, indent=2, ensure_ascii=False)

    return f"Query '{nome}' salva com sucesso!"

# Interface Gradio
gr.Interface(
    fn=salvar_query,
    inputs=[
        gr.Textbox(label="Projeto"),
        gr.Textbox(label="Regra linguística"),
        gr.Textbox(label="Ferramenta"),
        gr.Textbox(label="Data")
    ],
    outputs="text",
    title="Banco de regra linguística"
).launch()

!cat queries.json

!cat queries.json

import json
from pprint import pprint

with open("queries.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

pprint(dados)

import gradio as gr
import pandas as pd
import os
from google.colab import drive
from datetime import datetime

# Monta o Google Drive
drive.mount('/content/drive')
caminho_pasta = "/content/drive/MyDrive/syntax_search"
os.makedirs(caminho_pasta, exist_ok=True)
csv_path = os.path.join(caminho_pasta, "queries_linguisticas.csv")

# Função para salvar dados no CSV
def salvar_csv(projeto, analista, regra, ferramenta, data):
    nova_linha = {
        "Projeto": projeto,
        "Analista": analista,
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
    return "✅ Entrada salva com sucesso no Google Drive."

# Função para buscar por projeto
def buscar_por_projeto(nome_projeto):
    if not os.path.exists(csv_path):
        return "Nenhuma base encontrada no Drive."

    df = pd.read_csv(csv_path)
    df_filtro = df[df["Projeto"].str.contains(nome_projeto, case=False, na=False)]

    if df_filtro.empty:
        return f"Nenhuma entrada encontrada para o projeto: {nome_projeto}"

    resultado = ""
    for _, row in df_filtro.iterrows():
        resultado += f"📌 Projeto: {row['Projeto']}\n👤 Analista: {row['Analista']}\n🔤 Regra: {row['Regra']}\n🛠️ Ferramenta: {row['Ferramenta']}\n📅 Data: {row['Data']}\n---\n"
    return resultado

# Interface visual com caixas e abas destacadas
with gr.Blocks() as app:
    gr.Markdown("# 📚 Ferramenta de Registro de Regras Linguísticas")
    gr.Markdown("Use as abas abaixo para **cadastrar** novas regras ou **consultar** por projeto.")

    with gr.Tabs():
        with gr.TabItem("📥 Cadastrar nova entrada"):
            with gr.Group():
                gr.Markdown("### Preencha os dados da regra linguística")

                with gr.Row():
                    projeto = gr.Textbox(label="Nome do projeto")
                    analista = gr.Textbox(label="Analista responsável")

                with gr.Row():
                    regra = gr.Textbox(label="Regra linguística aplicada", lines=2)
                    ferramenta = gr.Radio(choices=["ELK", "FPK", "YT", "BW"], label="Ferramenta utilizada")

                with gr.Row():
                    data = gr.Textbox(label="Data do registro (opcional)", placeholder="AAAA-MM-DD")
                    salvar = gr.Button("Salvar entrada")

                status = gr.Textbox(label="Status da operação")
                salvar.click(fn=salvar_csv, inputs=[projeto, analista, regra, ferramenta, data], outputs=status)

        with gr.TabItem("🔎 Buscar por projeto"):
            with gr.Group():
                gr.Markdown("### Consulte regras linguísticas já registradas por nome de projeto")
                projeto_busca = gr.Textbox(label="Digite o nome do projeto")
                buscar = gr.Button("Buscar")
                resultado = gr.Textbox(label="Resultado da busca", lines=20)
                buscar.click(fn=buscar_por_projeto, inputs=projeto_busca, outputs=resultado)

app.launch()