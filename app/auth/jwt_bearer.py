# to check if the request is authorized or not [verification of the protected route]

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from app.auth.jwt_handler import decodeJWT
# from decouple import config
import os
import jwt
from configparser import ConfigParser
class jwtBearer(HTTPBearer):
    
    def __init__(self, auto_Error: bool = True):
        super(jwtBearer, self).__init__(auto_error = auto_Error)
    
    async def __call__(self, request : Request):
        
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request) # this will call the __call__ method of the HTTPBearer class and return the credentials
        if credentials:
            if not credentials.scheme == "Bearer": # if the scheme is not Bearer, raise an exception
                raise HTTPException(status_code = 403, detail = "Invalid or Expired Token")
            return credentials.credentials
        else:
            raise HTTPException(status_code = 403, detail = "Invalid or Expired Token")
## old code        
    # def verify_jwt(self, jwt_token: str):
    #     isTokenValid : bool = False # false flag
    #     payload = decodeJWT(jwt_token) # decode the token and get the payload
    #     if payload:
    #         isTokenValid = True
    #     return isTokenValid

def set_up():
    """Sets up configuration for the app"""

    env = os.getenv("ENV", ".config")

    if env == ".config":
        config = ConfigParser()
        config.read(".config")
        config = config["AUTH0"]
    else:
        config = {
            "DOMAIN": os.getenv("DOMAIN", "your.domain.com"),
            "API_AUDIENCE": os.getenv("API_AUDIENCE", "your.audience.com"),
            "ISSUER": os.getenv("ISSUER", "https://your.domain.com/"),
            "ALGORITHMS": os.getenv("ALGORITHMS", "RS256"),
        }
    return config    
class VerifyJWT():
    """Does all the token verification using PyJWT"""

    def __init__(self, token, permissions=None, scopes=None):
        self.token = token
        self.permissions = permissions
        self.scopes = scopes
        self.config = set_up()

        # This gets the JWKS from a given URL and does processing so you can use any of
        # the keys available
        jwks_url = f'https://{self.config["DOMAIN"]}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        # This gets the 'kid' from the passed token
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            return {"status": "error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

        try: 
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=self.config["ALGORITHMS"],
                audience=self.config["API_AUDIENCE"],
                issuer=self.config["ISSUER"],
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        if self.scopes:
            result = self._check_claims(payload, 'scope', str, self.scopes.split(' '))
            if result.get("error"):
                return result

        if self.permissions:
            result = self._check_claims(payload, 'permissions', list, self.permissions)
            if result.get("error"):
                return result

        return payload

    def _check_claims(self, payload, claim_name, claim_type, expected_value):

        instance_check = isinstance(payload[claim_name], claim_type)
        result = {"status": "success", "status_code": 200}

        payload_claim = payload[claim_name]

        if claim_name not in payload or not instance_check:
            result["status"] = "error"
            result["status_code"] = 400

            result["code"] = f"missing_{claim_name}"
            result["msg"] = f"No claim '{claim_name}' found in token."
            return result

        if claim_name == 'scope':
            payload_claim = payload[claim_name].split(' ')

        for value in expected_value:
            if value not in payload_claim:
                result["status"] = "error"
                result["status_code"] = 403

                result["code"] = f"insufficient_{claim_name}"
                result["msg"] = (f"Insufficient {claim_name} ({value}). You don't have access to this resource")
                return result
        return result    