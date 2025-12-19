import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Conferência de NF", layout="centered")

st.title("📦 Conferência por NF de Entrada")

uploaded_file = st.file_uploader("Primeiro, suba a planilha mestre (Excel ou CSV)", type=["xlsx", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file, header=1)
    else:
        df = pd.read_csv(uploaded_file, header=1)
    
    df['NF de Entrada'] = df['NF de Entrada'].astype(str).str.strip()

    nf_desejada = st.text_input("Digite o número da NF de Entrada para conferir (Ex: 66076):")

    if nf_desejada:
        df_filtrado = df[df['NF de Entrada'] == nf_desejada]

        if not df_filtrado.empty:
            st.success(f"Encontrados {len(df_filtrado)} registros para a NF {nf_desejada}")

            todas_pecas = []
            pecas_raw = df_filtrado['Peças'].dropna().astype(str).tolist()
            
            for entrada in pecas_raw:
                partes = re.split(r'\s{2,}', entrada.strip())
                for p in partes:
                    item = p.strip()
                    if item and not item.isdigit():
                        todas_pecas.append(item)
            
            if todas_pecas:
                df_contagem = pd.Series(todas_pecas).value_counts().reset_index()
                df_contagem.columns = ['Nome da Peça', 'Quantidade Total na Nota']

                st.subheader(f"Resumo de Peças - NF {nf_desejada}")
                st.table(df_contagem)
            else:
                st.warning("Nenhuma peça encontrada na coluna 'Peças' para esta nota.")
        else:
            st.error(f"A nota {nf_desejada} não foi encontrada na planilha.")