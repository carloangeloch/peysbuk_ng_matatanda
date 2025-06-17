from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from lib.db import engine
from lib.jwt import create_token, verify_token
import bcrypt
import json

from models.user import User

from serializers.user import PostUserSerializer, GetUserSerializer, LoginUserSerializer

router = APIRouter()

@router.get('/users')
async def get_users():
    return JSONResponse({'Message':'Hello From router'})

#signup
@router.post('/signup')
async def signup(req: PostUserSerializer):
    res = JSONResponse(content={})
    if len(req.password) < 8:
        return res({'Error': 'Password is less than 8 characters'}, status_code=status.HTTP_400_BAD_REQUEST)
    with Session(engine) as session:
        statement = select(User).where(User.email == req.email)
        user = session.exec(statement).first()
        if user:
            return res({'Error':'User already exists'}, status_code=status.HTTP_400_BAD_REQUEST)
        hashed_password = bcrypt.hashpw(req.password.encode('utf-8'),bcrypt.gensalt(10))
        new_user = User(
            username=req.username,
            email= req.email,
            password= hashed_password.decode('utf-8'),
            first_name= req.first_name,
            middle_name= req.middle_name,
            last_name=req.last_name,
            avatar_url= req.avatar_url
        )
        user_json = json.loads(GetUserSerializer.model_validate(new_user).model_dump_json())
        res = JSONResponse(user_json, status_code=status.HTTP_201_CREATED)
        access_token, refresh_token = create_token(user_json)
        res.set_cookie(key='jwt_access', value=access_token, secure=True, httponly=True, samesite='strict',max_age= 60 * 15)
        res.set_cookie(key='jwt_refresh', value=refresh_token, secure=True, httponly=True, samesite='strict', max_age= 7 * 24 * 60 * 60)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return res
    return JSONResponse({'Error':'Error on signing up user'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

#login
@router.post('/login')
async def login(req:LoginUserSerializer):
    #echck if user exists
    with Session(engine) as session:
        statement = select(User).where(User.email == req.email)
        user = session.exec(statement).first()
        if not user:
            return JSONResponse({'Error':'Invalid Credentials'}, status_code=status.HTTP_401_UNAUTHORIZED)
    #check if password match
        isMatch = bcrypt.checkpw(req.password.encode('utf-8'), user.password.encode('utf-8'))
        if not isMatch:
            return JSONResponse({'Error':'Invalid Credentials'}, status_code=status.HTTP_401_UNAUTHORIZED)  
    #create jwt 
        user_json = json.loads(GetUserSerializer.model_validate(user).model_dump_json())
        res = JSONResponse(user_json, status_code=status.HTTP_200_OK)
        access_token, refresh_token = create_token(user_json)
        res.set_cookie(key='jwt_access', value=access_token, secure=True, httponly=True, samesite='strict',max_age= 60 * 15)
        res.set_cookie(key='jwt_refresh', value=refresh_token, secure=True, httponly=True, samesite='strict', max_age= 7 * 24 * 60 * 60)
        return res
    return JSONResponse({'Error':'Error on signing up user'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

#logout
@router.post('/logout')
async def logout():
    res = JSONResponse({'Message': 'Logged out successfully'})
    res.delete_cookie('jwt_access')
    res.delete_cookie('jwt_refresh')
    return res

#check
@router.get('/check')
async def checkAuth(req: Request):
    try:
        payload = verify_token(req)
        if not payload:
            return JSONResponse({'Error':'Unauthorized - No token payload'}, status_code=status.HTTP_401_UNAUTHORIZED)
        access_token, refresh_token = create_token(payload)
        res = JSONResponse({'Success':'Token verified!'}, status_code=status.HTTP_200_OK)
        res.set_cookie(key='jwt_access', value=access_token, secure=True, httponly=True, samesite='strict',max_age= 60 * 15)
        res.set_cookie(key='jwt_refresh', value=refresh_token, secure=True, httponly=True, samesite='strict', max_age= 7 * 24 * 60 * 60)
        return res
    except:
        return JSONResponse({'Error':'Error on signing up user'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


    