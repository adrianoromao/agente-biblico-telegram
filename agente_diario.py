import os
import google.generativeai as genai
import requests

# Função para gerar a mensagem bíblica (já atualizada)
def gerar_mensagem_biblica():
    """Gera uma mensagem bíblica personalizada com o estilo de Timothy Keller."""
    try:
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=gemini_api_key)
        prompt = """
        Atue como um conselheiro espiritual e escritor, com um estilo de pensamento e escrita profundamente inspirado em Timothy Keller.
        Sua tarefa é escrever uma reflexão diária para homens de 30 a 50 anos.
        O tom deve ser pastoral, inteligente e empático, conectando verdades bíblicas profundas com as ansiedades e realidades da vida moderna (trabalho, família, propósito, dúvidas).
        Evite usar títulos de seção como "Reflexão", "Aplicação Prática" ou "Oração". A mensagem deve fluir como um único texto coeso e impactante.
        A estrutura deve ser a seguinte:
        1. Comece com uma observação ou pergunta que capture a atenção e se conecte com uma experiência comum da vida adulta.
        2. Desenvolva a ideia usando uma passagem ou princípio bíblico, explicando-o de forma clara e lógica, como Keller faria.
        3. Conclua com uma aplicação prática que não soe como uma ordem, mas sim como um convite à reflexão e transformação.
        4. Termine com uma oração curta e sincera que encapsule o tema do dia.
        5. Ao final de tudo, e apenas no final, liste 2 ou 3 referências bíblicas para meditação posterior, no formato "Para meditar: Gênesis 1:1; João 3:16".
        O texto final deve ser profundo, mas acessível e encorajador.
        """
        generation_config = {"temperature": 0.75, "top_p": 1, "top_k": 1, "max_output_tokens": 8192}
        model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)
        response = model.generate_content(prompt)
        print("Mensagem gerada com sucesso pelo Gemini (Estilo Keller).")
        return response.text
    except Exception as e:
        print(f"Erro ao gerar mensagem: {e}")
        return None

# Função para enviar a mensagem via Telegram
def enviar_mensagem_telegram(mensagem, bot_token, chat_id):
    """Envia uma mensagem de texto para um chat específico do Telegram."""
    try:
        caracteres_especiais = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        mensagem_limpa = mensagem
        for char in caracteres_especiais:
            mensagem_limpa = mensagem_limpa.replace(char, f'\\{char}')
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {'chat_id': chat_id, 'text': mensagem_limpa, 'parse_mode': 'MarkdownV2'}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Mensagem enviada com sucesso para o Telegram.")
        else:
            print(f"Erro ao enviar para o Telegram: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Erro na função de envio do Telegram: {e}")

# NOVA FUNÇÃO para enviar a mensagem via WhatsApp
def enviar_mensagem_whatsapp(mensagem, token, phone_id, recipient_number):
    """Envia uma mensagem de texto para um número de WhatsApp usando a API oficial."""
    try:
        url = f"https://graph.facebook.com/v19.0/{phone_id}/messages"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        data = {"messaging_product": "whatsapp", "to": recipient_number, "type": "text", "text": {"body": mensagem}}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("Mensagem enviada com sucesso para o WhatsApp.")
        else:
            print(f"Erro ao enviar para o WhatsApp: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Erro na função de envio do WhatsApp: {e}")

# Bloco principal ATUALIZADO para enviar para ambos
if __name__ == "__main__":
    print("Iniciando o agente bíblico diário...")
    
    mensagem_gerada = gerar_mensagem_biblica()

    if mensagem_gerada:
        # Envio para Telegram
        telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        if telegram_bot_token and telegram_chat_id:
            enviar_mensagem_telegram(mensagem_gerada, telegram_bot_token, telegram_chat_id)
        else:
            print("Credenciais do Telegram não encontradas. Envio pulado.")

        # Envio para WhatsApp
        whatsapp_token = os.getenv('WHATSAPP_TOKEN')
        whatsapp_phone_id = os.getenv('WHATSAPP_PHONE_ID')
        whatsapp_recipient = os.getenv('WHATSAPP_RECIPIENT_NUMBER')
        if whatsapp_token and whatsapp_phone_id and whatsapp_recipient:
            enviar_mensagem_whatsapp(mensagem_gerada, whatsapp_token, whatsapp_phone_id, whatsapp_recipient)
        else:
            print("Credenciais do WhatsApp não encontradas. Envio pulado.")
    else:
        print("Falha ao gerar mensagem. Nenhum envio foi realizado.")
    
    print("Agente finalizou a execução.")
