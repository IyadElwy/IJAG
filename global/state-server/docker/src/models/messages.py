from pydantic import BaseModel


class Reply(BaseModel):
    text: str
