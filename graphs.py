#Esta classe é responsável por gerar os gráficos;

import streamlit as st
import plotly.express as px

class Graphs:
    @staticmethod
    def render(rotinas_filtradas):
        #Insere uma linha divisória
        st.markdown("---")

        #Organiza os gráficos lado a lado
        col1, col2 = st.columns(2)

        #Cálcula o total de rotinas por status
        status_counts = rotinas_filtradas["Status"].value_counts().reindex(["OK", "ALERT", "ERROR", "UNKNOWN"], fill_value=0)

        #Cria um gráfico de rosca
        with col1:
            fig_pie = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                hole=0.5,
                title="Distribuição de Status",
                color=status_counts.index,
                color_discrete_map={"OK": "green", "ALERT": "orange", "ERROR": "red", "UNKNOWN": "gray"}
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        #cria o gráfico de barras empilhadas
        with col2:
            df_grouped = rotinas_filtradas.groupby(["Status", "Gerencia"]).size().reset_index(name="Total")
            fig_bar = px.bar(
                df_grouped,
                x="Status",
                y="Total",
                color="Gerencia",
                barmode="stack",
                title="Volume por Status e Gerência"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
