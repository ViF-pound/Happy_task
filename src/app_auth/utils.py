import bcrypt
import datetime
import jwt

from fastapi import HTTPException

from src.config import config


async def hach_password(password: str):

    return bcrypt.hashpw(password=password.encode("utf-8"), salt=bcrypt.gensalt())


async def check_hach_password(enter_password: str, hach_password: str):

    return bcrypt.checkpw(password=enter_password.encode("utf-8"), hashed_password=hach_password)


async def create_access_token(
        user_id: int,
        algorithm: str = config.auth_data.algorithm,
        private_key: str = config.auth_data.private_key.read_text()
) -> str:
    
    payload = {"user_id": user_id, "exp": (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=config.auth_data.days)).timestamp()}

    token = jwt.encode(payload=payload, algorithm=algorithm, key=private_key)

    return token


async def valid_access_token(
        token:str,
        algorithm:str = config.auth_data.algorithm,
        public_key:str = config.auth_data.public_key.read_text()
) -> int:
    
    try:
        payload = jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")

    exp = payload.get("exp")

    if exp and exp > datetime.datetime.now(datetime.timezone.utc).timestamp():
        return payload.get("user_id")
    
    raise HTTPException(status_code=401, detail="Token has expired.")