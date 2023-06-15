from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Record(BaseModel):
    id: Optional[str]
    timestamp: str
    method: str
    path: str
    query_params: str
    request_body: str
    response: str
