import pyttsx3
import pygame
import os
from datetime import datetime
import random
import json
import logging
import tkinter as tk
from tkinter import filedialog
import threading  # Importando threading
import time  # Importando time para a função de verificação em thread

# Configuração do mecanismo de voz
def configurar_voz():
    engine = pyttsx3.init()
    for v in engine.getProperty('voices'):
        if "portuguese" in v.name.lower() or "brazil" in v.name.lower():
            engine.setProperty('voice', v.id)
            break
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    return engine

voz_engine = configurar_voz()

# Configuração de pastas e arquivos
pasta_lembretes = "lembretes_categoria"
pasta_alarmes = "alarmes"
pasta_musica = "musicas"
arquivo_memoria = "memoria_zain.json"

os.makedirs(pasta_lembretes, exist_ok=True)
os.makedirs(pasta_alarmes, exist_ok=True)
os.makedirs(pasta_musica, exist_ok=True)

# Funções de memória
def carregar_memoria():
    if os.path.exists(arquivo_memoria):
        with open(arquivo_memoria, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return {}

def salvar_memoria(memoria):
    with open(arquivo_memoria, "w", encoding="utf-8") as arquivo:
        json.dump(memoria, arquivo, ensure_ascii=False, indent=4)

memoria = carregar_memoria()

# Funções auxiliares
def falar(texto):
    try:
        logging.info(f"Zain: {texto}")
        voz_engine.say(texto)
        voz_engine.runAndWait()
    except Exception as e:
        logging.error(f"Erro ao falar: {e}")
    print(f"Zain: {texto}")

def validar_data_hora(data_hora):
    try:
        datetime.strptime(data_hora, "%d/%m/%Y %H:%M")
        return True
    except ValueError:
        return False

# Funções relacionadas a alarmes
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

def tocar_musica(nome_musica):
    """Verifica se o arquivo de música existe na pasta de músicas e tenta tocá-lo."""
    caminho_musica = os.path.join(pasta_musica, nome_musica)
    if not os.path.exists(caminho_musica):
        logging.error(f"Música não encontrada: {caminho_musica}")
        falar(f"Música '{nome_musica}' não encontrada na pasta de músicas.")
        return

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(caminho_musica)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass  # Aguarda a música terminar
    except Exception as e:
        logging.error(f"Erro ao tocar música: {e}")
        falar("Erro ao tocar a música do alarme.")

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

def salvar_musica(nome_musica, conteudo):
    caminho = os.path.join(pasta_musica, nome_musica)
    if not os.path.exists(caminho):
        try:
            with open(caminho, "wb") as arquivo:
                arquivo.write(conteudo) 
            falar(f"Música '{nome_musica}' salva com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao salvar a música: {e}")
            falar(f"Erro ao salvar a música: {e}")
    else:
        falar(f"A música '{nome_musica}' já existe.")

def alterar_som_alarme():
    falar("digite o nome do arquivo de música que deseja usar como alarme (deve estar na pasta 'musicas'):")
    nome_musica = input("Nome do arquivo de música: ").strip()
    caminho_musica = os.path.join(pasta_musica, nome_musica)
    if os.path.exists(caminho_musica):
        falar(f"Música '{nome_musica}' selecionada como som do alarme.")
        return nome_musica
    else:
        falar(f"Música '{nome_musica}' não encontrada na pasta 'musicas'.")
        return None

# Funções relacionadas a lembretes
def criar_lembrete(categoria, lembrete):
    caminho = os.path.join(pasta_lembretes, f"{categoria}.txt")
    hora = datetime.now().strftime("%d/%m/%Y %H:%M")
    with open(caminho, "a") as arquivo:
        arquivo.write(f"{hora} - {lembrete}\n")

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

# Função relacionada ao RPG
def Zain_rpg(pergunta):
    if "dado" in pergunta:
        resultado = random.randint(1, 20)
        return f"Você rolou um d20 e tirou {resultado}!"
    elif "espada longa" in pergunta:
        return "Uma espada longa causa 1d8 de dano cortante."
    elif "piada" in pergunta:
        return "Por que o mago foi ao terapeuta? Porque ele estava conjurando muitos problemas!"
    return "Ainda não aprendi a responder isso. Tente outra pergunta."

def salvar_musica_por_upload():
    """Permite ao usuário fazer upload de um arquivo de música."""
    # Configura a janela do tkinter
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do tkinter

    # Abre a janela para selecionar o arquivo
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo de música",
        filetypes=[("Arquivos de áudio", "*.mp3 *.wav *.ogg"), ("Todos os arquivos", "*.*")]
    )

    if not caminho_arquivo:
        falar("Nenhum arquivo foi selecionado.")
        return

    # Obtém o nome do arquivo e copia para a pasta de músicas
    nome_musica = os.path.basename(caminho_arquivo)
    caminho_destino = os.path.join(pasta_musica, nome_musica)

    try:
        with open(caminho_arquivo, "rb") as arquivo_origem:
            with open(caminho_destino, "wb") as arquivo_destino:
                arquivo_destino.write(arquivo_origem.read())
        falar(f"Música '{nome_musica}' salva com sucesso na pasta de músicas.")
    except Exception as e:
        logging.error(f"Erro ao salvar a música: {e}")
        falar("Erro ao salvar a música.")

