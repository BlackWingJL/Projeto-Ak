import pyttsx3
import pygame
import os
from datetime import datetime
import random

voz_engine = pyttsx3.init()


for v in voz_engine.getProperty('voices'):
    if "portuguese" in v.name.lower() or "brazil" in v.name.lower():
        voz_engine.setProperty('voice', v.id)
        break

voz_engine.setProperty('rate', 150)
voz_engine.setProperty('volume', 1)

pasta_lembretes = "lembretes_categoria"
os.makedirs(pasta_lembretes, exist_ok=True)

pasta_alarmes = "alarmes"
os.makedirs(pasta_alarmes, exist_ok=True)

def tocar_musica(musica):
    if not os.path.isfile(musica): return
    pygame.mixer.init()
    pygame.mixer.music.load(musica)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass  # Aguarda a música terminar de tocar

    pygame.mixer.quit() 

def assistente(pergunta):
    pergunta = pergunta.lower()

def falar(texto):
    print("Zain:", texto)
    voz_engine.say(texto)
    voz_engine.runAndWait()

def salvar_alarme(texto, data_hora):
    caminho = os.path.join(pasta_alarmes, "alarmes.txt")
    with open(caminho, "a") as arquivo:
        arquivo.write(f"{data_hora}|{texto}\n")
    return f"Alarme para '{texto}' em {data_hora} salvo com sucesso!"

def verificar_alarmes():
    caminho = os.path.join(pasta_alarmes, "alarmes.txt")
    if not os.path.exists(caminho):
        return
    linhas_restantes = []
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    with open(caminho, "r") as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            data_hora, texto = linha.strip().split("|")
            if data_hora == agora:
                falar(f"🔔 Alarme: {texto}")
                tocar_musica("alarme.mp3")
            elif validar_data_hora(data_hora) and datetime.strptime(data_hora, "%d/%m/%Y %H:%M") > datetime.now():
                linhas_restantes.append(linha)
            else:
                linhas_restantes.append(linha)
    # Atualiza o arquivo para manter só os alarmes futuros
    with open(caminho, "w") as arquivo:
        arquivo.writelines(linhas_restantes)

def apagar_alarme(texto_ou_data=None):
    caminho = os.path.join(pasta_alarmes, "alarmes.txt")
    if not os.path.exists(caminho):
        return "Nenhum alarme encontrado."

    if texto_ou_data is None:
        os.remove(caminho)
        return "Todos os alarmes foram apagados."
    
    linhas_restantes = []
    alarme_apagado = False
    if not validar_data_hora(texto_ou_data):
        # Se não for uma data válida, assume que é um texto
        texto_ou_data = texto_ou_data.strip()

    with open(caminho, "r") as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            data_hora, texto = linha.strip().split("|")
            if texto_ou_data in data_hora or texto_ou_data in texto:
                alarme_apagado = True
            else:
                linhas_restantes.append(linha)

    with open(caminho, "w") as arquivo:
        arquivo.writelines(linhas_restantes)
        
    if alarme_apagado:
        return f"Alarme '{texto_ou_data}' apagado com sucesso!"
    return f"Nenhum alarme correspondente a '{texto_ou_data}' foi encontrado."

def salvar_lembrete(categoria, lembrete):
    caminho = os.path.join(pasta_lembretes, f"{categoria}.txt")
    hora = datetime.now().strftime("%d/%m/%Y %H:%M")  # Corrigido o formato da data
    with open(caminho, "a") as arquivo:
        arquivo.write(f"{hora} - {lembrete}\n")

def ler_lembretes(categoria):
    caminho = os.path.join(pasta_lembretes, f"{categoria}.txt")
    if os.path.exists(caminho):
        with open(caminho, "r") as arquivo:
            return arquivo.read()
    return "Nenhum lembrete encontrado."

def apagar_lembrete(categoria):
    caminho = os.path.join(pasta_lembretes, f"{categoria}.txt")
    if os.path.exists(caminho):
        os.remove(caminho)
        return f"Lembretes da categoria '{categoria}' apagados."
    return f"Nenhum lembrete encontrado para a categoria '{categoria}'."

def listar_categorias():
    categorias = [f[:-4] for f in os.listdir(pasta_lembretes) if f.endswith('.txt')]
    if categorias:
        return "Categorias de lembretes: " + ", ".join(categorias)
    return "Nenhuma categoria de lembretes encontrada."

def Zain_rpg(pergunta):
    if "dado" in pergunta:
        resultado = random.randint(1, 20)
        return f"Você rolou um d20 e tirou {resultado}!"
    elif "espada longa" in pergunta:
        return "Uma espada longa causa 1d8 de dano cortante."
    elif "piada" in pergunta:
        return "Por que o mago foi ao terapeuta? Porque ele estava conjurando muitos problemas!"
    return "Ainda não aprendi a responder isso. Tente outra pergunta."

def validar_data_hora(data_hora):
    try:
        datetime.strptime(data_hora, "%d/%m/%Y %H:%M")
        return True
    except ValueError:
        return False

while True:
    verificar_alarmes()
    pergunta_usuario = input("Você: ")
    if pergunta_usuario.lower() in ["sair", "exit", "parar"]:
        falar("Até mais!")
        break

    resposta = assistente(pergunta_usuario)
    if resposta is None:
        if "lembrete" in pergunta_usuario:
            if "criar" in pergunta_usuario:
                categoria = input("Digite a categoria do lembrete: ").strip()
                lembrete = input("Digite o lembrete: ").strip()
                salvar_lembrete(categoria, lembrete)
                resposta = f"Lembrete salvo na categoria '{categoria}'."
                
                # Perguntar se deseja criar um alarme
                criar_alarme = input("Deseja criar um alarme para este lembrete? (sim/não): ").strip().lower()
                if criar_alarme == "sim":
                    data_hora = input("Digite a data e hora para o alarme (dd/mm/aaaa hh:mm): ").strip()
                    if validar_data_hora(data_hora):
                        salvar_alarme(lembrete, data_hora)
                        resposta += f" Alarme para '{lembrete}' em {data_hora} salvo com sucesso!"
                    else:
                        resposta += " Formato de data e hora inválido. Alarme não criado."
            elif "ler" in pergunta_usuario:
                categoria = input("Digite a categoria do lembrete: ").strip()
                resposta = ler_lembretes(categoria)
            elif "apagar" in pergunta_usuario:
                categoria = input("Digite a categoria do lembrete: ").strip()
                resposta = apagar_lembrete(categoria)
            elif "listar" in pergunta_usuario:
                resposta = listar_categorias()
        elif "alarme" in pergunta_usuario and "criar" in pergunta_usuario:
            texto = input("Digite o que devo lembrar: ")
            data_hora = input("Digite a data e hora (dd/mm/aaaa hh:mm): ")
            if validar_data_hora(data_hora):
                resposta = salvar_alarme(texto, data_hora)
            else:
                resposta = "Formato de data e hora inválido. Tente novamente."
        elif "alarme" in pergunta_usuario and "apagar" in pergunta_usuario:
            apagar_todos = input("Deseja apagar todos os alarmes? (sim/não): ").strip().lower()
            if apagar_todos == "sim":
                resposta = apagar_alarme()  # Chama a função sem argumentos para apagar todos
            else:
                texto_ou_data = input("Digite o texto ou a data/hora do alarme que deseja apagar: ").strip()
                resposta = apagar_alarme(texto_ou_data)
        else:
            resposta = Zain_rpg(pergunta_usuario)

    falar(resposta)
