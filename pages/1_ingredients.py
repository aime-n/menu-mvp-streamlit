import os
import sys
from datetime import datetime

import pandas as pd
import streamlit as st

# Adiciona o diretório raiz ao path para importar o api_client
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from api_client import api_client

st.set_page_config(page_title="Ingredientes - Menu MVP", page_icon="🥕", layout="wide")

st.title("🥕 Gerenciamento de Ingredientes")
st.markdown("---")


# Função para carregar ingredientes da API
def load_ingredients():
    """Carrega ingredientes da API"""
    try:
        ingredients = api_client.get_ingredients()
        return ingredients
    except Exception as e:
        st.error(f"Erro ao carregar ingredientes: {str(e)}")
        return []


# Função para adicionar ingrediente via API
def add_ingredient(name):
    """Adiciona ingrediente via API"""
    try:
        result = api_client.create_ingredient(name)
        return result
    except Exception as e:
        st.error(f"Erro ao adicionar ingrediente: {str(e)}")
        return None


# Função para deletar ingrediente via API
def delete_ingredient(ingredient_id):
    """Deleta ingrediente via API"""
    try:
        result = api_client.delete_ingredient(ingredient_id)
        return result
    except Exception as e:
        st.error(f"Erro ao deletar ingrediente: {str(e)}")
        return None


# Sidebar para adicionar ingredientes
with st.sidebar:
    st.header("➕ Adicionar Ingrediente")

    with st.form("add_ingredient"):
        nome = st.text_input("Nome do ingrediente", placeholder="Ex: Tomate")

        submitted = st.form_submit_button("Adicionar Ingrediente")

        if submitted and nome:
            result = add_ingredient(nome)
            if result:
                st.success(f"Ingrediente '{nome}' adicionado com sucesso!")
                st.rerun()

# Área principal
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📋 Lista de Ingredientes")

    # Carregar ingredientes da API
    ingredients = load_ingredients()

    if ingredients:
        # Converter para DataFrame
        df = pd.DataFrame(ingredients)

        # Filtros
        search_term = st.text_input(
            "🔍 Buscar ingrediente", placeholder="Digite o nome..."
        )

        # Aplicar filtros
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[
                filtered_df["name"].str.contains(search_term, case=False)
            ]

        # Exibir tabela
        st.dataframe(filtered_df[["id", "name"]], use_container_width=True)

        # Estatísticas
        st.subheader("📊 Estatísticas")
        col_stats1, col_stats2 = st.columns(2)

        with col_stats1:
            st.metric("Total de ingredientes", len(df))

        with col_stats2:
            st.metric("Ingredientes filtrados", len(filtered_df))

    else:
        st.info(
            "Nenhum ingrediente cadastrado ainda. Adicione ingredientes usando o formulário na barra lateral."
        )

with col2:
    st.header("⚡ Ações Rápidas")

    if ingredients:
        # Deletar ingrediente
        st.subheader("🗑️ Remover Ingrediente")
        ingredient_delete = st.selectbox(
            "Selecione para remover",
            [f"{ing['id']} - {ing['name']}" for ing in ingredients],
        )

        if st.button("Remover", type="secondary"):
            if ingredient_delete:
                ingredient_id = int(ingredient_delete.split(" - ")[0])
                result = delete_ingredient(ingredient_id)
                if result:
                    st.success(f"Ingrediente removido com sucesso!")
                    st.rerun()
    else:
        st.info("Adicione ingredientes para ver as ações disponíveis.")

# Status da API
st.markdown("---")
st.header("🔗 Status da API")

if st.button("🔄 Verificar Status da API"):
    try:
        health = api_client.health_check()
        st.success(f"✅ API funcionando: {health}")
    except Exception as e:
        st.error(f"❌ Erro na API: {str(e)}")

# Exportar dados
if ingredients:
    st.markdown("---")
    st.header("💾 Exportar Dados")

    if st.button("📄 Exportar CSV"):
        df = pd.DataFrame(ingredients)
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"ingredientes_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )
