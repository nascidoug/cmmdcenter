# Esse script é responsável por criar a página/dashboard, para isso ele faz referência a outros scripts:
# - dala_loader: script responsável pelo carregamento das rotinas cadastradas (json);
# - utils: script responsável pelo cálculo/processamento/enriquecimento com base nos registros de log encontrados a partir do path registrado no json;
# - renderer: script responsável por renderizar (exibir) os dados processados no dashboard Streamlit;


import streamlit as st
from streamlit_autorefresh import st_autorefresh
from data_loader import DataLoader
from utils import DataProcessor
from renderer import Renderer

#Define o layout da tela (largura total) e a frequência de atualização da página (6000milisegundos = 6 segundos)
st.set_page_config(layout="wide")
st_autorefresh(interval=6000, limit=None, key="autorefresh")

st.title("📊 Página Principal - Command Center")

#Define um arquivo para um arquivo json (cadastro de rotinas) e executa o carregamento dos dados a partir da classe DataLoader
json_path = r"C:\Users\dgsou\Desktop\GITHUB\DADOS\PROJETOS\cmmd\dados\dados_rotinas.json"
data_loader = DataLoader(json_path)
rotinas = data_loader.rotinas

#Condição que define o que será carregado na página:
# caso esteja tudo certo:
# - utiliza a classe DataProcessor para executar os cáluclos/lógica de monitoramento;
# - executa a classe Rederer para Renderizar as visualizações (filtro, tabela, cards, gráficos);
# em caso de não encontrar o arquivo de cadastro ou o arquivo estar vazio, retorna uma mensagem.
if not rotinas.empty:
    rotinas = DataProcessor.process_rotinas(rotinas)
    Renderer(rotinas).render()
else:
    st.warning("⚠️ Nenhuma rotina cadastrada ou arquivo não encontrado.")
