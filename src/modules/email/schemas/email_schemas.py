from pydantic import BaseModel, EmailStr

class EmailSchema(BaseModel):
    subject: str
    recipients: list[EmailStr]
    body: str
