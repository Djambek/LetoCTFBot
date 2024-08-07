"""Файл с описанием классов для работы ORM SQLalchemy"""
import os

from sqlalchemy import create_engine, Column, Integer, String, Time, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base

from database import get_db

Base = declarative_base()

# Определение модели Users
class Users(Base):
    """Базовый класс user"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer)
    attack = Column(Integer, default=0)
    avatar = Column(String, default="base")
    name = Column(String)
    team_id = Column(Integer)
    hp = Column(Integer, default=3)


class Teams(Base):
    """Базовый класс teams, в которую будут объединяться users"""
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer)


class Items(Base):
    """Базовый класс вещи, которую юзер может получить"""
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    icon = Column(String)
    hp = Column(Integer)


class Event(Base):
    """Базовый класс для мероприятий"""
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    time = Column(Time)
    place = Column(String)
    team_size = Column(Integer, default=1)
    duration = Column(Integer)
    no_damage = Column(Boolean)


class Registration(Base):
    """Класс который регистрирует заявку на мероприятия"""
    __tablename__ = 'registation'
    event_id = Column(Integer, ForeignKey('events.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)



class Inventory(Base):
    """Класс инвентаря пользователя"""
    __tablename__ = 'inventory'
    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)


if __name__ == "__main__":
    DATABASE_URL = os.getenv('DATABASE_URL')
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    db = next(get_db())
    db.query(Items).delete()
    db.commit()
    items = {
        "миска корма": 1,
        "кошка жена": 3,
        "кошачья мята": 1,
        "блюдце молока": 1,
        "Комбез синий": -1,
        "Жилет спасательный": -1,
        "Каска золотая": -3
        }
    items_db = []
    for iname in items:
        items_db.append(Items(name=iname, hp=items[iname]))
        db.add(Items(name=iname, hp=items[iname]))
        db.commit()
    db.add(Users(tg_id=12, name="test"))
    db.add(Users(tg_id=10, name="test 2"))
    db.add(Inventory(user_id=1, item_id=2))
    db.add(Inventory(user_id=1, item_id=4))
    db.add(Inventory(user_id=1, item_id=6))
    db.add(Inventory(user_id=2, item_id=1))
    db.add(Inventory(user_id=2, item_id=3))
    db.add(Inventory(user_id=2, item_id=7))
    db.commit()
