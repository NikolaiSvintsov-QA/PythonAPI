
from pydantic import BaseModel

"""Pydantic-Схемы - для тела ответа"""
class TokenResponseSchema(BaseModel):
    accessToken: str