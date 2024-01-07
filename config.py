import os
from dotenv import load_dotenv

load_dotenv()

HOSTNAME=os.getenv("API_HOST")
PORT=os.getenv("API_PORT")
PROFILE=os.getenv("APP_PROFILE")
MAIL_USER=os.getenv("ROOT_EMAIL_USER")
MAIL_PASSWORD=os.getenv("ROOT_EMAIL_PASSWORD")
REDIS_HOST=os.getenv("REDIS_HOST")