def verificar_alarmes_em_thread(som_alarme):
    """Thread que verifica continuamente se há alarmes para tocar."""
    while True:
        verificar_alarmes(som_alarme)
        # Aguarda 1 minuto antes de verificar novamente
        time.sleep(60)

# Loop principal
def loop_principal():
    som_alarme = "som_alarme"  # Som padrão do alarme

    # Inicia a thread para verificar alarmes
    thread_verificar_alarmes = threading.Thread(target=verificar_alarmes_em_thread, args=(som_alarme,), daemon=True)
    thread_verificar_alarmes.start()

    while True:
        pergunta_usuario = input("Você: ").strip().lower()

        if pergunta_usuario in ["sair", "exit", "parar"]:
            falar("Até mais!")
            break

        if "alterar som do alarme" in pergunta_usuario:
            novo_som = alterar_som_alarme()
            if novo_som:
                som_alarme = novo_som  # Atualiza o som do alarme

        elif "salvar música" in pergunta_usuario:
            salvar_musica_por_upload()

        elif "upload música" in pergunta_usuario:
            salvar_musica_por_upload()

        elif "criar alarme" in pergunta_usuario:
            texto_alarme = input("Digite o texto do alarme: ")
            data_hora = input("Digite a data e hora do alarme (dd/mm/yyyy hh:mm): ")
            if validar_data_hora(data_hora):
                resposta = salvar_alarme(texto_alarme, data_hora)
                falar(resposta)
            else:
                falar("Data e hora inválidas. Use o formato dd/mm/yyyy hh:mm.")
                
        elif "apagar alarme" in pergunta_usuario:
            resposta = apagar_alarme()
            falar(resposta)

        elif "salvar lembrete" in pergunta_usuario:
            categoria = input("Qual é a categoria do lembrete? ")
            lembrete = input("Digite o lembrete: ")
            criar_lembrete(categoria, lembrete)
            falar(f"Lembrete salvo na categoria '{categoria}'.")

            criar_alarme = input("Você gostaria de criar um alarme para este lembrete? (sim/não): ").strip().lower()
            if criar_alarme == "sim":
                texto_alarme = lembrete
                data_hora = input("Digite a data e hora do alarme (dd/mm/yyyy hh:mm): ")
                if validar_data_hora(data_hora):
                    resposta = salvar_alarme(texto_alarme, data_hora)
                    falar(resposta)
                else:
                    falar("Data e hora inválidas. Use o formato dd/mm/yyyy hh:mm.")

        elif "ler lembretes" in pergunta_usuario:
            categoria = input("Qual categoria você deseja ler? ")
            resposta = ler_lembretes(categoria)
            falar(resposta)

        elif "listar categorias" in pergunta_usuario:
            resposta = listar_categorias()
            falar(resposta)

        elif "rpg" in pergunta_usuario:
            resposta = Zain_rpg(pergunta_usuario)
            falar(resposta)

        elif "lembrar" in pergunta_usuario:
            info = pergunta_usuario.replace("lembrar", "").strip()
            chave = input("Qual é a chave para lembrar? ").strip()
            memoria[chave] = info
            salvar_memoria(memoria)
            falar(f"Lembrei de '{info}' com a chave '{chave}'.")

        elif "o que você lembra" in pergunta_usuario:
            chave = input("Qual é a chave que você quer saber? ").strip()
            if chave in memoria:
                falar(f"Lembro de '{memoria[chave]}' com a chave '{chave}'.")
            else:
                falar(f"Não lembro de nada com a chave '{chave}'.")

        elif "esqueca" in pergunta_usuario:
            chave = input("Qual é a chave que você quer esquecer? ").strip()
            if chave in memoria:
                del memoria[chave]
                salvar_memoria(memoria)
                falar(f"Apagei o registro da chave '{chave}'.")
            else:
                falar(f"Não lembro de nada com a chave '{chave}' para esquecer.")

        else:
            falar("Desculpe, não entendi sua pergunta. Tente novamente.")

# Iniciar o programa
if __name__ == "__main__":
    loop_principal()