# this file is responsible for signing, encoding, decoding and returning JWTs.
import time
import jwt
from decouple import config  # helps organize setting and store parameter in ini  or .env file

JWT_SECRET = config("secret")  # secret key for encoding and decoding JWT strings
JWT_ALGORITHM = config("algorithm")  # algorithm used in the encoding and decoding JWT strings

# function to return the generated token in a JSON format (JWTs)
def token_response(token: str): 
    return {
        "access_token": token
    }
# function used for signing the JWT string   
def signJWT(userID: str):
    payload = {
        "userID": userID,
        "expiry": time.time() + 600
    }
    # encode the payload with the secret key and algorithm to generate the JWT string
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)  
    return token_response(token)


def decodeJWT(token : str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return decode_token if decode_token["expiry"] >= time.time() else None
    except:
        return  {}
