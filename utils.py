# Esse script cria a classe DataProcessor, responsável por enriquecer o dataframe;

import numpy as np
import pandas as pd
import os

class DataProcessor:
    @staticmethod
    def process_rotinas(rotinas: pd.DataFrame):
        #Obtém a data do dia da execução, sem considerar horário
        hoje = pd.to_datetime("today").normalize()

        #lista onde os dados processados serão acumulados
        status_reais, datas_status, resultados, descricoes_erro, ultimo_end_times = [], [], [], [], []

        for _, row in rotinas.iterrows():
            #Busca pelo arquivo Excel endereçado no Path do json, e define valores padrão
            caminho_log = row.get("Path", "")
            status, end_time, resultado, erro = "UNKNOWN", pd.NaT, None, ""

            if os.path.exists(caminho_log):
                #1. Verifica se possui as colunas esperadas;
                #2. Captura o último registro
                #3. Trata o registro de status
                #4. Avalia o registro de status
                #5. Captura e trata o registro de end_time
                #6. Captura o registro de results
                #7. Captura o registro de error_description
                try:
                    df_log = pd.read_excel(caminho_log, engine="openpyxl")
                    if not df_log.empty and all(col in df_log.columns for col in ["status", "end_time", "error_description", "results"]):
                        ultimo = df_log.iloc[-1]
                        status = str(ultimo["status"]).upper()
                        if status not in ["OK", "ALERT", "ERROR", "UNKNOWN"]:
                            status = "UNKNOWN"
                        end_time = pd.to_datetime(ultimo["end_time"], errors='coerce')
                        resultado = ultimo["results"]
                        erro = ultimo["error_description"] if status == "ERROR" else ""
                except:
                    pass
            #1. Trata o registro de frequência
            #2. Cálcula e cria o campo "intervalo"
            freq = str(row.get("Frequencia", "")).lower()
            if pd.isna(end_time):
                intervalo = None
            else:
                intervalo = np.busday_count(end_time.date(), hoje.date()) if freq in ["diária", "diaria"] else (hoje - end_time).days
            
            #Define os parâmetros para a lógica de frequência
            freq_map = {"diária": 1, "diaria": 1, "semanal": 7, "quinzenal": 15, "mensal": 30, "anual": 365}
            freq_dias = freq_map.get(freq, 1)

            #Compara o número de dias desde a última execução com a frequência esperada
            if intervalo is not None:
                if intervalo > freq_dias:
                    status, erro = "ERROR", "Rotina Atrasada"
                elif intervalo == freq_dias and status != "ERROR":
                    status, erro = "ALERT", "Rotina Próximo do vencimento"
            
            #1. Verifica se o arquivo excel existe;
            #2. Executa a leitura do arquivo excel;
            #3. Caso a coluna results exista, calcula a moda dos resultados
            #4. Caso o registro results for menor que 70% da moda e o status for 
            #   diferente de ERROR, altera o status para ALERT por volumetria incomum; 
            try:
                if os.path.exists(caminho_log):
                    df_log = pd.read_excel(caminho_log, engine="openpyxl")
                    if "results" in df_log.columns:
                        modas = df_log["results"].replace(0, pd.NA).dropna()
                        moda = modas.mode()
                        if not moda.empty and resultado is not None and resultado < 0.7 * moda.iloc[0]:
                            if status != "ERROR":
                                status, erro = "ALERT", "Volumetria fora do comum"
            except:
                pass
            
            
            status_reais.append(status)
            datas_status.append(end_time)
            resultados.append(resultado)
            descricoes_erro.append(erro)
            ultimo_end_times.append(end_time)
        #Armazena os dados processados listas por registro
        rotinas["Status"] = status_reais
        rotinas["Última Execução"] = ultimo_end_times
        rotinas["Resultado"] = resultados
        rotinas["Descricao Erro"] = descricoes_erro

        #Cria a coluna "Intervalo (dias)"
        intervalos_exibir = []
        for _, row in rotinas.iterrows():
            freq = str(row.get("Frequencia", "")).lower()
            end_time = row["Última Execução"]
            intervalo = np.busday_count(end_time.date(), hoje.date()) if freq in ["diária", "diaria"] else (hoje - end_time).days if pd.notna(end_time) else None
            intervalos_exibir.append(intervalo)

        rotinas["Intervalo (dias)"] = intervalos_exibir
        return rotinas
