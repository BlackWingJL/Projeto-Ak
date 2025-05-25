# Função principal da assistente
def assistente(pergunta):
    pergunta = pergunta.lower()

    if "seu nome" in pergunta:
        return "Meu nome é Ak, sua assistente pessoal !"

    elif "horas" in pergunta:
        from datetime import datetime
        agora = datetime.now().strftime("%H:%M")
        return f"Agora são {agora}."
    
    elif "data" in pergunta:
        from datetime import datetime
        hoje = datetime.now().strftime("%d/%m/%Y")
        return f"Hoje é {hoje}."  
    
def Ak_lembrete(pergunta):  
    if "criar lembrete" in pergunta:
        lembrete = pergunta.replace("criar lembrete", "").strip()
        if lembrete:
            with open("lembretes.txt", "a") as arquivo:
                arquivo.write(lembrete + "\n")
            return f"Lembrete '{lembrete}' criado com sucesso!"
        else:
            return "Por favor, diga o que você gostaria de lembrar."
        
    elif "ler lembrete" in pergunta:
        try:
            with open("lembretes.txt", "r") as arquivo:
                lembretes = arquivo.readlines()
            if lembretes:
                return "Seus lembretes:\n" + "".join(lembretes)
            else:
                return "Você não tem lembretes."
        except FileNotFoundError:
            return "Você não tem lembretes."
    
    elif "apagar lembrete" in pergunta:
        with open("lembretes.txt", "w") as arquivo:
            arquivo.write("")
        return "Todos os lembretes foram apagados."
        
def Ak_rpg(pergunta):
        
    if "dado" in pergunta:
        import random
        resultado = random.randint(1, 20)
        return f"Você rolou um d20 e tirou {resultado}!"
    
    elif "espada longa" in pergunta:
        return "Uma espada longa causa 1d8 de dano cortante."
    
    
    elif "heroi" in pergunta:
        return "Drack."
    
    elif "piada" in pergunta:
        return "Por que o mago foi ao terapeuta? Porque ele estava conjurando muitos problemas!"
    
    elif "quem é khalmyr" in pergunta:
        return "Um deus qualquer"

    else:
        return "Ainda não aprendi a responder isso. Tente outra pergunta."

# Interface de teste
while True:
    pergunta_usuario = input("Você: ")
    if pergunta_usuario.lower() in ["sair", "exit", "parar"]:
        print("Ak: Até mais!")
        break
    resposta = assistente(pergunta_usuario)
    if resposta is None:
        resposta = Ak_lembrete(pergunta_usuario) 
    if resposta is None:
        resposta = Ak_rpg(pergunta_usuario) 
    print("Ak:", resposta)
