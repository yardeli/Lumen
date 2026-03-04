# Lumen Privacy & Compliance Policy

## Core Principles

Lumen is built on **privacy by design**:
- Minimal data collection
- No persistent conversation logging
- Encrypted storage
- User-controlled data retention
- Transparent data handling

## Data We Collect

### Essential (Required)
- Email address (for account recovery)
- Age (for COPPA compliance)
- Grade level (for personalized responses)
- Parent email (for minors)
- Academic progress data (anonymized performance metrics)

### We DO NOT Collect
- Full conversation history (not stored by default)
- Behavioral tracking data
- Location data
- Device identifiers
- Browsing history outside Lumen

## COPPA Compliance (Children's Online Privacy Protection Act)

### For Users Under 13
- **Parental consent required** - Parent must verify email
- **Parent access** - Parent can view child's progress
- **Data deletion** - Parent can request all data deletion
- **No marketing** - No targeted ads or third-party sharing

### For Users 13+
- **Age verification required** - Self-certification at signup
- **No parental consent needed** (but encouraged)
- **Full user control** - Students manage their own data

## Data Storage

### Encryption
- All session data encrypted with Fernet (symmetric encryption)
- Database passwords hashed with bcrypt
- API keys stored in environment variables (never in code)

### Retention
- Session data: 90 days default (configurable)
- Progress data: Retained until deletion requested
- Conversation logs: Purged after 24 hours (not stored long-term)
- Activity logs: 30-day retention for security audits

### Deletion
- Users can request full data deletion anytime
- Automatic purge after account inactivity (180 days)
- GDPR right-to-be-forgotten supported

## Third-Party Sharing

**We do NOT share your data with:**
- Advertisers
- Data brokers
- Marketing companies
- Other third-party services

**We only share when:**
- Required by law (legal process)
- Parental access (if under 13)
- Academic institutions (if student explicitly requests)

## Security Measures

### Infrastructure
- HTTPS/TLS for all connections
- Firewall protecting database
- Regular penetration testing
- Security patching protocol

### Access Control
- JWT token-based authentication
- 8-hour token expiration
- Session invalidation on logout
- Rate limiting on API endpoints

### Monitoring
- Access logs (who logged in, when)
- Failed login attempts (to detect brute force)
- Anomaly detection for suspicious activity

## Parent/Student Rights

### View
- Your complete profile
- Progress reports
- Session summaries (non-detailed)

### Modify
- Email address
- Grade level
- Privacy preferences

### Delete
- Account and all associated data
- Individual sessions
- Progress history

### Control
- Opt-out of recommendations
- Disable new features
- Request data export (GDPR)

## Academic Integrity

### What Lumen Does
- **Explains concepts** - Teaches understanding
- **Reviews work** - Provides feedback, not answers
- **Tracks progress** - Shows learning patterns

### What Lumen Won't Do
- Solve homework problems directly
- Allow plagiarism or cheating
- Generate essays or full answers
- Bypass academic integrity checks

### Cheating Detection
- Flags suspicious requests
- Alerts parent/student if detected
- Does NOT share with school (unless requested)

## FERPA Compliance (Family Educational Rights and Privacy Act)

For US students:
- Education records are private
- Parents have access rights
- Students (18+) control their own records
- We follow FERPA guidelines for minors

## Changes to This Policy

- We may update this policy
- Users will be notified of major changes
- Changes take effect after 30-day notice
- Continued use = acceptance of new terms

## Contact

**Privacy Questions?**
privacy@lumen-ai.edu

**Data Deletion Request?**
support@lumen-ai.edu

**Legal Inquiry?**
legal@lumen-ai.edu

---

**Last Updated**: March 2026
**Version**: 1.0
