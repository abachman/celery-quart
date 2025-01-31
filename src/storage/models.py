from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship
from src.storage import Base


class Conversation(Base):
    __tablename__ = "conversations"

    conversation_id = Column(UUID, primary_key=True)
    title = Column(String(255))

    messages = relationship("Message", back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(UUID, primary_key=True)
    conversation_id = Column(
        UUID, ForeignKey("conversations.conversation_id"), nullable=False
    )
    role = Column(String(255))
    content = Column(String(255))
