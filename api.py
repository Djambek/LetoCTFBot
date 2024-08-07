from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie, Request
from sqlalchemy.orm import Session
from sqlalchemy import desc

import models
from job import split_teams
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta
from auth import *
from schemas import *
from database import get_db

router = APIRouter()


ADMIN_ID = [511612441, 650692477]

@router.post("/api/login")
def register_user(response: Response, user: UserBase, db: Session = Depends(get_db)):
    try:
        telebot_user = get_user_info(user.id)
        print(user.id)
        if telebot_user is None:
            raise HTTPException(status_code=400, detail="Вас нет в базе бота LetoCTF")
        if (db_user:=get_user_by_tgid(db, user.id)) is None:
            db_user = models.Users(name=telebot_user["username"], tg_id=user.id)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)

        token_data = {
            "sub": telebot_user["username"],
            "id": db_user.id,
            "exp": datetime.utcnow() + timedelta(minutes=60)
        }
        token = create_access_token(token_data)
        response.set_cookie(key="access_token", value=f"{token}", httponly=False)

        return {"message": "Login Successful"}
    except Exception:
        return {"message": "Something went wrong"}

@router.get("/api/profile")
def get_profile(request: Request, db: Session = Depends(get_db)):
    try:
        user = login(request.cookies, db)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        data = {
            "avatar": user.avatar,
            "name": user.name,
            "attack": user.attack,
            "hp": user.hp,
            "team_id": user.team_id
        }
        return data
    except Exception:
        return {"message": "Something went wrong"}

@router.get("/api/inventory")
def get_all_items(request: Request, db: Session = Depends(get_db)):
    try:
        user = login(request.cookies, db)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        data = db.query(models.Inventory.item_id).filter(models.Inventory.user_id == user.id).all()
        json_data = []
        for item in data:
            it = db.query(models.Items).filter(models.Items.id == item[0]).first()
            _ = {
                "id": it.id,
                "name": it.name,
                "icon": it.icon,
                "hp": it.hp
            }
            json_data.append(_)
        return json_data
    except Exception:
        return {"message": "Something went wrong"}

@router.get("/api/top")
def get_top(db: Session = Depends(get_db)):
    try:
        data = db.query(models.Users).order_by(desc(models.Users.hp)).all()
        print(data[0].name)
        answer = []
        for el in data:
            answer.append({"name": el.name, "hp": el.hp, "avatar": el.avatar})
        return answer
    except Exception:
        return {"message": "Something went wrong"}

@router.get("/api/use/{id_item}")
def use_item_inventory(request: Request, id_item: int, db: Session = Depends(get_db)):
    try:
        user = login(request.cookies, db)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        item_inv = db.query(models.Inventory).filter((models.Inventory.item_id == id_item) & (models.Inventory.user_id == user.id)).first()
        print(item_inv)
        if item_inv is None:
            return "Nice try, but I detected)"
        item = db.query(models.Items).filter(models.Items.id == item_inv.item_id).first()
        if item.hp > 0:
            user.hp += item.hp
        else:
            user.attack -= item.hp
        db.delete(item_inv)
        db.commit()
        return {"message": "Successfully used"}
    except Exception:
        return {"message": "Something went wrong"}

@router.post("/api/create_event")
def create_event(event: Event, request: Request,  db: Session = Depends(get_db)):
    try:
        user = login(request.cookies, db)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        if user.tg_id not in ADMIN_ID:
            raise HTTPException(status_code=401, detail="У вас нет прав")
        print("TIME TO FAPPING")
        print(event.time)
        event_db = models.Event(name=event.name, description=event.description,
                                time=event.time.time(),place=event.place, team_size=event.team_size,
                                duration=event.duration, no_damage=event.no_damage)

        db.add(event_db)
        db.commit()
        db.refresh(event_db)

        scheduler = BackgroundScheduler()
        before = (event.time + timedelta(minutes=-5)).time()
        scheduler.add_job(split_teams, 'cron', hour=before.hour, minute=before.minute, args=(db, event_db))
        scheduler.start()

        return {"message": "success"}
    except Exception:
        return {"message": "Something went wrong"}

@router.get("/api/get_events")
def get_all_events(request: Request, db: Session = Depends(get_db)):
    try:
        user = login(request.cookies, db)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        events = db.query(models.Event).order_by(desc(models.Event.time)).all()
        answer = []
        for ev in events:
            is_registered = db.query(models.Registration).filter((models.Registration.event_id == ev.id)
                                                               & (models.Registration.user_id == user.id)).first() \
                            is not None
            answer.append({"is_registered": is_registered, "id" : ev.id, "name": ev.name, "description": ev.description,
                           "time": ev.time, "place": ev.place, "team_size": ev.team_size,
                           "duration": ev.duration, "no_damage": ev.no_damage})
        return answer
    except:
        return {"message": "Something went wrong"}

@router.post("/api/reg_event/{event_id}")
def registration_on_event(event_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        user = login(request.cookies, db)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        if db.query(models.Registration).filter((models.Registration.user_id == user.id)
                                                & (models.Registration.event_id == event_id)).first() is not None:
            return {"message": "you have already joined"}
        reg = models.Registration(user_id=user.id, event_id=event_id)
        db.add(reg)
        db.commit()
        return {"message": "success"}
    except:
        return {"message": "Something went wrong"}

@router.post("/api/get_team/{team_id}")
def registration_on_event(team_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        user = login(request.cookies, db)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        users = db.query(models.Users).filter(models.Users.team_id==team_id).all()
        data = []
        for i in users:
            data.append({"name": i.name})
        return data
    except Exception:
        return {"message": "Something went wrong"}

@router.post("/api/get_event_teams/{event_id}")
def distribute_present(event_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        user = login(request.cookies, db)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        if user.tg_id not in ADMIN_ID:
            raise HTTPException(status_code=401, detail="У вас нет прав")
        teams = db.query(models.Teams.id).filter(models.Teams.event_id == event_id).all()
        team_parts = []
        print(teams)
        for team in teams:
            team_parts.append({team[0]:[i[0] for i in db.query(models.Users.name).filter(models.Users.team_id == team[0]).all()]})
        print(team_parts)
        return team_parts
    except Exception:
        return {"message": "Something went wrong"}
@router.post("/api/win/{team_id}")
def set_winner_team(team_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        user = login(request.cookies, db)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        if user.tg_id not in ADMIN_ID:
            raise HTTPException(status_code=401, detail="У вас нет прав")
        users = db.query(models.Users).filter(models.Users.team_id == team_id).all()
        event_id = db.query(models.Teams.event_id).filter(models.Teams.id == team_id).first()
        print(users)
        print(event_id)
        event_status = db.query(models.Event.no_damage).filter(models.Event.id == event_id[0]).first()
        presents = db.query(models.Items).filter(models.Items.hp > 0).all()
        print(presents)
        if event_status: # not damage
            for user_ in users:
                present = random.choice(presents)
                inv_db = models.Inventory(user_id=user_.id, item_id=present.id)
                db.add(inv_db)
                db.commit()
        else:
            sum_attack = 0
            for user_ in users:
                sum_attack += user_.attack
                user_.attack = 0
                db.commit()
        return {"message": "ok"}
    except Exception:
        return {"message": "Something went wrong"}




