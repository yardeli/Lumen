from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    age = Column(Integer)
    grade_level = Column(String)
    parent_email = Column(String, nullable=True)
    parent_consent_given = Column(Boolean, default=False)
    parent_consent_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)

class StudentSession(Base):
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    session_type = Column(String)  # "tutoring", "homework", "progress_review"
    subject = Column(String, nullable=True)
    encrypted_context = Column(Text)  # Encrypted session data
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    
class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    subject = Column(String)
    proficiency_level = Column(String)  # "beginner", "intermediate", "advanced"
    last_updated = Column(DateTime, default=datetime.utcnow)
    
class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
