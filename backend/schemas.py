# schemas.py
from pydantic import BaseModel
from typing import Optional

class GlossaryBase(BaseModel):
    term: str
    definition: str
    example: Optional[str] = None

class GlossaryCreate(GlossaryBase):
    pass

class GlossaryOut(GlossaryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


