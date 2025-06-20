from unittest.mock import Mock, patch

import pytest
import requests

from api_client import MenuMVPAPIClient


class TestMenuMVPAPIClient:
    """Testes para o cliente da API Menu MVP"""

    def setup_method(self):
        """Configuração para cada teste"""
        self.client = MenuMVPAPIClient("https://test-api.com")
        self.mock_response = Mock()
        self.mock_response.json.return_value = {"status": "success"}

    def test_init_with_trailing_slash(self):
        """Testa inicialização com URL terminando em /"""
        client = MenuMVPAPIClient("https://test-api.com/")
        assert client.base_url == "https://test-api.com"

    def test_init_without_trailing_slash(self):
        """Testa inicialização com URL sem /"""
        client = MenuMVPAPIClient("https://test-api.com")
        assert client.base_url == "https://test-api.com"

    @patch("requests.Session.get")
    def test_make_request_get_success(self, mock_get):
        """Testa requisição GET bem-sucedida"""
        mock_get.return_value = self.mock_response
        mock_get.return_value.raise_for_status.return_value = None

        result = self.client._make_request("GET", "/test")

        assert result == {"status": "success"}
        mock_get.assert_called_once_with("https://test-api.com/test")

    @patch("requests.Session.post")
    def test_make_request_post_success(self, mock_post):
        """Testa requisição POST bem-sucedida"""
        mock_post.return_value = self.mock_response
        mock_post.return_value.raise_for_status.return_value = None

        data = {"test": "data"}
        result = self.client._make_request("POST", "/test", data)

        assert result == {"status": "success"}
        mock_post.assert_called_once_with("https://test-api.com/test", json=data)

    @patch("requests.Session.get")
    def test_make_request_http_error(self, mock_get):
        """Testa tratamento de erro HTTP"""
        mock_get.return_value.raise_for_status.side_effect = requests.HTTPError("404")

        with pytest.raises(Exception) as exc_info:
            self.client._make_request("GET", "/test")

        assert "Erro na requisição" in str(exc_info.value)

    def test_make_request_invalid_method(self):
        """Testa método HTTP inválido"""
        with pytest.raises(ValueError) as exc_info:
            self.client._make_request("INVALID", "/test")

        assert "Método HTTP não suportado" in str(exc_info.value)

    @patch.object(MenuMVPAPIClient, "_make_request")
    def test_get_ingredients(self, mock_make_request):
        """Testa busca de ingredientes"""
        mock_make_request.return_value = [{"id": 1, "name": "Tomate"}]

        result = self.client.get_ingredients()

        assert result == [{"id": 1, "name": "Tomate"}]
        mock_make_request.assert_called_once_with("GET", "/ingredients/")

    @patch.object(MenuMVPAPIClient, "_make_request")
    def test_create_ingredient(self, mock_make_request):
        """Testa criação de ingrediente"""
        mock_make_request.return_value = {"id": 1, "name": "Tomate"}

        result = self.client.create_ingredient("Tomate")

        assert result == {"id": 1, "name": "Tomate"}
        mock_make_request.assert_called_once_with(
            "POST", "/ingredients/", {"name": "Tomate"}
        )

    @patch.object(MenuMVPAPIClient, "_make_request")
    def test_get_ingredient(self, mock_make_request):
        """Testa busca de ingrediente específico"""
        mock_make_request.return_value = {"id": 1, "name": "Tomate"}

        result = self.client.get_ingredient(1)

        assert result == {"id": 1, "name": "Tomate"}
        mock_make_request.assert_called_once_with("GET", "/ingredients/1")

    @patch.object(MenuMVPAPIClient, "_make_request")
    def test_update_ingredient(self, mock_make_request):
        """Testa atualização de ingrediente"""
        mock_make_request.return_value = {"id": 1, "name": "Tomate Atualizado"}

        result = self.client.update_ingredient(1, "Tomate Atualizado")

        assert result == {"id": 1, "name": "Tomate Atualizado"}
        mock_make_request.assert_called_once_with(
            "PUT", "/ingredients/1", {"name": "Tomate Atualizado"}
        )

    @patch.object(MenuMVPAPIClient, "_make_request")
    def test_delete_ingredient(self, mock_make_request):
        """Testa exclusão de ingrediente"""
        mock_make_request.return_value = {"status": "deleted"}

        result = self.client.delete_ingredient(1)

        assert result == {"status": "deleted"}
        mock_make_request.assert_called_once_with("DELETE", "/ingredients/1")

    @patch.object(MenuMVPAPIClient, "_make_request")
    def test_get_recipes(self, mock_make_request):
        """Testa busca de receitas"""
        mock_make_request.return_value = [{"id": 1, "name": "Receita Teste"}]

        result = self.client.get_recipes()

        assert result == [{"id": 1, "name": "Receita Teste"}]
        mock_make_request.assert_called_once_with("GET", "/recipes/")

    @patch.object(MenuMVPAPIClient, "_make_request")
    def test_get_recipe_by_name(self, mock_make_request):
        """Testa busca de receita por nome"""
        mock_make_request.return_value = {"id": 1, "name": "Receita Teste"}

        result = self.client.get_recipe_by_name("Receita Teste")

        assert result == {"id": 1, "name": "Receita Teste"}
        mock_make_request.assert_called_once_with("GET", "/recipes/Receita Teste")

    @patch.object(MenuMVPAPIClient, "_make_request")
    def test_create_recipe(self, mock_make_request):
        """Testa criação de receita"""
        mock_make_request.return_value = {"id": 1, "name": "Receita Teste"}
        ingredients = [{"name": "Tomate", "quantity": 2}]

        result = self.client.create_recipe("Receita Teste", "Instruções", ingredients)

        expected_data = {
            "name": "Receita Teste",
            "instructions": "Instruções",
            "ingredients": ingredients,
        }
        assert result == {"id": 1, "name": "Receita Teste"}
        mock_make_request.assert_called_once_with("POST", "/recipes/", expected_data)

    @patch.object(MenuMVPAPIClient, "_make_request")
    def test_create_recipes_bulk(self, mock_make_request):
        """Testa criação de múltiplas receitas"""
        recipes = [{"name": "Receita 1"}, {"name": "Receita 2"}]
        mock_make_request.return_value = [{"id": 1}, {"id": 2}]

        result = self.client.create_recipes_bulk(recipes)

        assert result == [{"id": 1}, {"id": 2}]
        mock_make_request.assert_called_once_with("POST", "/recipes/bulk", recipes)

    @patch.object(MenuMVPAPIClient, "_make_request")
    def test_delete_recipe(self, mock_make_request):
        """Testa exclusão de receita"""
        mock_make_request.return_value = {"status": "deleted"}

        result = self.client.delete_recipe(1)

        assert result == {"status": "deleted"}
        mock_make_request.assert_called_once_with("DELETE", "/recipes/id/1")

    @patch.object(MenuMVPAPIClient, "_make_request")
    def test_chat(self, mock_make_request):
        """Testa envio de mensagem para chat"""
        mock_make_request.return_value = {"response": "Olá!"}

        result = self.client.chat("Olá", "thread-123")

        expected_data = {"message": "Olá", "thread_id": "thread-123"}
        assert result == {"response": "Olá!"}
        mock_make_request.assert_called_once_with("POST", "/chat/invoke", expected_data)

    @patch.object(MenuMVPAPIClient, "_make_request")
    def test_chat_stream(self, mock_make_request):
        """Testa envio de mensagem para chat com streaming"""
        mock_make_request.return_value = {"response": "Olá!"}

        result = self.client.chat_stream("Olá", "thread-123")

        expected_data = {"message": "Olá", "thread_id": "thread-123"}
        assert result == {"response": "Olá!"}
        mock_make_request.assert_called_once_with(
            "POST", "/chat/stream-sse", expected_data
        )

    @patch.object(MenuMVPAPIClient, "_make_request")
    def test_health_check(self, mock_make_request):
        """Testa verificação de saúde da API"""
        mock_make_request.return_value = {"status": "healthy"}

        result = self.client.health_check()

        assert result == {"status": "healthy"}
        mock_make_request.assert_called_once_with("GET", "/")


class TestAPIClientGlobal:
    """Testes para a instância global do cliente"""

    def test_global_instance_exists(self):
        """Testa se a instância global existe"""
        from api_client import api_client

        assert isinstance(api_client, MenuMVPAPIClient)

    def test_global_instance_default_url(self):
        """Testa se a instância global usa a URL padrão"""
        from api_client import api_client

        assert api_client.base_url == "https://menu-mvp-api.onrender.com"
