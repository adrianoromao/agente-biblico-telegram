import os
import google.generativeai as genai
import requests
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ... (a função gerar_mensagem_biblica() continua a mesma) ...
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

# ... (a função enviar_mensagem_telegram() continua a mesma) ...
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

# NOVA FUNÇÃO para enviar a mensagem via E-mail com Brevo
def enviar_mensagem_email(mensagem, brevo_api_key, to_email, from_email):
    """Envia um e-mail usando a API SMTP do Brevo."""
    smtp_server = "smtp-relay.brevo.com"
    port = 587
    
    # Prepara o corpo do e-mail
    message = MIMEMultipart("alternative")
    message["Subject"] = "Sua Reflexão Bíblica Diária"
    message["From"] = from_email
    message["To"] = to_email

    # Converte o texto simples para HTML para manter as quebras de linha
    html_body = f"""\
    <html>
      <body>
        <p>Aqui está sua reflexão para hoje:</p>
        <p>{mensagem.replace('\n', '<br>')}</p>
      </body>
    </html>
    """
    message.attach(MIMEText(html_body, "html"))

    # Cria a conexão segura com o servidor e envia o e-mail
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)  # Habilita segurança
            server.login(from_email, brevo_api_key) # Login com seu e-mail e a CHAVE SMTP
            server.sendmail(from_email, to_email, message.as_string())
        print("Mensagem enviada com sucesso por E-mail (via Brevo).")
    except Exception as e:
        print(f"Erro ao enviar por E-mail: {e}")

# Bloco principal ATUALIZADO para enviar para Telegram e E-mail
if __name__ == "__main__":
    print("Iniciando o agente bíblico diário...")
    mensagem_gerada = gerar_mensagem_biblica()
    if mensagem_gerada:
        # Envio para Telegram
        telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        if telegram_bot_token and telegram_chat_id:
            enviar_mensagem_telegram(mensagem_gerada, telegram_bot_token, telegram_chat_id)
        
        # Envio para E-mail via Brevo
        brevo_api_key = os.getenv('BREVO_API_KEY')
        to_email = os.getenv('TO_EMAIL')
        from_email = os.getenv('FROM_EMAIL')
        if brevo_api_key and to_email and from_email:
            enviar_mensagem_email(mensagem_gerada, brevo_api_key, to_email, from_email)
    else:
        print("Falha ao gerar mensagem. Nenhum envio foi realizado.")
    print("Agente finalizou a execução.")
