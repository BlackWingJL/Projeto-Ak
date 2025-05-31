from funçõe.config import pasta_alarmes, pasta_musica, pasta_lembretes
from funçõe.lembrete import criar_lembrete, ler_lembretes, listar_categorias
from funçõe.memoria import salvar_memoria, carregar_memoria
from funçõe.alarme import verificar_alarmes, salvar_alarme, apagar_alarme, verificar_alarmes_em_thread
from funçõe.musica import tocar_musica, alterar_som_alarme, salvar_musica_por_upload
from funçõe.utils import validar_data_hora, falar, reconhecer_fala
from funçõe.aletar_discord import AlertaDiscord
import random
import threading 

webhook_url = "https://discord.com/api/webhooks/1378226249813594192/3mbWIZIPqcilavihlA4w2Z29h4NKDMc-68620bZFk9DE2c25LoL75SltivQ_nKIso3EX"  # Substitua pelo seu webhook do Discord

def Zain_rpg(pergunta):
    if "dado" in pergunta:
        resultado = random.randint(1, 20)
        return f"Você rolou um d20 e tirou {resultado}!"
    elif "espada longa" in pergunta:
        return "Uma espada longa causa 1d8 de dano cortante."
    elif "piada" in pergunta:
        return "Por que o mago foi ao terapeuta? Porque ele estava conjurando muitos problemas!"
    return "Ainda não aprendi a responder isso. Tente outra pergunta."

def log_terminal(mensagem):
    """Envia mensagens para o terminal e para o Discord."""
    print(mensagem)
    AlertaDiscord(mensagem, webhook_url)

# Loop principal
def loop_principal():
    som_alarme = "som_alarme"  # Som padrão do alarme
    memoria = carregar_memoria()

    # Inicia a thread para verificar alarmes
    thread_verificar_alarmes = threading.Thread(target=verificar_alarmes_em_thread, args=(som_alarme,), daemon=True)
    thread_verificar_alarmes.start()

    while True:
        pergunta_usuario = reconhecer_fala()  # Usa a função de reconhecimento de fala
        if not pergunta_usuario:
            continue
        AlertaDiscord(f"Usuário: {pergunta_usuario}", webhook_url)  # Envia a entrada do usuário para o Discord

        if pergunta_usuario in ["sair", "exit", "parar"]:
            falar("Até mais!")
            AlertaDiscord("Zain: Até mais!", webhook_url)  # Envia a mensagem de saída para o Discord
            break

        elif "alterar som do alarme" in pergunta_usuario:
            novo_som = alterar_som_alarme()
            if novo_som:
                som_alarme = novo_som  # Atualiza o som do alarme

        elif "salvar música" in pergunta_usuario or "upload música" in pergunta_usuario:
            salvar_musica_por_upload()

        elif "criar alarme" in pergunta_usuario:
            falar("Diga o texto do alarme.")
            texto_alarme = reconhecer_fala()
            if not texto_alarme:
                falar("Não consegui entender o texto do alarme. Tente novamente.")
                continue

            falar("Diga a data e hora .")
            data_hora = reconhecer_fala()
            if not data_hora or not validar_data_hora(data_hora):
                falar("Data e hora inválidas. Tente novamente.")
                continue

            resposta = salvar_alarme(texto_alarme, data_hora)
            falar(resposta)
            AlertaDiscord(f"Zain: {resposta}", webhook_url)

        elif "apagar alarme" in pergunta_usuario:
            resposta = apagar_alarme()
            falar(resposta)

        elif "salvar lembrete" in pergunta_usuario:
            falar("Diga a categoria do lembrete.")
            categoria = reconhecer_fala()
            if not categoria:
                falar("Não consegui entender a categoria. Tente novamente.")
                continue

            falar("Diga o lembrete.")
            lembrete = reconhecer_fala()
            if not lembrete:
                falar("Não consegui entender o lembrete. Tente novamente.")
                continue

            criar_lembrete(categoria, lembrete)
            falar(f"Lembrete salvo na categoria '{categoria}'.")

        elif "ler lembretes" in pergunta_usuario:
            falar("Diga a categoria que você deseja ler.")
            categoria = reconhecer_fala()
            if not categoria:
                falar("Não consegui entender a categoria. Tente novamente.")
                continue

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
            falar("Diga a chave para lembrar.")
            chave = reconhecer_fala()
            if not chave:
                falar("Não consegui entender a chave. Tente novamente.")
                continue

            memoria[chave] = info
            salvar_memoria(memoria)
            falar(f"Lembrei de '{info}' com a chave '{chave}'.")

        elif "o que você lembra" in pergunta_usuario:
            falar("Diga a chave que você quer saber.")
            chave = reconhecer_fala()
            if not chave:
                falar("Não consegui entender a chave. Tente novamente.")
                continue

            if chave in memoria:
                falar(f"Lembro de '{memoria[chave]}' com a chave '{chave}'.")
            else:
                falar(f"Não lembro de nada com a chave '{chave}'.")

        elif "esqueca" in pergunta_usuario:
            falar("Diga a chave que você quer esquecer.")
            chave = reconhecer_fala()
            if not chave:
                falar("Não consegui entender a chave. Tente novamente.")
                continue

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