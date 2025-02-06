# to check if the request is authorized or not [verification of the protected route]

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT
# from decouple import config

class jwtBearer(HTTPBearer):
    
    def __init__(self, auto_Error: bool = True):
        super(jwtBearer, self).__init__(auto_error = auto_Error)
    
    async def __call__(self, request : Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request) # this will call the __call__ method of the HTTPBearer class and return the credentials
        if credentials:
            if not credentials.scheme == "Bearer": # if the scheme is not Bearer, raise an exception
                raise HTTPException(status_code = 403, details = "Invalid or Expired Token")
            return credentials.credentials
        else:
            raise HTTPException(status_code = 403, details = "Invalid or Expired Token")
        
    def verify_jwt(self, jwt_token: str):
        isTokenValid : bool = False # false flag
        payload = decodeJWT(jwt_token) # decode the token and get the payload
        if payload:
            isTokenValid = True
        return isTokenValid
    
    