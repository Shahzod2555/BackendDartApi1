from flask_login import login_user
from pydantic import BaseModel, EmailStr, Field
from flask import Blueprint, request
from ..models.user import User
from typing import Optional
from ..extends import db, bcrypt
import re

register = Blueprint('register_blueprint', __name__)

class UserData(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, pattern=r'^(?:\+7\d{10}|8\d{10})$')
    password: str


@register.route('/register', methods=['POST'])
def register_endpoint():
    data = UserData(**request.json)
    if User.query.filter_by(username=data.username).first():
        return {"error": "Пользователь с таким логином уже существует."}, 404
    elif User.query.filter_by(email=data.email).first():
        return {"error": "Пользователь с таким email уже существует."}, 404
    elif User.query.filter_by(phone_number=data.phone_number).first():
        return {"error": "Пользователь с таким номером телефона уже существует."}, 404
    else:
        hash_password = bcrypt.generate_password_hash(password=data.password).decode('utf-8')
        user_new = User(username=data.username, password=hash_password, phone_number=data.phone, email=data.email)
        db.session.add(user_new)
        db.session.commit()
        login_user(user_new)
        return {'user': data.username, 'password': data.password}

