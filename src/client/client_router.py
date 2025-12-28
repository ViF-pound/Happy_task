import datetime

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user_model import User
from src.models.task_model import Task
from src.db import get_session
from src.client.shema import CreateTask, UpdateTask
from src.get_current_user import get_current_user
from src.client.websocket_connection import Connection


client_router = APIRouter(prefix="/client", tags=["Client"])


@client_router.websocket("get_task")
async def websocket_endpoint(websocket: WebSocket, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):

    await Connection.connect(websocket)

    try:
        while True:
            
            tasks = await session.scalars(select(Task).where(Task.user == user))

            return tasks.all()



@client_router.post("/create")
async def create_task(data: CreateTask, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):

    task_data = data.model_dump()
    task_data["created_at"] = datetime.date.today()
    task_data["user"] = user

    task = Task(**task_data)

    session.add(task)
    await session.commit()

    return {"status_code": 201, "detail": "task create", "task": task_data}


@client_router.get("/get")
async def get_tasks(session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):

    tasks = await session.scalars(select(Task).where(Task.user == user))

    return tasks.all()


@client_router.put("/update")
async def update_task(data: UpdateTask, session: AsyncSession = Depends(get_session)):

    task = await session.scalar(select(Task).where(Task.id == data.id))
    if not task:
        raise HTTPException(status_code=404, detail="not found task")
    
    if data.name:
        task.name = data.name
    if data.text:
        task.text = data.text

    await session.commit()
    await session.refresh(task)

    return {"status_code": 200, "detail": "task update", "update_task": data}


@client_router.delete("/delete")
async def delete_task(task_id: int, session: AsyncSession = Depends(get_session)):

    task = await session.scalar(select(Task).where(Task.id == task_id))
    if not task:
        raise HTTPException(status_code=404, detail="not found task")
    
    await session.delete(task)
    await session.commit()

    return {"status_code": 200, "detail": "task delete"}