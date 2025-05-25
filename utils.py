import numpy as np
import pandas as pd
import os

class DataProcessor:
    @staticmethod
    def process_rotinas(rotinas: pd.DataFrame):
        # Define a raiz do projeto (2 níveis acima de cmmd/pages/)
        try:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        except NameError:
            base_dir = os.getcwd()  # fallback para ambientes sem __file__

        hoje = pd.to_datetime("today").normalize()

        # Listas para armazenar dados processados
        status_reais = []
        datas_status = []
        resultados = []
        descricoes_erro = []
        intervalos_exibir = []

        freq_map = {
            "diaria": 1, "diária": 1,
            "semanal": 7,
            "quinzenal": 15,
            "mensal": 30,
            "anual": 365
        }

        for _, row in rotinas.iterrows():
            caminho_relativo = row.get("Path", "")
            caminho_log = os.path.join(base_dir, caminho_relativo)

            status, end_time, resultado, erro = "UNKNOWN", pd.NaT, None, ""
            df_log = None

            if os.path.exists(caminho_log):
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
                except Exception as e:
                    print(f"[Erro ao ler {caminho_log}]: {e}")

            # Frequência da rotina
            freq = str(row.get("Frequencia", "")).strip().lower().replace("í", "i")
            freq_dias = freq_map.get(freq, 1)

            # Calcula o intervalo
            if pd.isna(end_time):
                intervalo = None
            else:
                intervalo = np.busday_count(end_time.date(), hoje.date()) if freq == "diaria" else (hoje - end_time).days

                # Avaliação por frequência
                if intervalo > freq_dias:
                    status, erro = "ERROR", "Rotina Atrasada"
                elif intervalo == freq_dias and status != "ERROR":
                    status, erro = "ALERT", "Rotina Próxima do vencimento"

            # Verificação por volumetria
            try:
                if df_log is not None and "results" in df_log.columns:
                    modas = df_log["results"].replace(0, pd.NA).dropna()
                    moda = modas.mode()
                    if not moda.empty and resultado is not None and resultado < 0.7 * moda.iloc[0]:
                        if status != "ERROR":
                            status, erro = "ALERT", "Volumetria fora do comum"
            except Exception as e:
                print(f"[Erro ao processar volumetria de {caminho_log}]: {e}")

            # Armazena os dados
            status_reais.append(status)
            datas_status.append(end_time)
            resultados.append(resultado)
            descricoes_erro.append(erro)
            intervalos_exibir.append(intervalo)

        # Atualiza o DataFrame original
        rotinas["Status"] = status_reais
        rotinas["Última Execução"] = datas_status
        rotinas["Resultado"] = resultados
        rotinas["Descricao Erro"] = descricoes_erro
        rotinas["Intervalo (dias)"] = intervalos_exibir

        return rotinas
