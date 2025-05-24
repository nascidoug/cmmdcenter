#Esta classe é responsável por criar as métricas/bignumbers

import streamlit as st

class Metrics:
    @staticmethod
    def render(rotinas_filtradas):
        #Cálcula o total de rotinas
        total = len(rotinas_filtradas)

        #Cálcula o total de rotinas por status
        status_counts = rotinas_filtradas["Status"].value_counts().reindex(["OK", "ALERT", "ERROR", "UNKNOWN"], fill_value=0)

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total de Rotinas", total)
        c2.metric("OK", status_counts["OK"])
        c3.metric("ALERT", status_counts["ALERT"])
        c4.metric("ERROR", status_counts["ERROR"])
        c5.metric("UNKNOWN", status_counts["UNKNOWN"])
