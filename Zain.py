from funcoe.config import pasta_alarmes, pasta_musica, pasta_lembretes
from funcoe.lembrete import criar_lembrete, ler_lembretes, listar_categorias
from funcoe.memoria import salvar_memoria, carregar_memoria
from funcoe.alarme import verificar_alarmes, salvar_alarme, apagar_alarme, verificar_alarmes_em_thread
from funcoe.musica import tocar_musica, alterar_som_alarme, salvar_musica_por_upload
from funcoe.utils import validar_data_hora, falar, reconhecer_fala
from funcoe.aletar_discord import AlertaDiscord
from funcoe.gerador_nome import gerar_nome
from funcoe.rpg import Zain_rpg
import threading 
import random

webhook_url = "https://discord.com/api/webhooks/1378226249813594192/3mbWIZIPqcilavihlA4w2Z29h4NKDMc-68620bZFk9DE2c25LoL75SltivQ_nKIso3EX"

def log_terminal(mensagem):
    """Envia mensagens para o terminal e para o Discord."""
    print(mensagem)
    AlertaDiscord(mensagem, webhook_url)

# Loop principal
def loop_principal():
    som_alarme = "som_alarme"  # Som padrão do alarme
    memoria = carregar_memoria()

    # Pergunta ao usuário o modo de interação
    falar("Você gostaria de interagir por texto ou por voz? Diga 'texto' ou 'voz'.")
    modo_interacao = reconhecer_fala().strip().lower()  # Captura a escolha por voz
    if modo_interacao not in ["texto", "voz"]:
        falar("Não entendi sua escolha. Vou usar o modo de voz por padrão.")
        modo_interacao = "texto"  # Define o modo de interação padrão como texto

    # Inicia a thread para verificar alarmes
    thread_verificar_alarmes = threading.Thread(target=verificar_alarmes_em_thread, args=(som_alarme,), daemon=True)
    thread_verificar_alarmes.start()

    while True:
        # Captura a entrada do usuário com base no modo de interação
        if modo_interacao == "texto":
            pergunta_usuario = input("Você: ").strip().lower()
        else:  # Modo de voz
            pergunta_usuario = reconhecer_fala()
            if not pergunta_usuario:
                continue

        #AlertaDiscord(f"Usuário: {pergunta_usuario}", webhook_url)  # Envia a entrada do usuário para o Discord

        if pergunta_usuario in ["sair", "exit", "parar"]:
            falar("Até mais!")
            #AlertaDiscord("Zain: Até mais!", webhook_url)  # Envia a mensagem de saída para o Discord
            break

        elif "alterar som do alarme" in pergunta_usuario:
            novo_som = alterar_som_alarme()
            if novo_som:
                som_alarme = novo_som  # Atualiza o som do alarme

        elif "salvar música" in pergunta_usuario or "upload música" in pergunta_usuario:
            salvar_musica_por_upload()

        elif "criar alarme" in pergunta_usuario:
            falar("Diga o texto do alarme.")
            texto_alarme = reconhecer_fala() if modo_interacao == "voz" else input("Digite o texto do alarme: ")
            if not texto_alarme:
                falar("Não consegui entender o texto do alarme. Tente novamente.")
                continue

            falar("Diga a data e hora do alarme no formato dd/mm/yyyy hh:mm.")
            data_hora = reconhecer_fala() if modo_interacao == "voz" else input("Digite a data e hora do alarme (dd/mm/yyyy hh:mm): ")
            if not data_hora or not validar_data_hora(data_hora):
                falar("Data e hora inválidas. Tente novamente.")
                continue

            resposta = salvar_alarme(texto_alarme, data_hora)
            falar(resposta)
            #AlertaDiscord(f"Zain: {resposta}", webhook_url)

        elif "apagar alarme" in pergunta_usuario:
            resposta = apagar_alarme()
            falar(resposta)

        elif "salvar lembrete" in pergunta_usuario:
            falar("Diga a categoria do lembrete.")
            categoria = reconhecer_fala() if modo_interacao == "voz" else input("Digite a categoria do lembrete: ")
            if not categoria:
                falar("Não consegui entender a categoria. Tente novamente.")
                continue

            falar("Diga o lembrete.")
            lembrete = reconhecer_fala() if modo_interacao == "voz" else input("Digite o lembrete: ")
            if not lembrete:
                falar("Não consegui entender o lembrete. Tente novamente.")
                continue

            criar_lembrete(categoria, lembrete)
            falar(f"Lembrete salvo na categoria '{categoria}'.")

        elif "ler lembretes" in pergunta_usuario:
            falar("Diga a categoria que você deseja ler.")
            categoria = reconhecer_fala() if modo_interacao == "voz" else input("Digite a categoria que você deseja ler: ")
            if not categoria:
                falar("Não consegui entender a categoria. Tente novamente.")
                continue

            resposta = ler_lembretes(categoria)
            falar(resposta)

        elif "listar categorias" in pergunta_usuario:
            resposta = listar_categorias()
            falar(resposta)

        elif "rpg" in pergunta_usuario:
            resposta = Zain_rpg(pergunta_usuario, modo_interacao)
            falar(resposta)

        elif "lembrar" in pergunta_usuario:
            info = pergunta_usuario.replace("lembrar", "").strip()
            falar("Diga a chave para lembrar.")
            chave = reconhecer_fala() if modo_interacao == "voz" else input("Digite a chave para lembrar: ")
            if not chave:
                falar("Não consegui entender a chave. Tente novamente.")
                continue

            memoria[chave] = info
            salvar_memoria(memoria)
            falar(f"Lembrei de '{info}' com a chave '{chave}'.")

        elif "o que você lembra" in pergunta_usuario:
            falar("Diga a chave que você quer saber.")
            chave = reconhecer_fala() if modo_interacao == "voz" else input("Digite a chave que você quer saber: ")
            if not chave:
                falar("Não consegui entender a chave. Tente novamente.")
                continue

            if chave in memoria:
                falar(f"Lembro de '{memoria[chave]}' com a chave '{chave}'.")
            else:
                falar(f"Não lembro de nada com a chave '{chave}'.")

        elif "esqueca" in pergunta_usuario:
            falar("Diga a chave que você quer esquecer.")
            chave = reconhecer_fala() if modo_interacao == "voz" else input("Digite a chave que você quer esquecer: ")
            if not chave:
                falar("Não consegui entender a chave. Tente novamente.")
                continue

            if chave in memoria:
                del memoria[chave]
                salvar_memoria(memoria)
                falar(f"Apagei o registro da chave '{chave}'.")
            else:
                falar(f"Não lembro de nada com a chave '{chave}' para esquecer.")

        elif "gerar nome" in pergunta_usuario:
            nome_gerado = gerar_nome()
            falar(f"Nome gerado: {nome_gerado}")
            log_terminal(f"Nome gerado: {nome_gerado}")

        else:
            falar("Desculpe, não entendi sua pergunta. Tente novamente.")

# Iniciar o programa
if __name__ == "__main__":
    loop_principal()