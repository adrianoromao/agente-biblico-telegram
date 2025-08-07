import os
import google.generativeai as genai
import requests
# Bibliotecas da nova abordagem Brevo
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

# A função gerar_mensagem_biblica() continua a mesma
def gerar_mensagem_biblica():
    """Gera uma mensagem bíblica personalizada com o estilo do pastor Max Lucado."""
    try:
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=gemini_api_key)
        prompt = """
        Você é um teólogo e pregador cristão da Igreja do Evangelho Quadrangular, com um tom informal e acolhedor. 
        Use o estilo de escrita do pastor Max Lucado. 
        Seu objetivo é criar um devocional diário inspirador para homens pais de família, com idade entre 30 e 50 anos, que enfrentam desafios como liderança do lar, provisão financeira, educação dos filhos, busca por equilíbrio entre trabalho e família, entre outros.
        A estrutura do devocional deve ser:
        1. **Início informal:** Uma frase que se conecte diretamente com a rotina ou os desafios de um pai de família. 
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
        print("Mensagem gerada com sucesso pelo Gemini (Estilo Keller).")
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

# FUNÇÃO DE E-MAIL COM A CORREÇÃO DE SINTAXE
def enviar_mensagem_email(mensagem, api_key, to_email, from_email):
    """Envia um e-mail transacional usando a API v3 oficial do Brevo."""
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key
    
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    subject = "Sua Reflexão Bíblica Diária"
    sender = {"name": "Agente Bíblico", "email": from_email}
    to = [{"email": to_email}]

    # --- INÍCIO DA CORREÇÃO FINAL ---
    # 1. Primeiro, preparamos o HTML, fazendo a substituição das quebras de linha.
    mensagem_html = mensagem.replace('\n', '<br>')
    # 2. Depois, usamos a variável já pronta no conteúdo do e-mail, sem causar o erro de sintaxe.
    html_content = f"<html><body>{mensagem_html}</body></html>"
    # --- FIM DA CORREÇÃO FINAL ---
    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)
    
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print("E-mail enviado com sucesso via API Brevo (v3)!")
    except ApiException as e:
        print(f"Erro ao enviar e-mail via API Brevo (v3): {e}")

# O bloco principal continua o mesmo da versão anterior
if __name__ == "__main__":
    print("Iniciando o agente bíblico diário...")
    mensagem_gerada = gerar_mensagem_biblica()
    if mensagem_gerada:
        # Envio para Telegram
        telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        if telegram_bot_token and telegram_chat_id:
            enviar_mensagem_telegram(mensagem_gerada, telegram_bot_token, telegram_chat_id)
        
        # Envio para E-mail via API v3 do Brevo
        brevo_api_key = os.getenv('BREVO_API_KEY')
        to_email = os.getenv('TO_EMAIL')
        from_email = os.getenv('FROM_EMAIL')
        if all([brevo_api_key, to_email, from_email]):
            enviar_mensagem_email(mensagem_gerada, brevo_api_key, to_email, from_email)
        else:
            print("Credenciais do Brevo (API v3) incompletas. Envio de e-mail pulado.")
    else:
        print("Falha ao gerar mensagem. Nenhum envio foi realizado.")
    print("Agente finalizou a execução.")


