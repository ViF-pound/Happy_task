from pydantic import BaseModel


class CreateTask(BaseModel):

    name: str
    text: str

class UpdateTask(BaseModel):

    id: int
    name: str | None
    text: str | None