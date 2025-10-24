import smtplib
from email.message import EmailMessage


def send_email_gmail(destinatario, assunto, corpo, remetente, senha_app):
    msg = EmailMessage()
    msg["From"] = remetente
    msg["To"] = (
        ", ".join(destinatario) if isinstance(destinatario, list) else destinatario
    )
    msg["Subject"] = assunto
    msg.set_content(corpo, subtype="html")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remetente, senha_app)
            smtp.send_message(msg)
            print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
