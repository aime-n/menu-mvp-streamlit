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


def test_page_config_called(mock_streamlit):
    """Testa se set_page_config é chamado com os parâmetros corretos"""
    # Remove o módulo app se já foi importado
    if "app" in sys.modules:
        del sys.modules["app"]

    # Importa o app (isso executa o código)
    import app  # noqa: F401

    # Verifica se set_page_config foi chamado
    mock_streamlit["page_config"].assert_called_once_with(
        page_title="Menu MVP", page_icon="🍽️", layout="centered"
    )


def test_title_called(mock_streamlit):
    """Testa se o título é exibido corretamente"""
    # Remove o módulo app se já foi importado
    if "app" in sys.modules:
        del sys.modules["app"]

    # Importa o app
    import app  # noqa: F401

    # Verifica se title foi chamado com o texto correto
    mock_streamlit["title"].assert_called_once_with("Menu MVP Streamlit")


def test_welcome_message_called(mock_streamlit):
    """Testa se a mensagem de boas-vindas é exibida"""
    # Remove o módulo app se já foi importado
    if "app" in sys.modules:
        del sys.modules["app"]

    # Importa o app
    import app  # noqa: F401

    # Verifica se write foi chamado com a mensagem de boas-vindas
    mock_streamlit["write"].assert_called_once_with(
        "Bem-vindo ao Menu MVP! Esta é uma base para sua aplicação Streamlit."
    )


def test_text_input_called(mock_streamlit):
    """Testa se o input de texto é criado"""
    # Remove o módulo app se já foi importado
    if "app" in sys.modules:
        del sys.modules["app"]

    # Importa o app
    import app  # noqa: F401

    # Verifica se text_input foi chamado com o label correto
    mock_streamlit["text_input"].assert_called_once_with("Qual o seu nome?")


def test_success_message_with_name(mock_streamlit):
    """Testa se a mensagem de sucesso é exibida quando um nome é fornecido"""
    # Remove o módulo app se já foi importado
    if "app" in sys.modules:
        del sys.modules["app"]

    # Configura o mock para retornar um nome
    mock_streamlit["text_input"].return_value = "João"

    # Importa o app
    import app  # noqa: F401

    # Verifica se success foi chamado com a mensagem correta
    mock_streamlit["success"].assert_called_once_with(
        "Olá, João! Seja bem-vindo à sua página Streamlit."
    )


def test_no_success_message_without_name(mock_streamlit):
    """Testa se a mensagem de sucesso não é exibida quando nenhum nome é fornecido"""
    # Remove o módulo app se já foi importado
    if "app" in sys.modules:
        del sys.modules["app"]

    # Configura o mock para retornar None (sem nome)
    mock_streamlit["text_input"].return_value = None

    # Importa o app
    import app  # noqa: F401

    # Verifica se success NÃO foi chamado
    mock_streamlit["success"].assert_not_called()


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
