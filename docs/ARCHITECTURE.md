# Lumen Architecture

## Overview

Lumen is a privacy-first, AI-powered student assistant built on CrewAI. It provides tutoring, assignment feedback, and progress tracking while maintaining strict data privacy and academic integrity.

## System Design

### Backend (FastAPI)
- **Language**: Python 3.9+
- **Framework**: FastAPI for async API endpoints
- **Database**: SQLAlchemy ORM with SQLite (production: PostgreSQL)
- **Auth**: JWT tokens for stateless authentication

### AI Agents (CrewAI)
1. **TutorAgent** - Explains concepts using Socratic method
2. **TaskManagerAgent** - Tracks assignments and deadlines
3. **ProgressTrackerAgent** - Analyzes learning patterns
4. **EthicsGuard** - Detects homework cheating attempts

### Security Layer
- **Encryption**: Fernet (symmetric) for session data
- **Authentication**: JWT tokens (8-hour expiry)
- **Input Sanitization**: Only essential fields stored
- **Minimal Data Collection**: No unnecessary logging

## Data Flow

```
Student → Frontend → FastAPI Routes → CrewAI Agents
                        ↓
                   Security Layer
                        ↓
                   Database (Encrypted)
```

## Compliance

### COPPA Compliance
- Age verification (13+ required)
- Parental consent workflow
- Parent email verification
- Limited data collection for minors

### Privacy by Design
- No persistent conversation history
- Encrypted session storage
- No behavioral tracking
- Minimal analytics

## Authentication Flow

1. Student signs up (age verification)
2. System emails parent for consent
3. Parent verifies email and gives consent
4. Student receives JWT token
5. All requests include token in Authorization header

## Database Schema

### users
- id (PK)
- email (unique)
- age
- grade_level
- parent_email
- parent_consent_given
- created_at
- last_active

### sessions
- id (PK)
- user_id (FK)
- session_type (tutoring|homework|progress_review)
- subject
- encrypted_context
- started_at
- ended_at

### progress
- id (PK)
- user_id (FK)
- subject
- proficiency_level
- last_updated

### activity_logs
- id (PK)
- user_id (FK)
- action
- timestamp

## API Endpoints

### Auth
- `POST /auth/signup` - New student registration
- `POST /auth/parental-consent` - Parent consent submission

### Tutoring
- `POST /tutoring/explain` - Request concept explanation
- `GET /tutoring/history` - View tutoring sessions

### Assignments
- `POST /assignments/submit` - Submit work for review
- `GET /assignments/pending` - List pending assignments

### Progress
- `GET /progress` - Student progress report
- `GET /progress/recommendations` - Personalized recommendations

### Health
- `GET /health` - System status

## Deployment

### Development
```bash
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
```

### Production
- Use Gunicorn with multiple workers
- PostgreSQL database
- HTTPS/TLS required
- Rate limiting on all endpoints
- Regular security audits

## Future Enhancements

1. **Multi-language support** - Serve global students
2. **Mobile app** - iOS/Android client
3. **Teacher dashboard** - Parent/teacher access to progress
4. **Advanced analytics** - Learning pattern analysis
5. **Integration with LMS** - Canvas, Google Classroom
6. **Custom agents** - Teacher-customized agents
