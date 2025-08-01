import os
import google.generativeai as genai
import requests

# Função para gerar a mensagem bíblica com o Gemini
def gerar_mensagem_biblica():
    """Gera uma mensagem bíblica personalizada usando a API do Gemini."""
    try:
        # Pega a chave da API das variáveis de ambiente
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=gemini_api_key)

        # Define o prompt detalhado para a IA
        # Baseado nos requisitos do documento original
        prompt = """
        Atue como um conselheiro espiritual e teólogo.
        [cite_start]Crie uma mensagem bíblica diária, profunda e encorajadora, direcionada especificamente para homens cristãos de 30 a 50 anos. [cite: 6]
        A mensagem deve ter a seguinte estrutura:

        1.  **Tema do Dia:** Um título curto e impactante.
        2.  [cite_start]**Reflexão Bíblica:** Um texto de aproximadamente 150 palavras, abordando desafios e responsabilidades dessa faixa etária, como liderança familiar, integridade no trabalho, paternidade e propósito de vida. [cite: 32, 33]
        3.  [cite_start]**Aplicação Prática:** Um ou dois parágrafos curtos com sugestões de como aplicar a reflexão no dia a dia. [cite: 49]
        4.  [cite_start]**Versículos para Meditar:** Liste de 2 a 3 referências bíblicas (apenas o livro, capítulo e versículos) que sustentam a reflexão. [cite: 49]
        5.  [cite_start]**Oração do Dia:** Uma oração curta, de 50 a 80 palavras, relacionada ao tema. [cite: 49]

        Utilize uma linguagem reverente, mas acessível e direta.
        """

        # Configurações do modelo de geração
        generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 8192,
        }

        # Cria o modelo e gera o conteúdo
        model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)
        response = model.generate_content(prompt)
        
        print("Mensagem gerada com sucesso pelo Gemini.")
        return response.text

    except Exception as e:
        print(f"Erro ao gerar mensagem: {e}")
        return None

# Função para enviar a mensagem via Telegram
def enviar_mensagem_telegram(mensagem, bot_token, chat_id):
    """Envia uma mensagem de texto para um chat específico do Telegram."""
    try:
        # Monta a URL da API do Telegram
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        # Parâmetros da requisição: para quem enviar e o que enviar
        payload = {
            'chat_id': chat_id,
            'text': mensagem,
            'parse_mode': 'Markdown' # Permite usar negrito, itálico, etc.
        }
        
        # Envia a requisição
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print("Mensagem enviada com sucesso para o Telegram.")
        else:
            print(f"Erro ao enviar para o Telegram: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Erro na função de envio do Telegram: {e}")

# Bloco principal que executa o script
if __name__ == "__main__":
    print("Iniciando o agente bíblico diário...")
    
    # Pega as credenciais do Telegram das variáveis de ambiente
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    # Gera a mensagem bíblica
    mensagem_gerada = gerar_mensagem_biblica()

    # Se a mensagem foi gerada e as credenciais existem, envia
    if mensagem_gerada and telegram_bot_token and telegram_chat_id:
        enviar_mensagem_telegram(mensagem_gerada, telegram_bot_token, telegram_chat_id)
    else:
        print("Falha ao gerar mensagem ou credenciais não encontradas. Envio cancelado.")
    
    print("Agente finalizou a execução.")
