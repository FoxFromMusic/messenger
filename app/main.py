from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .database import get_db, engine, Base
from . import models, schemas

app = FastAPI()

@app.post("/chats/", response_model=schemas.Chat)
def create_chat(
        message: schemas.ChatCreate,
        db: Session = Depends(get_db)
):
    new_chat = models.Chat(title=message.title)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    return new_chat


@app.post("/chats/{chat_id}/messages/", response_model=schemas.Message)
def send_message(
        chat_id: int,
        message: schemas.MessageCreate,
        db: Session = Depends(get_db)
):
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    new_message = models.Message(
        text=message.text,
        chat_id=chat_id,
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message


@app.delete("/chats/{chat_id}/", status_code=204)
def delete_chat(
        chat_id: int,
        db: Session = Depends(get_db)
):
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    db.delete(chat)
    db.commit()
    return None


@app.get("/chats/{chat_id}/")
def read_chat(
        chat_id: int,
        limit: int = 20,
        db: Session = Depends(get_db)
):
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    messages = (db.query(models.Message)
                .filter(models.Message.chat_id == chat_id)
                .order_by(desc(models.Message.created_at))
                .limit(limit)
                .all())

    messages.reverse()

    return {
        "id": chat.id,
        "title": chat.title,
        "created_at": chat.created_at.isoformat(),
        "messages": messages
    }