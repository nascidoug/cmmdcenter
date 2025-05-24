import streamlit as st
import base64

# Codifica a imagem em base64
image_path = "img/itau-light.png"
with open(image_path, "rb") as img_file:
    img_base64 = base64.b64encode(img_file.read()).decode()

# Estilização Header
st.markdown(f"""
    <style>
        /* Ajustar o fundo e o tamanho da block-container */
        .block-container {{
            width: 100% !important; /* Preenche toda a largura */
            max-width: 100% !important; /* Garante que não haja limite de largura */
            height: 100% !important;
            max-height: 100% !important;
        }}
""", unsafe_allow_html=True)

st.title("PÁGINA DE INSERÇÃO DE LOG")

with st.form("form_log"):
    nome_rotina = st.text_input("Nome da Rotina")
    frequencia = st.selectbox("Frequência de Execução", ["Diário", "Semanal", "Quinzenal", "Mensal"])
    time_start = st.text_input("Inicío da Execução da Rotina")
    time_end = st.text_input("Término da Execução da Rotina")
    resultado = st.text_input("Volume Analisado")
    analista = st.text_input("Analista Responsável")
    coordenador = st.text_input("Coordenador")
    gerente = st.text_input("Gerente")
    
    submitted = st.form_submit_button("Cadastrar")

# Submissão do formulário alimenta JSON e cria o arquivo Excel
# if submitted:



