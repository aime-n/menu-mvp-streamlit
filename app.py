import streamlit as st

st.set_page_config(page_title="Menu MVP", page_icon="🍽️", layout="centered")

st.title("Menu MVP Streamlit")
st.write("Bem-vindo ao Menu MVP! Esta é uma base para sua aplicação Streamlit.")

# Exemplo de input
nome = st.text_input("Qual o seu nome?")

if nome:
    st.success(f"Olá, {nome}! Seja bem-vindo à sua página Streamlit.") 