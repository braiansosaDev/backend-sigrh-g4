from dotenv import load_dotenv
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_mail.schemas import MessageType
from src.modules.config.services.config_service import get_str, get_bool
from pydantic import SecretStr

from src.modules.email.schemas.email_schemas import EmailSchema

load_dotenv()
conf = ConnectionConfig(
    MAIL_USERNAME=get_str("MAIL_USERNAME"),
    MAIL_PASSWORD=SecretStr(get_str("MAIL_PASSWORD")),
    MAIL_FROM=get_str("MAIL_FROM"),
    MAIL_PORT=int(get_str("MAIL_PORT")),
    MAIL_SERVER=get_str("MAIL_SERVER"),
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=get_bool("MAIL_SSL_TLS"),
)

mail = FastMail(conf)

async def send_mail(background_tasks: BackgroundTasks, email: EmailSchema) -> None:
    message = MessageSchema(
        subject=email.subject,
        recipients=email.recipients,
        body=email.body,
        subtype=MessageType.html,
    )
    background_tasks.add_task(mail.send_message, message)
