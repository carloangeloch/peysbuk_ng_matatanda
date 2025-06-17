from authlib.jose import jwt, JoseError
from typing import Tuple
import os
import time
from fastapi import Request, status
from fastapi.responses import JSONResponse

JWT_SECRET = os.getenv('JWT_SECRET')
ACCESS_TOKEN_EXPIRY_SECONDS = 60 * 15 
REFRESH_TOKEN_EXPIRY_SECONDS = 7 * 24 * 60 * 60
ALGORITHM = 'HS256'

def create_token (data: dict) -> Tuple[str, str]:
    access_payload = data
    access_payload.update({'ait': time.time(), 'exp': time.time()  + ACCESS_TOKEN_EXPIRY_SECONDS,'scope':'access'})
    access_token = jwt.encode({'alg':ALGORITHM}, access_payload, JWT_SECRET).decode('utf-8')

    refresh_payload = data
    refresh_payload.update({'ait': time.time(), 'exp': time.time()  + REFRESH_TOKEN_EXPIRY_SECONDS,'scope':'refresh'})
    refresh_token = jwt.encode({'alg':ALGORITHM}, refresh_payload, JWT_SECRET).decode('utf-8')

    return access_token, refresh_token

def verify_token(req: Request):
    try:
        refresh_token = req.cookies.get('jwt_refresh')
        if not refresh_token:
            return JSONResponse({'Error':'Unauthoriz - No token found'}, status_code=status.HTTP_401_UNAUTHORIZED)
        payload = jwt.decode(refresh_token, JWT_SECRET)
        if not payload:
            return JSONResponse({'Error':'Unauthoriz - Invalid token'}, status_code=status.HTTP_401_UNAUTHORIZED)
        if payload['scope'] != 'refresh':
            return JSONResponse({'Error':'Unauthoriz - Invalid token'}, status_code=status.HTTP_401_UNAUTHORIZED)
        return payload
    except:
        return None
        

    