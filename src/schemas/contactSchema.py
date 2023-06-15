from pydantic import BaseModel
from typing import Optional


class Contact(BaseModel):
    id: Optional[int]
    firstname: str
    lastname: str
    email: str
    phone: str
    website: str
    estado_clickup: Optional[str]