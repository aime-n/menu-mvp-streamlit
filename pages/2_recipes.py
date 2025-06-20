import os
import sys
from datetime import datetime

import pandas as pd
import streamlit as st

# Adiciona o diretório raiz ao path para importar o api_client
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from api_client import api_client

st.set_page_config(page_title="Receitas - Menu MVP", page_icon="👨‍🍳", layout="wide")

st.title("👨‍🍳 Gerenciamento de Receitas")
st.markdown("---")


# Função para carregar receitas da API
def load_recipes():
    """Carrega receitas da API"""
    try:
        recipes = api_client.get_recipes()
        return recipes
    except Exception as e:
        st.error(f"Erro ao carregar receitas: {str(e)}")
        return []


# Função para carregar ingredientes da API
def load_ingredients():
    """Carrega ingredientes da API"""
    try:
        ingredients = api_client.get_ingredients()
        return ingredients
    except Exception as e:
        st.error(f"Erro ao carregar ingredientes: {str(e)}")
        return []


# Função para adicionar receita via API
def add_recipe(name, instructions, ingredients_list):
    """Adiciona receita via API"""
    try:
        # Converter ingredientes para o formato da API
        api_ingredients = []
        for ingredient in ingredients_list:
            if ingredient.strip():
                # Assumindo formato: "quantidade unidade nome"
                parts = ingredient.strip().split()
                if len(parts) >= 2:
                    quantity = parts[0]
                    unit = parts[1] if len(parts) > 2 else None
                    ingredient_name = (
                        " ".join(parts[2:]) if len(parts) > 2 else parts[1]
                    )

                    api_ingredients.append(
                        {
                            "ingredient_name": ingredient_name,
                            "quantity": quantity,
                            "unit": unit,
                        }
                    )

        result = api_client.create_recipe(name, instructions, api_ingredients)
        return result
    except Exception as e:
        st.error(f"Erro ao adicionar receita: {str(e)}")
        return None


# Sidebar para adicionar receitas
with st.sidebar:
    st.header("➕ Adicionar Receita")

    with st.form("add_recipe"):
        nome = st.text_input("Nome da receita", placeholder="Ex: Macarrão à Bolonhesa")

        # Ingredientes (formato simplificado)
        ingredientes_text = st.text_area(
            "Ingredientes (um por linha, formato: quantidade unidade nome)",
            placeholder="200 g macarrão\n2 unidade tomate\n1 unidade cebola\n...",
        )

        # Instruções
        instrucoes = st.text_area(
            "Instruções de preparo",
            placeholder="1. Ferva água...\n2. Cozinhe o macarrão...\n...",
        )

        submitted = st.form_submit_button("Adicionar Receita")

        if submitted and nome and instrucoes:
            # Converter ingredientes para lista
            ingredientes_list = (
                ingredientes_text.split("\n") if ingredientes_text else []
            )

            result = add_recipe(nome, instrucoes, ingredientes_list)
            if result:
                st.success(f"Receita '{nome}' adicionada com sucesso!")
                st.rerun()

# Área principal
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📋 Lista de Receitas")

    # Carregar receitas da API
    recipes = load_recipes()

    if recipes:
        # Converter para DataFrame
        df = pd.DataFrame(recipes)

        # Filtros
        search_term = st.text_input("🔍 Buscar receita", placeholder="Digite o nome...")

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
            st.metric("Total de receitas", len(df))

        with col_stats2:
            st.metric("Receitas filtradas", len(filtered_df))

    else:
        st.info(
            "Nenhuma receita cadastrada ainda. Adicione receitas usando o formulário na barra lateral."
        )

with col2:
    st.header("⚡ Ações Rápidas")

    if recipes:
        # Visualizar receita detalhada
        st.subheader("👁️ Visualizar Receita")
        recipe_view = st.selectbox(
            "Selecione a receita", [rec["name"] for rec in recipes]
        )

        if st.button("Ver Detalhes"):
            for recipe in recipes:
                if recipe["name"] == recipe_view:
                    st.subheader(f"📖 {recipe['name']}")
                    st.write(f"**ID:** {recipe['id']}")

                    st.write("**Ingredientes:**")
                    if recipe.get("ingredients"):
                        for ingredient in recipe["ingredients"]:
                            st.write(f"- {ingredient.get('name', 'N/A')}")
                    else:
                        st.write("Nenhum ingrediente cadastrado")

                    st.write("**Instruções:**")
                    st.text(recipe.get("instructions", "N/A"))
                    break
    else:
        st.info("Adicione receitas para ver as ações disponíveis.")

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
if recipes:
    st.markdown("---")
    st.header("💾 Exportar Dados")

    if st.button("📄 Exportar CSV"):
        df = pd.DataFrame(recipes)
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"receitas_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )
