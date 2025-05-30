import os
import datetime
from funçõe.config import pasta_lembretes
from funçõe.utils import validar_data_hora
from funçõe.alarme import salvar_alarme

os.path.join(pasta_lembretes, "lembretes.txt")
# Funções relacionadas a lembretes
def criar_lembrete(categoria, lembrete):
    """Cria um lembrete em uma categoria específica e pergunta se deseja criar um alarme."""
    caminho = os.path.join(pasta_lembretes, f"{categoria}.txt")
    hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    with open(caminho, "a") as arquivo:
        arquivo.write(f"{hora} - {lembrete}\n")
    print(f"Lembrete salvo na categoria '{categoria}'.")

    # Perguntar se o usuário deseja criar um alarme
    criar_alarme = input("Você gostaria de criar um alarme para este lembrete? (sim/não): ").strip().lower()
    if criar_alarme == "sim":
        data_hora = input("Digite a data e hora do alarme (dd/mm/yyyy hh:mm): ").strip()
        if validar_data_hora(data_hora):  # Valida a data e hora
            resposta = salvar_alarme(lembrete, data_hora)  # Salva o alarme
            print(resposta)
        else:
            print("Data e hora inválidas. Use o formato dd/mm/yyyy hh:mm.")


def ler_lembretes(categoria):
    caminho = os.path.join(pasta_lembretes, f"{categoria}.txt")
    if os.path.exists(caminho):
        with open(caminho, "r") as arquivo:
            return arquivo.read()
    return "Nenhum lembrete encontrado."

def apagar_lembrete():
    confirmar_tudo = input("Deseja apagar todos os lembretes? (sim/não): ").strip().lower()
    if confirmar_tudo == "sim":
        for arquivo in os.listdir(pasta_lembretes):
            caminho = os.path.join(pasta_lembretes, arquivo)
            if os.path.isfile(caminho):
                os.remove(caminho)
        return "Todos os lembretes foram apagados com sucesso!"
    elif confirmar_tudo == "não":
        categoria = input("Qual categoria você deseja apagar? ").strip()
        caminho = os.path.join(pasta_lembretes, f"{categoria}.txt")
        if os.path.exists(caminho):
            os.remove(caminho)
            return f"Lembretes da categoria '{categoria}' apagados."
        return f"Nenhum lembrete encontrado para a categoria '{categoria}'."
    else:
        return "Opção inválida. Nenhum lembrete foi apagado."

def listar_categorias():
    categorias = [f[:-4] for f in os.listdir(pasta_lembretes) if f.endswith('.txt')]
    if categorias:
        return "Categorias de lembretes: " + ", ".join(categorias)
    return "Nenhuma categoria de lembretes encontrada."