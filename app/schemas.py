from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class ChatCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)

    @field_validator('title')
    def trim_and_check_empty(cls, v):
        v = v.strip()  # Тримминг пробелов
        if not v:
            raise ValueError("Title cannot be empty")
        return v


class MessageCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)

    @field_validator('text')
    def trim_and_check_empty(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Text cannot be empty")
        return v


class Chat(BaseModel):
    id: int
    title: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class Message(BaseModel):
    id: int
    chat_id: int
    text: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
