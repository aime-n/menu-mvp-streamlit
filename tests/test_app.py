import os
import sys
from unittest.mock import patch

import pytest

# Adiciona o diretório raiz ao path para importar o app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# Mock do Streamlit para testes
@pytest.fixture
def mock_streamlit():
    """Mock do Streamlit para testes unitários"""
    with (
        patch("streamlit.title") as mock_title,
        patch("streamlit.write") as mock_write,
        patch("streamlit.text_input") as mock_text_input,
        patch("streamlit.success") as mock_success,
        patch("streamlit.set_page_config") as mock_page_config,
    ):

        # Configura os mocks para retornar valores padrão
        mock_text_input.return_value = "Teste"
        mock_title.return_value = None
        mock_write.return_value = None
        mock_success.return_value = None
        mock_page_config.return_value = None

        yield {
            "title": mock_title,
            "write": mock_write,
            "text_input": mock_text_input,
            "success": mock_success,
            "page_config": mock_page_config,
        }


def test_app_imports_correctly():
    """Testa se o app pode ser importado sem erros"""
    try:
        # Remove o módulo app se já foi importado
        if "app" in sys.modules:
            del sys.modules["app"]

        import app  # noqa: F401

        assert True  # Se chegou aqui, a importação foi bem-sucedida
    except ImportError as e:
        pytest.fail(f"Falha ao importar app: {e}")


def test_streamlit_available():
    """Testa se o Streamlit está disponível"""
    try:
        import streamlit  # noqa: F401

        assert True
    except ImportError:
        pytest.fail("Streamlit não está instalado")


if __name__ == "__main__":
    pytest.main([__file__])
