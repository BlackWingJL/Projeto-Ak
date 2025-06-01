from funcoe.config import pasta_musica
import os
import logging
import pygame
import tkinter as tk
from tkinter import filedialog
from funcoe.utils import falar

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
