#Este Script é responsável por exibir no dashboard:
#- Filtros
#- Indicadores (bignumbers)
#- Tabela
#- Gráficos

import streamlit as st
from metrics import Metrics
from graphs import Graphs
from table import Table

class Renderer:
    def __init__(self, rotinas):
        self.rotinas = rotinas

    #Constrói as listas de opções para os filtros
    def render(self):
        status_options = ["Todos", "OK", "ALERT", "ERROR", "UNKNOWN"]
        gerencia_options = ["Todos"] + sorted(self.rotinas["Gerencia"].dropna().unique().tolist())
        coord_options = ["Todos"] + sorted(self.rotinas["Coordenacao"].dropna().unique().tolist())
        freq_options = ["Todos"] + sorted(self.rotinas["Frequencia"].dropna().unique().tolist())

        #Cria um seletor para cada tipo de filtro
        col1, col2, col3, col4 = st.columns(4)
        status_filtro = col1.selectbox("Status", options=status_options)
        gerencia_filtro = col2.selectbox("Gerência", options=gerencia_options)
        coord_filtro = col3.selectbox("Coordenação", options=coord_options)
        freq_filtro = col4.selectbox("Frequência", options=freq_options)

        #Aplica os filtros 
        rotinas_filtradas = self.rotinas.copy()
        if status_filtro != "Todos":
            rotinas_filtradas = rotinas_filtradas[rotinas_filtradas["Status"] == status_filtro]
        if gerencia_filtro != "Todos":
            rotinas_filtradas = rotinas_filtradas[rotinas_filtradas["Gerencia"] == gerencia_filtro]
        if coord_filtro != "Todos":
            rotinas_filtradas = rotinas_filtradas[rotinas_filtradas["Coordenacao"] == coord_filtro]
        if freq_filtro != "Todos":
            rotinas_filtradas = rotinas_filtradas[rotinas_filtradas["Frequencia"] == freq_filtro]

        #Exibe os componentes no dashboard
        Metrics.render(rotinas_filtradas)
        Graphs.render(rotinas_filtradas)
        Table.render(rotinas_filtradas)
