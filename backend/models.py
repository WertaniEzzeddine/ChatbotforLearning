from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from database import SessionLocal, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    courses = relationship("Course", back_populates="owner")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    pdf_files = Column(String(1000), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    summary = Column(Text, nullable=False)
    exam = Column(Text, nullable=False)
    exam_correction=Column(Text, nullable=False)

    conversation = Column(JSON, nullable=True)  # Stores JSON list of conversations
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
  
    

    # Relationship to User
    owner = relationship("User", back_populates="courses")





class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    course_id=Column(Integer)
    sender = Column(String, index=True)
    text = Column(String)