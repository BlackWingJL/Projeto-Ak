import random
from funcoe.utils import falar, reconhecer_fala

def Zain_rpg(pergunta, modo_interacao):
    """Responde a perguntas relacionadas ao RPG."""
    if "rolar dado" in pergunta:
        try:
            # Solicita o tipo de dado
            falar("Diga o tipo de dado?")
            if modo_interacao == "voz":
                tipo_dado = reconhecer_fala()  # Captura a entrada por voz
            else:
                tipo_dado = input("Digite o tipo de dado (exemplo: d3,d4, d6, d8, d10, d12, d20, d100): ").strip().lower()

            if not tipo_dado.startswith("d") or not tipo_dado[1:].isdigit():
                return "Formato inválido. Use algo como 'd6' ou 'd20'."
            lados = int(tipo_dado[1:])

            # Solicita a quantidade de dados
            falar("Quantos dados você quer rolar?")
            if modo_interacao == "voz":
                quantidade = reconhecer_fala()  # Captura a entrada por voz
            else:
                quantidade = input("Digite a quantidade de dados que você quer rolar: ").strip()

            if not quantidade.isdigit() or int(quantidade) <= 0:
                return "A quantidade de dados deve ser um número maior que zero."
            quantidade = int(quantidade)

            # Rola os dados
            resultados = [random.randint(1, lados) for _ in range(quantidade)]
            soma = sum(resultados)
            return f"Você rolou {quantidade} {tipo_dado}(s): {resultados}. Soma total: {soma}."
        except ValueError:
            return "Não consegui entender o tipo de dado ou a quantidade. Tente novamente."
    elif "espada longa" in pergunta:
        return "Uma espada longa causa 1d8 de dano cortante."
    elif "piada" in pergunta:
        return "Por que o mago foi ao terapeuta? Porque ele estava conjurando muitos problemas!"
    return "Ainda não aprendi a responder isso. Tente outra pergunta."