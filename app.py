import os
import sys

import streamlit as st

# Adiciona o diretório raiz ao path para importar o api_client
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from api_client import api_client

st.set_page_config(
    page_title="Menu MVP - Sistema de Gerenciamento", page_icon="🍽️", layout="wide"
)

st.title("🍽️ Menu MVP - Sistema de Gerenciamento")
st.markdown("---")

# Introdução
st.header("👋 Bem-vindo ao Menu MVP!")
st.write(
    """
Este é um sistema completo para gerenciar suas receitas, ingredientes e planejamento de refeições. 
O sistema está integrado com uma API externa e inclui um assistente AI para ajudar com suas dúvidas culinárias.
"""
)

# Cards informativos
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
    ### 🥕 **Ingredientes**
    - Cadastre e gerencie seus ingredientes
    - Integração com API externa
    - Busca e filtros
    - Exportação para CSV
    """
    )

with col2:
    st.markdown(
        """
    ### 👨‍🍳 **Receitas**
    - Crie e organize suas receitas
    - Instruções detalhadas
    - Integração com ingredientes
    - Visualização completa
    """
    )

with col3:
    st.markdown(
        """
    ### 📅 **Planejamento**
    - Planeje suas refeições semanais
    - Gere listas de compras automaticamente
    - Visualização por dia da semana
    - Exporte dados para CSV
    """
    )

with col4:
    st.markdown(
        """
    ### 🤖 **Chat AI**
    - Assistente inteligente para dúvidas
    - Sugestões de receitas
    - Dicas de culinária
    - Ajuda com planejamento
    """
    )

# Status da API
st.markdown("---")
st.header("🔗 Status da Integração")

col_status1, col_status2 = st.columns(2)

with col_status1:
    if st.button("🔄 Verificar Status da API"):
        try:
            health = api_client.health_check()
            st.success(f"✅ API funcionando: {health}")
        except Exception as e:
            st.error(f"❌ Erro na API: {str(e)}")

with col_status2:
    st.markdown(
        """
    **API Base URL:** `https://menu-mvp-api.onrender.com`
    
    **Funcionalidades disponíveis:**
    - ✅ Gerenciamento de ingredientes
    - ✅ Gerenciamento de receitas
    - ✅ Chat AI para assistência
    - ✅ Endpoints RESTful
    """
    )

# Estatísticas gerais
st.markdown("---")
st.header("📊 Estatísticas Gerais")

# Carregar dados da API
try:
    ingredients = api_client.get_ingredients()
    recipes = api_client.get_recipes()
    total_ingredients = len(ingredients)
    total_recipes = len(recipes)
except Exception as e:
    total_ingredients = 0
    total_recipes = 0
    st.warning(f"Não foi possível carregar dados da API: {str(e)}")

# Verificar dados locais de planejamento
total_planned_meals = sum(
    len(meals)
    for day_plan in st.session_state.get("meal_plan", {}).values()
    for meals in day_plan.values()
)

col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)

with col_stats1:
    st.metric("🥕 Ingredientes", total_ingredients)

with col_stats2:
    st.metric("👨‍🍳 Receitas", total_recipes)

with col_stats3:
    st.metric("📅 Refeições Planejadas", total_planned_meals)

with col_stats4:
    if "shopping_list" in st.session_state:
        unique_items = len(
            set(item["ingrediente"] for item in st.session_state.shopping_list)
        )
        st.metric("🛒 Itens na Lista", unique_items)
    else:
        st.metric("🛒 Itens na Lista", 0)

# Dicas de uso
st.markdown("---")
st.header("💡 Dicas de Uso")

st.markdown(
    """
1. **Comece pelos Ingredientes** - Cadastre seus ingredientes básicos primeiro
2. **Crie Receitas** - Use os ingredientes cadastrados para criar receitas completas
3. **Planeje suas Refeições** - Organize sua semana com as receitas criadas
4. **Use o Chat AI** - Faça perguntas sobre culinária e receitas
5. **Gere Listas de Compras** - Deixe o sistema criar automaticamente sua lista
6. **Exporte Dados** - Use os botões de exportação para salvar seus dados
"""
)

# Informações técnicas
with st.expander("ℹ️ Informações Técnicas"):
    st.markdown(
        """
    **Tecnologias utilizadas:**
    - **Streamlit** - Interface web
    - **Pandas** - Manipulação de dados
    - **Python** - Lógica de negócio
    - **API REST** - Integração externa
    - **AI/LLM** - Assistente inteligente
    
    **Funcionalidades:**
    - Integração com API externa
    - Chat AI para assistência
    - Armazenamento em sessão (planejamento)
    - Exportação para CSV
    - Filtros e buscas
    - Interface responsiva
    
    **API Endpoints:**
    - `/ingredients/` - Gerenciamento de ingredientes
    - `/recipes/` - Gerenciamento de receitas
    - `/chat/invoke` - Chat AI
    - `/` - Health check
    """
    )

# Footer
st.markdown("---")
st.markdown("*Desenvolvido com ❤️ usando Streamlit e integrado com API externa*")
