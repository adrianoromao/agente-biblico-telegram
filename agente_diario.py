import os
import google.generativeai as genai
import requests
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

# A função gerar_mensagem_biblica() continua a mesma
def gerar_mensagem_biblica():
    """Gera uma mensagem bíblica personalizada com o estilo de Max Lucado."""
    try:
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=gemini_api_key)
        prompt = """

        Você deve atuar como um teólogo e pregador cristão da Igreja do Evangelho Quadrangular,use um tom informal e acolhedor. 
        Use o estilo de escrita do pastor Max Lucado. 
        Seu objetivo é criar um devocional diário inspirador para homens, com idade entre 30 e 50 anos, que enfrentam desafios como liderança do lar, provisão financeira, educação dos filhos, busca por equilíbrio entre trabalho e família, entre outros.
        A estrutura do devocional deve ser:
        1. **Início informal:** Uma frase que se conecte diretamente com a rotina ou os desafios de um homem nesta persona.Inicie sempre com o termo "Paz esteja contigo!" 
        2. **Contexto Bíblico:** Escolha um versículo bíblico (preferencialmente de Provérbios, Salmos, Efésios, Colossenses ou passagens sobre liderança/família) que se relacione com os desafios dessa persona.Apresente o versículo completo. 
        3. **Reflexão:** Uma reflexão prática e encorajadora sobre o versículo, aplicando-o aos desafios do dia a dia do pai. Use exemplos cotidianos. O tom deve ser de suporte e empatia. 
        4. **Chamado à Ação/Pensamento Final:** Um breve incentivo ou uma pergunta para o pai refletir. 
        5. **Oração:** Uma oração curta e poderosa, focada nos anseios e necessidades do pai de família (sabedoria, paciência, provisão, proteção da família). 
        O devocional deve ter entre 250 e 350 palavras. 
        Evite jargões excessivos e seja direto. utilize sempre um versículo de referência bíblico. 
        Não divida o texto com indicativos da estrutura, por exemplo: **Início formal** e etc. Desenvolva a mensagem em toda a estrutura proposta e após a oração. 
        Gere o devocional para o dia de hoje, focando no tema da dependência de Deus em meio às pressões." 
        Na confecção do texto você deve retirar TODA INFORMAÇÃO dos itens entre asteriscos(** **) Esta mensagem é destinada a várias pessoas, desta forma não cite nomes e que a mensagem seja ampla.
    
        """
        generation_config = {"temperature": 0.75, "top_p": 1, "top_k": 1, "max_output_tokens": 8192}
        model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)
        response = model.generate_content(prompt)
        print("Mensagem gerada com sucesso pelo Gemini (Estilo Max Lucado).")
        return response.text
    except Exception as e:
        print(f"Erro ao gerar mensagem: {e}")
        return None

# A função enviar_mensagem_telegram() continua a mesma
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

# A função enviar_mensagem_email() continua a mesma
def enviar_mensagem_email(mensagem, api_key, to_email, from_email):
    """Envia um e-mail transacional usando a API v3 oficial do Brevo."""
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = "Sua Reflexão Bíblica Diária"
    mensagem_html = mensagem.replace('\n', '<br>')
    html_content = f"<html><body>{mensagem_html}</body></html>"
    sender = {"name": "Agente Bíblico", "email": from_email}
    to = [{"email": to_email}]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print("E-mail enviado com sucesso via API Brevo (v3)!")
    except ApiException as e:
        print(f"Erro ao enviar e-mail via API Brevo (v3): {e}")

# FUNÇÃO REINTEGRADA para enviar a mensagem via WhatsApp
def enviar_mensagem_whatsapp(mensagem, token, phone_id, recipient_number):
    """Envia uma mensagem de texto para um número de WhatsApp usando a API oficial."""
    try:
        url = f"https://graph.facebook.com/v19.0/{phone_id}/messages"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        # O WhatsApp não suporta formatação complexa como HTML, então enviamos o texto puro.
        # A formatação com * para negrito e _ para itálico pode funcionar.
        data = {"messaging_product": "whatsapp", "to": recipient_number, "type": "text", "text": {"body": mensagem}}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("Mensagem enviada com sucesso para o WhatsApp.")
        else:
            print(f"Erro ao enviar para o WhatsApp: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Erro na função de envio do WhatsApp: {e}")

# Bloco principal ATUALIZADO para enviar para todos os canais
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

        # Envio para E-mail via Brevo
        brevo_api_key = os.getenv('BREVO_API_KEY')
        to_email = os.getenv('TO_EMAIL')
        from_email = os.getenv('FROM_EMAIL')
        if all([brevo_api_key, to_email, from_email]):
            enviar_mensagem_email(mensagem_gerada, brevo_api_key, to_email, from_email)
        else:
            print("Credenciais do Brevo (API v3) incompletas. Envio de e-mail pulado.")
            
        # Envio para WhatsApp
        whatsapp_token = os.getenv('WHATSAPP_TOKEN')
        whatsapp_phone_id = os.getenv('WHATSAPP_PHONE_ID')
        whatsapp_recipient = os.getenv('WHATSAPP_RECIPIENT_NUMBER')
        if all([whatsapp_token, whatsapp_phone_id, whatsapp_recipient]):
            enviar_mensagem_whatsapp(mensagem_gerada, whatsapp_token, whatsapp_phone_id, whatsapp_recipient)
        else:
            print("Credenciais do WhatsApp não encontradas. Envio pulado.")
    else:
        print("Falha ao gerar mensagem. Nenhum envio foi realizado.")
    
    print("Agente finalizou a execução.")



