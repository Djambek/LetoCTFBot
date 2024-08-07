import requests
import datetime
import jwt
import random
import json
import string

import models
random.seed(58934)
SECRET_KEY = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=64))

def get_user_info(id: int):
    try:
        r = requests.get(f"https://89.169.168.53/api/auth/telegram/{id}/?format=json", verify=False)
        data = json.loads(r.text)
        test = data["username"]
        return data
    except Exception as e:
        return None

def decode_acess_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        user_id: int = payload.get("id")
        return user_id
    except Exception:
        return None

def get_user_by_id(db, id):
    return db.query(models.Users).filter(models.Users.id == id).first()

def get_user_by_tgid(db, id):
    return db.query(models.Users).filter(models.Users.tg_id == id).first()

def login(token, db):
    try:
        id = decode_acess_token(token['access_token'])
        print("В логине")
        print(id)
        if id is None:
            return None
        user = get_user_by_id(db, id)
        return user
    except Exception:
        pass


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


