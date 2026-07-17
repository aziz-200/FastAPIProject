import datetime
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_
from schemas import SignUpModel, LoginModel
from database import session, engine
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash

from auth_utils import create_token, get_current_subject, get_current_subject_refresh

auth_router = APIRouter(prefix='/auth')

session = session(bind=engine)


@auth_router.get('/')
async def welcome(current_user: str = Depends(get_current_subject)):
    return {'message': "Bu auth route signup sahifasi"}


@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail='User with this email already exists')

    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail='User with this username already exists')

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    session.add(new_user)
    session.commit()
    data = {
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email,
        'is_staff': new_user.is_staff,
        'is_active': new_user.is_active
    }
    return {
        'success': True,
        'code': 201,
        'message': "user is created successfully",
        'data': data
    }


@auth_router.post('/login', status_code=200)
async def login(user: LoginModel):
    db_user = session.query(User).filter(
        or_(
            User.username == user.username_or_email,
            User.email == user.username_or_email
        )
    ).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = create_token(db_user.username, datetime.timedelta(minutes=60), token_type="access")
        refresh_token = create_token(db_user.username, datetime.timedelta(days=3), token_type="refresh")

        token = {"access": access_token, "refresh": refresh_token}
        response = {
            "success": True,
            "code": 200,
            "message": "User successfully login",
            "data": token
        }
        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")


@auth_router.get('/login/refresh')
async def refresh_token(current_user: str = Depends(get_current_subject_refresh)):
    access_token_expires = datetime.timedelta(minutes=60)
    refresh_token_expires = datetime.timedelta(days=3)
    db_user = session.query(User).filter(User.username == current_user).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    new_refresh_token = create_token(db_user.username, refresh_token_expires, token_type="refresh")
    new_access_token = create_token(db_user.username, access_token_expires, token_type="access", )
    return {
        'success': True,
        'code': 200,
        'message': "New access token is created",
        'data': {"access_token": new_access_token, "refresh_token": new_refresh_token}
    }