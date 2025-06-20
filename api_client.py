import json
from datetime import datetime
from typing import Dict, List, Optional

import requests


class MenuMVPAPIClient:
    """Cliente para a API do Menu MVP"""

    def __init__(self, base_url: str = "https://menu-mvp-api.onrender.com"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def _make_request(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> Dict:
        """Faz uma requisição para a API"""
        url = f"{self.base_url}{endpoint}"

        try:
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url)
            else:
                raise ValueError(f"Método HTTP não suportado: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro na requisição para {url}: {str(e)}")

    # Métodos para Ingredientes
    def get_ingredients(self) -> List[Dict]:
        """Busca todos os ingredientes"""
        return self._make_request("GET", "/ingredients/")

    def create_ingredient(self, name: str) -> Dict:
        """Cria um novo ingrediente"""
        data = {"name": name}
        return self._make_request("POST", "/ingredients/", data)

    def get_ingredient(self, ingredient_id: int) -> Dict:
        """Busca um ingrediente específico"""
        return self._make_request("GET", f"/ingredients/{ingredient_id}")

    def update_ingredient(self, ingredient_id: int, name: str) -> Dict:
        """Atualiza um ingrediente"""
        data = {"name": name}
        return self._make_request("PUT", f"/ingredients/{ingredient_id}", data)

    def delete_ingredient(self, ingredient_id: int) -> Dict:
        """Deleta um ingrediente"""
        return self._make_request("DELETE", f"/ingredients/{ingredient_id}")

    # Métodos para Receitas
    def get_recipes(self) -> List[Dict]:
        """Busca todas as receitas"""
        return self._make_request("GET", "/recipes/")

    def get_recipe_by_name(self, recipe_name: str) -> Dict:
        """Busca uma receita pelo nome"""
        return self._make_request("GET", f"/recipes/{recipe_name}")

    def create_recipe(
        self, name: str, instructions: str, ingredients: List[Dict]
    ) -> Dict:
        """Cria uma nova receita"""
        data = {"name": name, "instructions": instructions, "ingredients": ingredients}
        return self._make_request("POST", "/recipes/", data)

    def create_recipes_bulk(self, recipes: List[Dict]) -> List[Dict]:
        """Cria múltiplas receitas de uma vez"""
        return self._make_request("POST", "/recipes/bulk", recipes)

    def delete_recipe(self, recipe_id: int) -> Dict:
        """Deleta uma receita"""
        return self._make_request("DELETE", f"/recipes/id/{recipe_id}")

    # Métodos para Chat/AI
    def chat(self, message: str, thread_id: str) -> Dict:
        """Envia uma mensagem para o chat AI"""
        data = {"message": message, "thread_id": thread_id}
        return self._make_request("POST", "/chat/invoke", data)

    def chat_stream(self, message: str, thread_id: str) -> Dict:
        """Envia uma mensagem para o chat AI com streaming"""
        data = {"message": message, "thread_id": thread_id}
        return self._make_request("POST", "/chat/stream-sse", data)

    def health_check(self) -> Dict:
        """Verifica se a API está funcionando"""
        return self._make_request("GET", "/")


# Instância global do cliente
api_client = MenuMVPAPIClient()
