from pydantic import BaseModel


# TCG
class CardName(BaseModel):
    id: str
    name: str
