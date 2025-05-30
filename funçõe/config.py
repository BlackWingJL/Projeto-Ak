import os


pasta_lembretes = "lembretes_categoria"
pasta_alarmes = "alarmes"
pasta_musica = "musicas"
arquivo_memoria = "memoria_zain.json"

os.makedirs(pasta_lembretes, exist_ok=True)
os.makedirs(pasta_alarmes, exist_ok=True)
os.makedirs(pasta_musica, exist_ok=True)