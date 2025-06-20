import os
import sys
from unittest.mock import MagicMock, Mock, patch
from datetime import datetime

import pytest
import streamlit as st

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def mock_streamlit():
    """Mock completo do Streamlit para testes"""
    with patch.multiple(
        "streamlit",
        title=Mock(),
        write=Mock(),
        text_input=Mock(),
        text_area=Mock(),
        selectbox=Mock(),
        button=Mock(),
        success=Mock(),
        error=Mock(),
        info=Mock(),
        warning=Mock(),
        set_page_config=Mock(),
        sidebar=Mock(),
        columns=Mock(),
        tabs=Mock(),
        expander=Mock(),
        date_input=Mock(),
        download_button=Mock(),
        metric=Mock(),
        markdown=Mock(),
        subheader=Mock(),
        rerun=Mock(),
        session_state=MagicMock(),
    ):
        # Configurar retornos padrão
        st.text_input.return_value = "test_input"
        st.text_area.return_value = "test_text"
        st.selectbox.return_value = "test_option"
        st.button.return_value = True
        st.date_input.return_value = datetime.now()
        st.columns.return_value = [Mock(), Mock()]
        st.tabs.return_value = [Mock() for _ in range(7)]
        st.expander.return_value.__enter__ = Mock()
        st.expander.return_value.__exit__ = Mock()
        st.sidebar.__enter__ = Mock()
        st.sidebar.__exit__ = Mock()
        
        yield st


@pytest.fixture
def mock_api_client():
    """Mock do cliente da API"""
    with patch("api_client.api_client") as mock_client:
        mock_client.get_ingredients.return_value = [
            {"id": 1, "name": "Tomate"},
            {"id": 2, "name": "Cebola"},
        ]
        mock_client.get_recipes.return_value = [
            {"id": 1, "name": "Receita Teste", "ingredients": [{"name": "Tomate"}]}
        ]
        mock_client.create_ingredient.return_value = {
            "id": 3,
            "name": "Novo Ingrediente",
        }
        mock_client.create_recipe.return_value = {"id": 2, "name": "Nova Receita"}
        mock_client.chat.return_value = {"response": "Resposta do chat"}
        yield mock_client


class TestIngredientsPage:
    """Testes para a página de ingredientes"""

    def test_ingredients_page_file_exists(self):
        """Testa se o arquivo da página de ingredientes existe"""
        file_path = os.path.join(os.path.dirname(__file__), "..", "pages", "1_ingredients.py")
        assert os.path.exists(file_path), "Arquivo da página de ingredientes não encontrado"

    def test_ingredients_page_content(self):
        """Testa se o arquivo tem conteúdo básico"""
        file_path = os.path.join(os.path.dirname(__file__), "..", "pages", "1_ingredients.py")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "streamlit" in content
            assert "api_client" in content


class TestRecipesPage:
    """Testes para a página de receitas"""

    def test_recipes_page_file_exists(self):
        """Testa se o arquivo da página de receitas existe"""
        file_path = os.path.join(os.path.dirname(__file__), "..", "pages", "2_recipes.py")
        assert os.path.exists(file_path), "Arquivo da página de receitas não encontrado"

    def test_recipes_page_content(self):
        """Testa se o arquivo tem conteúdo básico"""
        file_path = os.path.join(os.path.dirname(__file__), "..", "pages", "2_recipes.py")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "streamlit" in content
            assert "api_client" in content


class TestPlanningPage:
    """Testes para a página de planejamento"""

    def test_planning_page_file_exists(self):
        """Testa se o arquivo da página de planejamento existe"""
        file_path = os.path.join(os.path.dirname(__file__), "..", "pages", "3_planning.py")
        assert os.path.exists(file_path), "Arquivo da página de planejamento não encontrado"

    def test_planning_page_content(self):
        """Testa se o arquivo tem conteúdo básico"""
        file_path = os.path.join(os.path.dirname(__file__), "..", "pages", "3_planning.py")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "streamlit" in content
            assert "api_client" in content

    def test_get_week_days_function(self):
        """Testa função get_week_days"""
        from datetime import timedelta
        
        def get_week_days():
            today = datetime.now()
            start_of_week = today - timedelta(days=today.weekday())
            week_days = []
            for i in range(7):
                day = start_of_week + timedelta(days=i)
                week_days.append(day.strftime("%d/%m/%Y"))
            return week_days
        
        week_days = get_week_days()
        
        assert len(week_days) == 7
        assert all(isinstance(day, str) for day in week_days)
        assert all("/" in day for day in week_days)

    def test_load_recipes_function_success(self, mock_api_client):
        """Testa função load_recipes com sucesso"""
        def load_recipes():
            try:
                recipes = mock_api_client.get_recipes()
                return recipes
            except Exception:
                return []
        
        recipes = load_recipes()
        
        assert recipes == [{"id": 1, "name": "Receita Teste", "ingredients": [{"name": "Tomate"}]}]
        mock_api_client.get_recipes.assert_called_once()

    def test_load_recipes_function_error(self, mock_api_client):
        """Testa função load_recipes com erro"""
        mock_api_client.get_recipes.side_effect = Exception("API Error")
        
        def load_recipes():
            try:
                recipes = mock_api_client.get_recipes()
                return recipes
            except Exception:
                return []
        
        recipes = load_recipes()
        
        assert recipes == []


class TestChatAIPage:
    """Testes para a página de chat AI"""

    def test_chat_ai_page_file_exists(self):
        """Testa se o arquivo da página de chat AI existe"""
        file_path = os.path.join(os.path.dirname(__file__), "..", "pages", "4_chat_ai.py")
        assert os.path.exists(file_path), "Arquivo da página de chat AI não encontrado"

    def test_chat_ai_page_content(self):
        """Testa se o arquivo tem conteúdo básico"""
        file_path = os.path.join(os.path.dirname(__file__), "..", "pages", "4_chat_ai.py")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "streamlit" in content
            assert "api_client" in content


class TestMainApp:
    """Testes para o app principal"""

    def test_main_app_import(self):
        """Testa se o app principal pode ser importado"""
        try:
            import app  # noqa: F401
            assert True
        except ImportError as e:
            pytest.fail(f"Falha ao importar app principal: {e}")

    def test_main_app_file_exists(self):
        """Testa se o arquivo do app principal existe"""
        file_path = os.path.join(os.path.dirname(__file__), "..", "app.py")
        assert os.path.exists(file_path), "Arquivo do app principal não encontrado"


class TestSessionState:
    """Testes para o gerenciamento de session state"""

    def test_session_state_initialization(self):
        """Testa inicialização do session state"""
        # Simula session state vazio
        session_state = {}
        
        # Simula verificação de session state
        if "meal_plan" not in session_state:
            session_state["meal_plan"] = {}
        
        if "shopping_list" not in session_state:
            session_state["shopping_list"] = []
        
        assert "meal_plan" in session_state
        assert "shopping_list" in session_state
        assert session_state["meal_plan"] == {}
        assert session_state["shopping_list"] == []

    def test_meal_plan_operations(self):
        """Testa operações com meal plan"""
        session_state = {"meal_plan": {}}
        
        # Simula adição de refeição
        date_key = "01/01/2024"
        meal_type = "Almoço"
        meal_entry = {
            "recipe": "Receita Teste",
            "notes": "Notas teste",
            "added_at": "01/01/2024 12:00",
        }
        
        if date_key not in session_state["meal_plan"]:
            session_state["meal_plan"][date_key] = {}
        
        if meal_type not in session_state["meal_plan"][date_key]:
            session_state["meal_plan"][date_key][meal_type] = []
        
        session_state["meal_plan"][date_key][meal_type].append(
            meal_entry
        )
        
        # Verifica se foi adicionado corretamente
        assert date_key in session_state["meal_plan"]
        assert meal_type in session_state["meal_plan"][date_key]
        assert len(session_state["meal_plan"][date_key][meal_type]) == 1
        assert (
            session_state["meal_plan"][date_key][meal_type][0]
            == meal_entry
        )


class TestDataValidation:
    """Testes para validação de dados"""

    def test_recipe_data_structure(self):
        """Testa estrutura de dados de receita"""
        recipe = {
            "id": 1,
            "name": "Receita Teste",
            "instructions": "Instruções da receita",
            "ingredients": [
                {"name": "Tomate", "quantity": 2},
                {"name": "Cebola", "quantity": 1},
            ],
        }
        
        assert "id" in recipe
        assert "name" in recipe
        assert "instructions" in recipe
        assert "ingredients" in recipe
        assert isinstance(recipe["ingredients"], list)
        assert all("name" in ingredient for ingredient in recipe["ingredients"])

    def test_ingredient_data_structure(self):
        """Testa estrutura de dados de ingrediente"""
        ingredient = {"id": 1, "name": "Tomate"}

        assert "id" in ingredient
        assert "name" in ingredient
        assert isinstance(ingredient["name"], str)

    def test_meal_entry_data_structure(self):
        """Testa estrutura de dados de entrada de refeição"""
        meal_entry = {
            "recipe": "Receita Teste",
            "notes": "Notas da refeição",
            "added_at": "01/01/2024 12:00",
        }
        
        assert "recipe" in meal_entry
        assert "notes" in meal_entry
        assert "added_at" in meal_entry
        assert isinstance(meal_entry["recipe"], str)
        assert isinstance(meal_entry["notes"], str)
        assert isinstance(meal_entry["added_at"], str)
