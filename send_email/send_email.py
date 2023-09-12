from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os
load_dotenv()
HOSTNAME = os.getenv("API_HOST")
PORT = os.getenv("API_PORT")
PROFILE = os.getenv("PROFILE")

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

async def send(email: str, api_key: str):
    if PROFILE == 'LOCAL': return {"message": "Email enviado com sucesso!"}
    try:
        fm = FastMail(conf)
        message = MessageSchema(
            subject="Ativação de API KEY",
            recipients=[email],
            # TODO: Ajustar url de acordo com ambiente
            body=f"Clique no link para ativar sua API KEY: http://{HOSTNAME}:{PORT}/key/{api_key}",
            subtype="html"
        )
        await fm.send_message(message)
        return {"message": "Email enviado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar o email: {str(e)}")
    