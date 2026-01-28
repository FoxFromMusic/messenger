from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="chat", cascade="all, delete")

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    text = Column(String(5000), nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    chat = relationship("Chat", back_populates="messages")