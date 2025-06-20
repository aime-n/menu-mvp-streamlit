import os
import sys
import uuid
from datetime import datetime

import streamlit as st

# Adiciona o diretório raiz ao path para importar o api_client
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from api_client import api_client

st.set_page_config(page_title="Chat AI - Menu MVP", page_icon="🤖", layout="wide")

st.title("🤖 Chat AI - Assistente de Menu")
st.markdown("---")

# Inicializar session state para chat
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())


# Função para enviar mensagem para a API
def send_message(message):
    """Envia mensagem para a API de chat"""
    try:
        response = api_client.chat(message, st.session_state.thread_id)
        return response
    except Exception as e:
        st.error(f"Erro ao enviar mensagem: {str(e)}")
        return None


# Sidebar para configurações
with st.sidebar:
    st.header("⚙️ Configurações")

    # Novo thread
    if st.button("🆕 Nova Conversa"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.chat_messages = []
        st.success("Nova conversa iniciada!")
        st.rerun()

    # Thread ID atual
    st.subheader("📋 Thread ID")
    st.code(st.session_state.thread_id[:8] + "...")

    # Status da API
    st.subheader("🔗 Status da API")
    if st.button("🔄 Verificar"):
        try:
            health = api_client.health_check()
            st.success("✅ API funcionando")
        except Exception as e:
            st.error("❌ Erro na API")

# Área principal do chat
st.header("💬 Conversa com o Assistente")

# Exibir mensagens anteriores
for message in st.session_state.chat_messages:
    if message["type"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant"):
            st.write(message["content"])

# Input para nova mensagem
if prompt := st.chat_input("Digite sua mensagem..."):
    # Adicionar mensagem do usuário
    st.session_state.chat_messages.append(
        {"type": "user", "content": prompt, "timestamp": datetime.now()}
    )

    # Exibir mensagem do usuário
    with st.chat_message("user"):
        st.write(prompt)

    # Enviar para API e exibir resposta
    with st.chat_message("assistant"):
        with st.spinner("🤖 Assistente pensando..."):
            response = send_message(prompt)

            if response and "output" in response:
                assistant_message = response["output"].get(
                    "content", "Desculpe, não consegui processar sua mensagem."
                )
                st.write(assistant_message)

                # Adicionar resposta do assistente
                st.session_state.chat_messages.append(
                    {
                        "type": "assistant",
                        "content": assistant_message,
                        "timestamp": datetime.now(),
                    }
                )
            else:
                st.error("Erro ao obter resposta do assistente")

# Exemplos de prompts
st.markdown("---")
st.header("💡 Exemplos de Prompts")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
    ### 🥕 **Sobre Ingredientes**
    - "Quais ingredientes são essenciais para uma cozinha básica?"
    - "Como substituir ovo em receitas veganas?"
    - "Quais são os melhores temperos para carnes?"
    """
    )

with col2:
    st.markdown(
        """
    ### 👨‍🍳 **Sobre Receitas**
    - "Sugira uma receita fácil para iniciantes"
    - "Como fazer um molho básico para macarrão?"
    - "Receita de bolo de chocolate simples"
    """
    )

with col3:
    st.markdown(
        """
    ### 📅 **Sobre Planejamento**
    - "Como planejar refeições para a semana?"
    - "Dicas para economizar na compra de ingredientes"
    - "Como organizar uma lista de compras eficiente?"
    """
    )

# Informações sobre o assistente
with st.expander("ℹ️ Sobre o Assistente AI"):
    st.markdown(
        """
    **Este assistente AI pode ajudar você com:**
    
    - **Dúvidas sobre ingredientes** - Substituições, conservação, tipos
    - **Sugestões de receitas** - Baseadas nos ingredientes disponíveis
    - **Dicas de culinária** - Técnicas, truques e melhores práticas
    - **Planejamento de refeições** - Organização e economia
    - **Informações nutricionais** - Sobre ingredientes e receitas
    
    **Como usar:**
    1. Digite sua pergunta na caixa de chat
    2. Aguarde a resposta do assistente
    3. Continue a conversa fazendo mais perguntas
    4. Use "Nova Conversa" para começar do zero
    """
    )

# Footer
st.markdown("---")
st.markdown("*Assistente AI integrado com a API do Menu MVP*")
