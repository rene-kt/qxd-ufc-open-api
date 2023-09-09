from pydantic import BaseModel

class CreateApiKey(BaseModel):
    name: str
    email: str
