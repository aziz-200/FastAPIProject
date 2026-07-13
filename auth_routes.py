from urllib import response

from fastapi import APIRouter
from sqlalchemy import null
from werkzeug.security import generate_password_hash, check_password_hash
from schemas import SignUpModel
from database import  session, engine
from models import User
auth_router = APIRouter(
    prefix="/auth",
)

session = session(bind=engine)

@auth_router.get("/")
async def signup():
    return {"message": "Signup"}

@auth_router.post("/signup", status_code=201)
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email:
        return {"message": "Email already exists"}
    else:
        # creating new user
        new_user = User(username=user.username,
                        email=user.email,
                        password=user.password, # sifhrlash
                        is_staff=False,
                        is_active=True)
        session.add(new_user)
        data = {
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "is_staff": False,
            "is_active": True
        }
        response_model = {
            'success': True,
            'code': 201,
            'message': 'User created successfully',
            'data': data
        }
        session.commit()
        session.close()
        return response_model

