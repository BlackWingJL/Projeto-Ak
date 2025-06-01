import os 
import json
from funcoe.config import  arquivo_memoria


def carregar_memoria():
    if os.path.exists(arquivo_memoria):
        with open(arquivo_memoria, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return {}

def salvar_memoria(memoria):
    with open(arquivo_memoria, "w", encoding="utf-8") as arquivo:
        json.dump(memoria, arquivo, ensure_ascii=False, indent=4)

memoria = carregar_memoria()

