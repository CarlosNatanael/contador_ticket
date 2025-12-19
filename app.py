import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Conferência de NF", layout="wide")

st.title("📦 Conferência por NF de Entrada")

uploaded_file = st.file_uploader("Suba a planilha mestre", type=["xlsx", "csv"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file, header=1)
        else:
            df = pd.read_csv(uploaded_file, header=1)

        df.columns = [str(c).strip() for c in df.columns]
        
        if 'NF de Entrada' in df.columns:
            df['NF de Entrada'] = df['NF de Entrada'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

            nf_desejada = st.text_input("Digite o número da NF de Entrada (Ex: 66076):").strip()

            if nf_desejada:
                df_filtrado = df[df['NF de Entrada'] == nf_desejada]

                if not df_filtrado.empty:
                    st.success(f"✅ {len(df_filtrado)} registros encontrados para a NF {nf_desejada}")
                    
                    todas_pecas = []
                    pecas_raw = df_filtrado['Peças'].dropna().astype(str).tolist()
                    
                    for entrada in pecas_raw:
                        partes = re.split(r'\s{2,}', entrada.strip())
                        for p in partes:
                            item = p.strip()
                            if item and not item.isdigit() and len(item) > 2:
                                todas_pecas.append(item)
                    
                    if todas_pecas:
                        df_contagem = pd.Series(todas_pecas).value_counts().reset_index()
                        df_contagem.columns = ['Nome da Peça', 'Quantidade Total']
                        
                        st.subheader(f"Resumo de Peças - NF {nf_desejada}")
                        st.dataframe(df_contagem, use_container_width=True)
                    else:
                        st.warning("Nenhuma peça identificada nesta nota.")
                else:
                    st.error(f"A nota '{nf_desejada}' não foi encontrada. Notas disponíveis: {', '.join(df['NF de Entrada'].unique()[:5])}...")
        else:
            st.error(f"Coluna 'NF de Entrada' não encontrada. Colunas detectadas: {list(df.columns)}")
            
    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")