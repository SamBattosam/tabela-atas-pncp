import streamlit as st
import pandas as pd
import requests
from st_aggrid import AgGrid, GridOptionsBuilder

def obter_tabela():
    api_url = "https://pncp.gov.br/api/search/?tipos_documento=ata&ordenacao=-data&pagina=1&tam_pagina=100&status=vigente&orgaos=26661"
    response = requests.get(api_url)
    data = response.json()
    items = data.get('items', [])

    tabela = []
    for item in items:
        tabela.append([
            item.get('title', 'N/A'),
            item.get('numero_controle_pncp', 'N/A'),
            item.get('modalidade_licitacao_nome', 'N/A'),
            item.get('municipio_nome', 'N/A') + ' - ' + item.get('uf', 'N/A'),
            item.get('description', 'N/A')  # Sem textwrap.fill para não quebrar
        ])
    
    return pd.DataFrame(tabela, columns=["Atas nº", "Id Ata PNCP", "Modalidade", "Local", "Objeto"])

# Interface Streamlit
st.title("📊 Tabela de Atas PNCP")
st.write("Interaja com os dados e selecione células individuais!")

df = obter_tabela()
df.loc[len(df)] = ["TOTAL", "", "", "", f"{len(df)} atas exibidas"]  # Adiciona linha total

# Configurações da tabela interativa
builder = GridOptionsBuilder.from_dataframe(df)
builder.configure_selection("single")  # Permite seleção individual de células
builder.configure_grid_options(domLayout='autoHeight')

grid_response = AgGrid(df, gridOptions=builder.build(), enable_enterprise_modules=True, fit_columns_on_grid_load=True)

# Exibir célula selecionada
if grid_response["selected_rows"]:
    st.write("🔹 **Célula selecionada:**", grid_response["selected_rows"])
