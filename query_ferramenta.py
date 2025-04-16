with abas[1]:
    st.subheader("Buscar por regra linguística")
    nome_projeto = st.text_input("Digite o nome da regra ou projeto para buscar")

    if nome_projeto:
        resultado = buscar_por_projeto(nome_projeto)
        if isinstance(resultado, str):
            st.info(resultado)
            resultado = pd.DataFrame(columns=['Projeto', 'Analista', 'Título da Regra', 'Regra', 'Ferramenta', 'Data'])
    else:
        resultado = pd.read_csv(csv_path)

    for idx, row in resultado.iterrows():
        with st.expander(f"📄 {row['Título da Regra']} – {row['Projeto']}"):
            regra_formatada = row['Regra'].replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
            st.markdown(f"""
            <div style='background-color: #1e1e1e; border-left: 4px solid #3399ff; border-right: 4px solid #3399ff; padding: 15px; border-radius: 8px; margin-bottom: 10px; font-family: "Proxima Nova", sans-serif;'>
                <strong style='color: #00ffff;'>Elaboração de regras linguística:</strong><br><br>
                <code style='color: white;'>{regra_formatada}</code>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"**Analista:** {row['Analista']} | **Ferramenta:** {row['Ferramenta']} | **Data:** {row['Data']}")

            if st.button(f"🗑️ Deletar regra", key=f"del_{idx}"):
                if st.radio("Tem certeza que deseja excluir esta regra?", ["Não", "Sim"], index=0, key=f"confirma_{idx}") == "Sim":
                    df = pd.read_csv(csv_path)
                    df = df.drop(resultado.index[idx])
                    df.to_csv(csv_path, index=False)
                    st.success("Regra deletada com sucesso!")
                    st.experimental_rerun()

            st.markdown("**Abrir em:**")

            conteudo_encoded = row['Regra'].replace(' ', '%20').replace('\n', '%0A')
            bloco_nota_link = f"data:text/plain,{conteudo_encoded}"
            google_docs_link = "https://drive.google.com/drive/folders/14PxmRK90jiYs2RfZsjrvqtHMyYiDEADY"
            onedrive_link = "https://onedrive.live.com/edit.aspx"

            st.markdown(f"- [📄 Baixar bloco de notas]({bloco_nota_link})")
            st.markdown(f"- [📝 Criar novo Google Docs com esse título]({google_docs_link})")
            st.markdown(f"- [☁️ Abrir OneDrive para colar]({onedrive_link})")
