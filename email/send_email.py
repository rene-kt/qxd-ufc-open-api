from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os
load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=str(os.getenv("ROOT_EMAIL_USER")),
    MAIL_PASSWORD=str(os.getenv("ROOT_EMAIL_PASSWORD")),
    MAIL_FROM=str(os.getenv("ROOT_EMAIL_USER")),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    USE_CREDENTIALS=True,
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True
)

async def send(email: str):
    try:
        fm = FastMail(conf)
        message = MessageSchema(
            subject="Assunto do Email",
            recipients=[email],
            body="Corpo do Email",
            subtype="html"
        )
        await fm.send_message(message)
        return {"message": "Email enviado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar o email: {str(e)}")
    