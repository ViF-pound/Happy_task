from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app_auth.utils import valid_access_token
from src.db import get_session
from src.models.user_model import User


bearer = HTTPBearer()


async def get_current_id(token: HTTPAuthorizationCredentials = Depends(bearer)):
    
    user_id = await valid_access_token(token=token.credentials)
    
    if not user_id:
            raise HTTPException(status_code=426, detail={"token":"Your token is not valid"})
            
    return user_id


async def get_current_user(user_id = Depends(get_current_id), session: AsyncSession = Depends(get_session)):
    
    user = await session.scalar(select(User).where(User.id == user_id))
    
    if not user:
            raise HTTPException(status_code=426, detail={"token":"Your token is not valid"})

    return user