import requests
import json
import sys
from threading import Thread
from discord_webhook import DiscordWebhook, DiscordEmbed
import time

class DiscordBot:
    def __init__(self, webhook_url, username="Zain", avatar_url=None):
        """
        Inicializa o logger que envia tudo do terminal para o Discord.
        
        Parâmetros:
        - webhook_url: URL do webhook do Discord
        - username: (opcional) Nome que aparecerá como autor das mensagens
        - avatar_url: (opcional) URL da imagem do avatar
        """
        self.webhook_url = webhook_url
        self.username = username
        self.avatar_url = avatar_url
        self.running = False
        self.buffer = []
        
        # Redireciona stdout e stderr
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = self
        sys.stderr = self
        
    def write(self, text):
        """Captura tudo que é escrito no terminal"""
        self.original_stdout.write(text)  # Mantém a saída no terminal
        if text.strip():  # Ignora linhas vazias
            self.buffer.append(text)
    
    def flush(self):
        """Método necessário para redirecionamento de stdout"""
        self.original_stdout.flush()
    
    def start(self):
        """Inicia o serviço de envio para o Discord"""
        self.running = True
        Thread(target=self._send_loop, daemon=True).start()
        print("Logger iniciado! Tudo no terminal será enviado para o Discord.")
    
    def stop(self):
        """Para o serviço"""
        self.running = False
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
        print("Logger parado.")
    
    def _send_loop(self):
        """Loop que envia mensagens periodicamente"""
        while self.running:
            if self.buffer:
                # Junta as mensagens para evitar flood
                message = "".join(self.buffer)
                self.buffer = []
                
                # Divide em chunks de 2000 caracteres (limite do Discord)
                for chunk in [message[i:i+2000] for i in range(0, len(message), 2000)]:
                    self._send_to_discord(chunk)
            
            time.sleep(1)  # Verifica a cada segundo
    
    def _send_to_discord(self, message):
        """Envia uma mensagem para o Discord"""
        dados = {
            "content": f"```\n{message}\n```",
            "username": self.username
        }
        
        if self.avatar_url:
            dados["avatar_url"] = self.avatar_url
        
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps(dados),
                headers=headers
            )
            
            if response.status_code != 204:
                print(f"Erro ao enviar para Discord: {response.status_code}")
        except Exception as e:
            print(f"Erro na conexão: {str(e)}")

def AlertaDiscord(mensagem, webhook_url):
    """Envia uma mensagem para o Discord usando um webhook."""
    try:
        webhook = DiscordWebhook(url=webhook_url, content=mensagem)
        response = webhook.execute()
        if response.status_code == 200:
            print("Mensagem enviada para o Discord com sucesso.")
        else:
            print(f"Erro ao enviar mensagem para o Discord: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para o Discord: {e}")

# Exemplo de uso
if __name__ == "__main__":
    # Substitua pela URL do seu webhook
    WEBHOOK_URL = "https://discord.com/api/webhooks/1378226249813594192/3mbWIZIPqcilavihlA4w2Z29h4NKDMc-68620bZFk9DE2c25LoL75SltivQ_nKIso3EX"
    
    # Inicializa o logger
    logger = DiscordBot(
        WEBHOOK_URL,
        username="Zain",
        avatar_url="https://i.imgur.com/abcdefg.png"
    )
    
    # Inicia o serviço
    logger.start()
    
    try:
        # Exemplo de interação - tudo que for digitado ou impresso será enviado
        while True:
            user_input = input("Digite algo (ou 'sair' para terminar): ")
            if user_input.lower() == 'sair':
                break
            print(f"Você digitou: {user_input}")
    finally:
        # Garante que o logger é parado corretamente
        logger.stop()