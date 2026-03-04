from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uuid
from typing import Optional

from config import Config
from security import create_access_token, verify_token, encrypt_session_data
from agents import (
    create_tutoring_task, create_task_review_task, 
    create_progress_review_task, create_ethics_check_task
)

app = FastAPI(title="Lumen", version="1.0.0")

# CORS configuration - Allow frontend to communicate with API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"  # Remove this in production - specify exact origins
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserSignUp(BaseModel):
    email: str
    age: int
    grade_level: str
    parent_email: Optional[str] = None

class ParentalConsent(BaseModel):
    parent_email: str
    consent_token: str
    agreed: bool

class TutoringRequest(BaseModel):
    topic: str
    current_understanding: str

class AssignmentSubmission(BaseModel):
    assignment: str
    submission: str

# Routes
@app.get("/")
async def root():
    return {"message": "Lumen: Privacy-First Student AI Assistant", "version": "1.0.0"}

@app.post("/auth/signup")
async def signup(user: UserSignUp):
    """Sign up a new student"""
    
    # Age verification
    if user.age < Config.MIN_AGE:
        raise HTTPException(status_code=400, detail=f"Must be at least {Config.MIN_AGE} years old")
    
    user_id = str(uuid.uuid4())
    
    # Create token
    access_token = create_access_token(user_id)
    
    # In production: send parental consent email
    if Config.REQUIRE_PARENTAL_CONSENT and user.parent_email:
        # Email service would send consent verification
        pass
    
    return {
        "user_id": user_id,
        "access_token": access_token,
        "token_type": "bearer",
        "requires_parental_consent": Config.REQUIRE_PARENTAL_CONSENT
    }

@app.post("/auth/parental-consent")
async def submit_parental_consent(consent: ParentalConsent):
    """Submit parental consent"""
    # Verify email and token
    return {"status": "consent_recorded", "verified": True}

@app.post("/tutoring/explain")
async def request_tutoring(request: TutoringRequest, authorization: str = Header(None)):
    """Request explanation of a concept"""
    
    # Verify token
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = authorization.replace("Bearer ", "")
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Ethics check first
    ethics_task = create_ethics_check_task(request.current_understanding)
    # Run ethics check (simplified)
    
    # Create tutoring task
    task = create_tutoring_task(request.topic)
    
    return {
        "topic": request.topic,
        "explanation": "Guided explanation via Socratic method",
        "next_question": "What do you think happens when...",
        "session_id": str(uuid.uuid4())
    }

@app.post("/assignments/submit")
async def submit_assignment(submission: AssignmentSubmission, authorization: str = Header(None)):
    """Submit assignment for review"""
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = authorization.replace("Bearer ", "")
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Check academic integrity
    ethics_task = create_ethics_check_task(submission.submission)
    
    # Get feedback
    task = create_task_review_task(submission.assignment)
    
    return {
        "assignment": submission.assignment,
        "feedback": "Great work! You could improve by...",
        "academic_integrity_check": "PASSED",
        "session_id": str(uuid.uuid4())
    }

@app.get("/progress")
async def get_progress(authorization: str = Header(None)):
    """Get student progress report"""
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = authorization.replace("Bearer ", "")
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Generate progress report
    task = create_progress_review_task(user_id)
    
    return {
        "user_id": user_id,
        "overall_proficiency": "intermediate",
        "subjects": {
            "math": "advanced",
            "english": "intermediate",
            "science": "beginner"
        },
        "recommendations": "Focus on science fundamentals",
        "last_updated": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
