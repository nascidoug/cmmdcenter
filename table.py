#Esta classe é responsável por exibir a tabela;

import streamlit as st

class Table:
    @staticmethod
    def render(rotinas_filtradas):
        #Cria uma linha divisória
        st.markdown("---")

        #Seleciona as colunas a serem exibidas
        tabela_final = rotinas_filtradas[[
            "Nome da Rotina", "Frequencia","Última Execução", "Intervalo (dias)", "Status", 
            "Resultado", "Descricao Erro", "Analista Responsavel", "Coordenacao", "Gerencia"
        ]]
        st.dataframe(tabela_final, use_container_width=True)
