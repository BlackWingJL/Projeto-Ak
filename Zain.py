from funçõe.config import pasta_alarmes, pasta_musica, pasta_lembretes
from funçõe.lembrete import criar_lembrete, ler_lembretes, listar_categorias
from funçõe.memoria import salvar_memoria, carregar_memoria
from funçõe.alarme import verificar_alarmes, salvar_alarme, apagar_alarme, verificar_alarmes_em_thread
from funçõe.musica import tocar_musica, alterar_som_alarme, salvar_musica_por_upload
from funçõe.utils import validar_data_hora, falar
import random
import threading  # Importando threading
 # Importando time para a função de verificação em thread
# Configuração do mecanismo de voz
# Funções auxiliares
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

# Loop principal
def loop_principal():
    som_alarme = "som_alarme"  # Som padrão do alarme

    # Inicializa a memória carregando do arquivo
    memoria = carregar_memoria()


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