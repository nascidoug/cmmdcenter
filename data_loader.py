# Esse script cria a classe DataLoader, reponsável por:
# - carregar os dados de um arquivo json e;
# - transforma-lo em um dataframe para executar cálculos/análises, etc

import pandas as pd
import json
import os

#Carrega os dados do arquivo json e converte em um dataframe, ou cria um dataframe vazio
class DataLoader:
    def __init__(self, json_path):
        self.json_path = json_path
        self.rotinas = self._load_data()

    def _load_data(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, "r") as file:
                try:
                    return pd.DataFrame(json.load(file))
                except json.JSONDecodeError:
                    return pd.DataFrame()
        return pd.DataFrame()
