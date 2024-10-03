from pydantic import BaseModel


class DlqEvent(BaseModel):
    event: dict
    error: str
