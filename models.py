from pydantic import BaseModel

class AnxietyInput(BaseModel):
    level: str  # high / medium / low
