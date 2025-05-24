import streamlit as st
import base64
import pandas as pd
import json
import os
import unicodedata
from datetime import datetime

# Funções auxiliares
def remover_acentos(texto):
    return ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))

def substituir_espacos_por_underscores(texto):
    return texto.replace(" ", "_")

# Estilização
st.markdown("""
    <style>
        .block-container {
            padding-top: 0;
            width: 60% !important;
            max-width: 60% !important;
            height: 40% !important;
            max-height: 40% !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("PÁGINA DE CADASTRO DE ROTINAS")

# Inicializa variáveis de estado
if "cadastro_realizado" not in st.session_state:
    st.session_state.cadastro_realizado = False

# Formulário
if not st.session_state.cadastro_realizado:
    with st.form("form_cadastro", clear_on_submit=True):
        nome_rotina = st.text_input("Nome da Rotina")
        frequencia = st.selectbox("Frequência de Execução", ["Diário", "Semanal", "Quinzenal", "Mensal"])
        analista = st.text_input("Analista Responsável")
        email_analista = st.text_input("Email do Analista Responsável")
        coordenacao = st.selectbox("Coordenação", ["Análise PF", "Análise PJ", "Score & Risco", "Performance de Modelos", "Fraude PF", "Inteligência de Fraudes", "Contratos & Garantias", "Monitoramento de Carteiras", "Indicadores & BI", "Governança de Dados"])
        gerencia = st.selectbox("Gerência", ["Análise de Crédito", "Modelagem de Risco","Prevenção à Fraude","Crédito Operacional","Planejamento de Crédito"])
        
        submitted = st.form_submit_button("Cadastrar")

    # Lógica de cadastro
    if submitted:
        pasta_logs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados\logs")
        os.makedirs(pasta_logs, exist_ok=True)

        nome_arquivo = f"{substituir_espacos_por_underscores(remover_acentos(nome_rotina))}_log.xlsx"
        path_arquivo = os.path.join(pasta_logs, nome_arquivo)

        novo_registro = {
            "Nome da Rotina": substituir_espacos_por_underscores(remover_acentos(nome_rotina)),
            "Frequencia": remover_acentos(frequencia),
            "Analista Responsavel": remover_acentos(analista),
            "Email Analista Responsavel": email_analista,
            "Coordenacao": remover_acentos(coordenacao),
            "Gerencia": remover_acentos(gerencia),
            "Path": path_arquivo
        }

        # Log inicial
        if not os.path.exists(path_arquivo):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            df_log = pd.DataFrame([{
                "start_time": now,
                "end_time": now,
                "status": "ERROR",
                "error_description": "cadastro novo, aguardando log",
                "results": 0
            }])
            df_log.to_excel(path_arquivo, index=False, engine="openpyxl")

        # Atualiza JSON
        json_file = r"C:\Users\dgsou\Desktop\GITHUB\DADOS\PROJETOS\cmmd\dados\dados_rotinas.json"
        if os.path.exists(json_file):
            try:
                with open(json_file, "r") as file:
                    dados_existentes = json.load(file)
            except json.JSONDecodeError:
                dados_existentes = []
        else:
            dados_existentes = []

        dados_existentes.append(novo_registro)

        with open(json_file, "w") as file:
            json.dump(dados_existentes, file, indent=4)

        st.session_state.cadastro_realizado = True
        st.rerun()  # Atualiza a interface (limpa formulário)

# Mensagem de sucesso e botão para reiniciar o formulário
else:
    st.success("✅ Rotina cadastrada com sucesso!")
    if st.button("Nova Rotina"):
        st.session_state.cadastro_realizado = False
        st.rerun()
