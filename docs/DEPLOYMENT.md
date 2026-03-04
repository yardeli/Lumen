# Lumen Deployment Guide

## Overview

Lumen can be deployed to various platforms. This guide covers the most common options.

## Pre-Deployment Checklist

- [ ] Update `SECRET_KEY` and `ENCRYPTION_KEY` in `.env`
- [ ] Switch database from SQLite to PostgreSQL
- [ ] Set `DEBUG=false`
- [ ] Set up HTTPS/TLS
- [ ] Configure proper CORS origins (not `*`)
- [ ] Review PRIVACY.md and LEGAL.md
- [ ] Legal review of terms (highly recommended)
- [ ] Set up error logging and monitoring
- [ ] Run security audit
- [ ] Load test the API
- [ ] Backup strategy in place

## Deployment Options

### Option 1: Heroku (Easiest)

**Requirements:**
- Heroku account
- Heroku CLI installed

**Steps:**

1. Create `Procfile`:
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT backend.main:app
```

2. Create `runtime.txt`:
```
python-3.11.8
```

3. Push to Heroku:
```bash
heroku login
heroku create lumen-app
heroku addons:create heroku-postgresql:standard-0
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ENCRYPTION_KEY=your-encryption-key
git push heroku main
```

4. Migrate database:
```bash
heroku run python -m alembic upgrade head
```

**Pros:** Easy, managed infrastructure, automatic SSL
**Cons:** Limited free tier, can be pricey at scale

---

### Option 2: AWS (ECS + RDS)

**Requirements:**
- AWS account
- AWS CLI installed
- Docker

**Steps:**

1. Build Docker image:
```bash
docker build -t lumen:latest .
```

2. Push to ECR:
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag lumen:latest <account>.dkr.ecr.us-east-1.amazonaws.com/lumen:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/lumen:latest
```

3. Create ECS cluster and RDS database via AWS Console

4. Deploy ECS service with ECR image

**Pros:** Scalable, highly available, flexible
**Cons:** More complex, higher learning curve

---

### Option 3: Google Cloud Run (Good balance)

**Requirements:**
- Google Cloud account
- gcloud CLI installed

**Steps:**

1. Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

2. Build and deploy:
```bash
gcloud run deploy lumen \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

3. Set environment variables:
```bash
gcloud run services update lumen \
  --set-env-vars SECRET_KEY=your-key,ENCRYPTION_KEY=your-key
```

**Pros:** Simple, scalable, good pricing
**Cons:** Requires Docker knowledge

---

### Option 4: DigitalOcean App Platform

**Requirements:**
- DigitalOcean account

**Steps:**

1. Connect GitHub repo to DigitalOcean
2. Create App via dashboard
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `uvicorn backend.main:app --host 0.0.0.0 --port 8080`
5. Add PostgreSQL database
6. Configure environment variables
7. Deploy

**Pros:** Simple, affordable, good support
**Cons:** Less flexible than AWS

---

### Option 5: Self-Hosted (VPS)

**Requirements:**
- VPS (DigitalOcean, Linode, AWS EC2, etc.)
- Linux knowledge
- SSL certificate

**Steps:**

1. SSH into server
2. Install dependencies:
```bash
sudo apt update
sudo apt install python3.11 postgresql nginx
```

3. Clone repository:
```bash
git clone https://github.com/yardeli/Lumen.git
cd Lumen
```

4. Create Python virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. Configure PostgreSQL:
```bash
createdb lumen
```

6. Create systemd service (`/etc/systemd/system/lumen.service`):
```ini
[Unit]
Description=Lumen API
After=network.target

[Service]
User=www-data
WorkingDirectory=/home/lumen
Environment="PATH=/home/lumen/venv/bin"
ExecStart=/home/lumen/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 backend.main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

7. Set up Nginx reverse proxy:
```nginx
server {
    listen 80;
    server_name lumen.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

8. Enable SSL (Let's Encrypt):
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d lumen.example.com
```

9. Start service:
```bash
sudo systemctl enable lumen
sudo systemctl start lumen
```

**Pros:** Full control, potentially cheapest
**Cons:** You manage everything, more maintenance

---

## Database Setup

### SQLite (Development)
Already configured. Just works.

### PostgreSQL (Production)

**Install:**
```bash
pip install psycopg2-binary
```

**Update `.env`:**
```
DATABASE_URL=postgresql://user:password@localhost/lumen_db
```

**Create database:**
```bash
createdb lumen_db
```

**Run migrations (if using Alembic):**
```bash
alembic upgrade head
```

---

## Monitoring & Logging

### Application Logging

Add to `backend/main.py`:
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/lumen.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
```

### Error Tracking

**Sentry (Recommended):**
```bash
pip install sentry-sdk
```

```python
import sentry_sdk
sentry_sdk.init(
    dsn="https://key@sentry.io/project",
    traces_sample_rate=1.0
)
```

### Performance Monitoring

**New Relic:**
```bash
pip install newrelic
newrelic-admin run-program gunicorn ...
```

---

## Scaling

### Horizontal Scaling
- Use load balancer (Nginx, AWS ELB)
- Multiple API server instances
- Shared database (PostgreSQL)

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize database queries
- Cache frequently accessed data (Redis)

### Database Optimization
- Add indexes to frequently queried columns
- Use connection pooling (pgBouncer)
- Consider read replicas for high traffic

---

## Security Hardening

### Network
- Enable firewall, block unnecessary ports
- Use VPN for database access
- Disable public database access

### Application
- Enable HTTPS only
- Set secure cookie flags
- Add rate limiting
- Enable CORS for specific origins only
- Regular dependency updates
- Run security scans

### Data
- Encrypt sensitive data at rest and in transit
- Regular backups
- Separate staging/production environments
- Audit logging

---

## Troubleshooting

### Port Already in Use
```bash
lsof -i :8000  # Find process
kill -9 <PID>  # Kill it
```

### Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check credentials in .env
# Test connection: psql postgresql://user:password@localhost/lumen_db
```

### CORS Errors
- Check `allow_origins` in `main.py`
- Ensure frontend URL is included
- Test with curl: `curl -H "Origin: http://localhost:3000" ...`

### Out of Memory
- Increase server resources
- Optimize database queries
- Add caching
- Reduce worker processes

---

## Cost Estimates (Monthly)

| Platform | Small | Medium | Large |
|----------|-------|--------|-------|
| Heroku | $50 | $500+ | $2000+ |
| AWS | $30 | $200 | $1000+ |
| Google Cloud Run | $20 | $100 | $500+ |
| DigitalOcean | $6 | $24 | $48+ |
| Self-Hosted VPS | $5 | $20 | $100+ |

---

## Recommendations

### For MVP/Testing
- **DigitalOcean App Platform** or **Google Cloud Run**
- Simple, affordable, easy to set up
- Good for validating product

### For Production (Small Team)
- **AWS ECS + RDS** or **Self-Hosted VPS**
- More control, better for scaling
- Invest in ops/DevOps knowledge

### For Growth
- **AWS** or **Google Cloud**
- Auto-scaling, global infrastructure
- Professional support available

---

## Next Steps

1. Pick deployment platform based on needs
2. Set up production database
3. Configure monitoring and logging
4. Set up CI/CD pipeline
5. Plan disaster recovery
6. Monitor usage and costs

---

**Questions?** Check platform-specific docs or reach out!
