import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user_model import User
from src.db import get_session
from src.app_auth.shema import Register, Login, Update, ReturnProfile
from src.app_auth.utils import hach_password, check_hach_password, create_access_token
from src.get_current_user import get_current_user


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register")
async def register(data: Register, session: AsyncSession = Depends(get_session)):

    user = await session.scalar(select(User).where(User.email == data.email))
    if user:
        raise HTTPException(status_code=403, detail="email is busy")

    user_data = data.model_dump()
    user_data["password"] = await hach_password(password=data.password)
    user_data["created_at"] = datetime.date.today()

    session_data = User(**user_data)

    session.add(session_data)
    await session.commit()

    user_data.pop("password")

    return {"status_code": 201, "detail": "register successful", "profile": user_data}


@auth_router.post("/login")
async def login(data: Login, session: AsyncSession = Depends(get_session)):

    if data.email:
        user = await session.scalar(select(User).where(User.email == data.email))
    else:
        raise HTTPException(status_code=400, detail="incorrect data")
    
    if await check_hach_password(hach_password=user.password, enter_password=data.password):
        user_token = await create_access_token(user_id=user.id)

        return {"status_code": 200, "detail": "login successful", "token": user_token}
    
    else:
        raise HTTPException(status_code=400, detail="incorrect password")
    

@auth_router.get("/profile", response_model=ReturnProfile)
async def return_profile(profile = Depends(get_current_user)):

    return profile


@auth_router.put("/update")
async def update(data: Update, session: AsyncSession = Depends(get_session), profile: User = Depends(get_current_user)):

    if data.user_name:
        profile.user_name = data.user_name
    
    if data.email:
        user = await session.scalar(select(User).where(User.email == data.email))
        if user:
            raise HTTPException(status_code=403, detail="email is busy")
        profile.email = data.email
    
    if data.password:
        profile.password = await hach_password(password=data.password)

    await session.commit()
    await session.refresh(profile)

    del profile.password # удаление пароля из объекта profile

    return {"status_code": 200, "detail": "update successful", "profile": profile}


@auth_router.delete("/delete")
async def delete_profile(session: AsyncSession = Depends(get_session), profile: User = Depends(get_current_user)):

    await session.delete(profile)
    await session.commit()

    return {"status_code": 200, "detail": "delete successful"}