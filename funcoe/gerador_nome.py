import random

def gerar_nome():
    """Gera um nome aleatório combinando prefixos e sufixos."""
    prefixos = ["Al", "Be", "Ca", "Da", "El", "Fa", "Ga", "Ha", "Il", "Ja", "Ka", "La", "Ma", "Na", "Oa", "Pa", "Ra", "Sa", "Ta", "Va", "Za"]
    sufixos = ["ron", "lia", "dor", "nus", "ria", "tor", "vin", "las", "mir", "nor", "tis", "zar", "len", "vos", "rin", "dar", "mel", "tan", "zor", "lin"]

    # Escolhe um prefixo e um sufixo aleatoriamente
    prefixo = random.choice(prefixos)
    sufixo = random.choice(sufixos)

    # Combina o prefixo e o sufixo para formar o nome
    nome = prefixo + sufixo
    return nome

if __name__ == "__main__":
    print("Gerador de Nomes")
    for _ in range(10):  # Gera 10 nomes aleatórios
        print(gerar_nome())