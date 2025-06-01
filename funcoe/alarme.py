from funcoe.config import pasta_alarmes
from funcoe.utils import falar, validar_data_hora,datetime
from funcoe.musica import tocar_musica
import logging
import os
import time

def verificar_alarmes(som_alarme):
    """Verifica alarmes e toca o som configurado."""
    caminho = os.path.join(pasta_alarmes, "alarmes.txt")
    if not os.path.exists(caminho):
        return
    linhas_restantes = []
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    with open(caminho, "r") as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            try:
                data_hora, texto = linha.strip().split("|")
                if data_hora == agora:
                    falar(f"🔔 Alarme: {texto}")
                    tocar_musica(som_alarme)  # Usa o som configurado
                elif datetime.strptime(data_hora, "%d/%m/%Y %H:%M") > datetime.now():
                    linhas_restantes.append(linha)
            except ValueError:
                logging.error(f"Erro ao processar a linha: {linha.strip()}. Formato de data inválido.")
    with open(caminho, "w") as arquivo:
        arquivo.writelines(linhas_restantes)

def salvar_alarme(texto, data_hora):
    caminho = os.path.join(pasta_alarmes, "alarmes.txt")
    try:
        with open(caminho, "a") as arquivo:
            arquivo.write(f"{data_hora}|{texto}\n")
        return f"Alarme para '{texto}' em {data_hora} salvo com sucesso!"
    except Exception as e:
        logging.error(f"Erro ao salvar o alarme: {e}")
        return f"Erro ao salvar o alarme: {e}"

def apagar_alarme():
    """Permite ao usuário apagar alarmes."""
    caminho = os.path.join(pasta_alarmes, "alarmes.txt")
    if not os.path.exists(caminho):
        return "Nenhum alarme encontrado para apagar."

    with open(caminho, "r") as arquivo:
        alarmes = arquivo.readlines()

    if not alarmes:
        return "Nenhum alarme encontrado para apagar."

    falar("Os seguintes alarmes estão salvos:")
    for i, alarme in enumerate(alarmes, start=1):
        falar(f"{i}. {alarme.strip()}")

    escolha = input("Digite o número do alarme que deseja apagar ou 'todos' para apagar todos: ").strip().lower()

    if escolha == "todos":
        os.remove(caminho)
        return "Todos os alarmes foram apagados com sucesso."
    elif escolha.isdigit() and 1 <= int(escolha) <= len(alarmes):
        indice = int(escolha) - 1
        del alarmes[indice]
        with open(caminho, "w") as arquivo:
            arquivo.writelines(alarmes)
        return "Alarme apagado com sucesso."
    else:
        return "Opção inválida. Nenhum alarme foi apagado."
    
def verificar_alarmes_em_thread(som_alarme):
    """Thread que verifica continuamente se há alarmes para tocar."""
    while True:
        verificar_alarmes(som_alarme)
        # Aguarda 1 minuto antes de verificar novamente
        time.sleep(60)