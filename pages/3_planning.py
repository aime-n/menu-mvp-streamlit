import os
import sys
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

# Adiciona o diretório raiz ao path para importar o api_client
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from api_client import api_client

st.set_page_config(page_title="Planejamento - Menu MVP", page_icon="📅", layout="wide")

st.title("📅 Planejamento de Refeições")
st.markdown("---")

# Inicializar session state para planejamento
if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = {}
if "shopping_list" not in st.session_state:
    st.session_state.shopping_list = []


# Função para obter dias da semana
def get_week_days():
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    week_days = []
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        week_days.append(day.strftime("%d/%m/%Y"))
    return week_days


# Função para carregar receitas da API
def load_recipes():
    """Carrega receitas da API"""
    try:
        recipes = api_client.get_recipes()
        return recipes
    except Exception as e:
        st.error(f"Erro ao carregar receitas: {str(e)}")
        return []


# Sidebar para planejamento
with st.sidebar:
    st.header("📝 Planejar Refeição")

    # Selecionar data
    selected_date = st.date_input(
        "Selecionar Data",
        value=datetime.now(),
        min_value=datetime.now() - timedelta(days=30),
        max_value=datetime.now() + timedelta(days=90),
    )

    # Selecionar tipo de refeição
    meal_type = st.selectbox(
        "Tipo de Refeição", ["Café da Manhã", "Almoço", "Jantar", "Lanche", "Ceia"]
    )

    # Carregar receitas da API
    recipes = load_recipes()

    # Selecionar receita (se existir)
    if recipes:
        recipe_options = [rec["name"] for rec in recipes]
        selected_recipe = st.selectbox(
            "Selecionar Receita", ["Nenhuma"] + recipe_options
        )
    else:
        selected_recipe = "Nenhuma"
        st.info("Adicione receitas primeiro!")

    # Notas adicionais
    notes = st.text_area(
        "Notas adicionais", placeholder="Observações sobre a refeição..."
    )

    # Adicionar ao planejamento
    if st.button("Adicionar ao Planejamento"):
        date_key = selected_date.strftime("%d/%m/%Y")
        if date_key not in st.session_state.meal_plan:
            st.session_state.meal_plan[date_key] = {}

        if meal_type not in st.session_state.meal_plan[date_key]:
            st.session_state.meal_plan[date_key][meal_type] = []

        meal_entry = {
            "recipe": (
                selected_recipe if selected_recipe != "Nenhuma" else "Refeição livre"
            ),
            "notes": notes,
            "added_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        }

        st.session_state.meal_plan[date_key][meal_type].append(meal_entry)
        st.success(f"Refeição adicionada para {date_key} - {meal_type}")

# Área principal
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📅 Planejamento Semanal")

    # Mostrar planejamento da semana atual
    week_days = get_week_days()

    # Criar tabs para cada dia
    tabs = st.tabs(week_days)

    for i, (tab, day) in enumerate(zip(tabs, week_days)):
        with tab:
            if day in st.session_state.meal_plan:
                day_plan = st.session_state.meal_plan[day]

                for meal_type in [
                    "Café da Manhã",
                    "Almoço",
                    "Jantar",
                    "Lanche",
                    "Ceia",
                ]:
                    if meal_type in day_plan:
                        st.subheader(f"🍽️ {meal_type}")

                        for meal in day_plan[meal_type]:
                            with st.expander(f"📋 {meal['recipe']}"):
                                st.write(f"**Receita:** {meal['recipe']}")
                                if meal["notes"]:
                                    st.write(f"**Notas:** {meal['notes']}")
                                st.write(f"**Adicionado em:** {meal['added_at']}")

                                # Botão para remover
                                remove_key = f"remove_{day}_{meal_type}_{i}"
                                if st.button(
                                    f"Remover {meal['recipe']}", key=remove_key
                                ):
                                    day_plan[meal_type].remove(meal)
                                    if not day_plan[meal_type]:
                                        del day_plan[meal_type]
                                    st.success("Refeição removida!")
                                    st.rerun()
            else:
                st.info("Nenhuma refeição planejada para este dia.")

with col2:
    st.header("🛒 Lista de Compras")

    # Gerar lista de compras automaticamente
    if st.button("🔄 Gerar Lista de Compras"):
        st.session_state.shopping_list = []

        # Carregar receitas da API
        recipes = load_recipes()

        # Coletar ingredientes das receitas planejadas
        for date, day_plan in st.session_state.meal_plan.items():
            for meal_type, meals in day_plan.items():
                for meal in meals:
                    if meal["recipe"] != "Refeição livre" and recipes:
                        # Encontrar a receita
                        for recipe in recipes:
                            if recipe["name"] == meal["recipe"]:
                                # Adicionar ingredientes à lista
                                if recipe.get("ingredients"):
                                    for ingredient in recipe["ingredients"]:
                                        ingredient_name = ingredient.get(
                                            "name", "Ingrediente desconhecido"
                                        )
                                        st.session_state.shopping_list.append(
                                            {
                                                "ingrediente": ingredient_name,
                                                "receita": meal["recipe"],
                                                "data": date,
                                                "refeicao": meal_type,
                                            }
                                        )

        st.success("Lista de compras gerada!")

    # Mostrar lista de compras
    if st.session_state.shopping_list:
        st.subheader("📋 Itens para Comprar")

        # Agrupar por ingrediente
        ingredientes_agrupados = {}
        for item in st.session_state.shopping_list:
            ingrediente = item["ingrediente"]
            if ingrediente not in ingredientes_agrupados:
                ingredientes_agrupados[ingrediente] = []
            ingredientes_agrupados[ingrediente].append(item)

        for ingrediente, items in ingredientes_agrupados.items():
            with st.expander(f"🛒 {ingrediente} ({len(items)}x)"):
                for item in items:
                    st.write(
                        f"- **{item['receita']}** ({item['data']} - {item['refeicao']})"
                    )

        # Limpar lista
        if st.button("🗑️ Limpar Lista"):
            st.session_state.shopping_list = []
            st.success("Lista de compras limpa!")
            st.rerun()
    else:
        st.info(
            "Nenhum item na lista de compras. Gere a lista baseada no planejamento."
        )

# Estatísticas do planejamento
if st.session_state.meal_plan:
    st.markdown("---")
    st.header("📊 Estatísticas do Planejamento")

    col_stats1, col_stats2, col_stats3 = st.columns(3)

    with col_stats1:
        total_meals = sum(
            len(meals)
            for day_plan in st.session_state.meal_plan.values()
            for meals in day_plan.values()
        )
        st.metric("Total de Refeições", total_meals)

    with col_stats2:
        days_planned = len(st.session_state.meal_plan)
        st.metric("Dias Planejados", days_planned)

    with col_stats3:
        if st.session_state.shopping_list:
            unique_items = len(
                set(item["ingrediente"] for item in st.session_state.shopping_list)
            )
            st.metric("Itens Únicos", unique_items)
        else:
            st.metric("Itens Únicos", 0)

# Exportar planejamento
if st.session_state.meal_plan:
    st.markdown("---")
    st.header("💾 Exportar Planejamento")

    if st.button("📄 Exportar CSV"):
        # Preparar dados para exportação
        export_data = []
        for date, day_plan in st.session_state.meal_plan.items():
            for meal_type, meals in day_plan.items():
                for meal in meals:
                    export_data.append(
                        {
                            "data": date,
                            "refeicao": meal_type,
                            "receita": meal["recipe"],
                            "notas": meal["notes"],
                            "adicionado_em": meal["added_at"],
                        }
                    )

        df = pd.DataFrame(export_data)
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"planejamento_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )
