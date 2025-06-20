import os
import sys
from datetime import datetime
from unittest.mock import Mock, patch
import warnings

import pytest

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

warnings.filterwarnings("ignore", message=".*ScriptRunContext.*")


class TestAPIIntegration:
    """Testes de integração com a API"""

    def test_api_client_creation(self):
        """Testa criação do cliente da API"""
        from api_client import MenuMVPAPIClient

        client = MenuMVPAPIClient("https://test-api.com")
        assert client.base_url == "https://test-api.com"
        assert hasattr(client, "session")

    def test_api_client_default_url(self):
        """Testa URL padrão do cliente da API"""
        from api_client import MenuMVPAPIClient

        client = MenuMVPAPIClient()
        assert client.base_url == "https://menu-mvp-api.onrender.com"

    @patch("requests.Session.get")
    def test_api_health_check(self, mock_get):
        """Testa health check da API"""
        from api_client import MenuMVPAPIClient

        # Mock da resposta
        mock_response = Mock()
        mock_response.json.return_value = {"status": "healthy"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = MenuMVPAPIClient("https://test-api.com")
        result = client.health_check()

        assert result == {"status": "healthy"}
        mock_get.assert_called_once_with("https://test-api.com/")

    @patch("requests.Session.get")
    def test_get_ingredients(self, mock_get):
        """Testa busca de ingredientes"""
        from api_client import MenuMVPAPIClient

        # Mock da resposta
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "name": "Tomate"},
            {"id": 2, "name": "Cebola"},
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = MenuMVPAPIClient("https://test-api.com")
        result = client.get_ingredients()

        assert len(result) == 2
        assert result[0]["name"] == "Tomate"
        assert result[1]["name"] == "Cebola"

    @patch("requests.Session.get")
    def test_get_recipes(self, mock_get):
        """Testa busca de receitas"""
        from api_client import MenuMVPAPIClient

        # Mock da resposta
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "name": "Receita Teste", "ingredients": [{"name": "Tomate"}]}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = MenuMVPAPIClient("https://test-api.com")
        result = client.get_recipes()

        assert len(result) == 1
        assert result[0]["name"] == "Receita Teste"
        assert len(result[0]["ingredients"]) == 1


class TestDataStructures:
    """Testes para estruturas de dados"""

    def test_recipe_structure(self):
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

        # Verifica campos obrigatórios
        required_fields = ["id", "name", "instructions", "ingredients"]
        for field in required_fields:
            assert field in recipe, f"Campo obrigatório '{field}' não encontrado"

        # Verifica tipos
        assert isinstance(recipe["id"], int)
        assert isinstance(recipe["name"], str)
        assert isinstance(recipe["instructions"], str)
        assert isinstance(recipe["ingredients"], list)

        # Verifica ingredientes
        for ingredient in recipe["ingredients"]:
            assert "name" in ingredient
            assert isinstance(ingredient["name"], str)

    def test_ingredient_structure(self):
        """Testa estrutura de dados de ingrediente"""
        ingredient = {"id": 1, "name": "Tomate"}

        # Verifica campos obrigatórios
        required_fields = ["id", "name"]
        for field in required_fields:
            assert field in ingredient, f"Campo obrigatório '{field}' não encontrado"

        # Verifica tipos
        assert isinstance(ingredient["id"], int)
        assert isinstance(ingredient["name"], str)

    def test_meal_plan_entry_structure(self):
        """Testa estrutura de dados de entrada de planejamento"""
        meal_entry = {
            "recipe": "Receita Teste",
            "notes": "Notas da refeição",
            "added_at": "01/01/2024 12:00",
        }

        # Verifica campos obrigatórios
        required_fields = ["recipe", "notes", "added_at"]
        for field in required_fields:
            assert field in meal_entry, f"Campo obrigatório '{field}' não encontrado"

        # Verifica tipos
        assert isinstance(meal_entry["recipe"], str)
        assert isinstance(meal_entry["notes"], str)
        assert isinstance(meal_entry["added_at"], str)


class TestDateFunctions:
    """Testes para funções de data"""

    def test_week_days_generation(self):
        """Testa geração de dias da semana"""
        from datetime import datetime, timedelta

        def get_week_days():
            today = datetime.now()
            start_of_week = today - timedelta(days=today.weekday())
            week_days = []
            for i in range(7):
                day = start_of_week + timedelta(days=i)
                week_days.append(day.strftime("%d/%m/%Y"))
            return week_days

        week_days = get_week_days()

        # Verifica se retorna 7 dias
        assert len(week_days) == 7

        # Verifica formato da data
        for day in week_days:
            assert "/" in day
            parts = day.split("/")
            assert len(parts) == 3
            assert all(part.isdigit() for part in parts)

    def test_date_formatting(self):
        """Testa formatação de datas"""
        test_date = datetime(2024, 1, 15)
        formatted = test_date.strftime("%d/%m/%Y")

        assert formatted == "15/01/2024"

        # Testa formatação com timestamp
        timestamp = test_date.strftime("%d/%m/%Y %H:%M")
        assert "15/01/2024" in timestamp
        assert ":" in timestamp


class TestSessionStateManagement:
    """Testes para gerenciamento de session state"""

    def test_session_state_initialization(self):
        """Testa inicialização do session state"""
        # Simula session state vazio
        session_state = {}

        # Inicializa campos necessários
        if "meal_plan" not in session_state:
            session_state["meal_plan"] = {}

        if "shopping_list" not in session_state:
            session_state["shopping_list"] = []

        # Verifica inicialização
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

        # Adiciona refeição
        if date_key not in session_state["meal_plan"]:
            session_state["meal_plan"][date_key] = {}

        if meal_type not in session_state["meal_plan"][date_key]:
            session_state["meal_plan"][date_key][meal_type] = []

        session_state["meal_plan"][date_key][meal_type].append(meal_entry)

        # Verifica se foi adicionado corretamente
        assert date_key in session_state["meal_plan"]
        assert meal_type in session_state["meal_plan"][date_key]
        assert len(session_state["meal_plan"][date_key][meal_type]) == 1
        assert session_state["meal_plan"][date_key][meal_type][0] == meal_entry

    def test_shopping_list_operations(self):
        """Testa operações com lista de compras"""
        session_state = {"shopping_list": []}

        # Adiciona item à lista
        item = {
            "ingrediente": "Tomate",
            "receita": "Receita Teste",
            "data": "01/01/2024",
            "refeicao": "Almoço",
        }

        session_state["shopping_list"].append(item)

        # Verifica se foi adicionado
        assert len(session_state["shopping_list"]) == 1
        assert session_state["shopping_list"][0] == item

        # Testa agrupamento por ingrediente
        ingredientes_agrupados = {}
        for item in session_state["shopping_list"]:
            ingrediente = item["ingrediente"]
            if ingrediente not in ingredientes_agrupados:
                ingredientes_agrupados[ingrediente] = []
            ingredientes_agrupados[ingrediente].append(item)

        assert "Tomate" in ingredientes_agrupados
        assert len(ingredientes_agrupados["Tomate"]) == 1


class TestErrorHandling:
    """Testes para tratamento de erros"""

    def test_api_error_handling(self):
        """Testa tratamento de erros da API"""
        from api_client import MenuMVPAPIClient
        
        client = MenuMVPAPIClient("https://invalid-url.com")
        
        # Simula erro de conexão
        with patch("requests.Session.get") as mock_get:
            mock_get.side_effect = Exception("Connection error")
            
            with pytest.raises(Exception) as exc_info:
                client.health_check()
            
            assert "Connection error" in str(exc_info.value)

    def test_invalid_http_method(self):
        """Testa método HTTP inválido"""
        from api_client import MenuMVPAPIClient

        client = MenuMVPAPIClient("https://test-api.com")

        with pytest.raises(ValueError) as exc_info:
            client._make_request("INVALID", "/test")

        assert "Método HTTP não suportado" in str(exc_info.value)


class TestDataValidation:
    """Testes para validação de dados"""

    def test_recipe_validation(self):
        """Testa validação de dados de receita"""

        def validate_recipe(recipe):
            required_fields = ["id", "name", "instructions", "ingredients"]
            for field in required_fields:
                if field not in recipe:
                    return False, f"Campo obrigatório '{field}' não encontrado"

            if not isinstance(recipe["ingredients"], list):
                return False, "Ingredientes deve ser uma lista"

            for ingredient in recipe["ingredients"]:
                if "name" not in ingredient:
                    return False, "Ingrediente deve ter campo 'name'"

            return True, "Receita válida"

        # Teste com receita válida
        valid_recipe = {
            "id": 1,
            "name": "Receita Teste",
            "instructions": "Instruções",
            "ingredients": [{"name": "Tomate"}],
        }

        is_valid, message = validate_recipe(valid_recipe)
        assert is_valid
        assert message == "Receita válida"

        # Teste com receita inválida
        invalid_recipe = {
            "id": 1,
            "name": "Receita Teste",
            # Faltam campos obrigatórios
        }

        is_valid, message = validate_recipe(invalid_recipe)
        assert not is_valid
        assert "Campo obrigatório" in message

    def test_ingredient_validation(self):
        """Testa validação de dados de ingrediente"""

        def validate_ingredient(ingredient):
            required_fields = ["id", "name"]
            for field in required_fields:
                if field not in ingredient:
                    return False, f"Campo obrigatório '{field}' não encontrado"

            if not isinstance(ingredient["name"], str):
                return False, "Nome deve ser uma string"

            if not ingredient["name"].strip():
                return False, "Nome não pode estar vazio"

            return True, "Ingrediente válido"

        # Teste com ingrediente válido
        valid_ingredient = {"id": 1, "name": "Tomate"}
        is_valid, message = validate_ingredient(valid_ingredient)
        assert is_valid
        assert message == "Ingrediente válido"

        # Teste com ingrediente inválido
        invalid_ingredient = {"id": 1, "name": ""}
        is_valid, message = validate_ingredient(invalid_ingredient)
        assert not is_valid
        assert "Nome não pode estar vazio" in message
