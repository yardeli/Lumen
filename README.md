# Lumen: Privacy-First Student AI Assistant

A CrewAI-powered educational platform that tutors, tracks progress, and maintains academic integrity—all while respecting student privacy.

## Features

✨ **Intelligent Tutoring**
- Socratic method explanations
- Concept clarification
- Subject-specific guidance

📊 **Progress Tracking**
- Real-time learning analytics
- Performance by subject
- Personalized recommendations

✅ **Assignment Feedback**
- Constructive review
- Academic integrity checks
- Step-by-step guidance (not answers)

🔐 **Privacy & Compliance**
- COPPA-compliant (ages 13+)
- FERPA-compliant (school records)
- GDPR-ready (data deletion)
- Encrypted session storage

## Quick Start

### Prerequisites
- Python 3.9+
- pip or poetry

### Installation

```bash
# Clone the repo
git clone https://github.com/Yarden.elias03/Lumen.git
cd Lumen

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your settings

# Initialize database
python backend/models.py
```

### Run Development Server

```bash
cd backend
python -m uvicorn main:app --reload
```

Server runs at `http://localhost:8000`

### API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Architecture

```
Lumen/
├── backend/
│   ├── main.py          # FastAPI app
│   ├── agents.py        # CrewAI agents
│   ├── models.py        # Database models
│   ├── security.py      # Encryption & auth
│   ├── config.py        # Configuration
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   └── app.js
├── docs/
│   ├── ARCHITECTURE.md  # System design
│   ├── PRIVACY.md       # Privacy policy
│   └── LEGAL.md         # Terms of service
├── .env.example
└── README.md
```

## API Endpoints

### Authentication
```
POST   /auth/signup                  Sign up new student
POST   /auth/parental-consent        Submit parent consent
```

### Tutoring
```
POST   /tutoring/explain             Request concept explanation
GET    /tutoring/history             View past sessions
```

### Assignments
```
POST   /assignments/submit           Submit work for review
GET    /assignments/pending          List pending assignments
```

### Progress
```
GET    /progress                     View progress report
GET    /progress/recommendations     Get personalized recommendations
```

### Health
```
GET    /health                       System status
```

## Configuration

### `.env` File

```env
# Database
DATABASE_URL=sqlite:///./lumen.db

# Security
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here

# COPPA & Compliance
MIN_AGE=13
REQUIRE_PARENTAL_CONSENT=true
PARENT_EMAIL_VERIFICATION=true

# API
DEBUG=false
API_PREFIX=/api/v1
```

## Data Privacy

### What We Collect
- Email, age, grade level (required)
- Academic progress (optional)
- Session metadata (encrypted)

### What We DON'T Collect
- Conversation history (not stored)
- Location data
- Behavioral tracking
- Device identifiers

### Your Rights
- **View**: Your profile and progress
- **Modify**: Email and preferences
- **Delete**: Request full account deletion
- **Export**: Download your data (GDPR)

**See [PRIVACY.md](docs/PRIVACY.md) for full details.**

## Academic Integrity

Lumen helps students **learn**, not cheat:
- ✅ Explains concepts and teaches understanding
- ✅ Reviews work and gives feedback
- ✅ Guides thinking with questions
- ❌ Does NOT solve homework directly
- ❌ Does NOT generate essays to submit
- ❌ Does NOT bypass academic standards

Our **EthicsGuard agent** detects and flags cheating attempts.

## Compliance

### COPPA (US, Under 13)
- Parental consent required
- Parent email verification
- Limited data collection
- Easy deletion

### FERPA (US, School Records)
- Student record privacy
- Parental access (if applicable)
- Proper data handling

### GDPR (EU/UK)
- Right to access
- Right to be forgotten
- Data portability
- Transparency

### CCPA (California)
- Consumer privacy rights
- Opt-out of data sharing
- Non-discrimination

**See [LEGAL.md](docs/LEGAL.md) for full terms.**

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
black backend/
flake8 backend/
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

## Deployment

### Production Checklist
- [ ] Change SECRET_KEY and ENCRYPTION_KEY
- [ ] Use PostgreSQL (not SQLite)
- [ ] Enable HTTPS/TLS
- [ ] Set up rate limiting
- [ ] Configure CORS properly
- [ ] Use Gunicorn with workers
- [ ] Set up monitoring/alerts
- [ ] Regular security audits
- [ ] Legal review of terms
- [ ] Privacy policy ready

### Docker Deployment
```bash
docker build -t lumen .
docker run -p 8000:8000 lumen
```

### Cloud Deployment
- **Heroku**: `git push heroku main`
- **AWS**: Use ECS + RDS
- **GCP**: Use Cloud Run + Cloud SQL

## Roadmap

**v1.1** (Q2 2026)
- [ ] Mobile app (iOS/Android)
- [ ] Teacher dashboard
- [ ] Parent access portal
- [ ] Google Classroom integration

**v2.0** (Q4 2026)
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] Canvas/Blackboard integration
- [ ] Customizable agents
- [ ] API for institutions

## Contributing

We welcome contributions! Please:
1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code of Conduct
- Be respectful
- No discrimination
- Prioritize user privacy
- Academic integrity always

## Support

**Questions?**
- Email: support@lumen-ai.edu
- GitHub Issues: [Create an issue](https://github.com/Yarden.elias03/Lumen/issues)
- Documentation: See `/docs`

**Security Issues?**
- Email: security@lumen-ai.edu (do NOT open public issue)

**Privacy Concerns?**
- Email: privacy@lumen-ai.edu

## License

MIT License - see LICENSE file

## Author

Built with ❤️ by [Your Name] with CrewAI

---

**Remember**: Lumen is a tool to help students learn better, not to replace teachers or enable cheating. Use responsibly. 🎓
