"""Класс для описания базовых моделей api"""
from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    """Класс описания входных полей класса User"""
    id: int

class Event(BaseModel):
    """Класс описания входных полей класса Event"""
    name: str
    description: str
    time: datetime
    place: str
    team_size: int
    duration: int # минуты
    no_damage: bool
